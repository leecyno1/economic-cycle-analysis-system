#!/usr/bin/env python
"""
WindAPI连接测试脚本
测试Wind数据库连接和数据获取功能
"""
import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.wind_data_collector import WindDataCollector, WindConnectionConfig
from data_hub.models import Indicator, IndicatorData
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_wind_integration():
    """测试Wind数据库集成"""
    
    print("=" * 80)
    print("WindAPI数据库集成测试")
    print("=" * 80)
    
    # 创建Wind配置
    wind_config = WindConnectionConfig(
        username="17600806220",
        password="iv19whot"
    )
    
    # 创建Wind数据收集器
    collector = WindDataCollector(wind_config)
    
    print(f"\n📋 Wind配置信息:")
    print(f"   用户名: {wind_config.username}")
    print(f"   密码: {'*' * len(wind_config.password)}")
    print(f"   超时时间: {wind_config.timeout}秒")
    
    # 测试连接
    print(f"\n🔍 测试Wind连接...")
    connection_result = collector.test_connection()
    
    if connection_result['connected']:
        print("   ✅ Wind连接成功!")
        print(f"   Wind版本: {connection_result.get('wind_version', '未知')}")
        print(f"   数据测试: {connection_result.get('test_data', '未测试')}")
    else:
        print(f"   ❌ Wind连接失败: {connection_result['error_message']}")
        return
    
    # 显示支持的指标
    print(f"\n📊 支持的Wind指标:")
    supported_indicators = collector.get_supported_indicators()
    print(f"   总计: {len(supported_indicators)} 个指标")
    
    # 按类型分组显示
    mappings = collector.wind_mappings
    categories = {}
    for code, config in mappings.items():
        data_type = config['data_type']
        if data_type not in categories:
            categories[data_type] = []
        categories[data_type].append((code, config))
    
    for category, indicators in categories.items():
        print(f"\n   📈 {category.upper()}类 ({len(indicators)}个):")
        for code, config in indicators[:5]:  # 只显示前5个
            print(f"     • {code}: {config['description']} ({config['wind_code']})")
        if len(indicators) > 5:
            print(f"     ... 还有{len(indicators)-5}个指标")
    
    # 测试数据收集
    print(f"\n🔄 测试数据收集...")
    
    # 创建测试指标（如果不存在）
    test_indicators = [
        ('WIND_CPI_YOY', 'Wind CPI当月同比', 'Wind数据库CPI当月同比指标'),
        ('WIND_CSI300', 'Wind 沪深300指数', 'Wind数据库沪深300指数'),
        ('WIND_10Y_TREASURY', 'Wind 10年期国债收益率', 'Wind数据库10年期国债收益率')
    ]
    
    for code, name, description in test_indicators:
        # 检查指标是否存在
        indicator, created = Indicator.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'description': description,
                'category': 'test',
                'frequency': 'D',
                'unit': '%',
                'source': 'wind',
                'phase': 1
            }
        )
        
        if created:
            print(f"   📝 创建测试指标: {code}")
        else:
            print(f"   📋 使用现有指标: {code}")
        
        # 测试数据收集
        print(f"   🔍 测试收集 {code} 数据...")
        
        # 设置时间范围（最近1年）
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        result = collector.collect_indicator_data(code, start_date, end_date)
        
        if result.success:
            print(f"     ✅ 成功收集 {result.records_count} 条数据")
            print(f"     📅 数据范围: {result.data_range[0]} ~ {result.data_range[1]}")
            print(f"     🔗 Wind代码: {result.wind_code}")
            
            # 显示最新几条数据
            latest_data = IndicatorData.objects.filter(
                indicator=indicator
            ).order_by('-date')[:5]
            
            if latest_data:
                print(f"     📊 最新数据:")
                for data in latest_data:
                    print(f"       {data.date}: {data.value:.4f}")
        else:
            print(f"     ❌ 数据收集失败: {result.error_message}")
            if result.error_code:
                print(f"     🔢 错误代码: {result.error_code}")
        
        print()
    
    # 断开连接
    collector.disconnect()
    
    print("=" * 80)
    print("WindAPI集成测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_wind_integration() 