# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 简化版计算指标配置
基于现有指标进行计算的衍生指标

目标：
1. 使用当前已采集的指标进行计算
2. 构建实用的投资分析指标
3. 验证计算框架的可行性
"""

# 基于现有指标的简化计算指标配置
SIMPLE_CALCULATED_INDICATORS = {
    "简化计算指标": {
        "description": "基于当前数据的计算指标",
        "indicators": [
            # 美国经济相关指标
            {
                "name": "美国就业综合指数", 
                "code": "US_EMPLOYMENT_COMPOSITE", 
                "calculation": "(100 - US_UNEMPLOYMENT) + (US_ADP_EMPLOYMENT / 100)", 
                "description": "综合失业率和ADP就业数据的就业指数",
                "frequency": "M", 
                "lead_lag": "LEAD"
            },
            
            {
                "name": "美国制造业-消费者信心差", 
                "code": "US_PMI_SENTIMENT_SPREAD", 
                "calculation": "US_PMI_MFG - (US_MICHIGAN_SENTIMENT / 10)", 
                "description": "制造业PMI与消费者信心(缩放后)的差值",
                "frequency": "M", 
                "lead_lag": "LEAD"
            },
            
            {
                "name": "美国房地产综合指数", 
                "code": "US_HOUSING_COMPOSITE", 
                "calculation": "(US_EXIST_HOME_SALES / 10) + (US_HOUSE_STARTS / 10)", 
                "description": "综合现房销售和新屋开工的房地产指数",
                "frequency": "M", 
                "lead_lag": "SYNC"
            },
            
            # 市场情绪指标
            {
                "name": "两融风险指数", 
                "code": "MARGIN_RISK_INDEX", 
                "calculation": "MARGIN_BALANCE / CSI300_INDEX", 
                "description": "两融余额与沪深300指数的比值，反映杠杆风险",
                "frequency": "D", 
                "lead_lag": "SYNC"
            },
            
            {
                "name": "北向资金流入强度", 
                "code": "NORTHBOUND_INTENSITY", 
                "calculation": "NORTHBOUND_CAPITAL / 1000", 
                "description": "北向资金流入强度(标准化)",
                "frequency": "D", 
                "lead_lag": "SYNC"
            },
            
            # 估值指标
            {
                "name": "市场整体PE-PB比", 
                "code": "MARKET_PE_PB_RATIO", 
                "calculation": "CSI300_PE / CSI300_PB", 
                "description": "沪深300的PE与PB比值，反映估值结构",
                "frequency": "D", 
                "lead_lag": "LAG"
            },
            
            {
                "name": "小盘股相对估值", 
                "code": "SMALL_CAP_RELATIVE_VALUATION", 
                "calculation": "CSI500_PE / CSI300_PE", 
                "description": "中证500与沪深300的PE比值，反映小盘股溢价",
                "frequency": "D", 
                "lead_lag": "LAG"
            },
            
            # 商品价格指标
            {
                "name": "工业金属综合指数", 
                "code": "INDUSTRIAL_METALS_INDEX", 
                "calculation": "(COPPER_PRICE + ALUMINUM_PRICE + ZINC_PRICE) / 3", 
                "description": "铜铝锌三种金属价格的平均值",
                "frequency": "D", 
                "lead_lag": "LEAD"
            },
            
            {
                "name": "能源金属比价", 
                "code": "ENERGY_METALS_RATIO", 
                "calculation": "CRUDE_OIL_PRICE / COPPER_PRICE", 
                "description": "原油与铜价比值，反映能源与工业品相对强度",
                "frequency": "D", 
                "lead_lag": "LEAD"
            },
            
            # 行业轮动指标
            {
                "name": "消费-周期相对强度", 
                "code": "CONSUMPTION_CYCLE_RATIO", 
                "calculation": "CONSUMER_INDEX / MATERIALS_INDEX", 
                "description": "消费板块与周期板块的相对强度",
                "frequency": "D", 
                "lead_lag": "SYNC"
            },
            
            {
                "name": "成长-价值相对强度", 
                "code": "GROWTH_VALUE_RATIO", 
                "calculation": "GROWTH_INDEX / VALUE_INDEX", 
                "description": "成长股与价值股的相对强度",
                "frequency": "D", 
                "lead_lag": "SYNC"
            },
            
            # 市场交易活跃度
            {
                "name": "市场交易活跃度指数", 
                "code": "MARKET_ACTIVITY_INDEX", 
                "calculation": "(TOTAL_TURNOVER / CSI300_INDEX) * 100", 
                "description": "成交额与市值的比值，反映市场活跃程度",
                "frequency": "D", 
                "lead_lag": "SYNC"
            }
        ]
    }
}

def get_simple_calc_indicators():
    """获取简化版计算指标列表"""
    return SIMPLE_CALCULATED_INDICATORS["简化计算指标"]["indicators"]

def get_available_base_indicators():
    """
    检查哪些基础指标在数据库中可用
    """
    from .models import Indicator
    
    available_codes = set(Indicator.objects.values_list('code', flat=True))
    required_codes = set()
    
    # 提取所有计算指标需要的基础指标
    for calc_indicator in get_simple_calc_indicators():
        calculation = calc_indicator["calculation"]
        import re
        pattern = r'\b[A-Z][A-Z0-9_]*\b'
        indicators = re.findall(pattern, calculation)
        required_codes.update(indicators)
    
    available_base = required_codes.intersection(available_codes)
    missing_base = required_codes - available_codes
    
    return {
        'available': sorted(list(available_base)),
        'missing': sorted(list(missing_base)),
        'available_count': len(available_base),
        'missing_count': len(missing_base)
    }

def get_executable_calc_indicators():
    """
    获取可以执行的计算指标（所有依赖都可用）
    """
    from .models import Indicator
    
    available_codes = set(Indicator.objects.values_list('code', flat=True))
    executable_indicators = []
    
    for calc_indicator in get_simple_calc_indicators():
        calculation = calc_indicator["calculation"]
        import re
        pattern = r'\b[A-Z][A-Z0-9_]*\b'
        required_indicators = set(re.findall(pattern, calculation))
        
        if required_indicators.issubset(available_codes):
            executable_indicators.append(calc_indicator)
    
    return executable_indicators

if __name__ == "__main__":
    print("=== 简化版计算指标配置 ===")
    indicators = get_simple_calc_indicators()
    print(f"总共{len(indicators)}个计算指标")
    
    for i, indicator in enumerate(indicators, 1):
        print(f"{i:2d}. {indicator['code']}")
        print(f"    名称: {indicator['name']}")
        print(f"    公式: {indicator['calculation']}")
        print(f"    描述: {indicator['description']}")
        print("")
    
    # 检查依赖情况
    print("=== 依赖指标分析 ===")
    analysis = get_available_base_indicators()
    print(f"可用基础指标: {analysis['available_count']}个")
    print(f"缺失基础指标: {analysis['missing_count']}个")
    
    if analysis['missing']:
        print(f"缺失指标: {', '.join(analysis['missing'])}")
    
    executable = get_executable_calc_indicators()
    print(f"可执行计算指标: {len(executable)}个") 