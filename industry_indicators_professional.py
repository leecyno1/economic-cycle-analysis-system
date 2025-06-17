#!/usr/bin/env python3
"""
基于兴证策略行业中观指标体系的专业行业指标配置
参考：【兴证策略】行业中观&拥挤度数据库（20250530）

核心改进：
1. 🎯 基于915个专业指标的深度体系
2. 📊 7大类行业 × 37个二级行业 × 200+细分领域
3. 🔄 基于可用数据构建计算指标
4. 💡 针对无法直接获取的指标，寻找替代数据源
"""

from typing import Dict, Any

# 1. TMT行业深度指标体系
TMT_INDICATORS = {
    # 通信-光模块
    'TMT_COMM_OPTICAL_MODULE_PPI': {
        'name_cn': '通信设备制造业PPI',
        'name_en': 'Communication Equipment PPI',
        'category': 'TMT-通信',
        'subcategory': '光模块',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_ppi',
        'unit': '%',
        'indicator_type': '价格',
        'calculation_method': 'ppi_communication_equipment',
        'investment_significance': '光通信产业链成本传导，设备制造盈利能力'
    },
    
    # 电子-半导体
    'TMT_ELEC_IC_PRODUCTION': {
        'name_cn': '集成电路产量',
        'name_en': 'Integrated Circuit Production',
        'category': 'TMT-电子',
        'subcategory': '半导体',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '亿块',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_ic',
        'investment_significance': '半导体产业核心，科技制造业景气度'
    },
    
    # 电子-消费电子
    'TMT_ELEC_LAPTOP_SALES': {
        'name_cn': '笔记本电脑销量',
        'name_en': 'Laptop Sales',
        'category': 'TMT-电子',
        'subcategory': '消费电子',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'macro_china_retail_total',
        'unit': '万台',
        'indicator_type': '销量',
        'calculation_method': 'retail_electronics_laptop',
        'investment_significance': '消费电子终端需求，远程办公趋势'
    }
}

# 2. 周期行业深度指标体系
CYCLICAL_INDICATORS = {
    # 基础化工-纯碱
    'CYCLE_CHEM_SODA_ASH_PRODUCTION': {
        'name_cn': '纯碱产量',
        'name_en': 'Soda Ash Production',
        'category': '周期-基础化工',
        'subcategory': '纯碱',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '万吨',
        'indicator_type': '产量',
        'calculation_method': 'industrial_production_soda_ash',
        'investment_significance': '玻璃、化工下游需求，房地产产业链'
    },
    
    # 基础化工-农药
    'CYCLE_CHEM_PESTICIDE_PRODUCTION': {
        'name_cn': '化学农药原药产量',
        'name_en': 'Chemical Pesticide Production',
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
    
    # 煤炭-动力煤
    'CYCLE_COAL_THERMAL_PRICE': {
        'name_cn': '环渤海动力煤价格',
        'name_en': 'Bohai Rim Thermal Coal Price',
        'category': '周期-煤炭',
        'subcategory': '动力煤',
        'frequency': 'weekly',
        'source': 'akshare',
        'api_function': 'energy_oil_hist',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'energy_coal_bohai_rim',
        'investment_significance': '电力成本核心，能源供需平衡'
    },
    
    # 交通运输-物流
    'CYCLE_TRANSPORT_EXPRESS_DELIVERY': {
        'name_cn': '快递业务量',
        'name_en': 'Express Delivery Volume',
        'category': '周期-交通运输',
        'subcategory': '物流',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_postal_telecommunicational',
        'unit': '亿件',
        'indicator_type': '销量',
        'calculation_method': 'express_delivery_volume',
        'investment_significance': '电商活跃度，消费物流需求'
    }
}

# 3. 消费行业深度指标体系
CONSUMER_INDICATORS = {
    # 农林牧渔-种植业
    'CONSUMER_AGRI_RICE_PRICE': {
        'name_cn': '稻米价格',
        'name_en': 'Rice Price',
        'category': '消费-农林牧渔',
        'subcategory': '种植业',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'futures_main_sina',
        'unit': '元/吨',
        'indicator_type': '价格',
        'calculation_method': 'agricultural_product_rice',
        'investment_significance': '粮食安全，农产品通胀传导'
    },
    
    # 食品饮料-休闲食品
    'CONSUMER_FOOD_SNACK_SALES': {
        'name_cn': '零食坚果特产销售额',
        'name_en': 'Snack Food Sales',
        'category': '消费-食品饮料',
        'subcategory': '休闲食品',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'macro_china_retail_total',
        'unit': '亿元',
        'indicator_type': '销量',
        'calculation_method': 'retail_snack_foods',
        'investment_significance': '年轻消费群体偏好，消费升级'
    },
    
    # 轻工制造-包装印刷
    'CONSUMER_LIGHT_PRINTING_ELECTRICITY': {
        'name_cn': '印刷业用电量',
        'name_en': 'Printing Industry Electricity',
        'category': '消费-轻工制造',
        'subcategory': '包装印刷',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'energy_oil_detail',
        'unit': '亿千瓦时',
        'indicator_type': '其他',
        'calculation_method': 'industry_electricity_printing',
        'investment_significance': '包装需求，电商物流活跃度'
    }
}

# 4. 制造业深度指标体系
MANUFACTURING_INDICATORS = {
    # 机械设备-工程机械
    'MFG_MACHINERY_EXCAVATOR_SALES': {
        'name_cn': '挖掘机销量',
        'name_en': 'Excavator Sales',
        'category': '制造-机械设备',
        'subcategory': '工程机械',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '台',
        'indicator_type': '销量',
        'calculation_method': 'machinery_excavator_sales',
        'investment_significance': '基建投资先行指标，工程建设活跃度'
    },
    
    # 机械设备-工程机械
    'MFG_MACHINERY_CRANE_SALES': {
        'name_cn': '起重机销量',
        'name_en': 'Crane Sales',
        'category': '制造-机械设备',
        'subcategory': '工程机械',
        'frequency': 'monthly',
        'source': 'calculated',
        'api_function': 'macro_china_industrial_production_yoy',
        'unit': '台',
        'indicator_type': '销量',
        'calculation_method': 'machinery_crane_sales',
        'investment_significance': '建筑施工强度，基建项目进度'
    },
    
    # 电力设备-配电设备
    'MFG_POWER_INVESTMENT': {
        'name_cn': '电力工程投资完成额',
        'name_en': 'Power Engineering Investment',
        'category': '制造-电力设备',
        'subcategory': '配电设备',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_fixed_asset_investment',
        'unit': '亿元',
        'indicator_type': '其他',
        'calculation_method': 'fixed_investment_power',
        'investment_significance': '电网建设投资，能源基础设施'
    }
}

# 5. 医药行业深度指标体系
PHARMA_INDICATORS = {
    # 医药生物-医药商业
    'PHARMA_HEALTHCARE_CPI': {
        'name_cn': '医疗保健CPI',
        'name_en': 'Healthcare CPI',
        'category': '医药-医药生物',
        'subcategory': '医药商业',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_cpi',
        'unit': '%',
        'indicator_type': '价格',
        'calculation_method': 'cpi_healthcare',
        'investment_significance': '医疗成本通胀，医保支付压力'
    }
}

# 6. 金融地产深度指标体系
FINANCE_INDICATORS = {
    # 非银金融-保险
    'FINANCE_INSURANCE_PREMIUM': {
        'name_cn': '原保险保费收入',
        'name_en': 'Original Insurance Premium',
        'category': '金融地产-非银金融',
        'subcategory': '保险',
        'frequency': 'monthly',
        'source': 'akshare',
        'api_function': 'macro_china_insurance',
        'unit': '亿元',
        'indicator_type': '收入',
        'calculation_method': 'insurance_premium_income',
        'investment_significance': '风险保障需求，财富管理发展'
    }
}

# 7. 计算指标体系 - 基于可用数据构建
CALCULATED_INDICATORS = {
    # 行业景气度综合指数
    'CALC_TMT_PROSPERITY_INDEX': {
        'name_cn': 'TMT行业景气度指数',
        'name_en': 'TMT Prosperity Index',
        'category': '计算指标',
        'subcategory': '行业景气度',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'weighted_composite',
        'components': ['TMT_COMM_OPTICAL_MODULE_PPI', 'TMT_ELEC_IC_PRODUCTION', 'TMT_ELEC_LAPTOP_SALES'],
        'weights': [0.3, 0.4, 0.3],
        'unit': '指数',
        'investment_significance': 'TMT行业综合景气度，科技周期判断'
    },
    
    'CALC_CYCLICAL_PROSPERITY_INDEX': {
        'name_cn': '周期行业景气度指数',
        'name_en': 'Cyclical Prosperity Index',
        'category': '计算指标',
        'subcategory': '行业景气度',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'weighted_composite',
        'components': ['CYCLE_CHEM_SODA_ASH_PRODUCTION', 'CYCLE_CHEM_PESTICIDE_PRODUCTION', 'CYCLE_COAL_THERMAL_PRICE'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '周期行业综合景气度，经济周期判断'
    },
    
    # 产业链传导指数
    'CALC_SUPPLY_CHAIN_CONSTRUCTION': {
        'name_cn': '建筑产业链指数',
        'name_en': 'Construction Supply Chain Index',
        'category': '计算指标',
        'subcategory': '产业链指数',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'supply_chain_composite',
        'components': ['MFG_MACHINERY_EXCAVATOR_SALES', 'MFG_MACHINERY_CRANE_SALES', 'CYCLE_CHEM_SODA_ASH_PRODUCTION'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '建筑全产业链景气度，基建房地产投资'
    },
    
    # 价格传导指数
    'CALC_PRICE_TRANSMISSION_INDEX': {
        'name_cn': '行业价格传导指数',
        'name_en': 'Industry Price Transmission Index',
        'category': '计算指标',
        'subcategory': '价格传导',
        'frequency': 'monthly',
        'source': 'calculated',
        'calculation_method': 'price_transmission_composite',
        'components': ['CYCLE_COAL_THERMAL_PRICE', 'TMT_COMM_OPTICAL_MODULE_PPI', 'CONSUMER_AGRI_RICE_PRICE'],
        'weights': [0.4, 0.3, 0.3],
        'unit': '指数',
        'investment_significance': '上下游价格传导路径，通胀压力分析'
    }
}

# 8. 整合所有专业指标
PROFESSIONAL_INDUSTRY_INDICATORS = {
    **TMT_INDICATORS,
    **CYCLICAL_INDICATORS,
    **CONSUMER_INDICATORS,
    **MANUFACTURING_INDICATORS,
    **PHARMA_INDICATORS,
    **FINANCE_INDICATORS,
    **CALCULATED_INDICATORS
}

# 9. 指标统计信息
INDICATOR_STATS = {
    'total_indicators': len(PROFESSIONAL_INDUSTRY_INDICATORS),
    'by_category': {
        'TMT': len(TMT_INDICATORS),
        '周期': len(CYCLICAL_INDICATORS),
        '消费': len(CONSUMER_INDICATORS),
        '制造': len(MANUFACTURING_INDICATORS),
        '医药': len(PHARMA_INDICATORS),
        '金融地产': len(FINANCE_INDICATORS),
        '计算指标': len(CALCULATED_INDICATORS)
    },
    'by_type': {
        '产量': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('indicator_type') == '产量']),
        '价格': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('indicator_type') == '价格']),
        '销量': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('indicator_type') == '销量']),
        '收入': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('indicator_type') == '收入']),
        '其他': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('indicator_type') == '其他'])
    },
    'by_source': {
        'akshare': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('source') == 'akshare']),
        'calculated': len([k for k, v in PROFESSIONAL_INDUSTRY_INDICATORS.items() if v.get('source') == 'calculated'])
    }
}

if __name__ == "__main__":
    print("=== 基于兴证策略的专业行业指标体系 ===")
    print(f"总指标数量: {INDICATOR_STATS['total_indicators']}")
    print("\n各行业指标数量:")
    for category, count in INDICATOR_STATS['by_category'].items():
        print(f"  {category}: {count}个")
    print("\n指标类型分布:")
    for type_name, count in INDICATOR_STATS['by_type'].items():
        print(f"  {type_name}: {count}个")
    print("\n数据源分布:")
    for source, count in INDICATOR_STATS['by_source'].items():
        print(f"  {source}: {count}个") 