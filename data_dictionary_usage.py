#!/usr/bin/env python3
"""
数据字典使用示例
演示如何在经济周期分析系统中使用指标字典
"""

import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta

class IndicatorsDictionary:
    """指标字典管理类"""
    
    def __init__(self, json_file_path: str = 'indicators_dictionary.json'):
        """初始化指标字典"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.indicators = self.data['indicators']
        self.composite_indicators = self.data['composite_indicators']
        self.metadata = self.data['metadata']
        self.api_mapping = self.data['api_mapping']
        
    def get_indicator_info(self, indicator_id: str) -> Dict[str, Any]:
        """获取指标详细信息"""
        if indicator_id in self.indicators:
            return self.indicators[indicator_id]
        elif indicator_id in self.composite_indicators:
            return self.composite_indicators[indicator_id]
        else:
            return None
    
    def get_indicators_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按行业分类获取指标"""
        result = []
        for indicator_id, info in self.indicators.items():
            if info['category'] == category:
                result.append({**info, 'id': indicator_id})
        return result
    
    def get_indicators_by_type(self, indicator_type: str) -> List[Dict[str, Any]]:
        """按指标类型获取指标"""
        result = []
        for indicator_id, info in self.indicators.items():
            if info['indicator_type'] == indicator_type:
                result.append({**info, 'id': indicator_id})
        return result
    
    def get_indicators_by_phase(self, phase: int) -> List[Dict[str, Any]]:
        """按实施阶段获取指标"""
        result = []
        for indicator_id, info in self.indicators.items():
            if info['implementation_phase'] == phase:
                result.append({**info, 'id': indicator_id})
        return result
    
    def get_high_priority_indicators(self) -> List[Dict[str, Any]]:
        """获取高优先级指标（重要程度 >= 4）"""
        result = []
        for indicator_id, info in self.indicators.items():
            if info['importance_level'] >= 4:
                result.append({**info, 'id': indicator_id})
        return result
    
    def get_api_functions(self) -> List[str]:
        """获取所有API函数列表"""
        functions = set()
        for info in self.indicators.values():
            functions.add(info['api_function'])
        return list(functions)
    
    def generate_indicator_report(self) -> str:
        """生成指标统计报告"""
        report = []
        report.append("=== 指标字典统计报告 ===\n")
        
        # 基本统计
        report.append(f"总指标数量: {self.metadata['total_indicators']}")
        report.append(f"一级行业数量: {self.metadata['coverage']['industries']}")
        report.append(f"二级行业数量: {self.metadata['coverage']['sub_industries']}")
        report.append(f"细分领域数量: {self.metadata['coverage']['sectors']}")
        report.append("")
        
        # 行业分布
        report.append("=== 行业分布 ===")
        for industry, count in self.metadata['distribution'].items():
            percentage = (count / self.metadata['total_indicators']) * 100
            report.append(f"{industry}: {count}个指标 ({percentage:.1f}%)")
        report.append("")
        
        # 指标类型分布
        type_counts = {}
        for info in self.indicators.values():
            type_name = info['indicator_type']
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        report.append("=== 指标类型分布 ===")
        for type_name, count in sorted(type_counts.items()):
            report.append(f"{type_name}: {count}个指标")
        report.append("")
        
        # 数据源分布
        source_counts = {}
        for info in self.indicators.values():
            source = info['data_source']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        report.append("=== 数据源分布 ===")
        for source, count in sorted(source_counts.items()):
            report.append(f"{source}: {count}个指标")
        report.append("")
        
        # 实施阶段分布
        phase_counts = {}
        for info in self.indicators.values():
            phase = info['implementation_phase']
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        report.append("=== 实施阶段分布 ===")
        for phase, count in sorted(phase_counts.items()):
            report.append(f"第{phase}阶段: {count}个指标")
        
        return "\n".join(report)

def demo_usage():
    """数据字典使用示例"""
    print("=== 数据字典使用示例 ===\n")
    
    # 初始化指标字典
    dict_manager = IndicatorsDictionary()
    
    # 1. 获取特定指标信息
    print("1. 获取特定指标信息:")
    indicator_info = dict_manager.get_indicator_info('TMT_ELEC_IC_PRODUCTION')
    if indicator_info:
        print(f"   指标名称: {indicator_info['name_cn']}")
        print(f"   英文名称: {indicator_info['name_en']}")
        print(f"   行业分类: {indicator_info['category']}")
        print(f"   指标类型: {indicator_info['indicator_type']}")
        print(f"   投资意义: {indicator_info['investment_significance']}")
    print()
    
    # 2. 按行业分类查询
    print("2. TMT行业指标:")
    tmt_indicators = dict_manager.get_indicators_by_category('TMT')
    for indicator in tmt_indicators[:3]:  # 只显示前3个
        print(f"   - {indicator['name_cn']} ({indicator['id']})")
    print(f"   ... 共{len(tmt_indicators)}个TMT指标")
    print()
    
    # 3. 按指标类型查询
    print("3. 价格类指标:")
    price_indicators = dict_manager.get_indicators_by_type('价格')
    for indicator in price_indicators:
        print(f"   - {indicator['name_cn']} ({indicator['unit']})")
    print()
    
    # 4. 按实施阶段查询
    print("4. 第一阶段指标（核心指标）:")
    phase1_indicators = dict_manager.get_indicators_by_phase(1)
    for indicator in phase1_indicators:
        print(f"   - {indicator['name_cn']} (重要程度: {'★' * indicator['importance_level']})")
    print()
    
    # 5. 高优先级指标
    print("5. 高优先级指标（重要程度>=4）:")
    high_priority = dict_manager.get_high_priority_indicators()
    for indicator in high_priority:
        print(f"   - {indicator['name_cn']} (★{'★' * indicator['importance_level']})")
    print()
    
    # 6. API函数统计
    print("6. 数据源API函数:")
    api_functions = dict_manager.get_api_functions()
    for func in sorted(api_functions):
        if func in dict_manager.api_mapping:
            desc = dict_manager.api_mapping[func]['description']
            print(f"   - {func}: {desc}")
    print()
    
    # 7. 生成统计报告
    print("7. 统计报告:")
    report = dict_manager.generate_indicator_report()
    print(report)

def create_development_checklist():
    """创建开发检查清单"""
    dict_manager = IndicatorsDictionary()
    
    checklist = []
    checklist.append("# 经济周期分析系统开发检查清单\n")
    
    # 按阶段组织检查清单
    for phase_key, phase_info in dict_manager.data['implementation_phases'].items():
        checklist.append(f"## {phase_info['name']}")
        checklist.append(f"**目标：** {phase_info['target_indicators']}个指标")
        checklist.append(f"**周期：** {phase_info['duration']}")
        checklist.append(f"**重点：** {phase_info['focus']}")
        checklist.append(f"**交付：** {phase_info['deliverable']}\n")
        
        checklist.append("### 优先指标列表")
        for indicator_id in phase_info['priority_indicators']:
            info = dict_manager.get_indicator_info(indicator_id)
            if info:
                checklist.append(f"- [ ] {info['name_cn']} (`{indicator_id}`)")
                checklist.append(f"  - 数据源: {info['data_source']}")
                checklist.append(f"  - API函数: {info['api_function']}")
                checklist.append(f"  - 数据可用性: {info['data_availability']}")
                checklist.append(f"  - 重要程度: {'★' * info['importance_level']}")
        checklist.append("")
    
    # 写入文件
    with open('development_checklist.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(checklist))
    
    print("✅ 开发检查清单已创建: development_checklist.md")

def validate_data_dictionary():
    """验证数据字典完整性"""
    dict_manager = IndicatorsDictionary()
    
    print("=== 数据字典验证 ===\n")
    
    # 检查必需字段
    required_fields = ['name_cn', 'name_en', 'category', 'indicator_type', 
                      'unit', 'frequency', 'data_source', 'api_function',
                      'investment_significance', 'importance_level', 
                      'data_availability', 'implementation_phase']
    
    missing_fields = []
    for indicator_id, info in dict_manager.indicators.items():
        for field in required_fields:
            if field not in info:
                missing_fields.append(f"{indicator_id}.{field}")
    
    if missing_fields:
        print("❌ 缺失字段:")
        for field in missing_fields:
            print(f"   - {field}")
    else:
        print("✅ 所有指标包含必需字段")
    
    # 检查数据一致性
    print("\n📊 数据一致性检查:")
    
    # 检查行业分类
    categories = set(info['category'] for info in dict_manager.indicators.values())
    print(f"   行业分类: {sorted(categories)}")
    
    # 检查指标类型
    types = set(info['indicator_type'] for info in dict_manager.indicators.values())
    print(f"   指标类型: {sorted(types)}")
    
    # 检查数据源
    sources = set(info['data_source'] for info in dict_manager.indicators.values())
    print(f"   数据源: {sorted(sources)}")
    
    # 检查频率
    frequencies = set(info['frequency'] for info in dict_manager.indicators.values())
    print(f"   数据频率: {sorted(frequencies)}")
    
    print("\n✅ 数据字典验证完成")

if __name__ == "__main__":
    # 运行使用示例
    demo_usage()
    
    print("\n" + "="*50 + "\n")
    
    # 创建开发检查清单
    create_development_checklist()
    
    print("\n" + "="*50 + "\n")
    
    # 验证数据字典
    validate_data_dictionary()