#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

# 设置Django环境
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.simple_indicator_calculator import test_simple_calculations

def main():
    print("=== 经济周期分析系统 - 简化版计算指标测试 ===")
    
    # 测试计算
    result = test_simple_calculations(dry_run=True)
    
    print(f"\n📊 测试结果统计:")
    print(f"总计算指标数量: {result['availability']['total_calc_indicators']}")
    print(f"可执行指标数量: {result['availability']['executable_indicators']}")
    print(f"计算成功: {result['success']} 个")
    print(f"计算失败: {result['error']} 个")
    
    print(f"\n📈 基础指标情况:")
    print(f"可用基础指标: {result['availability']['available_base_count']} 个")
    print(f"缺失基础指标: {result['availability']['missing_base_count']} 个")
    
    if result['availability']['available_base']:
        print(f"\n✅ 可用基础指标:")
        for indicator in result['availability']['available_base']:
            print(f"  - {indicator}")
    
    if result['availability']['missing_base']:
        print(f"\n❌ 缺失基础指标:")
        for indicator in result['availability']['missing_base']:
            print(f"  - {indicator}")
    
    print(f"\n🔧 计算结果详情:")
    for detail in result['details']:
        if detail['status'] == 'success':
            print(f"✅ {detail['code']}: {detail['name']}")
            print(f"   数据点: {detail['data_points']} 个")
            print(f"   时间范围: {detail['date_range']}")
            
            if detail['sample_values']:
                print(f"   最新数据:")
                for date, value in detail['sample_values'].items():
                    print(f"     {date}: {value:.4f}")
        else:
            print(f"❌ {detail['code']}: {detail['name']} - {detail['status']}")
            if 'error' in detail:
                print(f"   错误: {detail['error']}")
        print()

if __name__ == "__main__":
    main() 