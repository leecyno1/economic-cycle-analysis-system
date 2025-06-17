# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 扩充版指标配置文件
基于现有指标和AkShare数据，通过计算方式扩充关键投资分析指标

核心扩充策略：
1. 利用现有指标计算衍生指标（如M1-M2剪刀差、收益率曲线斜率）
2. 增加AkShare提供但未包含的重要指标
3. 建立计算指标的数据依赖关系
4. 保持原有指标体系不变，仅做增量扩充
"""

# 导入原有配置
from .indicators_config import INDICATORS_CONFIG

# 扩充的指标配置
EXPANDED_INDICATORS_CONFIG = INDICATORS_CONFIG.copy()

# 1. 流动性面 - 从宏观经济面独立出来并扩充
EXPANDED_INDICATORS_CONFIG["流动性面"] = {
    "description": "央行政策、银行间流动性、信用投放、利率传导",
    "indicators": [
        # 央行政策工具
        {"name": "存款准备金率", "code": "CN_RRR", "akshare_func": "tool_china_rrr", "frequency": "M", "lead_lag": "LEAD"},
        {"name": "央行公开市场操作", "code": "PBOC_OMO", "akshare_func": "bond_china_close_return", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "中期借贷便利MLF", "code": "PBOC_MLF", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
        
        # 银行间利率
        {"name": "7天SHIBOR", "code": "CN_SHIBOR_7D", "akshare_func": "macro_china_shibor_all", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "3个月SHIBOR", "code": "CN_SHIBOR_3M", "akshare_func": "macro_china_shibor_all", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "1年期SHIBOR", "code": "CN_SHIBOR_1Y", "akshare_func": "macro_china_shibor_all", "frequency": "D", "lead_lag": "LEAD"},
        
        # LPR利率
        {"name": "LPR1年期", "code": "CN_LPR_1Y", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
        {"name": "LPR5年期", "code": "CN_LPR_5Y", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
        
        # 货币供应量
        {"name": "M2货币供应量年率", "code": "CN_M2_YEARLY", "akshare_func": "macro_china_m2_yearly", "frequency": "M", "lead_lag": "LEAD"},
        {"name": "M1货币供应量年率", "code": "CN_M1_YEARLY", "akshare_func": "macro_china_m1_yearly", "frequency": "M", "lead_lag": "LEAD"},
        
        # 信贷投放
        {"name": "社会融资规模存量", "code": "CN_SOCIAL_FINANCING", "akshare_func": "macro_china_shrzgm", "frequency": "M", "lead_lag": "LEAD"},
        {"name": "新增人民币贷款", "code": "CN_NEW_RMB_LOAN", "akshare_func": "macro_rmb_loan", "frequency": "M", "lead_lag": "LEAD"},
        {"name": "新增社会融资", "code": "CN_NEW_FINANCIAL_CREDIT", "akshare_func": "macro_china_new_financial_credit", "frequency": "M", "lead_lag": "LEAD"},
        
        # 债券市场
        {"name": "10年期国债收益率", "code": "CN_10Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "5年期国债收益率", "code": "CN_5Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "2年期国债收益率", "code": "CN_2Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "1年期国债收益率", "code": "CN_1Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
        
        # 企业债收益率
        {"name": "AAA级企业债收益率", "code": "CN_AAA_CORP_YIELD", "akshare_func": "bond_china_yield", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "AA级企业债收益率", "code": "CN_AA_CORP_YIELD", "akshare_func": "bond_china_yield", "frequency": "D", "lead_lag": "LEAD"},
        
        # 回购利率
        {"name": "银行间质押式回购1天", "code": "CN_REPO_1D", "akshare_func": "repo_rate_hist", "frequency": "D", "lead_lag": "LEAD"},
        {"name": "银行间质押式回购7天", "code": "CN_REPO_7D", "akshare_func": "repo_rate_hist", "frequency": "D", "lead_lag": "LEAD"},
    ]
}

# 2. 扩充海外面指标
EXPANDED_INDICATORS_CONFIG["海外面"]["indicators"].extend([
    # 美国利率指标
    {"name": "美联储基准利率", "code": "US_FED_RATE", "akshare_func": "macro_usa_federal_fund_rate", "frequency": "M", "lead_lag": "LEAD"},
    {"name": "美国10年期国债收益率", "code": "US_10Y_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "美国2年期国债收益率", "code": "US_2Y_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "美国5年期国债收益率", "code": "US_5Y_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
    
    # 美国经济数据
    {"name": "美国核心CPI月率", "code": "US_CORE_CPI_MONTHLY", "akshare_func": "macro_usa_core_cpi_monthly", "frequency": "M", "lead_lag": "LEAD"},
    {"name": "美国非农就业人数", "code": "US_NONFARM_PAYROLL", "akshare_func": "macro_usa_non_farm", "frequency": "M", "lead_lag": "LEAD"},
    {"name": "美国服务业PMI", "code": "US_PMI_SERVICE", "akshare_func": "macro_usa_services_pmi", "frequency": "M", "lead_lag": "LEAD"},
    
    # 国际大宗商品
    {"name": "WTI原油期货", "code": "WTI_OIL_FUTURES", "akshare_func": "energy_oil_hist", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "布伦特原油期货", "code": "BRENT_OIL_FUTURES", "akshare_func": "energy_oil_hist", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "铜期货价格", "code": "COPPER_FUTURES", "akshare_func": "futures_global_commodity_hist", "frequency": "D", "lead_lag": "LEAD"},
    
    # 美股指数
    {"name": "道琼斯工业指数", "code": "DJI_INDEX", "akshare_func": "index_us_stock_sina", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "纳斯达克指数", "code": "NASDAQ_INDEX", "akshare_func": "index_us_stock_sina", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "标普500指数", "code": "SPX_INDEX", "akshare_func": "index_us_stock_sina", "frequency": "D", "lead_lag": "SYNC"},
    
    # 汇率
    {"name": "美元指数", "code": "USD_INDEX", "akshare_func": "currency_us_dollar_index", "frequency": "D", "lead_lag": "LEAD"},
])

# 3. 扩充宏观经济面指标
EXPANDED_INDICATORS_CONFIG["宏观经济面"]["indicators"].extend([
    # 核心通胀指标
    {"name": "中国核心CPI年率", "code": "CN_CORE_CPI_YEARLY", "akshare_func": "macro_china_core_cpi", "frequency": "M", "lead_lag": "LAG"},
    {"name": "PPIRM年率(原材料购进价格)", "code": "CN_PPIRM_YEARLY", "akshare_func": "macro_china_ppirm", "frequency": "M", "lead_lag": "LEAD"},
    
    # 投资和消费
    {"name": "固定资产投资累计同比", "code": "CN_FAI_YTD", "akshare_func": "macro_china_fixed_asset_investment", "frequency": "M", "lead_lag": "LAG"},
    {"name": "基建投资累计同比", "code": "CN_INFRASTRUCTURE_INV", "akshare_func": "macro_china_infrastructure_investment", "frequency": "M", "lead_lag": "LAG"},
    {"name": "房地产开发投资同比", "code": "CN_REALESTATE_INV", "akshare_func": "macro_china_real_estate", "frequency": "M", "lead_lag": "LAG"},
    {"name": "制造业投资累计同比", "code": "CN_MANUFACTURING_INV", "akshare_func": "macro_china_manufacturing_investment", "frequency": "M", "lead_lag": "LAG"},
    {"name": "社会消费品零售总额同比", "code": "CN_RETAIL_SALES", "akshare_func": "macro_china_retail_sales", "frequency": "M", "lead_lag": "LAG"},
    
    # 先行指标
    {"name": "财新服务业PMI", "code": "CN_PMI_CAIXIN_SERVICE", "akshare_func": "index_pmi_ser_cx", "frequency": "M", "lead_lag": "LEAD"},
    {"name": "财新综合PMI", "code": "CN_PMI_CAIXIN_COMPOSITE", "akshare_func": "index_pmi_com_cx", "frequency": "M", "lead_lag": "LEAD"},
    
    # 就业指标
    {"name": "城镇调查失业率", "code": "CN_URBAN_UNEMPLOYMENT", "akshare_func": "macro_china_unemployment", "frequency": "M", "lead_lag": "SYNC"},
    
    # 库存周期（关键！）
    {"name": "工业企业产成品库存同比", "code": "CN_INVENTORY_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "SYNC"},
])

# 4. 扩充企业基本面指标
EXPANDED_INDICATORS_CONFIG["企业基本面"]["indicators"].extend([
    # 企业盈利指标
    {"name": "规模以上工业企业利润总额同比", "code": "CN_INDUSTRIAL_PROFIT_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
    {"name": "规模以上工业企业营业收入同比", "code": "CN_INDUSTRIAL_REVENUE_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
    {"name": "工业企业资产负债率", "code": "CN_INDUSTRIAL_DEBT_RATIO", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
    
    # 更多估值指标
    {"name": "沪深300PE", "code": "CSI300_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
    {"name": "沪深300PB", "code": "CSI300_PB", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
    {"name": "上证50PB", "code": "SSE50_PB", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
    {"name": "创业板指PB", "code": "CHINEXT_PB", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
])

# 5. 扩充政策面指标
EXPANDED_INDICATORS_CONFIG["政策面"]["indicators"].extend([
    # 财政政策
    {"name": "一般公共预算收入同比", "code": "CN_FISCAL_REVENUE_GROWTH", "akshare_func": "macro_china_fiscal_revenue", "frequency": "M", "lead_lag": "LAG"},
    {"name": "一般公共预算支出同比", "code": "CN_FISCAL_EXPENDITURE_GROWTH", "akshare_func": "macro_china_fiscal_expenditure", "frequency": "M", "lead_lag": "LAG"},
    {"name": "政府性基金收入同比", "code": "CN_GOV_FUND_REVENUE_GROWTH", "akshare_func": "macro_china_gov_fund_revenue", "frequency": "M", "lead_lag": "LAG"},
    
    # 房地产政策效果
    {"name": "70大中城市房价指数", "code": "CN_HOUSE_PRICE_INDEX", "akshare_func": "macro_china_house_price", "frequency": "M", "lead_lag": "LAG"},
    {"name": "商品房销售面积同比", "code": "CN_HOUSE_SALES_AREA_GROWTH", "akshare_func": "macro_china_house_sales", "frequency": "M", "lead_lag": "LAG"},
    {"name": "商品房销售额同比", "code": "CN_HOUSE_SALES_VALUE_GROWTH", "akshare_func": "macro_china_house_sales", "frequency": "M", "lead_lag": "LAG"},
    
    # 债券发行
    {"name": "地方政府专项债发行规模", "code": "CN_LOCAL_SPECIAL_BOND", "akshare_func": "bond_china_local_government", "frequency": "M", "lead_lag": "LEAD"},
])

# 6. 扩充市场面指标
EXPANDED_INDICATORS_CONFIG["市场面"]["indicators"].extend([
    # 更多行业指数
    {"name": "军工指数", "code": "SW_DEFENSE", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "新能源指数", "code": "SW_NEW_ENERGY", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "半导体指数", "code": "SW_SEMICONDUCTOR", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "消费指数", "code": "SW_CONSUMPTION", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
    
    # 期货品种
    {"name": "螺纹钢主力合约", "code": "REBAR_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "铁矿石主力合约", "code": "IRON_ORE_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "焦煤主力合约", "code": "COKING_COAL_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "焦炭主力合约", "code": "COKE_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "动力煤主力合约", "code": "THERMAL_COAL_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "沪铜主力合约", "code": "COPPER_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "沪锌主力合约", "code": "ZINC_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    {"name": "沪铝主力合约", "code": "ALUMINUM_MAIN", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
    
    # 汇率相关
    {"name": "美元兑人民币汇率", "code": "USD_CNY_RATE", "akshare_func": "currency_convert", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "欧元兑人民币汇率", "code": "EUR_CNY_RATE", "akshare_func": "currency_convert", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "人民币汇率指数", "code": "RMB_INDEX", "akshare_func": "currency_rmb_index", "frequency": "D", "lead_lag": "SYNC"},
])

# 7. 扩充情绪面指标
EXPANDED_INDICATORS_CONFIG["情绪面"]["indicators"].extend([
    # 中国版恐慌指数
    {"name": "中国波动率指数", "code": "CN_VIX", "akshare_func": "index_vix_zh", "frequency": "D", "lead_lag": "LEAD"},
    
    # 资金流向细分
    {"name": "深股通资金流入", "code": "SZSE_CONNECT_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "沪股通资金流入", "code": "SSE_CONNECT_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
    
    # 交易活跃度
    {"name": "A股平均换手率", "code": "A_SHARE_TURNOVER_RATE", "akshare_func": "stock_zh_a_spot_em", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "两市成交金额", "code": "TOTAL_MARKET_TURNOVER", "akshare_func": "stock_zh_a_spot_em", "frequency": "D", "lead_lag": "SYNC"},
    
    # 机构行为
    {"name": "股票型基金净值增长率", "code": "EQUITY_FUND_NAV_GROWTH", "akshare_func": "fund_em_change", "frequency": "D", "lead_lag": "SYNC"},
    {"name": "ETF资金净流入", "code": "ETF_NET_INFLOW", "akshare_func": "fund_etf_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
    
    # 新股供给
    {"name": "IPO募资总额", "code": "IPO_FUND_RAISED", "akshare_func": "stock_ipo_info", "frequency": "M", "lead_lag": "LAG"},
    {"name": "可转债发行规模", "code": "CONVERTIBLE_BOND_ISSUANCE", "akshare_func": "bond_cb_index_jsl", "frequency": "M", "lead_lag": "LAG"},
])

# 8. 新增：计算指标配置
CALCULATED_INDICATORS_CONFIG = {
    "计算指标": {
        "description": "基于现有指标计算的衍生指标，用于投资分析和周期判断",
        "indicators": [
            # 流动性指标
            {"name": "M1-M2剪刀差", "code": "CN_M1_M2_SPREAD", "calculation": "CN_M1_YEARLY - CN_M2_YEARLY", 
             "description": "M1增速减去M2增速，反映企业活力", "frequency": "M", "lead_lag": "LEAD"},
            
            # 利率指标
            {"name": "收益率曲线斜率(10Y-2Y)", "code": "CN_YIELD_CURVE_SLOPE", 
             "calculation": "CN_10Y_BOND_YIELD - CN_2Y_BOND_YIELD", 
             "description": "长短端利差，反映经济增长预期", "frequency": "D", "lead_lag": "LEAD"},
            
            {"name": "收益率曲线斜率(10Y-1Y)", "code": "CN_YIELD_CURVE_SLOPE_10Y1Y", 
             "calculation": "CN_10Y_BOND_YIELD - CN_1Y_BOND_YIELD", 
             "description": "长短端利差（备选指标）", "frequency": "D", "lead_lag": "LEAD"},
            
            {"name": "LPR利差(5Y-1Y)", "code": "CN_LPR_SPREAD", 
             "calculation": "CN_LPR_5Y - CN_LPR_1Y", 
             "description": "LPR长短端利差", "frequency": "M", "lead_lag": "LEAD"},
            
            # 信用风险指标
            {"name": "信用利差(AAA-国债10Y)", "code": "CN_CREDIT_SPREAD_AAA", 
             "calculation": "CN_AAA_CORP_YIELD - CN_10Y_BOND_YIELD", 
             "description": "AAA企业债与国债利差，反映信用风险", "frequency": "D", "lead_lag": "LEAD"},
            
            {"name": "信用利差(AA-国债10Y)", "code": "CN_CREDIT_SPREAD_AA", 
             "calculation": "CN_AA_CORP_YIELD - CN_10Y_BOND_YIELD", 
             "description": "AA企业债与国债利差", "frequency": "D", "lead_lag": "LEAD"},
            
            # 国际比较指标
            {"name": "中美利差(10年期)", "code": "CN_US_INTEREST_SPREAD", 
             "calculation": "CN_10Y_BOND_YIELD - US_10Y_YIELD", 
             "description": "中美10年期国债利差", "frequency": "D", "lead_lag": "LEAD"},
            
            {"name": "中美利差(2年期)", "code": "CN_US_INTEREST_SPREAD_2Y", 
             "calculation": "CN_2Y_BOND_YIELD - US_2Y_YIELD", 
             "description": "中美2年期国债利差", "frequency": "D", "lead_lag": "LEAD"},
            
            {"name": "美债收益率曲线斜率", "code": "US_YIELD_CURVE_SLOPE", 
             "calculation": "US_10Y_YIELD - US_2Y_YIELD", 
             "description": "美国长短端利差，重要的衰退预警指标", "frequency": "D", "lead_lag": "LEAD"},
            
            # 风险偏好指标
            {"name": "股债收益率比", "code": "CN_STOCK_BOND_YIELD_RATIO", 
             "calculation": "(1/CSI300_PE) / (CN_10Y_BOND_YIELD/100)", 
             "description": "股票收益率与债券收益率比值", "frequency": "D", "lead_lag": "SYNC"},
            
            {"name": "股票风险溢价", "code": "CN_EQUITY_RISK_PREMIUM", 
             "calculation": "(1/CSI300_PE) - (CN_10Y_BOND_YIELD/100)", 
             "description": "股票收益率减去无风险收益率", "frequency": "D", "lead_lag": "SYNC"},
        ]
    }
}

# 合并所有配置
EXPANDED_INDICATORS_CONFIG["计算指标"] = CALCULATED_INDICATORS_CONFIG["计算指标"]

def get_expanded_indicator_count():
    """获取扩充版指标总数"""
    return sum(len(category["indicators"]) for category in EXPANDED_INDICATORS_CONFIG.values())

def get_calculation_dependencies():
    """获取计算指标的依赖关系"""
    dependencies = {}
    for indicator in CALCULATED_INDICATORS_CONFIG["计算指标"]["indicators"]:
        if "calculation" in indicator:
            # 简单的依赖解析（实际实现时需要更复杂的解析）
            calculation = indicator["calculation"]
            deps = []
            for category_data in EXPANDED_INDICATORS_CONFIG.values():
                for base_indicator in category_data["indicators"]:
                    if base_indicator["code"] in calculation:
                        deps.append(base_indicator["code"])
            dependencies[indicator["code"]] = deps
    return dependencies

def get_enhanced_category_summary():
    """获取增强版各类别指标统计"""
    summary = {}
    total_count = 0
    for category, data in EXPANDED_INDICATORS_CONFIG.items():
        count = len(data["indicators"])
        summary[category] = {
            "count": count,
            "description": data["description"]
        }
        total_count += count
    
    summary["总计"] = {"count": total_count, "description": "所有指标总数"}
    return summary

# 投资逻辑应用配置
INVESTMENT_LOGIC_APPLICATIONS = {
    "美林投资时钟": {
        "经济增长指标": ["CN_GDP_YEARLY", "CN_PMI_MFG", "CN_INDUSTRIAL_ADDED_VALUE"],
        "通胀指标": ["CN_CPI_YEARLY", "CN_CORE_CPI_YEARLY", "CN_PPI_YEARLY"],
        "象限判断逻辑": {
            "复苏": "经济增长回升 + 通胀温和",
            "过热": "经济增长高位 + 通胀上升", 
            "滞胀": "经济增长放缓 + 通胀高位",
            "衰退": "经济增长低迷 + 通胀回落"
        }
    },
    
    "流动性周期": {
        "央行政策": ["CN_RRR", "PBOC_OMO", "PBOC_MLF"],
        "流动性状况": ["CN_M1_M2_SPREAD", "CN_SHIBOR_7D", "CN_YIELD_CURVE_SLOPE"],
        "信用传导": ["CN_CREDIT_SPREAD_AAA", "CN_NEW_RMB_LOAN", "CN_SOCIAL_FINANCING"]
    },
    
    "库存周期": {
        "库存指标": ["CN_INVENTORY_GROWTH", "INVENTORY_OUTPUT_RATIO"],
        "价格传导": ["CN_PPI_YEARLY", "CN_PPI_CPI_SPREAD"],
        "需求指标": ["CN_PMI_MFG", "CN_INDUSTRIAL_ADDED_VALUE"]
    },
    
    "风险偏好": {
        "恐慌指标": ["VIX_INDEX", "CN_VIX"],
        "资金流向": ["NORTHBOUND_CAPITAL", "MARGIN_BALANCE"],
        "估值指标": ["CN_STOCK_BOND_YIELD_RATIO", "CN_EQUITY_RISK_PREMIUM"]
    }
}

if __name__ == "__main__":
    print("=== 扩充版经济周期指标体系 ===")
    summary = get_enhanced_category_summary()
    for category, info in summary.items():
        print(f"{category}: {info['count']}个指标")
        if category != "总计":
            print(f"  描述: {info['description']}")
    
    print(f"\n=== 计算指标依赖关系 ===")
    deps = get_calculation_dependencies()
    for calc_indicator, base_indicators in deps.items():
        print(f"{calc_indicator}: 依赖 {base_indicators}") 