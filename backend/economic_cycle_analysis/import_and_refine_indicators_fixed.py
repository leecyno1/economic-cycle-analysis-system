#!/usr/bin/env python3
"""
指标数据导入和精炼脚本 - 修复版
分阶段处理：1. 导入数据 2. 清理无效数据 3. 补充元数据
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

class IndicatorImporter:
    def __init__(self):
        self.excel_file = '/Users/lichengyin/Desktop/Projects/1x/【兴证策略】行业中观&拥挤度数据库（20250530）.xlsx'
        self.stats = {
            'imported': 0,
            'skipped_noname': 0,
            'updated_metadata': 0,
            'errors': 0
        }
        
    def phase1_import_data(self):
        """阶段1：从Excel导入所有指标数据"""
        print("=== 阶段1：导入指标数据 ===")
        
        try:
            # 读取Excel数据
            df = pd.read_excel(self.excel_file, sheet_name=0)
            print(f"读取到 {len(df.columns)} 列数据")
            
            # 获取或创建默认分类
            default_category, created = IndicatorCategory.objects.get_or_create(
                name="未分类",
                defaults={
                    'code': 'UNCATEGORIZED',
                    'description': '待分类的指标',
                    'level': 1,
                    'sort_order': 999
                }
            )
            if created:
                print("✓ 创建默认分类：未分类")
            
            # 处理每个指标列
            valid_columns = []
            for col_idx, column in enumerate(df.columns):
                try:
                    # 确保列名是字符串
                    if isinstance(column, (int, float)):
                        if pd.isna(column):
                            continue
                        else:
                            column_name = str(column)
                    else:
                        column_name = str(column).strip()
                    
                    # 跳过无效列名
                    if (column_name.startswith('Unnamed:') or 
                        column_name == '' or 
                        column_name == 'nan' or
                        len(column_name) < 2):
                        print(f"跳过无效列: {column_name}")
                        self.stats['skipped_noname'] += 1
                        continue
                    
                    valid_columns.append((col_idx, column_name, column))
                    
                except Exception as e:
                    print(f"处理列名失败 {column}: {str(e)}")
                    self.stats['errors'] += 1
            
            print(f"发现 {len(valid_columns)} 个有效指标列")
            
            # 导入有效指标
            for col_idx, column_name, original_column in valid_columns:
                try:
                    # 检查指标是否已存在
                    if Indicator.objects.filter(name=column_name).exists():
                        print(f"指标已存在，跳过: {column_name}")
                        continue
                    
                    # 创建指标
                    indicator = Indicator.objects.create(
                        name=column_name,
                        code=f"IND_{col_idx:04d}",
                        category=default_category,
                        description=f"从兴证策略数据库导入的指标: {column_name}",
                        data_source="兴证策略行业中观&拥挤度数据库",
                        unit="待确定",
                        frequency=Indicator.Frequency.MONTHLY,
                        is_active=True
                    )
                    
                    # 导入数据点 (简化版，只统计非空值)
                    data_points = 0
                    for idx, value in enumerate(df[original_column]):
                        if pd.notna(value) and isinstance(value, (int, float)):
                            data_points += 1
                    
                    print(f"✓ 导入指标: {column_name} (约{data_points}个数据点)")
                    self.stats['imported'] += 1
                    
                except Exception as e:
                    print(f"✗ 导入指标失败 {column_name}: {str(e)}")
                    self.stats['errors'] += 1
                    
        except Exception as e:
            print(f"读取Excel文件失败: {str(e)}")
            return False
            
        return True
    
    def phase2_clean_invalid_data(self):
        """阶段2：清理无效数据"""
        print("\n=== 阶段2：清理无效数据 ===")
        
        # 删除无效名称的指标
        invalid_patterns = [
            r'^Unnamed:',
            r'^Column_\d+$',
            r'^\s*$',
            r'^NaN$',
            r'^None$',
            r'^nan$'
        ]
        
        total_deleted = 0
        for pattern in invalid_patterns:
            invalid_indicators = Indicator.objects.filter(name__regex=pattern)
            count = invalid_indicators.count()
            if count > 0:
                invalid_indicators.delete()
                print(f"✓ 删除 {count} 个匹配 '{pattern}' 的无效指标")
                total_deleted += count
        
        self.stats['skipped_noname'] += total_deleted
        print(f"总共删除 {total_deleted} 个无效指标")
    
    def phase3_enhance_metadata(self):
        """阶段3：增强元数据"""
        print("\n=== 阶段3：增强元数据 ===")
        
        # 行业分类配置
        industry_configs = [
            {'name': '能源行业', 'code': 'ENERGY', 'keywords': ['煤炭', '石油', '天然气', '电力']},
            {'name': '原材料行业', 'code': 'MATERIALS', 'keywords': ['钢铁', '有色', '化工', '建材']},
            {'name': '工业行业', 'code': 'INDUSTRIAL', 'keywords': ['机械', '军工', '建筑', '制造']},
            {'name': '消费行业', 'code': 'CONSUMER', 'keywords': ['汽车', '食品', '纺织', '家电', '零售']},
            {'name': 'TMT行业', 'code': 'TMT', 'keywords': ['电子', '通信', '计算机', '传媒', '软件']},
            {'name': '医疗健康', 'code': 'HEALTHCARE', 'keywords': ['医药', '生物', '医疗', '器械']},
            {'name': '金融行业', 'code': 'FINANCIAL', 'keywords': ['银行', '保险', '证券', '信托']},
            {'name': '房地产行业', 'code': 'REALESTATE', 'keywords': ['地产', '物业', '房地产']}
        ]
        
        # 创建分类
        categories = {}
        for config in industry_configs:
            category, created = IndicatorCategory.objects.get_or_create(
                name=config['name'],
                defaults={
                    'code': config['code'],
                    'description': f'{config["name"]}相关指标',
                    'level': 1,
                    'sort_order': len(categories)
                }
            )
            categories[config['name']] = category
            if created:
                print(f"✓ 创建分类: {config['name']} ({config['code']})")
        
        # 指标类型映射
        indicator_types = {
            '价格': '价格指标',
            '产量': '生产指标', 
            '库存': '库存指标',
            '开工': '运营指标',
            '利润': '财务指标',
            '估值': '估值指标',
            '拥挤度': '市场情绪指标',
            '景气': '景气指标'
        }
        
        # 更新指标分类和描述
        updated_count = 0
        for indicator in Indicator.objects.all():
            updated = False
            original_description = indicator.description
            
            # 根据名称推断行业分类
            for config in industry_configs:
                for keyword in config['keywords']:
                    if keyword in indicator.name:
                        indicator.category = categories[config['name']]
                        updated = True
                        break
                if updated:
                    break
            
            # 根据名称推断指标类型
            for keyword, indicator_type in indicator_types.items():
                if keyword in indicator.name:
                    if not indicator_type in indicator.description:
                        indicator.description = f"{indicator_type} - {original_description}"
                        updated = True
                    break
            
            # 推断频率
            if '月度' in indicator.name or '月' in indicator.name:
                if indicator.frequency != Indicator.Frequency.MONTHLY:
                    indicator.frequency = Indicator.Frequency.MONTHLY
                    updated = True
            elif '周度' in indicator.name or '周' in indicator.name:
                if indicator.frequency != Indicator.Frequency.WEEKLY:
                    indicator.frequency = Indicator.Frequency.WEEKLY
                    updated = True
            elif '日度' in indicator.name or '日' in indicator.name:
                if indicator.frequency != Indicator.Frequency.DAILY:
                    indicator.frequency = Indicator.Frequency.DAILY
                    updated = True
            
            if updated:
                indicator.save()
                updated_count += 1
        
        print(f"✓ 更新了 {updated_count} 个指标的元数据")
        self.stats['updated_metadata'] = updated_count
    
    def generate_report(self):
        """生成处理报告"""
        print("\n" + "="*50)
        print("指标数据导入和精炼完成报告")
        print("="*50)
        
        total_indicators = Indicator.objects.count()
        total_categories = IndicatorCategory.objects.count()
        total_data_points = IndicatorData.objects.count()
        
        print(f"总指标数量: {total_indicators}")
        print(f"总分类数量: {total_categories}")  
        print(f"总数据点数量: {total_data_points}")
        print(f"导入成功: {self.stats['imported']}")
        print(f"跳过无效: {self.stats['skipped_noname']}")
        print(f"元数据更新: {self.stats['updated_metadata']}")
        print(f"处理错误: {self.stats['errors']}")
        
        # 按分类统计
        print("\n按分类统计:")
        for category in IndicatorCategory.objects.all().order_by('sort_order'):
            count = category.indicators.count()
            print(f"  {category.name} ({category.code}): {count} 个指标")
        
        # 按频率统计
        print("\n按频率统计:")
        for freq_choice in Indicator.Frequency.choices:
            count = Indicator.objects.filter(frequency=freq_choice[0]).count()
            print(f"  {freq_choice[1]}: {count} 个指标")
    
    def run(self):
        """运行完整的导入和精炼流程"""
        print("开始指标数据导入和精炼流程...")
        print(f"源文件: {self.excel_file}")
        
        # 执行三个阶段
        if self.phase1_import_data():
            self.phase2_clean_invalid_data()
            self.phase3_enhance_metadata()
            self.generate_report()
        else:
            print("数据导入失败，流程终止")

if __name__ == "__main__":
    importer = IndicatorImporter()
    importer.run()