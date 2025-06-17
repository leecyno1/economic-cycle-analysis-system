# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 现实版计算指标配置
基于实际有数据的指标进行计算的衍生指标
"""

# 基于实际有数据指标的计算指标配置
REALISTIC_CALCULATED_INDICATORS = {
    "现实计算指标": {
        "description": "基于实际有数据的指标计算的衍生指标",
        "indicators": [
            # 美国经济指标组合
            {
                "name": "美国经济压力指数", 
                "code": "US_ECONOMIC_STRESS", 
                "calculation": "US_UNEMPLOYMENT + (1 / US_PMI_MFG * 100)", 
                "description": "失业率加上制造业PMI倒数，反映经济压力",
                "frequency": "M", 
                "lead_lag": "LAG"
            },
            
            {
                "name": "美国通胀-制造业指数", 
                "code": "US_INFLATION_MFG_INDEX", 
                "calculation": "US_CPI_MONTHLY * US_PMI_MFG / 100", 
                "description": "CPI与制造业PMI的组合指标",
                "frequency": "M", 
                "lead_lag": "LEAD"
            },
            
            {
                "name": "美国劳动力市场健康度", 
                "code": "US_LABOR_HEALTH", 
                "calculation": "(100 - US_UNEMPLOYMENT) * (US_PMI_MFG / 50)", 
                "description": "就业状况与制造业景气度的组合指标",
                "frequency": "M", 
                "lead_lag": "SYNC"
            },
            
            # 美国PMI相对指标
            {
                "name": "美国制造业景气偏离度", 
                "code": "US_MFG_PMI_DEVIATION", 
                "calculation": "US_PMI_MFG - 50", 
                "description": "制造业PMI偏离中性值(50)的程度",
                "frequency": "M", 
                "lead_lag": "LEAD"
            },
            
            # 失业率变化指标
            {
                "name": "美国就业稳定性指数", 
                "code": "US_EMPLOYMENT_STABILITY", 
                "calculation": "10 - US_UNEMPLOYMENT", 
                "description": "就业稳定性指数，10减去失业率",
                "frequency": "M", 
                "lead_lag": "LAG"
            },
            
            # CPI标准化指标
            {
                "name": "美国通胀压力指数", 
                "code": "US_INFLATION_PRESSURE", 
                "calculation": "abs(US_CPI_MONTHLY) * 10", 
                "description": "通胀压力指数，CPI月率的绝对值放大",
                "frequency": "M", 
                "lead_lag": "LAG"
            },
            
            # 综合经济健康指标
            {
                "name": "美国经济健康综合指数", 
                "code": "US_ECONOMIC_HEALTH_COMPOSITE", 
                "calculation": "((100 - US_UNEMPLOYMENT) + US_PMI_MFG - abs(US_CPI_MONTHLY) * 10) / 3", 
                "description": "综合就业、制造业和通胀的经济健康指标",
                "frequency": "M", 
                "lead_lag": "SYNC"
            },
            
            # PMI效率指标
            {
                "name": "美国制造业效率指数", 
                "code": "US_MFG_EFFICIENCY", 
                "calculation": "US_PMI_MFG / (US_UNEMPLOYMENT + 1)", 
                "description": "制造业PMI与失业率的比值，反映制造业效率",
                "frequency": "M", 
                "lead_lag": "SYNC"
            },
            
            # 价格调整的PMI
            {
                "name": "通胀调整制造业PMI", 
                "code": "US_INFLATION_ADJUSTED_PMI", 
                "calculation": "US_PMI_MFG - US_CPI_MONTHLY", 
                "description": "制造业PMI减去CPI月率，反映实际制造业状况",
                "frequency": "M", 
                "lead_lag": "LEAD"
            },
            
            # 经济动能指标
            {
                "name": "美国经济动能指数", 
                "code": "US_ECONOMIC_MOMENTUM", 
                "calculation": "(US_PMI_MFG - 50) * (100 - US_UNEMPLOYMENT) / 100", 
                "description": "PMI景气度与就业率的乘积，反映经济动能",
                "frequency": "M", 
                "lead_lag": "LEAD"
            }
        ]
    }
}

def get_realistic_calc_indicators():
    """获取现实版计算指标列表"""
    return REALISTIC_CALCULATED_INDICATORS["现实计算指标"]["indicators"]

def check_realistic_data_availability():
    """检查现实版计算指标的数据可用性"""
    from .models import Indicator, IndicatorData
    
    # 需要的基础指标
    required_indicators = ["US_CPI_MONTHLY", "US_UNEMPLOYMENT", "US_PMI_MFG"]
    
    availability = {}
    total_available = 0
    
    for code in required_indicators:
        try:
            indicator = Indicator.objects.get(code=code)
            data_count = IndicatorData.objects.filter(indicator=indicator).count()
            availability[code] = {
                'exists': True,
                'data_count': data_count,
                'has_data': data_count > 0
            }
            if data_count > 0:
                total_available += 1
        except Indicator.DoesNotExist:
            availability[code] = {
                'exists': False,
                'data_count': 0,
                'has_data': False
            }
    
    return {
        'required_count': len(required_indicators),
        'available_count': total_available,
        'all_available': total_available == len(required_indicators),
        'details': availability
    }

def get_executable_realistic_indicators():
    """获取可执行的现实版计算指标"""
    availability = check_realistic_data_availability()
    
    if availability['all_available']:
        return get_realistic_calc_indicators()
    else:
        return []

if __name__ == "__main__":
    print("=== 现实版计算指标配置 ===")
    indicators = get_realistic_calc_indicators()
    print(f"总共{len(indicators)}个计算指标")
    
    for i, indicator in enumerate(indicators, 1):
        print(f"{i:2d}. {indicator['code']}")
        print(f"    名称: {indicator['name']}")
        print(f"    公式: {indicator['calculation']}")
        print(f"    描述: {indicator['description']}")
        print("")
    
    # 检查数据可用性
    print("=== 数据可用性检查 ===")
    availability = check_realistic_data_availability()
    print(f"需要基础指标: {availability['required_count']}个")
    print(f"可用基础指标: {availability['available_count']}个")
    print(f"全部可用: {'是' if availability['all_available'] else '否'}")
    
    for code, detail in availability['details'].items():
        status = "✅" if detail['has_data'] else "❌"
        print(f"{status} {code}: {detail['data_count']}条数据")
    
    executable = get_executable_realistic_indicators()
    print(f"\n可执行计算指标: {len(executable)}个") 