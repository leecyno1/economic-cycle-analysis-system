#!/usr/bin/env python3
"""
测试实际可用的AkShare指标
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def test_sw_industry_indicators():
    """测试申万行业指数"""
    print("=" * 50)
    print("测试申万行业指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    try:
        # 测试申万实时指数
        total_count += 1
        df = ak.index_realtime_sw()
        if not df.empty:
            print(f"✅ 申万实时指数: {len(df)} 条数据")
            print(f"   包含行业: {df['指数名称'].tolist()[:10]}")
            success_count += 1
        else:
            print(f"❌ 申万实时指数: 无数据")
    except Exception as e:
        print(f"❌ 申万实时指数: 获取失败 - {str(e)}")
    
    try:
        # 测试申万历史指数
        total_count += 1
        df = ak.index_hist_sw()
        if not df.empty:
            print(f"✅ 申万历史指数: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 申万历史指数: 无数据")
    except Exception as e:
        print(f"❌ 申万历史指数: 获取失败 - {str(e)}")
    
    try:
        # 测试申万分析数据
        total_count += 1
        df = ak.index_analysis_daily_sw()
        if not df.empty:
            print(f"✅ 申万日度分析: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 申万日度分析: 无数据")
    except Exception as e:
        print(f"❌ 申万日度分析: 获取失败 - {str(e)}")
    
    print(f"\n申万行业指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_shipping_indicators():
    """测试航运指标"""
    print("\n" + "=" * 50)
    print("测试航运指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    try:
        # 测试波罗的海干散货指数
        total_count += 1
        df = ak.macro_shipping_bdi()
        if not df.empty:
            print(f"✅ 波罗的海干散货指数(BDI): {len(df)} 条数据")
            print(f"   最新数据: {df.iloc[-1]['日期']} - {df.iloc[-1]['最新值']}")
            success_count += 1
        else:
            print(f"❌ 波罗的海干散货指数(BDI): 无数据")
    except Exception as e:
        print(f"❌ 波罗的海干散货指数(BDI): 获取失败 - {str(e)}")
    
    print(f"\n航运指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_energy_indicators():
    """测试能源指标"""
    print("\n" + "=" * 50)
    print("测试能源指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    try:
        # 测试中国能源指数
        total_count += 1
        df = ak.macro_china_energy_index()
        if not df.empty:
            print(f"✅ 中国能源指数: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 中国能源指数: 无数据")
    except Exception as e:
        print(f"❌ 中国能源指数: 获取失败 - {str(e)}")
    
    try:
        # 测试中国日度能源数据
        total_count += 1
        df = ak.macro_china_daily_energy()
        if not df.empty:
            print(f"✅ 中国日度能源数据: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 中国日度能源数据: 无数据")
    except Exception as e:
        print(f"❌ 中国日度能源数据: 获取失败 - {str(e)}")
    
    try:
        # 测试碳排放数据
        total_count += 1
        df = ak.energy_carbon_domestic()
        if not df.empty:
            print(f"✅ 国内碳排放数据: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 国内碳排放数据: 无数据")
    except Exception as e:
        print(f"❌ 国内碳排放数据: 获取失败 - {str(e)}")
    
    print(f"\n能源指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_stock_market_indicators():
    """测试股市相关指标"""
    print("\n" + "=" * 50)
    print("测试股市相关指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    try:
        # 测试股市市值数据
        total_count += 1
        df = ak.macro_china_stock_market_cap()
        if not df.empty:
            print(f"✅ 中国股市市值: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ 中国股市市值: 无数据")
    except Exception as e:
        print(f"❌ 中国股市市值: 获取失败 - {str(e)}")
    
    try:
        # 测试A股统计数据
        total_count += 1
        df = ak.stock_a_all_pb()
        if not df.empty:
            print(f"✅ A股PB统计: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ A股PB统计: 无数据")
    except Exception as e:
        print(f"❌ A股PB统计: 获取失败 - {str(e)}")
    
    print(f"\n股市指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_macro_indicators():
    """测试宏观经济指标"""
    print("\n" + "=" * 50)
    print("测试宏观经济指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 查看可用的宏观指标
    macro_functions = [attr for attr in dir(ak) if attr.startswith('macro_china_')]
    print(f"可用的中国宏观指标函数: {len(macro_functions)} 个")
    print(f"前10个: {macro_functions[:10]}")
    
    # 测试几个重要的宏观指标
    test_functions = [
        ('macro_china_gdp', '中国GDP'),
        ('macro_china_cpi', '中国CPI'),
        ('macro_china_ppi', '中国PPI'),
        ('macro_china_pmi', '中国PMI'),
        ('macro_china_exports_yoy', '中国出口同比'),
        ('macro_china_imports_yoy', '中国进口同比')
    ]
    
    for func_name, desc in test_functions:
        total_count += 1
        try:
            if hasattr(ak, func_name):
                func = getattr(ak, func_name)
                df = func()
                if not df.empty:
                    print(f"✅ {desc}: {len(df)} 条数据")
                    success_count += 1
                else:
                    print(f"❌ {desc}: 无数据")
            else:
                print(f"⚠️  {desc}: 函数不存在")
        except Exception as e:
            print(f"❌ {desc}: 获取失败 - {str(e)}")
    
    print(f"\n宏观指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_alternative_data():
    """测试替代数据指标"""
    print("\n" + "=" * 50)
    print("测试替代数据指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 查看可用的替代数据
    alternative_functions = [
        ('drewry_wci_index', 'Drewry世界集装箱指数'),
        ('article_epu_index', 'EPU经济政策不确定性指数'),
        ('futures_index_ccidx', '期货指数'),
    ]
    
    for func_name, desc in alternative_functions:
        total_count += 1
        try:
            if hasattr(ak, func_name):
                func = getattr(ak, func_name)
                df = func()
                if not df.empty:
                    print(f"✅ {desc}: {len(df)} 条数据")
                    success_count += 1
                else:
                    print(f"❌ {desc}: 无数据")
            else:
                print(f"⚠️  {desc}: 函数不存在")
        except Exception as e:
            print(f"❌ {desc}: 获取失败 - {str(e)}")
    
    print(f"\n替代数据指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def main():
    """主测试函数"""
    print("开始测试实际可用的AkShare指标...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_success = 0
    total_indicators = 0
    
    # 测试各类指标
    sw_success, sw_total = test_sw_industry_indicators()
    total_success += sw_success
    total_indicators += sw_total
    
    shipping_success, shipping_total = test_shipping_indicators()
    total_success += shipping_success
    total_indicators += shipping_total
    
    energy_success, energy_total = test_energy_indicators()
    total_success += energy_success
    total_indicators += energy_total
    
    stock_success, stock_total = test_stock_market_indicators()
    total_success += stock_success
    total_indicators += stock_total
    
    macro_success, macro_total = test_macro_indicators()
    total_success += macro_success
    total_indicators += macro_total
    
    alt_success, alt_total = test_alternative_data()
    total_success += alt_success
    total_indicators += alt_total
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试指标数: {total_indicators}")
    print(f"成功获取数据: {total_success}")
    print(f"成功率: {total_success/total_indicators*100:.1f}%")
    
    # 建议
    print("\n实施建议:")
    print("1. ✅ 优先实现成功率高的指标类别")
    print("2. 🔄 基于可用数据构建计算指标")
    print("3. 📊 重点关注申万行业、航运、能源等高质量数据源")
    print("4. 🎯 针对无法直接获取的指标，寻找替代数据源或计算方法")
    
    return total_success, total_indicators

if __name__ == "__main__":
    main() 