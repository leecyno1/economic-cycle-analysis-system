# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 指标配置文件
定义7大类别、100+指标的详细配置信息

7大类别：
1. 海外面 - 美经济数据、联邦利率、国际政策评分
2. 资金面 - 北向、南向、两融数据
3. 宏观经济面 - CPI、PPI、PMI、社融、信用、M1、M2、克强指数等
4. 企业基本面 - 盈利预期、财务数据
5. 政策面 - 赤字率、专项债、地方债、特别国债发行、重大产业政策评分、央行相关数据等
6. 市场面 - 全球大宗、股市、债券市场、A股风格指数、行业指数量价表现
7. 情绪面 - 交易情绪指标、舆情指数等
"""

INDICATORS_CONFIG = {
    # 1. 海外面 (Overseas)
    "海外面": {
        "description": "美经济数据、联邦利率、国际政策评分",
        "indicators": [
            # 美国经济指标
            {"name": "美国CPI月率", "code": "US_CPI_MONTHLY", "akshare_func": "macro_usa_cpi_monthly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国失业率", "code": "US_UNEMPLOYMENT", "akshare_func": "macro_usa_unemployment_rate", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "美国制造业PMI", "code": "US_PMI_MFG", "akshare_func": "macro_usa_pmi", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国初请失业金", "code": "US_INITIAL_JOBLESS", "akshare_func": "macro_usa_initial_jobless", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国ADP就业", "code": "US_ADP_EMPLOYMENT", "akshare_func": "macro_usa_adp_employment", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国耐用品订单", "code": "US_DURABLE_GOODS", "akshare_func": "macro_usa_durable_goods_orders", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国零售销售", "code": "US_RETAIL_SALES", "akshare_func": "macro_usa_retail_sales", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "美国现房销售", "code": "US_EXIST_HOME_SALES", "akshare_func": "macro_usa_exist_home_sales", "frequency": "M", "lead_lag": "LAG"},
            {"name": "美国新屋开工", "code": "US_HOUSE_STARTS", "akshare_func": "macro_usa_house_starts", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国密歇根消费者信心", "code": "US_MICHIGAN_SENTIMENT", "akshare_func": "macro_usa_michigan_consumer_sentiment", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国劳动力市场状况指数", "code": "US_LMCI", "akshare_func": "macro_usa_lmci", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "美国EIA原油库存", "code": "US_EIA_CRUDE", "akshare_func": "macro_usa_eia_crude_rate", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "美国API原油库存", "code": "US_API_CRUDE", "akshare_func": "macro_usa_api_crude_stock", "frequency": "M", "lead_lag": "SYNC"},
        ]
    },
    
    # 2. 资金面 (Capital Flow)
    "资金面": {
        "description": "北向、南向、两融数据",
        "indicators": [
            {"name": "北向资金净流入", "code": "NORTHBOUND_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "南向资金净流入", "code": "SOUTHBOUND_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "融资余额", "code": "MARGIN_BALANCE", "akshare_func": "stock_margin_detail_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "融券余额", "code": "SHORT_BALANCE", "akshare_func": "stock_margin_detail_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "两融余额", "code": "TOTAL_MARGIN", "akshare_func": "stock_margin_detail_em", "frequency": "D", "lead_lag": "SYNC"},
        ]
    },

    # 3. 宏观经济面 (Macroeconomic)  
    "宏观经济面": {
        "description": "CPI、PPI、PMI、社融、信用、M1、M2、克强指数等",
        "indicators": [
            # 价格指标
            {"name": "中国CPI月率", "code": "CN_CPI_MONTHLY", "akshare_func": "macro_china_cpi_monthly", "frequency": "M", "lead_lag": "LAG"},
            {"name": "中国PPI年率", "code": "CN_PPI_YEARLY", "akshare_func": "macro_china_ppi_yearly", "frequency": "M", "lead_lag": "LEAD"},
            
            # 货币供应量
            {"name": "M2货币供应量年率", "code": "CN_M2_YEARLY", "akshare_func": "macro_china_m2_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "M1货币供应量年率", "code": "CN_M1_YEARLY", "akshare_func": "macro_china_m1_yearly", "frequency": "M", "lead_lag": "LEAD"},
            
            # PMI指标
            {"name": "中国官方制造业PMI", "code": "CN_PMI_MFG", "akshare_func": "macro_china_pmi_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "中国官方非制造业PMI", "code": "CN_PMI_NON_MFG", "akshare_func": "macro_china_non_man_pmi", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "财新制造业PMI", "code": "CN_PMI_CAIXIN_MFG", "akshare_func": "index_pmi_man_cx", "frequency": "M", "lead_lag": "LEAD"},
            
            # 贸易指标  
            {"name": "中国进口年率(美元)", "code": "CN_IMPORTS_YOY", "akshare_func": "macro_china_imports_yoy", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "中国出口年率(美元)", "code": "CN_EXPORTS_YOY", "akshare_func": "macro_china_exports_yoy", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "中国贸易差额", "code": "CN_TRADE_BALANCE", "akshare_func": "macro_china_trade_balance", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "外商直接投资", "code": "CN_FDI", "akshare_func": "macro_china_fdi", "frequency": "M", "lead_lag": "LAG"},
            
            # 社融与信贷
            {"name": "社会融资规模存量", "code": "CN_SOCIAL_FINANCING", "akshare_func": "macro_china_shrzgm", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "新增人民币贷款", "code": "CN_NEW_RMB_LOAN", "akshare_func": "macro_rmb_loan", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "新增社会融资", "code": "CN_NEW_FINANCIAL_CREDIT", "akshare_func": "macro_china_new_financial_credit", "frequency": "M", "lead_lag": "LEAD"},
            
            # GDP与增长
            {"name": "中国GDP年率", "code": "CN_GDP_YEARLY", "akshare_func": "macro_china_gdp_yearly", "frequency": "M", "lead_lag": "LAG"},
            {"name": "工业增加值年率", "code": "CN_INDUSTRIAL_ADDED_VALUE", "akshare_func": "macro_china_industrial_added_value", "frequency": "M", "lead_lag": "SYNC"},
            
            # 利率指标
            {"name": "上海银行间同业拆放利率", "code": "CN_SHIBOR", "akshare_func": "macro_china_shibor_all", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "LPR利率", "code": "CN_LPR", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
        ]
    },

    # 4. 企业基本面 (Corporate Fundamentals)
    "企业基本面": {
        "description": "盈利预期、财务数据",
        "indicators": [
            {"name": "A股整体PE", "code": "A_SHARE_PE", "akshare_func": "stock_zh_valuation_baidu", "frequency": "D", "lead_lag": "LAG"},
            {"name": "A股整体PB", "code": "A_SHARE_PB", "akshare_func": "stock_zh_valuation_baidu", "frequency": "D", "lead_lag": "LAG"},
            {"name": "创业板指PE", "code": "CHINEXT_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
            {"name": "中证500PE", "code": "CSI500_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
            {"name": "上证50PE", "code": "SSE50_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
        ]
    },

    # 5. 政策面 (Policy)
    "政策面": {
        "description": "赤字率、专项债、地方债、特别国债发行、重大产业政策评分、央行相关数据等",
        "indicators": [
            {"name": "央行公开市场操作", "code": "PBOC_OMO", "akshare_func": "bond_china_close_return", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "国债收益率10年", "code": "CN_BOND_10Y", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "国债收益率1年", "code": "CN_BOND_1Y", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "国债收益率5年", "code": "CN_BOND_5Y", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "存款准备金率", "code": "CN_RRR", "akshare_func": "tool_china_rrr", "frequency": "M", "lead_lag": "LEAD"},
        ]
    },

    # 6. 市场面 (Market Performance)
    "市场面": {
        "description": "全球大宗、股市、债券市场、A股风格指数、行业指数量价表现",
        "indicators": [
            # 股票指数
            {"name": "上证指数", "code": "SSE_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "深证成指", "code": "SZSE_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "创业板指", "code": "CHINEXT_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证500", "code": "CSI500_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "上证50", "code": "SSE50_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "沪深300", "code": "CSI300_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 风格指数
            {"name": "中证红利", "code": "CSI_DIVIDEND", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证价值", "code": "CSI_VALUE", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证成长", "code": "CSI_GROWTH", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 行业指数 (申万一级)
            {"name": "银行指数", "code": "SW_BANK", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "券商指数", "code": "SW_BROKER", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "房地产指数", "code": "SW_REALESTATE", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "有色金属", "code": "SW_NONFERROUS", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "钢铁指数", "code": "SW_STEEL", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "煤炭指数", "code": "SW_COAL", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "石油石化", "code": "SW_PETROCHEMICAL", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "电力指数", "code": "SW_POWER", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "食品饮料", "code": "SW_FOOD", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "医药生物", "code": "SW_PHARMA", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "电子指数", "code": "SW_ELECTRONICS", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "计算机指数", "code": "SW_COMPUTER", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "通信指数", "code": "SW_TELECOM", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "汽车指数", "code": "SW_AUTO", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "机械设备", "code": "SW_MACHINERY", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 大宗商品
            {"name": "黄金价格", "code": "GOLD_PRICE", "akshare_func": "macro_cons_gold", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "伦敦金属交易所库存", "code": "LME_STOCK", "akshare_func": "macro_euro_lme_stock", "frequency": "D", "lead_lag": "SYNC"},
            
            # 国际市场
            {"name": "全球股市指数", "code": "GLOBAL_INDICES", "akshare_func": "index_global_spot_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "港股指数", "code": "HK_INDICES", "akshare_func": "stock_hk_index_spot_sina", "frequency": "D", "lead_lag": "SYNC"},
        ]
    },

    # 7. 情绪面 (Market Sentiment)
    "情绪面": {
        "description": "交易情绪指标、舆情指数等",
        "indicators": [
            {"name": "VIX恐慌指数", "code": "VIX_INDEX", "akshare_func": "index_vix", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "股市成交额", "code": "MARKET_TURNOVER", "akshare_func": "stock_zh_a_spot_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "新增投资者数量", "code": "NEW_INVESTORS", "akshare_func": "stock_account_statistics_em", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "IPO发行数量", "code": "IPO_COUNT", "akshare_func": "stock_ipo_info", "frequency": "M", "lead_lag": "LAG"},
        ]
    }
}

def get_all_indicators():
    """获取所有指标的平铺列表"""
    all_indicators = []
    for category_name, category_data in INDICATORS_CONFIG.items():
        for indicator in category_data["indicators"]:
            indicator_copy = indicator.copy()
            indicator_copy["category"] = category_name
            all_indicators.append(indicator_copy)
    return all_indicators

def get_indicators_by_category(category_name):
    """根据类别获取指标"""
    if category_name in INDICATORS_CONFIG:
        return INDICATORS_CONFIG[category_name]["indicators"]
    return []

def get_indicator_count():
    """获取指标总数"""
    return sum(len(category["indicators"]) for category in INDICATORS_CONFIG.values())

if __name__ == "__main__":
    print(f"总指标数量: {get_indicator_count()}")
    for category, data in INDICATORS_CONFIG.items():
        print(f"{category}: {len(data['indicators'])}个指标") 