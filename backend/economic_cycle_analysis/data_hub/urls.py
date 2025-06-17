from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IndicatorCategoryViewSet, 
    IndicatorViewSet, 
    IndicatorDataViewSet,
    wind_status,
    wind_test_connection,
    wind_initialize_indicators,
    wind_collect_data,
    wind_sync_indicators,
    wind_supported_indicators,
    wind_data_quality_report
)

# 创建DRF路由器
router = DefaultRouter()
router.register(r'categories', IndicatorCategoryViewSet, basename='category')
router.register(r'indicators', IndicatorViewSet, basename='indicator')
router.register(r'data', IndicatorDataViewSet, basename='data')

app_name = 'data_hub'

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Wind数据源API端点
    path('api/wind/status/', wind_status, name='wind-status'),
    path('api/wind/test-connection/', wind_test_connection, name='wind-test-connection'),
    path('api/wind/initialize-indicators/', wind_initialize_indicators, name='wind-initialize-indicators'),
    path('api/wind/collect-data/', wind_collect_data, name='wind-collect-data'),
    path('api/wind/sync-indicators/', wind_sync_indicators, name='wind-sync-indicators'),
    path('api/wind/supported-indicators/', wind_supported_indicators, name='wind-supported-indicators'),
    path('api/wind/quality-report/', wind_data_quality_report, name='wind-quality-report'),
] 