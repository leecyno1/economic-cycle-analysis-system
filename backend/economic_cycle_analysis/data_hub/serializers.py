from rest_framework import serializers
from .models import IndicatorCategory, Indicator, IndicatorData


class IndicatorCategorySerializer(serializers.ModelSerializer):
    """指标分类序列化器"""
    indicator_count = serializers.SerializerMethodField()
    
    class Meta:
        model = IndicatorCategory
        fields = ['id', 'name', 'description', 'indicator_count']
    
    def get_indicator_count(self, obj):
        """获取分类下的指标数量"""
        return obj.indicators.count()


class IndicatorSerializer(serializers.ModelSerializer):
    """指标序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    latest_value = serializers.SerializerMethodField()
    latest_date = serializers.SerializerMethodField()
    data_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Indicator
        fields = [
            'id', 'code', 'name', 'category', 'category_name', 
            'description', 'source', 'frequency', 'lead_lag_status',
            'latest_value', 'latest_date', 'data_count'
        ]
    
    def get_latest_value(self, obj):
        """获取最新数据值"""
        latest_data = obj.data_points.order_by('-date').first()
        return latest_data.value if latest_data else None
    
    def get_latest_date(self, obj):
        """获取最新数据日期"""
        latest_data = obj.data_points.order_by('-date').first()
        return latest_data.date if latest_data else None
    
    def get_data_count(self, obj):
        """获取数据点数量"""
        return obj.data_points.count()


class IndicatorDataSerializer(serializers.ModelSerializer):
    """指标数据序列化器"""
    indicator_code = serializers.CharField(source='indicator.code', read_only=True)
    indicator_name = serializers.CharField(source='indicator.name', read_only=True)
    
    class Meta:
        model = IndicatorData
        fields = [
            'id', 'indicator', 'indicator_code', 'indicator_name', 
            'date', 'value'
        ]


class IndicatorDataBulkSerializer(serializers.Serializer):
    """批量数据操作序列化器"""
    indicator_codes = serializers.ListField(
        child=serializers.CharField(),
        help_text="指标代码列表",
        required=True
    )
    start_date = serializers.DateField(
        help_text="开始日期 (YYYY-MM-DD格式)",
        required=False
    )
    end_date = serializers.DateField(
        help_text="结束日期 (YYYY-MM-DD格式)",
        required=False
    )
    
    def validate(self, data):
        """验证日期范围"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("开始日期不能大于结束日期")
        
        return data


class IndicatorStatsSerializer(serializers.Serializer):
    """指标统计信息序列化器"""
    indicator_code = serializers.CharField()
    indicator_name = serializers.CharField()
    total_count = serializers.IntegerField()
    latest_date = serializers.DateField()
    earliest_date = serializers.DateField()
    latest_value = serializers.DecimalField(max_digits=20, decimal_places=6)
    avg_value = serializers.DecimalField(max_digits=20, decimal_places=6)
    max_value = serializers.DecimalField(max_digits=20, decimal_places=6)
    min_value = serializers.DecimalField(max_digits=20, decimal_places=6) 