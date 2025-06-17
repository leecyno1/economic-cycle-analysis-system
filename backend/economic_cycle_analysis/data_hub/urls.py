from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndicatorCategoryViewSet, IndicatorViewSet, IndicatorDataViewSet

# 创建DRF路由器
router = DefaultRouter()
router.register(r'categories', IndicatorCategoryViewSet, basename='category')
router.register(r'indicators', IndicatorViewSet, basename='indicator')
router.register(r'data', IndicatorDataViewSet, basename='data')

app_name = 'data_hub'

urlpatterns = [
    path('api/', include(router.urls)),
] 