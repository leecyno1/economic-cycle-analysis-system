# -*- coding: utf-8 -*-
"""
指标映射更新器
将数据库中的815个指标映射到相应的AkShare函数
"""

import os
import django
import logging
from typing import Dict, List, Tuple

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator

logger = logging.getLogger(__name__)


class IndicatorMappingUpdater:
    """指标映射更新器"""
    
    def __init__(self):
        self.akshare_function_groups = self._build_function_groups()
        self.mapping_rules = self._build_mapping_rules()
        
    def _build_function_groups(self) -> Dict[str, List[Dict]]:
        """构建AkShare函数分组"""
        return {
            # 宏观经济数据组
            'macro_china': [
                {
                    'patterns': ['CPI', 'cpi', '消费者价格指数', '消费价格'],
                    'func': 'macro_china_cpi_monthly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['PPI', 'ppi', '生产者价格指数', '生产价格'],
                    'func': 'macro_china_ppi_yearly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['M1', 'm1', '货币供应量M1'],
                    'func': 'macro_china_m1_yearly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['M2', 'm2', '货币供应量M2'],
                    'func': 'macro_china_m2_yearly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['PMI', 'pmi', '制造业PMI'],
                    'func': 'macro_china_pmi_yearly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['GDP', 'gdp', '国内生产总值'],
                    'func': 'macro_china_gdp_yearly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'Q'
                },
                {
                    'patterns': ['工业增加值', '工业生产', '工业产出'],
                    'func': 'macro_china_industrial_added_value',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['出口', '出口额', '进出口'],
                    'func': 'macro_china_exports_yoy',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['进口', '进口额'],
                    'func': 'macro_china_imports_yoy',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['贸易差额', '贸易平衡', '净出口'],
                    'func': 'macro_china_trade_balance',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['FDI', 'fdi', '外商直接投资', '外资'],
                    'func': 'macro_china_fdi',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['社会融资规模', '社融', '社会融资'],
                    'func': 'macro_china_shrzgm',
                    'date_col': '日期',
                    'value_col': '社会融资规模存量',
                    'frequency': 'M'
                },
                {
                    'patterns': ['新增人民币贷款', 'RMB贷款', '银行信贷'],
                    'func': 'macro_rmb_loan',
                    'date_col': '月份',
                    'value_col': '新增人民币贷款',
                    'frequency': 'M'
                }
            ],
            
            # 美国经济数据组
            'macro_usa': [
                {
                    'patterns': ['美国', 'US_', '美'],
                    'func': 'macro_usa_cpi_monthly',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                }
            ],
            
            # 股票指数组
            'stock_indices': [
                {
                    'patterns': ['上证指数', '上证综指', 'SSE', '000001'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '000001', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                },
                {
                    'patterns': ['深证成指', '深圳成指', 'SZSE', '399001'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '399001', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                },
                {
                    'patterns': ['创业板指', '创业板', 'CHINEXT', '399006'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '399006', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                },
                {
                    'patterns': ['沪深300', 'CSI300', 'HS300', '000300'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '000300', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                },
                {
                    'patterns': ['中证500', 'CSI500', 'ZZ500', '000905'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '000905', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                },
                {
                    'patterns': ['上证50', 'SSE50', 'SZ50', '000016'],
                    'func': 'index_zh_a_hist',
                    'params': {'symbol': '000016', 'period': 'daily'},
                    'date_col': '日期',
                    'value_col': '收盘',
                    'frequency': 'D'
                }
            ],
            
            # 利率债券组
            'rates_bonds': [
                {
                    'patterns': ['国债收益率', '十年期国债', '10年国债', '10Y'],
                    'func': 'bond_zh_us_rate',
                    'date_col': '日期',
                    'value_col': '中国国债收益率10年',
                    'frequency': 'D'
                },
                {
                    'patterns': ['五年期国债', '5年国债', '5Y'],
                    'func': 'bond_zh_us_rate',
                    'date_col': '日期',
                    'value_col': '中国国债收益率5年',
                    'frequency': 'D'
                },
                {
                    'patterns': ['一年期国债', '1年国债', '1Y'],
                    'func': 'bond_zh_us_rate',
                    'date_col': '日期',
                    'value_col': '中国国债收益率1年',
                    'frequency': 'D'
                },
                {
                    'patterns': ['SHIBOR', 'shibor', '银行间拆借利率'],
                    'func': 'macro_china_shibor_all',
                    'date_col': '日期',
                    'value_col': 'Shibor隔夜',
                    'frequency': 'D'
                },
                {
                    'patterns': ['LPR', 'lpr', '贷款基础利率'],
                    'func': 'rate_interbank',
                    'date_col': '日期',
                    'value_col': '1年期LPR',
                    'frequency': 'M'
                }
            ],
            
            # 商品期货组
            'commodities': [
                {
                    'patterns': ['黄金', '金价', 'GOLD'],
                    'func': 'macro_cons_gold',
                    'date_col': '日期',
                    'value_col': '库存总量',
                    'frequency': 'D'
                },
                {
                    'patterns': ['原油', '石油', 'OIL', 'WTI', 'BRENT'],
                    'func': 'macro_usa_eia_crude_rate',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'W'
                },
                {
                    'patterns': ['动力煤', '煤价', '煤炭'],
                    'func': 'futures_zh_spot',
                    'params': {'symbol': '动力煤'},
                    'date_col': '日期',
                    'value_col': '收盘价',
                    'frequency': 'D'
                }
            ],
            
            # 行业数据组
            'industry_data': [
                {
                    'patterns': ['用电量', '电力消费', '耗电量'],
                    'func': 'macro_china_electricity_quantity',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['快递业务量', '快递', '物流'],
                    'func': 'macro_china_express_quantity',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['保险业务', '保险保费', '保险收入'],
                    'func': 'macro_china_insurance_income',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                },
                {
                    'patterns': ['平板玻璃', '玻璃产量'],
                    'func': 'macro_china_glass_output',
                    'date_col': '日期',
                    'value_col': '今值',
                    'frequency': 'M'
                }
            ],
            
            # 估值指标组
            'valuation': [
                {
                    'patterns': ['PE', 'pe', '市盈率'],
                    'func': 'stock_zh_valuation_baidu',
                    'date_col': '日期',
                    'value_col': 'PE',
                    'frequency': 'D'
                },
                {
                    'patterns': ['PB', 'pb', '市净率'],
                    'func': 'stock_zh_valuation_baidu',
                    'date_col': '日期',
                    'value_col': 'PB',
                    'frequency': 'D'
                }
            ],
            
            # 资金流向组
            'capital_flow': [
                {
                    'patterns': ['北向资金', '北上资金', '外资流入'],
                    'func': 'stock_connect_hist_sina',
                    'date_col': '日期',
                    'value_col': '北向资金',
                    'frequency': 'D'
                },
                {
                    'patterns': ['南向资金', '南下资金'],
                    'func': 'stock_connect_hist_sina',
                    'date_col': '日期',
                    'value_col': '南向资金',
                    'frequency': 'D'
                }
            ]
        }
    
    def _build_mapping_rules(self) -> Dict[str, str]:
        """构建特殊映射规则"""
        return {
            # 兴证策略特定代码映射
            'XZ_': 'custom_xz_data',  # 兴证策略数据需要特殊处理
            
            # 通用行业映射
            'INDUSTRY_': 'industry_specific_data',
            
            # 通用宏观映射
            'MACRO_': 'macro_economic_data',
            
            # 通用技术指标映射
            'TECH_': 'technical_indicators'
        }
    
    def analyze_current_indicators(self) -> Dict[str, List]:
        """分析当前数据库中的指标"""
        indicators = Indicator.objects.all()
        
        analysis = {
            'total_count': indicators.count(),
            'by_category': {},
            'by_prefix': {},
            'unmapped': [],
            'mappable': [],
            'special_cases': []
        }
        
        for indicator in indicators:
            # 按前缀分类
            prefix = indicator.code.split('_')[0] if '_' in indicator.code else 'OTHER'
            if prefix not in analysis['by_prefix']:
                analysis['by_prefix'][prefix] = []
            analysis['by_prefix'][prefix].append(indicator)
            
            # 按类别分类
            category = str(indicator.category) if indicator.category else 'UNKNOWN'
            if category not in analysis['by_category']:
                analysis['by_category'][category] = []
            analysis['by_category'][category].append(indicator)
            
            # 检查是否可映射
            mapping_result = self.find_mapping_for_indicator(indicator)
            if mapping_result:
                analysis['mappable'].append((indicator, mapping_result))
            else:
                analysis['unmapped'].append(indicator)
        
        return analysis
    
    def find_mapping_for_indicator(self, indicator: Indicator) -> Dict:
        """为单个指标查找映射"""
        code = indicator.code
        name = indicator.name
        category = str(indicator.category) if indicator.category else ''
        
        # 检查所有函数组
        for group_name, functions in self.akshare_function_groups.items():
            for func_config in functions:
                patterns = func_config['patterns']
                
                # 检查代码和名称是否匹配模式
                for pattern in patterns:
                    if (pattern.lower() in code.lower() or 
                        pattern.lower() in name.lower() or 
                        pattern.lower() in category.lower()):
                        
                        # 构建映射配置
                        mapping = {
                            'indicator_code': code,
                            'akshare_func': func_config['func'],
                            'date_col': func_config['date_col'],
                            'value_col': func_config['value_col'],
                            'frequency': func_config['frequency'],
                            'params': func_config.get('params', {}),
                            'match_pattern': pattern,
                            'group': group_name,
                            'confidence': self._calculate_confidence(pattern, code, name)
                        }
                        return mapping
        
        return None
    
    def _calculate_confidence(self, pattern: str, code: str, name: str) -> float:
        """计算映射置信度"""
        confidence = 0.0
        
        # 代码精确匹配
        if pattern.upper() == code.upper():
            confidence += 0.8
        elif pattern.upper() in code.upper():
            confidence += 0.6
        
        # 名称匹配
        if pattern in name:
            confidence += 0.5
        
        # 模式匹配质量
        if len(pattern) > 3:  # 长模式更可靠
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def generate_mapping_config(self) -> Dict[str, Dict]:
        """生成完整的映射配置"""
        analysis = self.analyze_current_indicators()
        mapping_config = {}
        
        for indicator, mapping in analysis['mappable']:
            mapping_config[indicator.code] = {
                'func': mapping['akshare_func'],
                'params': mapping['params'],
                'date_col': mapping['date_col'],
                'value_col': mapping['value_col'],
                'data_type': mapping['group'],
                'frequency': mapping['frequency'],
                'confidence': mapping['confidence'],
                'match_pattern': mapping['match_pattern']
            }
        
        return mapping_config
    
    def update_enhanced_collector(self):
        """更新增强版采集器的映射配置"""
        mapping_config = self.generate_mapping_config()
        
        # 写入新的映射文件
        config_file = 'data_hub/enhanced_mapping_config.py'
        
        config_content = f'''# -*- coding: utf-8 -*-
"""
自动生成的指标映射配置
由 IndicatorMappingUpdater 生成
"""

ENHANCED_AKSHARE_MAPPINGS = {mapping_config}

# 映射统计信息
MAPPING_STATS = {{
    'total_indicators': {len(mapping_config)},
    'generation_time': '{datetime.now().isoformat()}',
    'coverage_rate': {len(mapping_config) / Indicator.objects.count() * 100:.2f}
}}
'''
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"已生成映射配置文件: {config_file}")
        print(f"映射了 {len(mapping_config)} 个指标")
        
        return mapping_config
    
    def print_analysis_report(self):
        """打印分析报告"""
        analysis = self.analyze_current_indicators()
        
        print("=" * 60)
        print("指标映射分析报告")
        print("=" * 60)
        
        print(f"总指标数: {analysis['total_count']}")
        print(f"可映射指标: {len(analysis['mappable'])}")
        print(f"未映射指标: {len(analysis['unmapped'])}")
        print(f"映射覆盖率: {len(analysis['mappable']) / analysis['total_count'] * 100:.1f}%")
        
        print("\n按前缀分布:")
        for prefix, indicators in analysis['by_prefix'].items():
            print(f"  {prefix}: {len(indicators)} 个")
        
        print("\n按类别分布:")
        for category, indicators in analysis['by_category'].items():
            print(f"  {category}: {len(indicators)} 个")
        
        print("\n可映射指标示例:")
        for indicator, mapping in analysis['mappable'][:10]:
            print(f"  {indicator.code:15s} -> {mapping['akshare_func']:25s} (置信度: {mapping['confidence']:.2f})")
        
        if len(analysis['mappable']) > 10:
            print(f"  ... 还有 {len(analysis['mappable']) - 10} 个")
        
        print("\n未映射指标示例:")
        for indicator in analysis['unmapped'][:10]:
            print(f"  {indicator.code:15s} - {indicator.name[:40]}")
        
        if len(analysis['unmapped']) > 10:
            print(f"  ... 还有 {len(analysis['unmapped']) - 10} 个")


if __name__ == "__main__":
    from datetime import datetime
    
    updater = IndicatorMappingUpdater()
    updater.print_analysis_report()
    
    print("\n" + "=" * 60)
    print("开始生成映射配置...")
    
    mapping_config = updater.update_enhanced_collector()
    
    print("映射配置生成完成!")
    print("=" * 60) 