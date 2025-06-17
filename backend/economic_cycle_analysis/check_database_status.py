#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator, IndicatorCategory

def check_database_status():
    """检查数据库中的指标状态"""
    print('=== 🔍 数据库状态检查 ===\n')
    
    # 总体统计
    total_indicators = Indicator.objects.count()
    total_categories = IndicatorCategory.objects.count()
    
    print(f'📊 总指标数: {total_indicators}')
    print(f'📂 总分类数: {total_categories}\n')
    
    # 分类分布
    print('=== 📋 分类分布 ===')
    for cat in IndicatorCategory.objects.all():
        count = cat.indicators.count()
        if count > 0:
            print(f'  {cat.name}: {count} 个指标')
    
    # 维度分布
    print('\n=== 🏷️ 维度分布 ===')
    dimensions = [
        ('dimension_prosperity', '景气度'),
        ('dimension_valuation', '估值'),  
        ('dimension_fundamental', '基本面'),
        ('dimension_supply_chain', '供应链'),
        ('dimension_policy', '政策敏感'),
        ('dimension_innovation', '创新'),
        ('dimension_risk', '风险'),
        ('dimension_seasonality', '季节性'),
    ]
    
    for field, name in dimensions:
        count = Indicator.objects.filter(**{field: True}).count()
        if count > 0:
            print(f'  {name}: {count} 个指标')
    
    # 实施阶段分布
    print('\n=== 🚀 实施阶段分布 ===')
    for phase in [1, 2, 3]:
        count = Indicator.objects.filter(implementation_phase=phase).count()
        if count > 0:
            percent = (count / total_indicators * 100) if total_indicators > 0 else 0
            print(f'  第{phase}阶段: {count} 个 ({percent:.1f}%)')
    
    # 详细指标列表
    print('\n=== 📝 详细指标列表 ===')
    for indicator in Indicator.objects.all()[:10]:  # 显示前10个
        dims = []
        if indicator.dimension_prosperity: dims.append('景气')
        if indicator.dimension_valuation: dims.append('估值')
        if indicator.dimension_fundamental: dims.append('基本面')
        if indicator.dimension_supply_chain: dims.append('供应链')
        
        dims_str = ', '.join(dims) if dims else '无'
        print(f'  {indicator.code}: {indicator.name} [{indicator.category.name}] - 维度: {dims_str}')
    
    if total_indicators > 10:
        print(f'  ... 还有 {total_indicators - 10} 个指标')
    
    print('\n=== ✅ 检查完成 ===')
    
    # 返回状态摘要
    return {
        'total_indicators': total_indicators,
        'total_categories': total_categories,
        'completion_rate': (total_indicators / 1064) * 100  # 基于1064个目标
    }

if __name__ == '__main__':
    status = check_database_status()
    print(f'\n📈 当前完成度: {status["completion_rate"]:.1f}% ({status["total_indicators"]}/1064)') 