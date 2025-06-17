#!/usr/bin/env python3
"""
8维度指标体系导入脚本
整合7个总量维度 + 1个行业维度，形成完整的8维度指标体系

8个维度：
1. 海外面 - 美经济数据、联邦利率、国际政策评分
2. 资金面 - 北向、南向、两融数据  
3. 宏观经济面 - CPI、PPI、PMI、社融、信用、M1、M2、克强指数等
4. 企业基本面 - 盈利预期、财务数据
5. 政策面 - 赤字率、专项债、地方债、特别国债发行、重大产业政策评分、央行相关数据等
6. 市场面 - 全球大宗、股市、债券市场、A股风格指数、行业指数量价表现
7. 情绪面 - 交易情绪指标、舆情指数等
8. 行业维度 - 兴证策略737个专业行业指标 (已存在)
"""

import os
import sys
import django
from datetime import datetime
import json
from typing import Dict, List, Tuple

# 设置Django环境
sys.path.append('/Users/lichengyin/Desktop/Projects/1x/backend/economic_cycle_analysis')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import IndicatorCategory, Indicator, IndicatorData
from data_hub.indicators_config import INDICATORS_CONFIG

class EightDimensionIndicatorImporter:
    def __init__(self):
        self.stats = {
            'categories_created': 0,
            'indicators_imported': 0,
            'skipped_existing': 0,
            'errors': 0
        }
        
    def import_dimension_indicators(self):
        """导入7大总量维度指标"""
        print("🚀 开始导入8维度指标体系...")
        print("=" * 80)
        
        for dimension_name, dimension_data in INDICATORS_CONFIG.items():
            print(f"\\n📊 处理维度: {dimension_name}")
            print(f"   描述: {dimension_data['description']}")
            
            # 创建或获取指标分类
            category, created = IndicatorCategory.objects.get_or_create(
                name=dimension_name,
                defaults={
                    'code': self.generate_category_code(dimension_name),
                    'description': dimension_data['description']
                }
            )
            
            if created:
                self.stats['categories_created'] += 1
                print(f"   ✅ 创建新分类: {dimension_name}")
            else:
                print(f"   📝 使用现有分类: {dimension_name}")
            
            # 导入该维度的指标
            for indicator_config in dimension_data['indicators']:
                self.import_single_indicator(category, indicator_config)
        
        self.print_final_statistics()
        
    def import_single_indicator(self, category: IndicatorCategory, config: dict):
        """导入单个指标"""
        try:
            # 检查指标是否已存在
            if Indicator.objects.filter(code=config['code']).exists():
                self.stats['skipped_existing'] += 1
                print(f"      ⏭️  跳过已存在: {config['name']}")
                return
            
            # 创建指标
            indicator = Indicator.objects.create(
                name=config['name'],
                code=config['code'],
                category=category,
                description=f"通过AkShare的{config['akshare_func']}函数获取",
                source="AkShare",
                api_function=config['akshare_func'],
                unit="待确定",
                frequency=self.convert_frequency(config['frequency']),
                lead_lag_status=config['lead_lag'],
                investment_significance=f"{category.name}总量指标，反映{category.description}",
                is_active=True,
                metadata={
                    'akshare_function': config['akshare_func'],
                    'lead_lag_type': config['lead_lag'],
                    'original_config': config,
                    'dimension': category.name,
                    'import_date': datetime.now().isoformat()
                }
            )
            
            self.stats['indicators_imported'] += 1
            print(f"      ✅ 导入指标: {config['name']} ({config['code']})")
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"      ❌ 导入失败: {config['name']} - {str(e)}")
    
    def generate_category_code(self, name: str) -> str:
        """生成分类代码"""
        mapping = {
            '海外面': 'OVERSEAS',
            '资金面': 'CAPITAL_FLOW', 
            '宏观经济面': 'MACROECONOMIC',
            '企业基本面': 'CORPORATE_FUNDAMENTALS',
            '政策面': 'POLICY',
            '市场面': 'MARKET_PERFORMANCE',
            '情绪面': 'MARKET_SENTIMENT'
        }
        return mapping.get(name, name.upper().replace(' ', '_'))
    
    def convert_frequency(self, freq: str) -> str:
        """转换频率格式"""
        mapping = {
            'D': 'daily',
            'M': 'monthly',
            'Q': 'quarterly',
            'Y': 'yearly'
        }
        return mapping.get(freq, 'daily')
    
    def print_final_statistics(self):
        """打印最终统计结果"""
        print("\\n" + "=" * 80)
        print("🎉 8维度指标体系导入完成！")
        print("=" * 80)
        
        # 统计结果
        print(f"📈 导入统计:")
        print(f"   新增分类: {self.stats['categories_created']} 个")
        print(f"   新增指标: {self.stats['indicators_imported']} 个")
        print(f"   跳过重复: {self.stats['skipped_existing']} 个")
        print(f"   错误数量: {self.stats['errors']} 个")
        
        # 当前数据库统计
        print(f"\\n📊 当前数据库统计:")
        total_indicators = Indicator.objects.count()
        total_categories = IndicatorCategory.objects.count()
        print(f"   总指标数量: {total_indicators} 个")
        print(f"   总分类数量: {total_categories} 个")
        
        # 8维度分布统计
        print(f"\\n🎯 8维度指标分布:")
        for category in IndicatorCategory.objects.all():
            count = category.indicators.count()
            if count > 0:
                print(f"   {category.name}: {count} 个指标")
        
        # 行业指标特殊说明
        industry_indicators = Indicator.objects.filter(
            category__name__in=['TMT行业', '制造业', '消费行业', '周期行业', '医疗健康', '金融地产']
        ).count()
        
        print(f"\\n🏭 行业指标维度统计:")
        print(f"   第8维度(行业指标): {industry_indicators} 个专业指标")
        print(f"   来源: 兴证策略行业中观&拥挤度数据库")
        
        total_8_dimensions = total_indicators
        print(f"\\n🌟 8维度指标体系总计: {total_8_dimensions} 个指标")
        
        # 保存统计报告
        self.save_dimension_report()
    
    def save_dimension_report(self):
        """保存8维度报告"""
        report = {
            'metadata': {
                'version': '2.0',
                'created_date': datetime.now().isoformat(),
                'title': '8维度经济指标体系',
                'description': '整合7个总量维度 + 1个行业维度的完整指标体系'
            },
            'dimension_structure': {
                'total_dimensions': 8,
                'total_indicators': Indicator.objects.count(),
                'total_categories': IndicatorCategory.objects.count()
            },
            'dimensions': {},
            'import_statistics': self.stats
        }
        
        # 收集各维度详情
        for category in IndicatorCategory.objects.all():
            indicators = category.indicators.all()
            if indicators.exists():
                report['dimensions'][category.name] = {
                    'code': category.code,
                    'description': category.description,
                    'indicator_count': indicators.count(),
                    'indicators': [
                        {
                            'name': ind.name,
                            'code': ind.code,
                            'frequency': ind.frequency,
                            'source': ind.source
                        } for ind in indicators
                    ]
                }
        
        # 保存JSON报告
        with open('8_dimension_indicators_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\\n📄 详细报告已保存: 8_dimension_indicators_report.json")

def main():
    """主函数"""
    importer = EightDimensionIndicatorImporter()
    importer.import_dimension_indicators()

if __name__ == "__main__":
    main()