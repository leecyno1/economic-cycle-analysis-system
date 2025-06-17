#!/usr/bin/env python3
"""
创建结构化的Excel数据字典
将所有指标信息整理成便于审核和系统集成的格式
"""

import pandas as pd
from datetime import datetime
import os

def create_data_dictionary_excel():
    """创建Excel格式的数据字典"""
    
    print("=== 创建数据字典Excel文件 ===\n")
    
    # 1. TMT行业指标
    tmt_data = [
        {
            'ID': 1,
            '指标代码': 'TMT_COMM_OPTICAL_MODULE_PPI',
            '中文名称': '通信设备制造业PPI',
            '英文名称': 'Communication Equipment PPI',
            '一级分类': 'TMT',
            '二级分类': '通信',
            '三级分类': '光模块',
            '指标类型': '价格',
            '单位': '%',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_ppi',
            '计算方法': 'ppi_communication_equipment',
            '投资意义': '光通信产业链成本传导，设备制造盈利能力',
            '行业占比': 'TMT (14.3%)',
            '数据可用性': '高',
            '重要程度': '★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 2,
            '指标代码': 'TMT_ELEC_IC_PRODUCTION',
            '中文名称': '集成电路产量',
            '英文名称': 'Integrated Circuit Production',
            '一级分类': 'TMT',
            '二级分类': '电子',
            '三级分类': '半导体',
            '指标类型': '产量',
            '单位': '亿块',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_industrial_production_yoy',
            '计算方法': 'industrial_production_ic',
            '投资意义': '半导体产业核心，科技制造业景气度',
            '行业占比': 'TMT (14.3%)',
            '数据可用性': '高',
            '重要程度': '★★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 3,
            '指标代码': 'TMT_ELEC_LAPTOP_SALES',
            '中文名称': '笔记本电脑销量',
            '英文名称': 'Laptop Sales',
            '一级分类': 'TMT',
            '二级分类': '电子',
            '三级分类': '消费电子',
            '指标类型': '销量',
            '单位': '万台',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'macro_china_retail_total',
            '计算方法': 'retail_electronics_laptop',
            '投资意义': '消费电子终端需求，远程办公趋势',
            '行业占比': 'TMT (14.3%)',
            '数据可用性': '中',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        }
    ]
    
    # 2. 周期行业指标
    cyclical_data = [
        {
            'ID': 4,
            '指标代码': 'CYCLE_CHEM_SODA_ASH_PRODUCTION',
            '中文名称': '纯碱产量',
            '英文名称': 'Soda Ash Production',
            '一级分类': '周期',
            '二级分类': '基础化工',
            '三级分类': '纯碱',
            '指标类型': '产量',
            '单位': '万吨',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_industrial_production_yoy',
            '计算方法': 'industrial_production_soda_ash',
            '投资意义': '玻璃、化工下游需求，房地产产业链',
            '行业占比': '周期 (27.1%)',
            '数据可用性': '高',
            '重要程度': '★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 5,
            '指标代码': 'CYCLE_CHEM_PESTICIDE_PRODUCTION',
            '中文名称': '化学农药原药产量',
            '英文名称': 'Chemical Pesticide Production',
            '一级分类': '周期',
            '二级分类': '基础化工',
            '三级分类': '农药',
            '指标类型': '产量',
            '单位': '万吨',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_industrial_production_yoy',
            '计算方法': 'industrial_production_pesticide',
            '投资意义': '农业生产投入，农产品价格传导',
            '行业占比': '周期 (27.1%)',
            '数据可用性': '高',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        },
        {
            'ID': 6,
            '指标代码': 'CYCLE_COAL_THERMAL_PRICE',
            '中文名称': '环渤海动力煤价格',
            '英文名称': 'Bohai Rim Thermal Coal Price',
            '一级分类': '周期',
            '二级分类': '煤炭',
            '三级分类': '动力煤',
            '指标类型': '价格',
            '单位': '元/吨',
            '数据频率': '周度',
            '数据源': 'AkShare',
            'API函数': 'energy_oil_hist',
            '计算方法': 'energy_coal_bohai_rim',
            '投资意义': '电力成本核心，能源供需平衡',
            '行业占比': '周期 (27.1%)',
            '数据可用性': '高',
            '重要程度': '★★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 7,
            '指标代码': 'CYCLE_TRANSPORT_EXPRESS_DELIVERY',
            '中文名称': '快递业务量',
            '英文名称': 'Express Delivery Volume',
            '一级分类': '周期',
            '二级分类': '交通运输',
            '三级分类': '物流',
            '指标类型': '销量',
            '单位': '亿件',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_postal_telecommunicational',
            '计算方法': 'express_delivery_volume',
            '投资意义': '电商活跃度，消费物流需求',
            '行业占比': '周期 (27.1%)',
            '数据可用性': '高',
            '重要程度': '★★★★',
            '实施阶段': '第一阶段'
        }
    ]
    
    # 3. 消费行业指标
    consumer_data = [
        {
            'ID': 8,
            '指标代码': 'CONSUMER_AGRI_RICE_PRICE',
            '中文名称': '稻米价格',
            '英文名称': 'Rice Price',
            '一级分类': '消费',
            '二级分类': '农林牧渔',
            '三级分类': '种植业',
            '指标类型': '价格',
            '单位': '元/吨',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'futures_main_sina',
            '计算方法': 'agricultural_product_rice',
            '投资意义': '粮食安全，农产品通胀传导',
            '行业占比': '消费 (29.3%)',
            '数据可用性': '高',
            '重要程度': '★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 9,
            '指标代码': 'CONSUMER_FOOD_SNACK_SALES',
            '中文名称': '零食坚果特产销售额',
            '英文名称': 'Snack Food Sales',
            '一级分类': '消费',
            '二级分类': '食品饮料',
            '三级分类': '休闲食品',
            '指标类型': '销量',
            '单位': '亿元',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'macro_china_retail_total',
            '计算方法': 'retail_snack_foods',
            '投资意义': '年轻消费群体偏好，消费升级',
            '行业占比': '消费 (29.3%)',
            '数据��用性': '中',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        },
        {
            'ID': 10,
            '指标代码': 'CONSUMER_LIGHT_PRINTING_ELECTRICITY',
            '中文名称': '印刷业用电量',
            '英文名称': 'Printing Industry Electricity',
            '一级分类': '消费',
            '二级分类': '轻工制造',
            '三级分类': '包装印刷',
            '指标类型': '其他',
            '单位': '亿千瓦时',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'energy_oil_detail',
            '计算方法': 'industry_electricity_printing',
            '投资意义': '包装需求，电商物流活跃度',
            '行业占比': '消费 (29.3%)',
            '数据可用性': '中',
            '重要程度': '★★',
            '实施阶段': '第三阶段'
        }
    ]
    
    # 4. 制造业指标
    manufacturing_data = [
        {
            'ID': 11,
            '指标代码': 'MFG_MACHINERY_EXCAVATOR_SALES',
            '中文名称': '挖掘机销量',
            '英文名称': 'Excavator Sales',
            '一级分类': '制造',
            '二级分类': '机械设备',
            '三级分类': '工程机械',
            '指标类型': '销量',
            '单位': '台',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'macro_china_industrial_production_yoy',
            '计算方法': 'machinery_excavator_sales',
            '投资意义': '基建投资先行指标，工程建设活跃度',
            '行业占比': '制造 (17.3%)',
            '数据可用性': '中',
            '重要程度': '★★★★★',
            '实施阶段': '第一阶段'
        },
        {
            'ID': 12,
            '指标代码': 'MFG_MACHINERY_CRANE_SALES',
            '中文名称': '起重机销量',
            '英文名称': 'Crane Sales',
            '一级分类': '制造',
            '二级分类': '机械设备',
            '三级分类': '工程机械',
            '指标类型': '销量',
            '单位': '台',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'macro_china_industrial_production_yoy',
            '计算方法': 'machinery_crane_sales',
            '投资意义': '建筑施工强度，基建项目进度',
            '行业占比': '制造 (17.3%)',
            '数据可用性': '中',
            '重要程度': '★★★★',
            '实施阶段': '第二阶段'
        },
        {
            'ID': 13,
            '指标代码': 'MFG_POWER_INVESTMENT',
            '中文名称': '电力工程投资完成额',
            '英文名称': 'Power Engineering Investment',
            '一级分类': '制造',
            '二级分类': '电力设备',
            '三级分类': '配电设备',
            '指标类型': '其他',
            '单位': '亿元',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_fixed_asset_investment',
            '计算方法': 'fixed_investment_power',
            '投资意义': '电网建设投资，能源基础设施',
            '行业占比': '制造 (17.3%)',
            '数据可用性': '高',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        }
    ]
    
    # 5. 医药行业指标
    pharma_data = [
        {
            'ID': 14,
            '指标代码': 'PHARMA_HEALTHCARE_CPI',
            '中文名称': '医疗保健CPI',
            '英文名称': 'Healthcare CPI',
            '一级分类': '医药',
            '二级分类': '医药生物',
            '三级分类': '医药商业',
            '指标类型': '价格',
            '单位': '%',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_cpi',
            '计算方法': 'cpi_healthcare',
            '投资意义': '医疗成本通胀，医保支付压力',
            '行业占比': '医药 (6.8%)',
            '数据可用性': '高',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        }
    ]
    
    # 6. 金融地产指标
    finance_data = [
        {
            'ID': 15,
            '指标代码': 'FINANCE_INSURANCE_PREMIUM',
            '中文名称': '原保险保费收入',
            '英文名称': 'Original Insurance Premium',
            '一级分类': '金融地产',
            '二级分类': '非银金融',
            '三级分类': '保险',
            '指标类型': '收入',
            '单位': '亿元',
            '数据频率': '月度',
            '数据源': 'AkShare',
            'API函数': 'macro_china_insurance',
            '计算方法': 'insurance_premium_income',
            '投资意义': '风险保障需求，财富管理发展',
            '行业占比': '金融地产 (5.3%)',
            '数据可用性': '高',
            '重要程度': '★★★',
            '实施阶段': '第二阶段'
        }
    ]
    
    # 7. 计算指标
    calculated_data = [
        {
            'ID': 16,
            '指标代码': 'CALC_TMT_PROSPERITY_INDEX',
            '中文名称': 'TMT行业景气度指数',
            '英文名称': 'TMT Prosperity Index',
            '一级分类': '计算指标',
            '二级分类': '行业景气度',
            '三级分类': '综合指数',
            '指标类型': '指数',
            '单位': '指数',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'weighted_composite',
            '计算方法': '通信设备PPI*0.3 + 集成电路产量*0.4 + 笔记本销量*0.3',
            '投资意义': 'TMT行业综合景气度，科技周期判断',
            '行业占比': '计算指标',
            '数据可用性': '依赖组成指标',
            '重要程度': '★★★★★',
            '实施阶段': '第三阶段'
        },
        {
            'ID': 17,
            '指标代码': 'CALC_CYCLICAL_PROSPERITY_INDEX',
            '中文名称': '周期行业景气度指数',
            '英文名称': 'Cyclical Prosperity Index',
            '一级分类': '计算指标',
            '二级分类': '行业景气度',
            '三级分类': '综合指数',
            '指标类型': '指数',
            '单位': '指数',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'weighted_composite',
            '计算方法': '纯碱产量*0.4 + 农药产量*0.3 + 动力煤价格*0.3',
            '投资意义': '周期行业综合景气度，经济周期判断',
            '行业占比': '计算指标',
            '数据可用性': '依赖组成指标',
            '重要程度': '★★★★★',
            '实施阶段': '第三阶段'
        },
        {
            'ID': 18,
            '指标代码': 'CALC_SUPPLY_CHAIN_CONSTRUCTION',
            '中文名称': '建筑产业链指数',
            '英文名称': 'Construction Supply Chain Index',
            '一级分类': '计算指标',
            '二级分类': '产业链指数',
            '三级分类': '供应链传导',
            '指标类型': '指数',
            '单位': '指数',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'supply_chain_composite',
            '计算方法': '挖掘机销量*0.4 + 起重机销量*0.3 + 纯碱产量*0.3',
            '投资意义': '建筑全产业链景气度，基建房地产投资',
            '行业占比': '计算指标',
            '数据可用性': '依赖组成指标',
            '重要程度': '★★★★',
            '实施阶段': '第三阶段'
        },
        {
            'ID': 19,
            '指标代码': 'CALC_PRICE_TRANSMISSION_INDEX',
            '中文名称': '行业价格传导指数',
            '英文名称': 'Industry Price Transmission Index',
            '一级分类': '计算指标',
            '二级分类': '价格传导',
            '三级分类': '成本传导',
            '指标类型': '指数',
            '单位': '指数',
            '数据频率': '月度',
            '数据源': '计算',
            'API函数': 'price_transmission_composite',
            '计算方法': '动力煤价格*0.4 + 通信设备PPI*0.3 + 稻米价格*0.3',
            '投资意义': '上下游价格传导路径，通胀压力分析',
            '行业占比': '计算指标',
            '数据可用性': '依赖组成指标',
            '重要程度': '★★★★',
            '实施阶段': '第三阶段'
        }
    ]
    
    # 合并所有数据
    all_indicators = tmt_data + cyclical_data + consumer_data + manufacturing_data + pharma_data + finance_data + calculated_data
    df_indicators = pd.DataFrame(all_indicators)
    
    # 创建统计汇总数据
    summary_data = [
        {'项目': '总指标数量', '数值': 1064, '说明': '基于兴证策略的完整指标体系'},
        {'项目': '一级行业数量', '数值': 7, '说明': 'TMT、周期、消费、制造、医药、金融地产、计算指标'},
        {'项目': '二级行业数量', '数值': 37, '说明': '覆盖主要细分行业'},
        {'项目': '细分领域数量', '数值': 200, '说明': '深度细分专业领域'},
        {'项目': '消费行业指标', '数值': 312, '说明': '占比29.3%'},
        {'项目': '周期行业指标', '数值': 288, '说明': '占比27.1%'},
        {'项目': '制造业指标', '数值': 184, '说明': '占比17.3%'},
        {'项目': 'TMT行业指标', '数值': 152, '说明': '占比14.3%'},
        {'项目': '医药行业指标', '数值': 72, '说明': '占比6.8%'},
        {'项目': '金融地产指标', '数值': 56, '说明': '占比5.3%'}
    ]
    df_summary = pd.DataFrame(summary_data)
    
    # 创建API函数映射表
    api_mapping = [
        {'API函数': 'macro_china_ppi', '功能描述': '工业品出厂价格指数', '数据类型': '价格指数', '更新频率': '月度'},
        {'API函数': 'macro_china_industrial_production_yoy', '功能描述': '工业增加值同比', '数据类型': '生产数据', '更新频率': '月度'},
        {'API函数': 'macro_china_consumer_goods_retail', '功能描述': '消费品零售总额', '数据类型': '消费数据', '更新频率': '月度'},
        {'API函数': 'macro_china_fixed_asset_investment', '功能描述': '固定资产投资', '数据类型': '投资数据', '更新频率': '月度'},
        {'API函数': 'macro_china_cpi', '功能描述': '消费者价格指数', '数据类型': '价格指数', '更新频率': '月度'},
        {'API函数': 'energy_oil_hist', '功能描述': '能源价格历史数据', '数据类型': '能源数据', '更新频率': '日度'},
        {'API函数': 'futures_main_sina', '功能描述': '主力合约数据', '数据类型': '期货数据', '更新频率': '日度'},
        {'API函数': 'macro_china_postal_telecommunicational', '功能描述': '邮电业务量', '数据类型': '行业数据', '更新频率': '月度'},
        {'API函数': 'macro_china_insurance', '功能描述': '保险业务数据', '数据类型': '金融数据', '更新频率': '月度'},
        {'API函数': 'energy_oil_detail', '功能描述': '能源详细数据', '数据类型': '能源数据', '更新频率': '日度'}
    ]
    df_api = pd.DataFrame(api_mapping)
    
    # 创建实施计划表
    implementation_plan = [
        {'阶段': '第一阶段', '目标指标数': 230, '时间周期': '3-4周', '重点内容': 'TMT、周期、消费行业核心指标', '交付物': '基础数据获取和存储'},
        {'阶段': '第二阶段', '目标指标数': 834, '时间周期': '4-5周', '重点内容': '完善各行业指标体系', '交付物': '完整的行业指标数据库'},
        {'阶段': '第三阶段', '目标指标数': 144, '时间周期': '3-4周', '重点内容': '计算指标和综合指数', '交付物': '完整的指标分析系统'}
    ]
    df_plan = pd.DataFrame(implementation_plan)
    
    # 写入Excel文件
    output_file = '经济周期分析系统_数据字典.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 主要指标详情
        df_indicators.to_excel(writer, sheet_name='指标详情', index=False)
        
        # 统计汇总
        df_summary.to_excel(writer, sheet_name='统计汇总', index=False)
        
        # API函数映射
        df_api.to_excel(writer, sheet_name='API函数映射', index=False)
        
        # 实施计划
        df_plan.to_excel(writer, sheet_name='实施计划', index=False)
        
        # 按行业分类的详细表格
        for category in ['TMT', '周期', '消费', '制造', '医药', '金融地产', '计算指标']:
            category_df = df_indicators[df_indicators['一级分类'] == category]
            if not category_df.empty:
                category_df.to_excel(writer, sheet_name=f'{category}行业指标', index=False)
    
    print(f"✅ Excel数据字典已创建: {output_file}")
    print(f"📊 包含 {len(df_indicators)} 个指标详情")
    print(f"📋 包含 {len(df_summary)} 项统计汇总")
    print(f"🔗 包含 {len(df_api)} 个API函数映射")
    print(f"📅 包含 {len(df_plan)} 个实施阶段")
    
    # 打印各Sheet页内容
    print("\n=== Excel文件结构 ===")
    print("1. 指标详情 - 所有指标的完整信息")
    print("2. 统计汇总 - 指标体系统计数据")
    print("3. API函数映射 - 数据源API说明")
    print("4. 实施计划 - 分阶段开发计划")
    print("5. TMT行业指标 - TMT行业专项指标")
    print("6. 周期行业指标 - 周期行业专项指标")
    print("7. 消费行业指标 - 消费行业专项指标")
    print("8. 制造行业指标 - 制造业专项指标")
    print("9. 医药行业指标 - 医药行业专项指标")
    print("10. 金融地产行业指标 - 金融地产专项指标")
    print("11. 计算指标行业指标 - 计算指标专项指标")
    
    return output_file

if __name__ == "__main__":
    create_data_dictionary_excel()