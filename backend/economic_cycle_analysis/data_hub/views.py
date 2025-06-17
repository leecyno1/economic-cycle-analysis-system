from django.db.models import Avg, Max, Min, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta
from django.db.models import Q

from .models import IndicatorCategory, Indicator, IndicatorData
from .serializers import (
    IndicatorCategorySerializer, IndicatorSerializer, 
    IndicatorDataSerializer, IndicatorDataBulkSerializer,
    IndicatorStatsSerializer
)


class IndicatorCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    指标分类ViewSet - 只读
    提供指标分类的列表和详情查看功能
    """
    queryset = IndicatorCategory.objects.all().order_by('name')
    serializer_class = IndicatorCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    @method_decorator(cache_page(60 * 15))  # 缓存15分钟
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def indicators(self, request, pk=None):
        """获取分类下的所有指标"""
        category = self.get_object()
        indicators = category.indicators.all().order_by('name')
        serializer = IndicatorSerializer(indicators, many=True)
        return Response(serializer.data)


class IndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    指标ViewSet - 只读
    提供指标的列表、详情、搜索、过滤功能
    """
    queryset = Indicator.objects.select_related('category').all()
    serializer_class = IndicatorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'source', 'frequency']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['name', 'code']
    ordering = ['category__name', 'name']

    @method_decorator(cache_page(60 * 10))  # 缓存10分钟
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """按分类分组返回指标"""
        categories = IndicatorCategory.objects.prefetch_related('indicators').all()
        result = {}
        for category in categories:
            indicators = category.indicators.all()
            result[category.name] = IndicatorSerializer(indicators, many=True).data
        return Response(result)

    @action(detail=True, methods=['get'])
    def latest_data(self, request, pk=None):
        """获取指标的最新数据点"""
        indicator = self.get_object()
        latest_data = indicator.data_points.order_by('-date').first()
        if latest_data:
            serializer = IndicatorDataSerializer(latest_data)
            return Response(serializer.data)
        return Response({'message': '暂无数据'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """获取指标的统计信息"""
        indicator = self.get_object()
        data_points = indicator.data_points.all()
        
        if not data_points.exists():
            return Response({'message': '暂无数据'}, status=status.HTTP_404_NOT_FOUND)
        
        stats = data_points.aggregate(
            total_count=Count('id'),
            avg_value=Avg('value'),
            max_value=Max('value'),
            min_value=Min('value')
        )
        
        latest_data = data_points.order_by('-date').first()
        earliest_data = data_points.order_by('date').first()
        
        stats_data = {
            'indicator_code': indicator.code,
            'indicator_name': indicator.name,
            'total_count': stats['total_count'],
            'latest_date': latest_data.date,
            'earliest_date': earliest_data.date,
            'latest_value': latest_data.value,
            'avg_value': stats['avg_value'],
            'max_value': stats['max_value'],
            'min_value': stats['min_value']
        }
        
        serializer = IndicatorStatsSerializer(stats_data)
        return Response(serializer.data)


class IndicatorDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    指标数据ViewSet - 只读
    提供指标数据的查询、过滤、时间范围查询功能
    """
    queryset = IndicatorData.objects.select_related('indicator').all()
    serializer_class = IndicatorDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['indicator', 'indicator__category']
    ordering_fields = ['date', 'value', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """根据查询参数过滤数据"""
        queryset = super().get_queryset()
        
        # 指标代码过滤
        indicator_code = self.request.query_params.get('indicator_code')
        if indicator_code:
            queryset = queryset.filter(indicator__code=indicator_code)
        
        # 日期范围过滤
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass
        
        # 最近N天的数据
        recent_days = self.request.query_params.get('recent_days')
        if recent_days:
            try:
                days = int(recent_days)
                since_date = datetime.now().date() - timedelta(days=days)
                queryset = queryset.filter(date__gte=since_date)
            except ValueError:
                pass
        
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_query(self, request):
        """批量查询多个指标的数据"""
        serializer = IndicatorDataBulkSerializer(data=request.data)
        if serializer.is_valid():
            indicator_codes = serializer.validated_data['indicator_codes']
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            
            # 构建查询条件
            queryset = self.get_queryset().filter(
                indicator__code__in=indicator_codes
            )
            
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
            
            # 按指标分组返回数据
            result = {}
            for code in indicator_codes:
                indicator_data = queryset.filter(indicator__code=code).order_by('-date')
                result[code] = IndicatorDataSerializer(indicator_data, many=True).data
            
            return Response(result)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def latest_all(self, request):
        """获取所有指标的最新数据"""
        # 获取每个指标的最新数据
        indicators = Indicator.objects.all()
        result = []
        
        for indicator in indicators:
            latest_data = indicator.data_points.order_by('-date').first()
            if latest_data:
                result.append({
                    'indicator_code': indicator.code,
                    'indicator_name': indicator.name,
                    'category': indicator.category.name,
                    'date': latest_data.date,
                    'value': latest_data.value
                })
        
        return Response(result)

    @action(detail=False, methods=['get'])
    def time_series(self, request):
        """获取指定指标的时间序列数据"""
        indicator_code = request.query_params.get('indicator_code')
        if not indicator_code:
            return Response(
                {'error': '请提供indicator_code参数'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            indicator = Indicator.objects.get(code=indicator_code)
        except Indicator.DoesNotExist:
            return Response(
                {'error': f'未找到指标: {indicator_code}'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 获取时间序列数据
        queryset = self.get_queryset().filter(indicator=indicator).order_by('date')
        
        # 格式化为时间序列格式
        data = []
        for item in queryset:
            data.append({
                'date': item.date.strftime('%Y-%m-%d'),
                'value': float(item.value)
            })
        
        return Response({
            'indicator_code': indicator.code,
            'indicator_name': indicator.name,
            'data': data
        })
