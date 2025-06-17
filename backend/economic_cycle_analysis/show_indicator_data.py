#!/usr/bin/env python
"""
显示CPI和半导体相关指标的现有数据
"""
import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator, IndicatorData
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_indicator_data():
    """显示CPI和半导体相关指标的数据"""
    
    print("=" * 80)
    print("CPI和半导体相关指标数据展示")
    print("=" * 80)
    
    # 查找CPI相关指标
    cpi_indicators = Indicator.objects.filter(name__icontains='CPI')
    print(f"\n🔍 找到 {cpi_indicators.count()} 个CPI指标")
    
    # 查找半导体相关指标
    semiconductor_indicators = Indicator.objects.filter(name__iregex=r'半导体|芯片|集成电路|晶圆|存储器')
    print(f"🔍 找到 {semiconductor_indicators.count()} 个半导体指标")
    
    # 显示CPI指标数据
    print("\n" + "="*60)
    print("📊 CPI相关指标数据")
    print("="*60)
    
    for i, indicator in enumerate(cpi_indicators, 1):
        data_count = IndicatorData.objects.filter(indicator=indicator).count()
        print(f"\n{i}. {indicator.name} ({indicator.code})")
        print(f"   数据点数量: {data_count}")
        
        if data_count > 0:
            # 显示数据范围
            earliest = IndicatorData.objects.filter(indicator=indicator).order_by('date').first()
            latest = IndicatorData.objects.filter(indicator=indicator).order_by('-date').first()
            print(f"   数据范围: {earliest.date} ~ {latest.date}")
            
            # 显示最近10年的数据（如果有）
            ten_years_ago = datetime.now().date() - timedelta(days=10*365)
            recent_data = IndicatorData.objects.filter(
                indicator=indicator,
                date__gte=ten_years_ago
            ).order_by('-date')[:10]
            
            if recent_data:
                print(f"   最近10个数据点:")
                for data in recent_data:
                    print(f"     {data.date}: {data.value:.2f}")
        else:
            print("   ❌ 暂无数据")
    
    # 显示半导体指标数据
    print("\n" + "="*60)
    print("📊 半导体相关指标数据")
    print("="*60)
    
    for i, indicator in enumerate(semiconductor_indicators, 1):
        data_count = IndicatorData.objects.filter(indicator=indicator).count()
        print(f"\n{i}. {indicator.name} ({indicator.code})")
        print(f"   数据点数量: {data_count}")
        
        if data_count > 0:
            # 显示数据范围
            earliest = IndicatorData.objects.filter(indicator=indicator).order_by('date').first()
            latest = IndicatorData.objects.filter(indicator=indicator).order_by('-date').first()
            print(f"   数据范围: {earliest.date} ~ {latest.date}")
            
            # 显示最近10年的数据（如果有）
            ten_years_ago = datetime.now().date() - timedelta(days=10*365)
            recent_data = IndicatorData.objects.filter(
                indicator=indicator,
                date__gte=ten_years_ago
            ).order_by('-date')[:10]
            
            if recent_data:
                print(f"   最近10个数据点:")
                for data in recent_data:
                    print(f"     {data.date}: {data.value:.2f}")
        else:
            print("   ❌ 暂无数据")
    
    # 统计总结
    total_indicators = cpi_indicators.count() + semiconductor_indicators.count()
    total_with_data = 0
    total_data_points = 0
    
    for indicator in list(cpi_indicators) + list(semiconductor_indicators):
        data_count = IndicatorData.objects.filter(indicator=indicator).count()
        if data_count > 0:
            total_with_data += 1
            total_data_points += data_count
    
    print("\n" + "="*60)
    print("📈 数据统计总结")
    print("="*60)
    print(f"总指标数: {total_indicators}")
    print(f"有数据的指标数: {total_with_data}")
    print(f"无数据的指标数: {total_indicators - total_with_data}")
    print(f"总数据点数: {total_data_points:,}")
    print(f"数据覆盖率: {total_with_data/total_indicators*100:.1f}%")
    
    # 显示最近10年有数据的指标
    print(f"\n📅 最近10年有数据的指标:")
    ten_years_ago = datetime.now().date() - timedelta(days=10*365)
    
    for indicator in list(cpi_indicators) + list(semiconductor_indicators):
        recent_count = IndicatorData.objects.filter(
            indicator=indicator,
            date__gte=ten_years_ago
        ).count()
        
        if recent_count > 0:
            print(f"   ✓ {indicator.name}: {recent_count} 个数据点")

if __name__ == "__main__":
    show_indicator_data() 