# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 增强版指标配置文件
基于投资理论优化的指标体系

投资理论基础：
1. 美林投资时钟：经济增长 + 通胀水平 → 资产配置
2. 康德拉季耶夫周期：技术创新驱动的长期经济周期
3. 库兹涅茨周期：房地产和基建驱动的中期周期
4. 基钦周期：库存周期驱动的短期波动
5. 流动性传导机制：央行政策 → 流动性 → 资产价格

增强的8大类别：
1. 海外面 - 全球经济环境与流动性
2. 流动性面 - 央行政策与市场流动性
3. 宏观经济面 - 增长、通胀、就业三大核心
4. 企业基本面 - 盈利能力与财务健康
5. 政策面 - 财政政策与产业政策
6. 市场面 - 资产价格与风险偏好
7. 情绪面 - 投资者行为与市场情绪
8. 周期特征面 - 专门的周期识别指标
"""

ENHANCED_INDICATORS_CONFIG = {
    # 1. 海外面 - 增强版
    "海外面": {
        "description": "全球经济环境、美联储政策、国际资本流动",
        "indicators": [
            # 美国核心经济指标
            {"name": "美国CPI月率", "code": "US_CPI_MONTHLY", "akshare_func": "macro_usa_cpi_monthly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国核心CPI年率", "code": "US_CORE_CPI_YEARLY", "akshare_func": "macro_usa_core_cpi_monthly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国失业率", "code": "US_UNEMPLOYMENT", "akshare_func": "macro_usa_unemployment_rate", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "美国非农就业", "code": "US_NONFARM_PAYROLL", "akshare_func": "macro_usa_non_farm", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美联储基准利率", "code": "US_FED_RATE", "akshare_func": "macro_usa_federal_fund_rate", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国10年期国债收益率", "code": "US_10Y_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "美国2年期国债收益率", "code": "US_2Y_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "美债收益率曲线斜率", "code": "US_YIELD_CURVE_SLOPE", "akshare_func": "calculated", "frequency": "D", "lead_lag": "LEAD"},
            
            # 美国先行指标
            {"name": "美国制造业PMI", "code": "US_PMI_MFG", "akshare_func": "macro_usa_pmi", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国服务业PMI", "code": "US_PMI_SERVICE", "akshare_func": "macro_usa_services_pmi", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国初请失业金", "code": "US_INITIAL_JOBLESS", "akshare_func": "macro_usa_initial_jobless", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国耐用品订单", "code": "US_DURABLE_GOODS", "akshare_func": "macro_usa_durable_goods_orders", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "美国消费者信心指数", "code": "US_CONSUMER_CONFIDENCE", "akshare_func": "macro_usa_michigan_consumer_sentiment", "frequency": "M", "lead_lag": "LEAD"},
            
            # 国际大宗商品（通胀传导）
            {"name": "WTI原油价格", "code": "WTI_OIL_PRICE", "akshare_func": "energy_oil_hist", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "布伦特原油价格", "code": "BRENT_OIL_PRICE", "akshare_func": "energy_oil_hist", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "铜期货价格", "code": "COPPER_FUTURES", "akshare_func": "futures_global_commodity_hist", "frequency": "D", "lead_lag": "LEAD"},
            
            # 全球股市风险偏好
            {"name": "道琼斯指数", "code": "DJI_INDEX", "akshare_func": "index_us_stock_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "纳斯达克指数", "code": "NASDAQ_INDEX", "akshare_func": "index_us_stock_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "美元指数", "code": "USD_INDEX", "akshare_func": "currency_us_dollar_index", "frequency": "D", "lead_lag": "LEAD"},
        ]
    },
    
    # 2. 流动性面 - 新增独立类别
    "流动性面": {
        "description": "央行政策、银行间流动性、信用投放",
        "indicators": [
            # 央行政策工具
            {"name": "存款准备金率", "code": "CN_RRR", "akshare_func": "tool_china_rrr", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "央行公开市场操作", "code": "PBOC_OMO", "akshare_func": "bond_china_close_return", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "中期借贷便利MLF", "code": "PBOC_MLF", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "常备借贷便利SLF", "code": "PBOC_SLF", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
            
            # 市场利率
            {"name": "上海银行间同业拆放利率SHIBOR", "code": "CN_SHIBOR", "akshare_func": "macro_china_shibor_all", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "LPR1年期利率", "code": "CN_LPR_1Y", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "LPR5年期利率", "code": "CN_LPR_5Y", "akshare_func": "rate_interbank", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "国债逆回购利率", "code": "CN_REPO_RATE", "akshare_func": "bond_repo_zh_sina", "frequency": "D", "lead_lag": "LEAD"},
            
            # 流动性数量指标
            {"name": "M2货币供应量年率", "code": "CN_M2_YEARLY", "akshare_func": "macro_china_m2_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "M1货币供应量年率", "code": "CN_M1_YEARLY", "akshare_func": "macro_china_m1_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "M1-M2剪刀差", "code": "CN_M1_M2_SPREAD", "akshare_func": "calculated", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "社会融资规模存量增速", "code": "CN_SOCIAL_FINANCING_GROWTH", "akshare_func": "macro_china_shrzgm", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "新增人民币贷款", "code": "CN_NEW_RMB_LOAN", "akshare_func": "macro_rmb_loan", "frequency": "M", "lead_lag": "LEAD"},
            
            # 信用利差（风险偏好）
            {"name": "10年期国债收益率", "code": "CN_10Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "AAA企业债收益率", "code": "CN_AAA_CORP_YIELD", "akshare_func": "bond_china_yield", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "信用利差(AAA-国债)", "code": "CN_CREDIT_SPREAD", "akshare_func": "calculated", "frequency": "D", "lead_lag": "LEAD"},
        ]
    },

    # 3. 宏观经济面 (Macroeconomic) - 优化版
    "宏观经济面": {
        "description": "经济增长、通胀压力、就业状况 - 美林时钟核心变量",
        "indicators": [
            # 经济增长指标
            {"name": "中国GDP年率", "code": "CN_GDP_YEARLY", "akshare_func": "macro_china_gdp_yearly", "frequency": "M", "lead_lag": "LAG"},
            {"name": "工业增加值年率", "code": "CN_INDUSTRIAL_ADDED_VALUE", "akshare_func": "macro_china_industrial_added_value", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "固定资产投资累计增速", "code": "CN_FAI_YTD", "akshare_func": "macro_china_fixed_asset_investment", "frequency": "M", "lead_lag": "LAG"},
            {"name": "基建投资增速", "code": "CN_INFRASTRUCTURE_INV", "akshare_func": "macro_china_infrastructure_investment", "frequency": "M", "lead_lag": "LAG"},
            {"name": "房地产投资增速", "code": "CN_REALESTATE_INV", "akshare_func": "macro_china_real_estate", "frequency": "M", "lead_lag": "LAG"},
            {"name": "制造业投资增速", "code": "CN_MANUFACTURING_INV", "akshare_func": "macro_china_manufacturing_investment", "frequency": "M", "lead_lag": "LAG"},
            
            # 消费指标
            {"name": "社会消费品零售总额增速", "code": "CN_RETAIL_SALES", "akshare_func": "macro_china_retail_sales", "frequency": "M", "lead_lag": "LAG"},
            {"name": "消费者信心指数", "code": "CN_CONSUMER_CONFIDENCE", "akshare_func": "macro_china_consumer_confidence", "frequency": "M", "lead_lag": "LEAD"},
            
            # 通胀指标 - 关键！
            {"name": "中国CPI年率", "code": "CN_CPI_YEARLY", "akshare_func": "macro_china_cpi_yearly", "frequency": "M", "lead_lag": "LAG"},
            {"name": "中国核心CPI年率", "code": "CN_CORE_CPI_YEARLY", "akshare_func": "macro_china_core_cpi", "frequency": "M", "lead_lag": "LAG"},
            {"name": "中国PPI年率", "code": "CN_PPI_YEARLY", "akshare_func": "macro_china_ppi_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "PPIRM年率(工业品出厂价格)", "code": "CN_PPIRM_YEARLY", "akshare_func": "macro_china_ppirm", "frequency": "M", "lead_lag": "LEAD"},
            
            # 先行指标
            {"name": "中国官方制造业PMI", "code": "CN_PMI_MFG", "akshare_func": "macro_china_pmi_yearly", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "中国官方非制造业PMI", "code": "CN_PMI_NON_MFG", "akshare_func": "macro_china_non_man_pmi", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "财新制造业PMI", "code": "CN_PMI_CAIXIN_MFG", "akshare_func": "index_pmi_man_cx", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "财新服务业PMI", "code": "CN_PMI_CAIXIN_SERVICE", "akshare_func": "index_pmi_ser_cx", "frequency": "M", "lead_lag": "LEAD"},
            
            # 对外贸易
            {"name": "中国出口年率(美元)", "code": "CN_EXPORTS_YOY", "akshare_func": "macro_china_exports_yoy", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "中国进口年率(美元)", "code": "CN_IMPORTS_YOY", "akshare_func": "macro_china_imports_yoy", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "贸易差额", "code": "CN_TRADE_BALANCE", "akshare_func": "macro_china_trade_balance", "frequency": "M", "lead_lag": "SYNC"},
            
            # 库存周期指标（基钦周期）
            {"name": "工业企业产成品库存增速", "code": "CN_INVENTORY_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "SYNC"},
        ]
    },

    # 4. 企业基本面 (Corporate Fundamentals) - 增强版
    "企业基本面": {
        "description": "企业盈利能力、财务健康度、投资回报率",
        "indicators": [
            # 估值指标
            {"name": "全A股PE(TTM)", "code": "A_SHARE_PE_TTM", "akshare_func": "stock_zh_valuation_baidu", "frequency": "D", "lead_lag": "LAG"},
            {"name": "全A股PB(LF)", "code": "A_SHARE_PB_LF", "akshare_func": "stock_zh_valuation_baidu", "frequency": "D", "lead_lag": "LAG"},
            {"name": "沪深300PE", "code": "CSI300_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
            {"name": "中证500PE", "code": "CSI500_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
            {"name": "创业板指PE", "code": "CHINEXT_PE", "akshare_func": "index_value_hist_funddb", "frequency": "D", "lead_lag": "LAG"},
            
            # 盈利指标
            {"name": "规模以上工业企业利润增速", "code": "CN_INDUSTRIAL_PROFIT_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
            {"name": "规模以上工业企业营收增速", "code": "CN_INDUSTRIAL_REVENUE_GROWTH", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
            {"name": "工业企业资产负债率", "code": "CN_INDUSTRIAL_DEBT_RATIO", "akshare_func": "macro_china_industrial_enterprise_profits", "frequency": "M", "lead_lag": "LAG"},
            
            # 风险偏好
            {"name": "股债收益率比", "code": "STOCK_BOND_YIELD_RATIO", "akshare_func": "calculated", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "风险溢价", "code": "EQUITY_RISK_PREMIUM", "akshare_func": "calculated", "frequency": "D", "lead_lag": "SYNC"},
        ]
    },

    # 5. 政策面 (Policy) - 增强版  
    "政策面": {
        "description": "财政政策、产业政策、监管政策",
        "indicators": [
            # 财政政策
            {"name": "一般公共预算收入增速", "code": "CN_FISCAL_REVENUE_GROWTH", "akshare_func": "macro_china_fiscal_revenue", "frequency": "M", "lead_lag": "LAG"},
            {"name": "一般公共预算支出增速", "code": "CN_FISCAL_EXPENDITURE_GROWTH", "akshare_func": "macro_china_fiscal_expenditure", "frequency": "M", "lead_lag": "LAG"},
            {"name": "政府性基金收入增速", "code": "CN_GOV_FUND_REVENUE_GROWTH", "akshare_func": "macro_china_gov_fund_revenue", "frequency": "M", "lead_lag": "LAG"},
            {"name": "地方政府专项债发行额", "code": "CN_LOCAL_SPECIAL_BOND", "akshare_func": "bond_china_local_government", "frequency": "M", "lead_lag": "LEAD"},
            
            # 房地产政策相关
            {"name": "70城房价指数", "code": "CN_HOUSE_PRICE_INDEX", "akshare_func": "macro_china_house_price", "frequency": "M", "lead_lag": "LAG"},
            {"name": "商品房销售面积增速", "code": "CN_HOUSE_SALES_AREA_GROWTH", "akshare_func": "macro_china_house_sales", "frequency": "M", "lead_lag": "LAG"},
            {"name": "房地产开发投资增速", "code": "CN_REALESTATE_DEV_INV", "akshare_func": "macro_china_real_estate_investment", "frequency": "M", "lead_lag": "LAG"},
            
            # 债券市场政策传导
            {"name": "国债1年期收益率", "code": "CN_1Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "国债5年期收益率", "code": "CN_5Y_BOND_YIELD", "akshare_func": "bond_zh_us_rate", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "国债收益率曲线斜率", "code": "CN_YIELD_CURVE_SLOPE", "akshare_func": "calculated", "frequency": "D", "lead_lag": "LEAD"},
        ]
    },

    # 6. 市场面 (Market Performance) - 精简优化版
    "市场面": {
        "description": "股票、债券、商品等资产价格表现",
        "indicators": [
            # 核心股指
            {"name": "上证指数", "code": "SSE_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "沪深300", "code": "CSI300_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证500", "code": "CSI500_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "创业板指", "code": "CHINEXT_INDEX", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 风格指数
            {"name": "中证红利", "code": "CSI_DIVIDEND", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证价值", "code": "CSI_VALUE", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "中证成长", "code": "CSI_GROWTH", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 重要行业（经济周期敏感度高）
            {"name": "银行指数", "code": "SW_BANK", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "房地产指数", "code": "SW_REALESTATE", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "有色金属", "code": "SW_NONFERROUS", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "煤炭指数", "code": "SW_COAL", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "钢铁指数", "code": "SW_STEEL", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "食品饮料", "code": "SW_FOOD", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "医药生物", "code": "SW_PHARMA", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "电子指数", "code": "SW_ELECTRONICS", "akshare_func": "index_zh_a_hist", "frequency": "D", "lead_lag": "SYNC"},
            
            # 大宗商品
            {"name": "黄金价格", "code": "GOLD_PRICE", "akshare_func": "macro_cons_gold", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "螺纹钢期货", "code": "REBAR_FUTURES", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "铁矿石期货", "code": "IRON_ORE_FUTURES", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "原油期货", "code": "CRUDE_OIL_FUTURES", "akshare_func": "futures_zh_spot", "frequency": "D", "lead_lag": "LEAD"},
            
            # 汇率
            {"name": "人民币兑美元汇率", "code": "USD_CNY_RATE", "akshare_func": "currency_convert", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "人民币指数", "code": "RMB_INDEX", "akshare_func": "currency_rmb_index", "frequency": "D", "lead_lag": "SYNC"},
        ]
    },

    # 7. 情绪面 (Market Sentiment) - 增强版
    "情绪面": {
        "description": "投资者情绪、资金流向、交易行为",
        "indicators": [
            # 恐慌指标
            {"name": "VIX恐慌指数", "code": "VIX_INDEX", "akshare_func": "index_vix", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "中国版VIX", "code": "CN_VIX", "akshare_func": "index_vix_zh", "frequency": "D", "lead_lag": "LEAD"},
            
            # 资金流向
            {"name": "北向资金净流入", "code": "NORTHBOUND_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "南向资金净流入", "code": "SOUTHBOUND_CAPITAL", "akshare_func": "stock_connect_hist_sina", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "融资余额", "code": "MARGIN_BALANCE", "akshare_func": "stock_margin_detail_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "融券余额", "code": "SHORT_BALANCE", "akshare_func": "stock_margin_detail_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "两融余额占流通市值比", "code": "MARGIN_TO_MCAP_RATIO", "akshare_func": "calculated", "frequency": "D", "lead_lag": "SYNC"},
            
            # 交易活跃度
            {"name": "A股总成交额", "code": "A_SHARE_TURNOVER", "akshare_func": "stock_zh_a_spot_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "换手率", "code": "TURNOVER_RATE", "akshare_func": "stock_zh_a_spot_em", "frequency": "D", "lead_lag": "SYNC"},
            {"name": "新增投资者数量", "code": "NEW_INVESTORS", "akshare_func": "stock_account_statistics_em", "frequency": "M", "lead_lag": "SYNC"},
            
            # 新股发行（供给压力）
            {"name": "IPO发行数量", "code": "IPO_COUNT", "akshare_func": "stock_ipo_info", "frequency": "M", "lead_lag": "LAG"},
            {"name": "IPO募资金额", "code": "IPO_AMOUNT", "akshare_func": "stock_ipo_info", "frequency": "M", "lead_lag": "LAG"},
            
            # 机构行为
            {"name": "股票型基金仓位", "code": "EQUITY_FUND_POSITION", "akshare_func": "fund_position_change_em", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "重要股东减持金额", "code": "MAJOR_SHAREHOLDER_REDUCTION", "akshare_func": "stock_hold_management_detail_em", "frequency": "M", "lead_lag": "LAG"},
        ]
    },

    # 8. 周期特征面 (Cycle Characteristics) - 新增
    "周期特征面": {
        "description": "专门的周期识别与特征指标",
        "indicators": [
            # 领先指标综合
            {"name": "中国经济景气指数", "code": "CN_ECONOMIC_BOOM_INDEX", "akshare_func": "macro_china_boom_index", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "中国经济先行指数", "code": "CN_LEADING_INDICATOR", "akshare_func": "macro_china_leading_indicator", "frequency": "M", "lead_lag": "LEAD"},
            {"name": "中国一致指数", "code": "CN_COINCIDENT_INDICATOR", "akshare_func": "macro_china_coincident_indicator", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "中国滞后指数", "code": "CN_LAGGING_INDICATOR", "akshare_func": "macro_china_lagging_indicator", "frequency": "M", "lead_lag": "LAG"},
            
            # 周期特征指标
            {"name": "库存产出比", "code": "INVENTORY_OUTPUT_RATIO", "akshare_func": "calculated", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "价格产出缺口", "code": "PRICE_OUTPUT_GAP", "akshare_func": "calculated", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "利率风险溢价", "code": "INTEREST_RATE_RISK_PREMIUM", "akshare_func": "calculated", "frequency": "D", "lead_lag": "LEAD"},
            
            # 国际周期对比
            {"name": "中美GDP增速差", "code": "CN_US_GDP_SPREAD", "akshare_func": "calculated", "frequency": "M", "lead_lag": "SYNC"},
            {"name": "中美利差", "code": "CN_US_INTEREST_SPREAD", "akshare_func": "calculated", "frequency": "D", "lead_lag": "LEAD"},
            {"name": "中美通胀差", "code": "CN_US_INFLATION_SPREAD", "akshare_func": "calculated", "frequency": "M", "lead_lag": "SYNC"},
        ]
    }
}

def get_enhanced_indicator_count():
    """获取增强版指标总数"""
    return sum(len(category["indicators"]) for category in ENHANCED_INDICATORS_CONFIG.values())

def get_category_summary():
    """获取各类别指标统计"""
    summary = {}
    for category, data in ENHANCED_INDICATORS_CONFIG.items():
        summary[category] = {
            "count": len(data["indicators"]),
            "description": data["description"]
        }
    return summary

# 投资逻辑映射
INVESTMENT_LOGIC_MAPPING = {
    "美林投资时钟": {
        "description": "基于经济增长和通胀的四象限资产配置理论",
        "key_indicators": [
            "CN_GDP_YEARLY", "CN_CPI_YEARLY", "CN_PMI_MFG", 
            "CN_M2_YEARLY", "CN_10Y_BOND_YIELD"
        ],
        "asset_rotation": {
            "复苏(低通胀+高增长)": ["股票", "大宗商品"],
            "过热(高通胀+高增长)": ["大宗商品"],
            "滞胀(高通胀+低增长)": ["现金"],
            "衰退(低通胀+低增长)": ["债券"]
        }
    },
    "流动性传导": {
        "description": "央行政策→银行间流动性→实体经济→资产价格",
        "key_indicators": [
            "CN_RRR", "PBOC_OMO", "CN_SHIBOR", "CN_M1_M2_SPREAD",
            "CN_CREDIT_SPREAD", "NORTHBOUND_CAPITAL"
        ]
    },
    "基钦库存周期": {
        "description": "3-4年的短期库存调整周期",
        "key_indicators": [
            "CN_INVENTORY_GROWTH", "CN_PPI_YEARLY", "CN_PMI_MFG",
            "INVENTORY_OUTPUT_RATIO"
        ]
    }
}

if __name__ == "__main__":
    print(f"增强版总指标数量: {get_enhanced_indicator_count()}")
    print("\n各类别统计:")
    for category, info in get_category_summary().items():
        print(f"{category}: {info['count']}个指标 - {info['description']}") 