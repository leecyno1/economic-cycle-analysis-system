#!/usr/bin/env python3
"""
基于兴证策略行业中观指标体系的专业行业指标配置
参考：【兴证策略】行业中观&拥挤度数据库（20250530）

指标体系架构：
- 7大类行业：TMT、周期、消费、医药、金融地产、制造、主题
- 37个二级行业
- 200+个细分领域
- 915个专业指标

指标类型：
- 产量指标：反映行业生产活动
- 价格指标：反映供需关系和成本传导
- 销量指标：反映终端需求
- 收入指标：反映行业盈利能力
- 其他指标：用电量、投资、库存等
"""

from typing import Dict, Any

# 1. TMT行业指标体系
TMT_INDICATORS = {
    # 通信行业
    'COMM_5G_BASE_STATIONS': {
        'name_cn': '5G基站建设数量',
        'name_en': '5G Base Stations',
        'category': 'TMT-通信',
        'subcategory': '基站',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'tool_trade_date_hist_sina',  # 需要替代数据源
        'unit': '万个',
        'indicator_type': '产量',
        'calculation_method': 'direct',
        'investment_significance': '5G建设进度，通信设备需求先行指标'
    },
    'COMM_OPTICAL_MODULE_PRICE': {
        'name_cn': '光模块价格指数',
        'name_en': 'Optical Module Price Index',
        'category': 'TMT-通信',
        'subcategory': '光模块',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'macro_china_ppi',  # 使用PPI通信设备制造业
        'unit': '指数',
        'indicator_type': '价格',
        'calculation_method': 'ppi_communication_equipment',
        'investment_significance': '光通信产业链成本传导，影响通信设备盈利'
    },
    'COMM_IDC_POWER_CONSUMPTION': {
        'name_cn': 'IDC用电量',
        'name_en': 'IDC Power Consumption',
        'category': 'TMT-通信',
        'subcategory': 'IDC',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'energy_oil_detail',  # 使用能源数据计算
        'unit': '亿千瓦时',
        'indicator_type': '其他',
        'calculation_method': 'industry_electricity_consumption',
        'investment_significance': '数据中心建设和运营活跃度，云计算需求指标'
    },
    
    # 电子行业
    'ELEC_SEMICONDUCTOR_SALES': {
        'name_cn': '半导体销售额',
        'name_en': 'Semiconductor Sales',
        'category': 'TMT-电子',
        'subcategory': '半导体',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '亿元',
        'indicator_type': '销量',
        'calculation_method': 'industrial_production_electronics',
        'investment_significance': '电子产业链核心，科技周期关键指标'
    },
    'ELEC_PCB_PRODUCTION': {
        'name_cn': 'PCB产量',
        'name_en': 'PCB Production',
        'category': 'TMT-电子',
        'subcategory': 'PCB',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万平方米',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_pcb',
        'investment_significance': '电子制造基础材料，反映电子产品需求'
    },
    'ELEC_CONSUMER_ELECTRONICS_SALES': {
        'name_cn': '消费电子销量',
        'name_en': 'Consumer Electronics Sales',
        'category': 'TMT-电子',
        'subcategory': '消费电子',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_retail_total',
        'unit': '万台',
        'indicator_type': '销量',
        'calculation_method': 'retail_electronics',
        'investment_significance': '消费电子终端需求，消费升级指标'
    },
    
    # 计算机行业
    'COMP_SOFTWARE_REVENUE': {
        'name_cn': '软件业务收入',
        'name_en': 'Software Revenue',
        'category': 'TMT-计算机',
        'subcategory': '软件服务',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '亿元',
        'indicator_type': '收入',
        'calculation_method': 'software_industry_revenue',
        'investment_significance': '数字化转型进度，软件行业景气度'
    },
    'COMP_CLOUD_SERVICES': {
        'name_cn': '云服务市场规模',
        'name_en': 'Cloud Services Market Size',
        'category': 'TMT-计算机',
        'subcategory': '云计算',
        'frequency': 'quarterly',
        'source': 'calculated',
        'api_function': 'macro_china_gdp',
        'unit': '亿元',
        'indicator_type': '收入',
        'calculation_method': 'gdp_tertiary_it_services',
        'investment_significance': '企业数字化投入，云计算渗透率'
    }
}

# 2. 周期行业指标体系
CYCLICAL_INDICATORS = {
    # 基础化工
    'CHEM_ETHYLENE_PRODUCTION': {
        'name_cn': '乙烯产量',
        'name_en': 'Ethylene Production',
        'category': '周期-基础化工',
        'subcategory': '基础化工原料',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_ethylene',
        'investment_significance': '化工产业链源头，经济活动先行指标'
    },
    'CHEM_SODA_ASH_PRICE': {
        'name_cn': '纯碱价格',
        'name_en': 'Soda Ash Price',
        'category': '周期-基础化工',
        'subcategory': '纯碱',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'futures_main_sina',  # 期货价格
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'futures_soda_ash',
        'investment_significance': '玻璃、化工下游需求，房地产产业链指标'
    },
    'CHEM_PESTICIDE_PRODUCTION': {
        'name_cn': '农药产量',
        'name_en': 'Pesticide Production',
        'category': '周期-基础化工',
        'subcategory': '农药',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_pesticide',
        'investment_significance': '农业生产投入，农产品价格传导'
    },
    
    # 钢铁行业
    'STEEL_CRUDE_PRODUCTION': {
        'name_cn': '粗钢产量',
        'name_en': 'Crude Steel Production',
        'category': '周期-钢铁',
        'subcategory': '普钢',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_steel',
        'investment_significance': '基建、房地产需求核心指标'
    },
    'STEEL_REBAR_PRICE': {
        'name_cn': '螺纹钢价格',
        'name_en': 'Rebar Price',
        'category': '周期-钢铁',
        'subcategory': '建筑钢材',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'futures_main_sina',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'futures_rebar',
        'investment_significance': '建筑需求直接指标，基建投资先行'
    },
    'STEEL_IRON_ORE_INVENTORY': {
        'name_cn': '铁矿石库存',
        'name_en': 'Iron Ore Inventory',
        'category': '周期-钢铁',
        'subcategory': '冶钢原料',
        'frequency': 'weekly',
        'source': 'akshare',
        'api_function': 'futures_inventory_99',
        'unit': '万吨',
        'indicator_type': '其他',
        'calculation_method': 'inventory_iron_ore',
        'investment_significance': '钢铁生产预期，供需平衡指标'
    },
    
    # 煤炭行业
    'COAL_THERMAL_PRICE': {
        'name_cn': '动力煤价格',
        'name_en': 'Thermal Coal Price',
        'category': '周期-煤炭',
        'subcategory': '动力煤',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'energy_oil_hist',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'energy_coal_price',
        'investment_significance': '电力成本，能源供需核心指标'
    },
    'COAL_COKING_PRODUCTION': {
        'name_cn': '焦炭产量',
        'name_en': 'Coke Production',
        'category': '周期-煤炭',
        'subcategory': '焦炭',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_coke',
        'investment_significance': '钢铁生产原料，制造业活跃度'
    },
    
    # 有色金属
    'METAL_COPPER_PRICE': {
        'name_cn': '铜价',
        'name_en': 'Copper Price',
        'category': '周期-有色金属',
        'subcategory': '工业金属',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'futures_main_sina',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'futures_copper',
        'investment_significance': '经济活动温度计，制造业需求指标'
    },
    'METAL_ALUMINUM_PRODUCTION': {
        'name_cn': '电解铝产量',
        'name_en': 'Aluminum Production',
        'category': '周期-有色金属',
        'subcategory': '轻金属',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_aluminum',
        'investment_significance': '汽车、建筑、包装需求综合指标'
    },
    'METAL_LITHIUM_PRICE': {
        'name_cn': '碳酸锂价格',
        'name_en': 'Lithium Carbonate Price',
        'category': '周期-有色金属',
        'subcategory': '能源金属',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'futures_main_sina',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'spot_lithium_carbonate',
        'investment_significance': '新能源汽车产业链核心，电池需求'
    },
    
    # 建筑材料
    'BUILDING_CEMENT_PRODUCTION': {
        'name_cn': '水泥产量',
        'name_en': 'Cement Production',
        'category': '周期-建筑材料',
        'subcategory': '水泥',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_cement',
        'investment_significance': '基建、房地产开工核心指标'
    },
    'BUILDING_GLASS_PRODUCTION': {
        'name_cn': '平板玻璃产量',
        'name_en': 'Flat Glass Production',
        'category': '周期-建筑材料',
        'subcategory': '玻璃制造',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万重量箱',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_glass',
        'investment_significance': '房地产竣工指标，建筑需求'
    },
    
    # 交通运输
    'TRANSPORT_FREIGHT_VOLUME': {
        'name_cn': '货运总量',
        'name_en': 'Total Freight Volume',
        'category': '周期-交通运输',
        'subcategory': '物流',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_freight_index',
        'unit': '亿吨',
        'indicator_type': '其他',
        'calculation_method': 'freight_volume_total',
        'investment_significance': '经济活动强度，商品流通指标'
    },
    'TRANSPORT_EXPRESS_DELIVERY': {
        'name_cn': '快递业务量',
        'name_en': 'Express Delivery Volume',
        'category': '周期-交通运输',
        'subcategory': '快递物流',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_postal_telecommunicational',
        'unit': '亿件',
        'indicator_type': '销量',
        'calculation_method': 'express_delivery_volume',
        'investment_significance': '电商活跃度，消费物流需求'
    },
    'TRANSPORT_BDI_INDEX': {
        'name_cn': '波罗的海干散货指数',
        'name_en': 'Baltic Dry Index',
        'category': '周期-交通运输',
        'subcategory': '航运港口',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'index_bdi',
        'unit': '点',
        'indicator_type': '价格',
        'calculation_method': 'direct',
        'investment_significance': '全球贸易活跃度，大宗商品需求'
    }
}

# 3. 消费行业指标体系
CONSUMER_INDICATORS = {
    # 食品饮料
    'FOOD_LIQUOR_PRODUCTION': {
        'name_cn': '白酒产量',
        'name_en': 'Liquor Production',
        'category': '消费-食品饮料',
        'subcategory': '白酒',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万千升',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_liquor',
        'investment_significance': '高端消费指标，消费升级代表'
    },
    'FOOD_SNACK_SALES': {
        'name_cn': '休闲食品销售额',
        'name_en': 'Snack Food Sales',
        'category': '消费-食品饮料',
        'subcategory': '休闲食品',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_retail_total',
        'unit': '亿元',
        'indicator_type': '销量',
        'calculation_method': 'retail_food_snacks',
        'investment_significance': '年轻消费群体偏好，消费结构变化'
    },
    'FOOD_DAIRY_PRODUCTION': {
        'name_cn': '乳制品产量',
        'name_en': 'Dairy Production',
        'category': '消费-食品饮料',
        'subcategory': '乳制品',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_dairy',
        'investment_significance': '营养消费升级，健康消费趋势'
    },
    
    # 家用电器
    'APPLIANCE_AC_SALES': {
        'name_cn': '空调销量',
        'name_en': 'Air Conditioner Sales',
        'category': '消费-家用电器',
        'subcategory': '大家电',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_retail_total',
        'unit': '万台',
        'indicator_type': '销量',
        'calculation_method': 'retail_appliances_ac',
        'investment_significance': '房地产后周期，消费电器需求'
    },
    'APPLIANCE_KITCHEN_SALES': {
        'name_cn': '厨卫电器销量',
        'name_en': 'Kitchen Appliance Sales',
        'category': '消费-家用电器',
        'subcategory': '厨卫电器',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_retail_total',
        'unit': '万台',
        'indicator_type': '销量',
        'calculation_method': 'retail_kitchen_appliances',
        'investment_significance': '生活品质提升，厨房经济指标'
    },
    
    # 纺织服饰
    'TEXTILE_CLOTHING_EXPORT': {
        'name_cn': '服装出口额',
        'name_en': 'Clothing Export Value',
        'category': '消费-纺织服饰',
        'subcategory': '服装家纺',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_export_value',
        'unit': '亿美元',
        'indicator_type': '销量',
        'calculation_method': 'export_clothing',
        'investment_significance': '全球消费需求，制造业出口竞争力'
    },
    'TEXTILE_COTTON_PRICE': {
        'name_cn': '棉花价格',
        'name_en': 'Cotton Price',
        'category': '消费-纺织服饰',
        'subcategory': '纺织原料',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'futures_main_sina',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'futures_cotton',
        'investment_significance': '纺织成本，农产品价格传导'
    },
    
    # 汽车
    'AUTO_PASSENGER_SALES': {
        'name_cn': '乘用车销量',
        'name_en': 'Passenger Car Sales',
        'category': '消费-汽车',
        'subcategory': '乘用车',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'car_cpca_data',
        'unit': '万辆',
        'indicator_type': '销量',
        'calculation_method': 'direct',
        'investment_significance': '消费升级核心指标，制造业需求'
    },
    'AUTO_NEV_PENETRATION': {
        'name_cn': '新能源汽车渗透率',
        'name_en': 'NEV Penetration Rate',
        'category': '消费-汽车',
        'subcategory': '新能源汽车',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'car_cpca_data',
        'unit': '%',
        'indicator_type': '其他',
        'calculation_method': 'nev_penetration_rate',
        'investment_significance': '产业升级进度，绿色转型指标'
    }
}

# 4. 制造业指标体系
MANUFACTURING_INDICATORS = {
    # 机械设备
    'MACHINERY_EXCAVATOR_SALES': {
        'name_cn': '挖掘机销量',
        'name_en': 'Excavator Sales',
        'category': '制造-机械设备',
        'subcategory': '工程机械',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '台',
        'indicator_type': '销量',
        'calculation_method': 'machinery_excavator_sales',
        'investment_significance': '基建投资先行指标，工程建设活跃度'
    },
    'MACHINERY_CRANE_SALES': {
        'name_cn': '起重机销量',
        'name_en': 'Crane Sales',
        'category': '制造-机械设备',
        'subcategory': '工程机械',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '台',
        'indicator_type': '销量',
        'calculation_method': 'machinery_crane_sales',
        'investment_significance': '建筑施工强度，基建项目进度'
    },
    'MACHINERY_ROBOT_PRODUCTION': {
        'name_cn': '工业机器人产量',
        'name_en': 'Industrial Robot Production',
        'category': '制造-机械设备',
        'subcategory': '自动化设备',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '台',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_robot',
        'investment_significance': '制造业升级，自动化投资需求'
    },
    
    # 电力设备
    'POWER_SOLAR_INSTALLATION': {
        'name_cn': '光伏装机容量',
        'name_en': 'Solar Installation Capacity',
        'category': '制造-电力设备',
        'subcategory': '光伏发电',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'energy_oil_detail',
        'unit': 'GW',
        'indicator_type': '其他',
        'calculation_method': 'renewable_energy_capacity',
        'investment_significance': '绿色能源投资，碳中和进度'
    },
    'POWER_WIND_INSTALLATION': {
        'name_cn': '风电装机容量',
        'name_en': 'Wind Installation Capacity',
        'category': '制造-电力设备',
        'subcategory': '风力发电',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'energy_oil_detail',
        'unit': 'GW',
        'indicator_type': '其他',
        'calculation_method': 'renewable_energy_capacity',
        'investment_significance': '清洁能源发展，电力结构转型'
    },
    'POWER_BATTERY_PRODUCTION': {
        'name_cn': '动力电池产量',
        'name_en': 'Power Battery Production',
        'category': '制造-电力设备',
        'subcategory': '储能电池',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': 'GWh',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_battery',
        'investment_significance': '新能源汽车产业链，储能需求'
    }
}

# 5. 医药行业指标体系
PHARMA_INDICATORS = {
    'PHARMA_DRUG_PRODUCTION': {
        'name_cn': '化学药品产量',
        'name_en': 'Chemical Drug Production',
        'category': '医药-医药生物',
        'subcategory': '化学制药',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_pharma',
        'investment_significance': '医疗需求，人口老龄化指标'
    },
    'PHARMA_MEDICAL_DEVICE_SALES': {
        'name_cn': '医疗器械销售额',
        'name_en': 'Medical Device Sales',
        'category': '医药-医药生物',
        'subcategory': '医疗器械',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_retail_total',
        'unit': '亿元',
        'indicator_type': '销量',
        'calculation_method': 'retail_medical_devices',
        'investment_significance': '医疗投入增长，健康消费升级'
    },
    'PHARMA_HEALTHCARE_CPI': {
        'name_cn': '医疗保健CPI',
        'name_en': 'Healthcare CPI',
        'category': '医药-医药生物',
        'subcategory': '医疗服务',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_cpi',
        'unit': '%',
        'indicator_type': '价格',
        'calculation_method': 'cpi_healthcare',
        'investment_significance': '医疗成本通胀，医保支付压力'
    }
}

# 6. 金融地产指标体系
FINANCE_REALESTATE_INDICATORS = {
    # 银行
    'BANK_LOAN_GROWTH': {
        'name_cn': '银行放贷增速',
        'name_en': 'Bank Loan Growth',
        'category': '金融地产-银行',
        'subcategory': '银行',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_money_supply',
        'unit': '%',
        'indicator_type': '其他',
        'calculation_method': 'loan_growth_rate',
        'investment_significance': '流动性投放，信贷周期指标'
    },
    'BANK_DEPOSIT_GROWTH': {
        'name_cn': '银行存款增速',
        'name_en': 'Bank Deposit Growth',
        'category': '金融地产-银行',
        'subcategory': '银行',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_money_supply',
        'unit': '%',
        'indicator_type': '其他',
        'calculation_method': 'deposit_growth_rate',
        'investment_significance': '储蓄偏好，流动性供给'
    },
    
    # 保险
    'INSURANCE_PREMIUM_INCOME': {
        'name_cn': '保险保费收入',
        'name_en': 'Insurance Premium Income',
        'category': '金融地产-非银金融',
        'subcategory': '保险',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_insurance',
        'unit': '亿元',
        'indicator_type': '收入',
        'calculation_method': 'insurance_premium_total',
        'investment_significance': '风险保障需求，财富管理发展'
    },
    
    # 房地产
    'REALESTATE_SALES_AREA': {
        'name_cn': '商品房销售面积',
        'name_en': 'Commercial Housing Sales Area',
        'category': '金融地产-房地产',
        'subcategory': '房地产',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_real_estate',
        'unit': '万平方米',
        'indicator_type': '销量',
        'calculation_method': 'real_estate_sales_area',
        'investment_significance': '房地产需求，消费信心指标'
    },
    'REALESTATE_INVESTMENT': {
        'name_cn': '房地产开发投资',
        'name_en': 'Real Estate Development Investment',
        'category': '金融地产-房地产',
        'subcategory': '房地产',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_real_estate',
        'unit': '亿元',
        'indicator_type': '其他',
        'calculation_method': 'real_estate_investment',
        'investment_significance': '房地产供给，固定资产投资'
    }
}

# 7. 计算指标定义
CALCULATED_INDICATORS = {
    # 行业景气度指数
    'INDUSTRY_PROSPERITY_TMT': {
        'name_cn': 'TMT行业景气度指数',
        'name_en': 'TMT Industry Prosperity Index',
        'category': '计算指标',
        'subcategory': '行业景气度',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'weighted_average',
        'components': ['COMM_5G_BASE_STATIONS', 'ELEC_SEMICONDUCTOR_SALES', 'COMP_SOFTWARE_REVENUE'],
        'weights': [0.3, 0.4, 0.3],
        'unit': '指数',
        'investment_significance': 'TMT行业综合景气度，科技周期判断'
    },
    'INDUSTRY_PROSPERITY_CYCLICAL': {
        'name_cn': '周期行业景气度指数',
        'name_en': 'Cyclical Industry Prosperity Index',
        'category': '计算指标',
        'subcategory': '行业景气度',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'weighted_average',
        'components': ['STEEL_CRUDE_PRODUCTION', 'CHEM_ETHYLENE_PRODUCTION', 'BUILDING_CEMENT_PRODUCTION'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '周期行业综合景气度，经济周期判断'
    },
    'INDUSTRY_PROSPERITY_CONSUMER': {
        'name_cn': '消费行业景气度指数',
        'name_en': 'Consumer Industry Prosperity Index',
        'category': '计算指标',
        'subcategory': '行业景气度',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'weighted_average',
        'components': ['AUTO_PASSENGER_SALES', 'FOOD_LIQUOR_PRODUCTION', 'APPLIANCE_AC_SALES'],
        'weights': [0.5, 0.3, 0.2],
        'unit': '指数',
        'investment_significance': '消费行业综合景气度，消费周期判断'
    },
    
    # 产业链指数
    'SUPPLY_CHAIN_AUTOMOTIVE': {
        'name_cn': '汽车产业链指数',
        'name_en': 'Automotive Supply Chain Index',
        'category': '计算指标',
        'subcategory': '产业链指数',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'supply_chain_composite',
        'components': ['AUTO_PASSENGER_SALES', 'STEEL_CRUDE_PRODUCTION', 'METAL_ALUMINUM_PRODUCTION', 'POWER_BATTERY_PRODUCTION'],
        'weights': [0.4, 0.2, 0.2, 0.2],
        'unit': '指数',
        'investment_significance': '汽车全产业链景气度，制造业核心'
    },
    'SUPPLY_CHAIN_CONSTRUCTION': {
        'name_cn': '建筑产业链指数',
        'name_en': 'Construction Supply Chain Index',
        'category': '计算指标',
        'subcategory': '产业链指数',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'supply_chain_composite',
        'components': ['BUILDING_CEMENT_PRODUCTION', 'STEEL_REBAR_PRICE', 'MACHINERY_EXCAVATOR_SALES'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '建筑全产业链景气度，基建房地产'
    },
    
    # 价格传导指数
    'PRICE_TRANSMISSION_UPSTREAM': {
        'name_cn': '上游价格传导指数',
        'name_en': 'Upstream Price Transmission Index',
        'category': '计算指标',
        'subcategory': '价格传导',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'price_transmission',
        'components': ['COAL_THERMAL_PRICE', 'METAL_COPPER_PRICE', 'CHEM_SODA_ASH_PRICE'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '上游成本压力，通胀传导路径'
    },
    'PRICE_TRANSMISSION_DOWNSTREAM': {
        'name_cn': '下游价格传导指数',
        'name_en': 'Downstream Price Transmission Index',
        'category': '计算指标',
        'subcategory': '价格传导',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'price_transmission',
        'components': ['PHARMA_HEALTHCARE_CPI', 'FOOD_LIQUOR_PRODUCTION', 'AUTO_PASSENGER_SALES'],
        'weights': [0.3, 0.4, 0.3],
        'unit': '指数',
        'investment_significance': '下游需求强度，消费价格弹性'
    }
}

# 8. 整合所有指标
PROFESSIONAL_INDUSTRY_INDICATORS = {
    **TMT_INDICATORS,
    **CYCLICAL_INDICATORS,
    **CONSUMER_INDICATORS,
    **MANUFACTURING_INDICATORS,
    **PHARMA_INDICATORS,
    **FINANCE_REALESTATE_INDICATORS,
    **CALCULATED_INDICATORS
}

# 9. 指标分类统计
INDICATOR_CATEGORIES = {
    'TMT': len(TMT_INDICATORS),
    '周期': len(CYCLICAL_INDICATORS),
    '消费': len(CONSUMER_INDICATORS),
    '制造': len(MANUFACTURING_INDICATORS),
    '医药': len(PHARMA_INDICATORS),
    '金融地产': len(FINANCE_REALESTATE_INDICATORS),
    '计算指标': len(CALCULATED_INDICATORS)
}

# 10. 数据源统计
DATA_SOURCES = {
    'akshare': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('source') == 'akshare']),
    'calculated': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('source') == 'calculated']),
    'total': len(PROFESSIONAL_INDUSTRY_INDICATORS)
}

if __name__ == "__main__":
    print("=== 专业行业指标体系统计 ===")
    print(f"总指标数量: {DATA_SOURCES['total']}")
    print(f"直接数据源: {DATA_SOURCES['akshare']}")
    print(f"计算指标: {DATA_SOURCES['calculated']}")
    print("\n各行业指标数量:")
    for category, count in INDICATOR_CATEGORIES.items():
        print(f"  {category}: {count}个") 