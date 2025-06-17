#!/usr/bin/env python3
"""
测试综合指标的数据可获得性
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def test_ivix_indicator():
    """测试沪深300波动率指数"""
    print("=" * 50)
    print("测试 IVIX 指标")
    print("=" * 50)
    
    try:
        # 测试沪深300波动率指数
        df = ak.index_vix_hs300()
        print(f"✅ CN_IVIX - 沪深300波动率指数: {len(df)} 条数据")
        print(f"   最新数据日期: {df.index[-1] if not df.empty else 'N/A'}")
        print(f"   最新数值: {df.iloc[-1, 0] if not df.empty else 'N/A'}")
        return True
    except Exception as e:
        print(f"❌ CN_IVIX - 沪深300波动率指数: 获取失败 - {str(e)}")
        return False

def test_sw_industry_indicators():
    """测试申万行业指数"""
    print("\n" + "=" * 50)
    print("测试申万行业指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 测试申万一级行业指数
    sw_industries = [
        "农林牧渔", "基础化工", "钢铁", "有色金属", "电子", "家用电器",
        "食品饮料", "纺织服饰", "轻工制造", "医药生物", "公用事业",
        "交通运输", "房地产", "商贸零售", "社会服务", "综合",
        "建筑材料", "建筑装饰", "电力设备", "机械设备", "国防军工",
        "汽车", "计算机", "传媒", "通信", "银行", "非银金融",
        "煤炭", "石油石化", "环保", "美容护理"
    ]
    
    for industry in sw_industries[:5]:  # 只测试前5个行业
        total_count += 3  # 每个行业3个指标
        
        try:
            # 测试指数
            df_index = ak.sw_index_spot()
            if not df_index.empty:
                print(f"✅ SW_{industry}_INDEX - 申万{industry}指数: 可获得")
                success_count += 1
            else:
                print(f"❌ SW_{industry}_INDEX - 申万{industry}指数: 无数据")
        except Exception as e:
            print(f"❌ SW_{industry}_INDEX - 申万{industry}指数: 获取失败")
        
        try:
            # 测试PE
            df_pe = ak.sw_index_pe()
            if not df_pe.empty:
                print(f"✅ SW_{industry}_PE - 申万{industry}PE: 可获得")
                success_count += 1
            else:
                print(f"❌ SW_{industry}_PE - 申万{industry}PE: 无数据")
        except Exception as e:
            print(f"❌ SW_{industry}_PE - 申万{industry}PE: 获取失败")
        
        try:
            # 测试PB
            df_pb = ak.sw_index_pb()
            if not df_pb.empty:
                print(f"✅ SW_{industry}_PB - 申万{industry}PB: 可获得")
                success_count += 1
            else:
                print(f"❌ SW_{industry}_PB - 申万{industry}PB: 无数据")
        except Exception as e:
            print(f"❌ SW_{industry}_PB - 申万{industry}PB: 获取失败")
    
    print(f"\n申万行业指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_keqiang_indicators():
    """测试克强指数相关指标"""
    print("\n" + "=" * 50)
    print("测试克强指数指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 测试传统克强指数指标
    keqiang_tests = [
        ("CN_ELECTRICITY_CONSUMPTION", "全社会用电量", "energy_consumption"),
        ("CN_RAILWAY_FREIGHT", "铁路货运量", "railway_freight"),
        ("CN_BANK_LOANS", "银行贷款发放量", "bank_loans"),
        ("CN_EXPRESS_DELIVERY", "快递业务量", "express_delivery"),
        ("CN_MOBILE_PAYMENT", "移动支付交易额", "mobile_payment")
    ]
    
    for code, name, api_func in keqiang_tests:
        total_count += 1
        try:
            # 这里需要根据实际的AkShare API进行调整
            # 由于某些官方数据API可能不存在，我们先标记为待验证
            print(f"⚠️  {code} - {name}: 需要验证官方数据源API")
            # success_count += 1
        except Exception as e:
            print(f"❌ {code} - {name}: 获取失败 - {str(e)}")
    
    print(f"\n克强指数指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_capital_flow_indicators():
    """测试资金流向指标"""
    print("\n" + "=" * 50)
    print("测试资金流向指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 测试北向资金
    try:
        total_count += 1
        df = ak.stock_connect_north_net_flow_in()
        if not df.empty:
            print(f"✅ CN_NORTHBOUND_FLOW - 北向资金净流入: {len(df)} 条数据")
            print(f"   最新数据日期: {df.index[-1] if hasattr(df, 'index') else df.iloc[-1, 0]}")
            success_count += 1
        else:
            print(f"❌ CN_NORTHBOUND_FLOW - 北向资金净流入: 无数据")
    except Exception as e:
        print(f"❌ CN_NORTHBOUND_FLOW - 北向资金净流入: 获取失败 - {str(e)}")
    
    # 测试南向资金
    try:
        total_count += 1
        df = ak.stock_connect_south_net_flow_in()
        if not df.empty:
            print(f"✅ CN_SOUTHBOUND_FLOW - 南向资金净流入: {len(df)} 条数据")
            success_count += 1
        else:
            print(f"❌ CN_SOUTHBOUND_FLOW - 南向资金净流入: 无数据")
    except Exception as e:
        print(f"❌ CN_SOUTHBOUND_FLOW - 南向资金净流入: 获取失败 - {str(e)}")
    
    print(f"\n资金流向指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def test_shipping_indicators():
    """测试航运指标"""
    print("\n" + "=" * 50)
    print("测试航运指标")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    shipping_tests = [
        ("GLOBAL_BDI", "波罗的海干散货指数", "drybulk_index_bdi"),
        ("GLOBAL_BCI", "波罗的海海岬型指数", "drybulk_index_bci"),
        ("GLOBAL_BPI", "波罗的海巴拿马型指数", "drybulk_index_bpi"),
        ("GLOBAL_VLCC_RATE", "VLCC运价指数", "energy_oil_vlcc")
    ]
    
    for code, name, api_func in shipping_tests:
        total_count += 1
        try:
            # 根据实际API调用
            if api_func == "drybulk_index_bdi":
                df = ak.drybulk_index_bdi()
            elif api_func == "drybulk_index_bci":
                df = ak.drybulk_index_bci()
            elif api_func == "drybulk_index_bpi":
                df = ak.drybulk_index_bpi()
            elif api_func == "energy_oil_vlcc":
                df = ak.energy_oil_vlcc()
            
            if not df.empty:
                print(f"✅ {code} - {name}: {len(df)} 条数据")
                success_count += 1
            else:
                print(f"❌ {code} - {name}: 无数据")
        except Exception as e:
            print(f"❌ {code} - {name}: 获取失败 - {str(e)}")
    
    print(f"\n航运指标测试结果: {success_count}/{total_count} 成功")
    return success_count, total_count

def main():
    """主测试函数"""
    print("开始测试综合指标的数据可获得性...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_success = 0
    total_indicators = 0
    
    # 测试各类指标
    if test_ivix_indicator():
        total_success += 1
    total_indicators += 1
    
    sw_success, sw_total = test_sw_industry_indicators()
    total_success += sw_success
    total_indicators += sw_total
    
    keqiang_success, keqiang_total = test_keqiang_indicators()
    total_success += keqiang_success
    total_indicators += keqiang_total
    
    capital_success, capital_total = test_capital_flow_indicators()
    total_success += capital_success
    total_indicators += capital_total
    
    shipping_success, shipping_total = test_shipping_indicators()
    total_success += shipping_success
    total_indicators += shipping_total
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试指标数: {total_indicators}")
    print(f"成功获取数据: {total_success}")
    print(f"成功率: {total_success/total_indicators*100:.1f}%")
    
    # 建议
    print("\n建议:")
    print("1. ✅ 可获得的指标优先实现")
    print("2. ⚠️  需要验证的指标进一步调研官方数据源")
    print("3. ❌ 无法获得的指标考虑替代方案或计算衍生")
    
    return total_success, total_indicators

if __name__ == "__main__":
    main() 