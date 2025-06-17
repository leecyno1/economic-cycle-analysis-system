#!/usr/bin/env python3
"""
测试基于兴证策略的专业行业指标数据可用性
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def test_professional_indicators():
    """测试专业行业指标的数据可用性"""
    
    print("=== 专业行业指标数据可用性测试 ===\n")
    
    # 测试结果统计
    results = {
        'success': [],
        'failed': [],
        'total_tested': 0
    }
    
    # 1. TMT行业指标测试
    print("1. TMT行业指标测试")
    print("-" * 50)
    
    # 通信设备制造业PPI
    try:
        ppi_data = ak.macro_china_ppi()
        if len(ppi_data) > 0:
            print("✅ 通信设备制造业PPI: 成功")
            print(f"   数据量: {len(ppi_data)} 条记录")
            print(f"   最新数据: {ppi_data.iloc[-1]['日期']}")
            results['success'].append('通信设备制造业PPI')
        else:
            print("❌ 通信设备制造业PPI: 无数据")
            results['failed'].append('通信设备制造业PPI')
    except Exception as e:
        print(f"❌ 通信设备制造业PPI: 错误 - {e}")
        results['failed'].append('通信设备制造业PPI')
    
    results['total_tested'] += 1
    
    # 集成电路产量
    try:
        ic_data = ak.macro_china_industrial_production_yoy()
        if len(ic_data) > 0:
            print("✅ 工业生产数据(集成电路): 成功")
            print(f"   数据量: {len(ic_data)} 条记录")
            print(f"   最新数据: {ic_data.iloc[-1]['日期']}")
            results['success'].append('工业生产数据')
        else:
            print("❌ 工业生产数据: 无数据")
            results['failed'].append('工业生产数据')
    except Exception as e:
        print(f"❌ 工业生产数据: 错误 - {e}")
        results['failed'].append('工业生产数据')
    
    results['total_tested'] += 1
    
    # 2. 周期行业指标测试
    print("\n2. 周期行业指标测试")
    print("-" * 50)
    
    # 煤炭价格
    try:
        coal_data = ak.energy_oil_hist(symbol="煤炭价格指数")
        if len(coal_data) > 0:
            print("✅ 煤炭价格指数: 成功")
            print(f"   数据量: {len(coal_data)} 条记录")
            print(f"   最新价格: {coal_data.iloc[-1]['收盘']}")
            results['success'].append('煤炭价格指数')
        else:
            print("❌ 煤炭价格指数: 无数据")
            results['failed'].append('煤炭价格指数')
    except Exception as e:
        print(f"❌ 煤炭价格指数: 错误 - {e}")
        results['failed'].append('煤炭价格指数')
    
    results['total_tested'] += 1
    
    # 快递业务量
    try:
        express_data = ak.macro_china_postal_telecommunicational()
        if len(express_data) > 0:
            print("✅ 邮政电信业务数据: 成功")
            print(f"   数据量: {len(express_data)} 条记录")
            print(f"   最新数据: {express_data.iloc[-1]['日期']}")
            results['success'].append('邮政电信业务数据')
        else:
            print("❌ 邮政电信业务数据: 无数据")
            results['failed'].append('邮政电信业务数据')
    except Exception as e:
        print(f"❌ 邮政电信业务数据: 错误 - {e}")
        results['failed'].append('邮政电信业务数据')
    
    results['total_tested'] += 1
    
    # 3. 消费行业指标测试
    print("\n3. 消费行业指标测试")
    print("-" * 50)
    
    # 农产品价格
    try:
        futures_data = ak.futures_main_sina(symbol="粳稻")
        if len(futures_data) > 0:
            print("✅ 农产品期货价格(粳稻): 成功")
            print(f"   数据量: {len(futures_data)} 条记录")
            print(f"   最新价格: {futures_data.iloc[-1]['close']}")
            results['success'].append('农产品期货价格')
        else:
            print("❌ 农产品期货价格: 无数据")
            results['failed'].append('农产品期货价格')
    except Exception as e:
        print(f"❌ 农产品期货价格: 错误 - {e}")
        results['failed'].append('农产品期货价格')
    
    results['total_tested'] += 1
    
    # 社会消费品零售总额
    try:
        retail_data = ak.macro_china_retail_total()
        if len(retail_data) > 0:
            print("✅ 社会消费品零售总额: 成功")
            print(f"   数据量: {len(retail_data)} 条记录")
            print(f"   最新数据: {retail_data.iloc[-1]['日期']}")
            results['success'].append('社会消费品零售总额')
        else:
            print("❌ 社会消费品零售总额: 无数据")
            results['failed'].append('社会消费品零售总额')
    except Exception as e:
        print(f"❌ 社会消费品零售总额: 错误 - {e}")
        results['failed'].append('社会消费品零售总额')
    
    results['total_tested'] += 1
    
    # 4. 制造业指标测试
    print("\n4. 制造业指标测试")
    print("-" * 50)
    
    # 固定资产投资
    try:
        investment_data = ak.macro_china_fixed_asset_investment()
        if len(investment_data) > 0:
            print("✅ 固定资产投资: 成功")
            print(f"   数据量: {len(investment_data)} 条记录")
            print(f"   最新数据: {investment_data.iloc[-1]['日期']}")
            results['success'].append('固定资产投资')
        else:
            print("❌ 固定资产投资: 无数据")
            results['failed'].append('固定资产投资')
    except Exception as e:
        print(f"❌ 固定资产投资: 错误 - {e}")
        results['failed'].append('固定资产投资')
    
    results['total_tested'] += 1
    
    # 5. 医药行业指标测试
    print("\n5. 医药行业指标测试")
    print("-" * 50)
    
    # CPI医疗保健
    try:
        cpi_data = ak.macro_china_cpi()
        if len(cpi_data) > 0:
            print("✅ CPI数据(含医疗保健): 成功")
            print(f"   数据量: {len(cpi_data)} 条记录")
            print(f"   最新数据: {cpi_data.iloc[-1]['日期']}")
            results['success'].append('CPI数据')
        else:
            print("❌ CPI数据: 无数据")
            results['failed'].append('CPI数据')
    except Exception as e:
        print(f"❌ CPI数据: 错误 - {e}")
        results['failed'].append('CPI数据')
    
    results['total_tested'] += 1
    
    # 6. 金融地产指标测试
    print("\n6. 金融地产指标测试")
    print("-" * 50)
    
    # 保险数据
    try:
        insurance_data = ak.macro_china_insurance()
        if len(insurance_data) > 0:
            print("✅ 保险行业数据: 成功")
            print(f"   数据量: {len(insurance_data)} 条记录")
            print(f"   最新数据: {insurance_data.iloc[-1]['日期']}")
            results['success'].append('保险行业数据')
        else:
            print("❌ 保险行业数据: 无数据")
            results['failed'].append('保险行业数据')
    except Exception as e:
        print(f"❌ 保险行业数据: 错误 - {e}")
        results['failed'].append('保险行业数据')
    
    results['total_tested'] += 1
    
    # 7. 测试结果汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    success_rate = len(results['success']) / results['total_tested'] * 100
    print(f"总测试指标: {results['total_tested']}")
    print(f"成功获取: {len(results['success'])} ({success_rate:.1f}%)")
    print(f"获取失败: {len(results['failed'])} ({100-success_rate:.1f}%)")
    
    print(f"\n✅ 成功指标: {', '.join(results['success'])}")
    if results['failed']:
        print(f"\n❌ 失败指标: {', '.join(results['failed'])}")
    
    # 8. 数据质量评估
    print(f"\n数据质量评估:")
    if success_rate >= 80:
        print("🟢 优秀 - 数据可用性高，可以构建完整的专业指标体系")
    elif success_rate >= 60:
        print("🟡 良好 - 大部分数据可用，需要寻找替代数据源")
    else:
        print("🔴 需要改进 - 数据可用性较低，需要重新设计指标体系")
    
    return results

if __name__ == "__main__":
    test_results = test_professional_indicators() 