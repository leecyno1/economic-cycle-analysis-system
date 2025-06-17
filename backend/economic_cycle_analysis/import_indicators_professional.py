#!/usr/bin/env python3
"""
专业指标数据导入脚本 - 从兴证策略数据库导入1064个专业指标
"""

import os
import sys
import django
from datetime import datetime
import pandas as pd
import json
import re
from typing import Dict, List, Tuple

# 设置Django环境
sys.path.append('/Users/lichengyin/Desktop/Projects/1x/backend/economic_cycle_analysis')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import IndicatorCategory, Indicator, IndicatorData

class ProfessionalIndicatorImporter:
    def __init__(self):
        self.excel_file = '/Users/lichengyin/Desktop/Projects/1x/【兴证策略】行业中观&拥挤度数据库（20250530）.xlsx'
        self.sheet_name = '1.5 中观指标明细'
        self.stats = {
            'imported': 0,
            'skipped_duplicate': 0,
            'updated_metadata': 0,
            'errors': 0,
            'categories_created': 0
        }
        
        # 行业分类映射
        self.industry_mapping = {
            '周期': '周期行业',
            'TMT': 'TMT行业', 
            '消费': '消费行业',
            '医药': '医疗健康',
            '制造': '制造业',
            '金融地产': '金融地产'
        }
        
        # 指标类型映射
        self.indicator_type_mapping = {
            '价格': '价格指标',
            '产量': '生产指标',
            '销量': '销售指标',
            '库存': '库存指标',
            '其他': '综合指标',
            '开工': '运营指标',
            '利润': '财务指标'
        }
        
    def setup_categories(self):
        """设置指标分类体系"""
        print("=== 设置指标分类体系 ===")
        
        categories = {}
        
        # 按大类行业创建一级分类
        for big_industry, category_name in self.industry_mapping.items():
            category, created = IndicatorCategory.objects.get_or_create(
                name=category_name,
                defaults={
                    'code': big_industry.upper().replace('TMT', 'TMT'),
                    'description': f'{category_name}相关的经济指标',
                    'level': 1,
                    'sort_order': len(categories)
                }
            )
            categories[big_industry] = category
            if created:
                print(f"✓ 创建一级分类: {category_name} ({category.code})")
                self.stats['categories_created'] += 1
        
        # 创建特殊分类
        special_categories = [
            {'name': '景气指数', 'code': 'PROSPERITY', 'desc': '各行业景气度指数'},
            {'name': '拥挤度指标', 'code': 'CROWDING', 'desc': '市场拥挤度相关指标'},
            {'name': '未分类', 'code': 'UNCATEGORIZED', 'desc': '待分类的指标'}
        ]
        
        for cat_config in special_categories:
            category, created = IndicatorCategory.objects.get_or_create(
                name=cat_config['name'],
                defaults={
                    'code': cat_config['code'],
                    'description': cat_config['desc'],
                    'level': 1,
                    'sort_order': 999
                }
            )
            categories[cat_config['name']] = category
            if created:
                print(f"✓ 创建特殊分类: {cat_config['name']} ({category.code})")
                self.stats['categories_created'] += 1
        
        return categories
        
    def import_indicators(self):
        """从Excel导入指标数据"""
        print("\n=== 导入专业指标数据 ===")
        
        try:
            # 读取指标明细数据
            df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name, header=0)
            print(f"读取到 {len(df)} 个指标记录")
            
            # 设置分类
            categories = self.setup_categories()
            
            # 处理每个指标
            for idx, row in df.iterrows():
                try:
                    # 提取指标信息
                    indicator_name = str(row['指标']).strip()
                    big_industry = str(row['大类行业映射']).strip()
                    industry_level1 = str(row['一级行业映射']).strip()
                    industry_188 = str(row['188行业']).strip()
                    indicator_type = str(row['指标类型']).strip()
                    correlation = row.get('近三年股价相关性', 0)
                    latest_date = str(row.get('最新数据日期', ''))
                    is_prosperity = row.get('是否纳入景气指数', 0)
                    
                    # 跳过无效指标名
                    if (pd.isna(indicator_name) or 
                        indicator_name in ['nan', 'NaN', ''] or
                        len(indicator_name) < 3):
                        print(f"跳过无效指标: {indicator_name}")
                        continue
                    
                    # 检查指标是否已存在
                    if Indicator.objects.filter(name=indicator_name).exists():
                        print(f"指标已存在，跳过: {indicator_name}")
                        self.stats['skipped_duplicate'] += 1
                        continue
                    
                    # 确定分类
                    category = categories.get(big_industry, categories['未分类'])
                    
                    # 生成指标代码
                    indicator_code = f"XZ_{idx+1:04d}"
                    
                    # 构建描述
                    description_parts = []
                    if indicator_type in self.indicator_type_mapping:
                        description_parts.append(self.indicator_type_mapping[indicator_type])
                    
                    description_parts.extend([
                        f"行业: {industry_level1}/{industry_188}",
                        f"数据源: 兴证策略数据库",
                        f"最新数据: {latest_date}"
                    ])
                    
                    if is_prosperity == 1:
                        description_parts.append("纳入景气指数计算")
                    
                    description = " | ".join(description_parts)
                    
                    # 推断频率
                    frequency = Indicator.Frequency.MONTHLY  # 默认月度
                    if '日' in indicator_name:
                        frequency = Indicator.Frequency.DAILY
                    elif '周' in indicator_name:
                        frequency = Indicator.Frequency.WEEKLY
                    elif '年' in indicator_name:
                        frequency = Indicator.Frequency.YEARLY
                    
                    # 创建指标
                    indicator = Indicator.objects.create(
                        name=indicator_name,
                        code=indicator_code,
                        category=category,
                        description=description,
                        source="兴证策略行业中观&拥挤度数据库",
                        unit="待确定",
                        frequency=frequency,
                        is_active=True,
                        # 扩展字段
                        sector=industry_level1,
                        industry=industry_188,
                        sub_category=indicator_type,
                        # 设置元数据
                        metadata={
                            'stock_correlation': float(correlation) if pd.notna(correlation) else 0.0,
                            'latest_date': latest_date,
                            'is_prosperity_indicator': is_prosperity == 1,
                            'original_big_industry': big_industry
                        }
                    )
                    
                    print(f"✓ 导入指标: {indicator_name} [{big_industry}/{industry_level1}]")
                    self.stats['imported'] += 1
                    
                except Exception as e:
                    print(f"✗ 导入指标失败 {idx}: {str(e)}")
                    self.stats['errors'] += 1
                    continue
                    
        except Exception as e:
            print(f"读取Excel文件失败: {str(e)}")
            return False
            
        return True
    
    def enhance_metadata(self):
        """增强指标元数据"""
        print("\n=== 增强指标元数据 ===")
        
        # 更新单位信息
        unit_patterns = {
            '%': ['同比', '环比', '占比', '增长率'],
            '元/吨': ['价格', '均价'],
            '万吨': ['产量', '库存'],
            '亿元': ['投资', '销售额', '收入'],
            '个': ['企业数', '项目数'],
            '指数': ['指数', 'PMI', 'CPI', 'PPI']
        }
        
        updated_count = 0
        for indicator in Indicator.objects.filter(unit='待确定'):
            for unit, keywords in unit_patterns.items():
                if any(keyword in indicator.name for keyword in keywords):
                    indicator.unit = unit
                    indicator.save()
                    updated_count += 1
                    break
        
        print(f"✓ 更新了 {updated_count} 个指标的单位信息")
        self.stats['updated_metadata'] = updated_count
    
    def generate_report(self):
        """生成导入报告"""
        print("\n" + "="*60)
        print("兴证策略专业指标导入完成报告")
        print("="*60)
        
        total_indicators = Indicator.objects.count()
        total_categories = IndicatorCategory.objects.count()
        
        print(f"总指标数量: {total_indicators}")
        print(f"总分类数量: {total_categories}")
        print(f"本次导入: {self.stats['imported']}")
        print(f"跳过重复: {self.stats['skipped_duplicate']}")
        print(f"创建分类: {self.stats['categories_created']}")
        print(f"元数据更新: {self.stats['updated_metadata']}")
        print(f"处理错误: {self.stats['errors']}")
        
        # 按分类统计
        print("\n按分类统计:")
        for category in IndicatorCategory.objects.all().order_by('sort_order'):
            count = category.indicators.count()
            print(f"  {category.name} ({category.code}): {count} 个指标")
        
        # 按指标类型统计
        print("\n按指标类型统计:")
        for indicator_type in self.indicator_type_mapping.values():
            count = Indicator.objects.filter(description__contains=indicator_type).count()
            print(f"  {indicator_type}: {count} 个指标")
        
        # 按频率统计
        print("\n按频率统计:")
        for freq_choice in Indicator.Frequency.choices:
            count = Indicator.objects.filter(frequency=freq_choice[0]).count()
            print(f"  {freq_choice[1]}: {count} 个指标")
        
        # 高相关性指标统计
        high_corr_count = Indicator.objects.filter(metadata__stock_correlation__gte=0.3).count()
        print(f"\n高股价相关性指标(≥0.3): {high_corr_count} 个")
        
        print("\n导入完成！已构建专业级指标体系。")
    
    def run(self):
        """运行完整的导入流程"""
        print("开始兴证策略专业指标导入流程...")
        print(f"源文件: {self.excel_file}")
        print(f"工作表: {self.sheet_name}")
        
        if self.import_indicators():
            self.enhance_metadata()
            self.generate_report()
        else:
            print("指标导入失败，流程终止")

if __name__ == "__main__":
    importer = ProfessionalIndicatorImporter()
    importer.run()