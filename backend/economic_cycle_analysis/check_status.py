# -*- coding: utf-8 -*-
"""
检查数据库状态和数据采集器支持情况
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator, IndicatorData
from data_hub.enhanced_data_collector_methods import EnhancedDataCollectorMethods


def check_database_status():
    """检查数据库状态"""
    print("=" * 50)
    print("数据库状态检查")
    print("=" * 50)
    
    # 检查指标数量
    total_indicators = Indicator.objects.count()
    print(f"数据库中共有 {total_indicators} 个指标")
    
    # 按阶段统计
    phase_stats = {}
    for phase in [1, 2, 3]:
        count = Indicator.objects.filter(implementation_phase=phase).count()
        phase_stats[phase] = count
        print(f"第 {phase} 阶段指标: {count} 个")
    
    # 检查数据量
    total_data_points = IndicatorData.objects.count()
    print(f"数据库中共有 {total_data_points:,} 个数据点")
    
    # 检查有数据的指标
    indicators_with_data = IndicatorData.objects.values('indicator').distinct().count()
    print(f"已有数据的指标: {indicators_with_data} 个")
    
    # 显示前10个指标
    print("\n前10个指标:")
    indicators = Indicator.objects.all().order_by('implementation_phase', '-importance_level')[:10]
    for i, indicator in enumerate(indicators, 1):
        data_count = IndicatorData.objects.filter(indicator=indicator).count()
        print(f"{i:2d}. {indicator.code:15s} - {indicator.name[:30]:30s} (阶段{indicator.implementation_phase}, 数据: {data_count})")


def check_collector_support():
    """检查采集器支持情况"""
    print("\n" + "=" * 50)
    print("数据采集器支持情况")
    print("=" * 50)
    
    try:
        collector = EnhancedDataCollectorMethods()
        supported_indicators = collector.get_supported_indicators()
        print(f"增强版采集器支持 {len(supported_indicators)} 个指标类型")
        
        print("\n支持的指标类型:")
        for i, code in enumerate(supported_indicators[:15], 1):
            is_supported, message = collector.validate_indicator_support(code)
            print(f"{i:2d}. {code:20s} - {message}")
        
        if len(supported_indicators) > 15:
            print(f"... 还有 {len(supported_indicators) - 15} 个指标类型")
        
        # 检查数据库指标的支持情况
        print("\n数据库指标支持情况:")
        db_indicators = Indicator.objects.all()[:10]
        supported_count = 0
        
        for indicator in db_indicators:
            is_supported, message = collector.validate_indicator_support(indicator.code)
            if is_supported:
                supported_count += 1
                status = "✓"
            else:
                status = "✗"
            print(f"{status} {indicator.code:15s} - {indicator.name[:30]:30s}")
        
        print(f"\n前10个指标中支持的数量: {supported_count}/10")
        
    except Exception as e:
        print(f"检查采集器时发生错误: {e}")


def test_single_collection():
    """测试单个指标数据采集"""
    print("\n" + "=" * 50)
    print("测试单个指标数据采集")
    print("=" * 50)
    
    try:
        collector = EnhancedDataCollectorMethods()
        supported_indicators = collector.get_supported_indicators()
        
        if supported_indicators:
            test_code = supported_indicators[0]  # 测试第一个支持的指标
            print(f"测试指标: {test_code}")
            
            # 检查数据库中是否有此指标
            try:
                indicator = Indicator.objects.get(code=test_code)
                print(f"找到指标: {indicator.name}")
                
                # 尝试采集数据（仅测试，获取最近30天）
                from datetime import datetime, timedelta
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                
                print(f"测试采集时间范围: {start_date} 到 {end_date}")
                result = collector.collect_indicator_data(test_code, start_date, end_date)
                
                if result.success:
                    print(f"✓ 测试成功! 采集到 {result.records_count} 条数据")
                    print(f"  API函数: {result.api_function}")
                    print(f"  数据范围: {result.data_range[0]} 到 {result.data_range[1]}")
                else:
                    print(f"✗ 测试失败: {result.error_message}")
                
            except Indicator.DoesNotExist:
                print(f"数据库中未找到指标 {test_code}，需要先创建指标记录")
        else:
            print("没有支持的指标可供测试")
            
    except Exception as e:
        print(f"测试数据采集时发生错误: {e}")


if __name__ == "__main__":
    check_database_status()
    check_collector_support()
    test_single_collection()
    
    print("\n" + "=" * 50)
    print("检查完成")
    print("=" * 50) 