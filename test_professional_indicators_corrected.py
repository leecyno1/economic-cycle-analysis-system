#!/usr/bin/env python3
"""
修正版：测试基于兴证策略的专业行业指标数据可用性
使用正确的AkShare API函数名称
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def test_professional_indicators_corrected():
    """测试专业行业指标的数据可用性（修正版）"""
    
    print("=== 专业行业指标数据可用性测试（修正版）===\n")
    
    # 测试结果统计
    results = {
        'success': [],
        'failed': [],
        'total_tested': 0,
        'data_details': {}
    }
    
    # 1. TMT行业指标测试
    print("1. TMT行业指标测试")
    print("-" * 50)
    
    # PPI数据（包含通信设备制造业）
    try:
        ppi_data = ak.macro_china_ppi()
        if len(ppi_data) > 0:
            print("✅ PPI数据(含通信设备制造业): 成功")
            print(f"   数据量: {len(ppi_data)} 条记录")
            print(f"   数据列: {list(ppi_data.columns)}")
            results['success'].append('PPI数据')
            results['data_details']['PPI数据'] = len(ppi_data)
        else:
            print("❌ PPI数据: 无数据")
            results['failed'].append('PPI数据')
    except Exception as e:
        print(f"❌ PPI数据: 错误 - {e}")
        results['failed'].append('PPI数据')
    
    results['total_tested'] += 1
    
    # 工业增加值数据
    try:
        industrial_data = ak.macro_china_industrial_production_yoy()
        if len(industrial_data) > 0:
            print("✅ 工业增加值数据: 成功")
            print(f"   数据量: {len(industrial_data)} 条记录")
            print(f"   最新数据: {industrial_data.iloc[-1].iloc[0]}")
            results['success'].append('工业增加值数据')
            results['data_details']['工业增加值数据'] = len(industrial_data)
        else:
            print("❌ 工业增加值数据: 无数据")
            results['failed'].append('工业增加值数据')
    except Exception as e:
        print(f"❌ 工业增加值数据: 错误 - {e}")
        results['failed'].append('工业增加值数据')
    
    results['total_tested'] += 1
    
    # 2. 周期行业指标测试
    print("\n2. 周期行业指标测试")
    print("-" * 50)
    
    # 能源指数
    try:
        energy_data = ak.macro_china_energy_index()
        if len(energy_data) > 0:
            print("✅ 能源指数: 成功")
            print(f"   数据量: {len(energy_data)} 条记录")
            print(f"   数据列: {list(energy_data.columns)}")
            results['success'].append('能源指数')
            results['data_details']['能源指数'] = len(energy_data)
        else:
            print("❌ 能源指数: 无数据")
            results['failed'].append('能源指数')
    except Exception as e:
        print(f"❌ 能源指数: 错误 - {e}")
        results['failed'].append('能源指数')
    
    results['total_tested'] += 1
    
    # 货运指数
    try:
        freight_data = ak.macro_china_freight_index()
        if len(freight_data) > 0:
            print("✅ 货运指数: 成功")
            print(f"   数据量: {len(freight_data)} 条记录")
            print(f"   数据列: {list(freight_data.columns)}")
            results['success'].append('货运指数')
            results['data_details']['货运指数'] = len(freight_data)
        else:
            print("❌ 货运指数: 无数据")
            results['failed'].append('货运指数')
    except Exception as e:
        print(f"❌ 货运指数: 错误 - {e}")
        results['failed'].append('货运指数')
    
    results['total_tested'] += 1
    
    # 3. 消费行业指标测试
    print("\n3. 消费行业指标测试")
    print("-" * 50)
    
    # 消费品零售总额
    try:
        retail_data = ak.macro_china_consumer_goods_retail()
        if len(retail_data) > 0:
            print("✅ 消费品零售总额: 成功")
            print(f"   数据量: {len(retail_data)} 条记录")
            print(f"   数据列: {list(retail_data.columns)}")
            results['success'].append('消费品零售总额')
            results['data_details']['消费品零售总额'] = len(retail_data)
        else:
            print("❌ 消费品零售总额: 无数据")
            results['failed'].append('消费品零售总额')
    except Exception as e:
        print(f"❌ 消费品零售总额: 错误 - {e}")
        results['failed'].append('消费品零售总额')
    
    results['total_tested'] += 1
    
    # 农产品价格指数
    try:
        agri_data = ak.macro_china_agricultural_product()
        if len(agri_data) > 0:
            print("✅ 农产品价格指数: 成功")
            print(f"   数据量: {len(agri_data)} 条记录")
            print(f"   数据列: {list(agri_data.columns)}")
            results['success'].append('农产品价格指数')
            results['data_details']['农产品价格指数'] = len(agri_data)
        else:
            print("❌ 农产品价格指数: 无数据")
            results['failed'].append('农产品价格指数')
    except Exception as e:
        print(f"❌ 农产品价格指数: 错误 - {e}")
        results['failed'].append('农产品价格指数')
    
    results['total_tested'] += 1
    
    # 4. 制造业指标测试
    print("\n4. 制造业指标测试")
    print("-" * 50)
    
    # 制造业PMI
    try:
        pmi_data = ak.macro_china_pmi()
        if len(pmi_data) > 0:
            print("✅ 制造业PMI: 成功")
            print(f"   数据量: {len(pmi_data)} 条记录")
            print(f"   数据列: {list(pmi_data.columns)}")
            results['success'].append('制造业PMI')
            results['data_details']['制造业PMI'] = len(pmi_data)
        else:
            print("❌ 制造业PMI: 无数据")
            results['failed'].append('制造业PMI')
    except Exception as e:
        print(f"❌ 制造业PMI: 错误 - {e}")
        results['failed'].append('制造业PMI')
    
    results['total_tested'] += 1
    
    # 建筑业指数
    try:
        construction_data = ak.macro_china_construction_index()
        if len(construction_data) > 0:
            print("✅ 建筑业指数: 成功")
            print(f"   数据量: {len(construction_data)} 条记录")
            print(f"   数据列: {list(construction_data.columns)}")
            results['success'].append('建筑业指数')
            results['data_details']['建筑业指数'] = len(construction_data)
        else:
            print("❌ 建筑业指数: 无数据")
            results['failed'].append('建筑业指数')
    except Exception as e:
        print(f"❌ 建筑业指数: 错误 - {e}")
        results['failed'].append('建筑业指数')
    
    results['total_tested'] += 1
    
    # 5. 医药行业指标测试
    print("\n5. 医药行业指标测试")
    print("-" * 50)
    
    # CPI数据
    try:
        cpi_data = ak.macro_china_cpi()
        if len(cpi_data) > 0:
            print("✅ CPI数据(含医疗保健): 成功")
            print(f"   数据量: {len(cpi_data)} 条记录")
            print(f"   数据列: {list(cpi_data.columns)}")
            results['success'].append('CPI数据')
            results['data_details']['CPI数据'] = len(cpi_data)
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
    
    # 货币供应量
    try:
        money_data = ak.macro_china_money_supply()
        if len(money_data) > 0:
            print("✅ 货币供应量: 成功")
            print(f"   数据量: {len(money_data)} 条记录")
            print(f"   数据列: {list(money_data.columns)}")
            results['success'].append('货币供应量')
            results['data_details']['货币供应量'] = len(money_data)
        else:
            print("❌ 货币供应量: 无数据")
            results['failed'].append('货币供应量')
    except Exception as e:
        print(f"❌ 货币供应量: 错误 - {e}")
        results['failed'].append('货币供应量')
    
    results['total_tested'] += 1
    
    # 房地产投资
    try:
        real_estate_data = ak.macro_china_real_estate()
        if len(real_estate_data) > 0:
            print("✅ 房地产投资: 成功")
            print(f"   数据量: {len(real_estate_data)} 条记录")
            print(f"   数据列: {list(real_estate_data.columns)}")
            results['success'].append('房地产投资')
            results['data_details']['房地产投资'] = len(real_estate_data)
        else:
            print("❌ 房地产投资: 无数据")
            results['failed'].append('房地产投资')
    except Exception as e:
        print(f"❌ 房地产投资: 错误 - {e}")
        results['failed'].append('房地产投资')
    
    results['total_tested'] += 1
    
    # 7. 测试结果汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    success_rate = len(results['success']) / results['total_tested'] * 100
    print(f"总测试指标: {results['total_tested']}")
    print(f"成功获取: {len(results['success'])} ({success_rate:.1f}%)")
    print(f"获取失败: {len(results['failed'])} ({100-success_rate:.1f}%)")
    
    print(f"\n✅ 成功指标:")
    for indicator in results['success']:
        data_count = results['data_details'].get(indicator, 0)
        print(f"   • {indicator}: {data_count} 条记录")
    
    if results['failed']:
        print(f"\n❌ 失败指标: {', '.join(results['failed'])}")
    
    # 8. 数据质量评估和建议
    print(f"\n数据质量评估:")
    if success_rate >= 80:
        print("🟢 优秀 - 数据可用性高，可以构建完整的专业指标体系")
        recommendation = "建议：直接基于现有数据源构建指标体系"
    elif success_rate >= 60:
        print("🟡 良好 - 大部分数据可用，需要寻找替代数据源")
        recommendation = "建议：优先使用可用指标，为失败指标寻找替代方案"
    else:
        print("🔴 需要改进 - 数据可用性较低，需要重新设计指标体系")
        recommendation = "建议：重新评估指标选择，优先选择高可用性数据源"
    
    print(f"\n💡 {recommendation}")
    
    # 9. 基于测试结果的指标体系建议
    print(f"\n基于测试结果的指标体系建议:")
    print("="*60)
    
    if len(results['success']) >= 8:
        print("🎯 可以构建以下专业指标体系:")
        print("   • TMT行业: PPI价格指标 + 工业增加值")
        print("   • 周期行业: 能源指数 + 货运指数")
        print("   • 消费行业: 零售总额 + 农产品价格")
        print("   • 制造业: PMI + 建筑业指数")
        print("   • 医药行业: CPI医疗保健分项")
        print("   • 金融地产: 货币供应量 + 房地产投资")
        print("   • 计算指标: 基于以上数据构建综合景气度指数")
    else:
        print("🔄 建议优化策略:")
        print("   • 重点使用成功获取的指标")
        print("   • 为失败指标寻找替代数据源")
        print("   • 考虑使用第三方数据接口")
        print("   • 构建基于可用数据的计算指标")
    
    return results

if __name__ == "__main__":
    test_results = test_professional_indicators_corrected() 