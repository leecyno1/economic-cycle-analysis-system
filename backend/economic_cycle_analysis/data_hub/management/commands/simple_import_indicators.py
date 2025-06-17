# -*- coding: utf-8 -*-
"""
简化版指标导入命令 - 避免字段不匹配问题
"""

import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from data_hub.models import IndicatorCategory, Indicator


class Command(BaseCommand):
    help = '简化版指标导入 - 避免字段不匹配问题'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 开始简化导入指标字典...')
        )

        # 确定JSON文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..', '..', '..', '..')
        json_file_path = os.path.join(project_root, 'indicators_dictionary.json')

        # 检查文件是否存在
        if not os.path.exists(json_file_path):
            raise CommandError(f'JSON文件不存在: {json_file_path}')

        # 读取JSON数据
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.stdout.write(f'✅ 成功读取JSON文件: {json_file_path}')
        except Exception as e:
            raise CommandError(f'读取JSON文件失败: {e}')

        # 开始导入
        try:
            with transaction.atomic():
                self._import_categories(data)
                self._import_indicators(data)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'导入过程中出错: {e}')
            )
            raise

        self.stdout.write(
            self.style.SUCCESS('🎉 简化版指标字典导入完成！')
        )

    def _import_categories(self, data):
        """导入指标分类 - 仅使用核心字段"""
        self.stdout.write('📂 导入指标分类...')
        
        indicators_data = data.get('indicators', {})
        categories = set()
        
        # 收集所有分类
        for indicator_code, indicator_info in indicators_data.items():
            category = indicator_info.get('category')
            if category:
                categories.add(category)
        
        created_count = 0

        # 创建分类 - 只使用最基础的字段
        for category_name in categories:
            if not IndicatorCategory.objects.filter(code=category_name.upper()).exists():
                try:
                    category = IndicatorCategory.objects.create(
                        code=category_name.upper(),
                        name=category_name,
                        description=f'{category_name}行业指标分类',
                        level=1,
                        sort_order=0,
                    )
                    created_count += 1
                    self.stdout.write(f'  + 创建分类: {category.name}')
                except Exception as e:
                    self.stdout.write(f'  ❌ 创建分类失败 {category_name}: {e}')

        self.stdout.write(
            self.style.SUCCESS(f'✅ 分类导入完成，共创建 {created_count} 个分类')
        )

    def _import_indicators(self, data):
        """导入指标 - 仅使用核心字段"""
        self.stdout.write('📊 导入指标...')
        
        indicators_data = data.get('indicators', {})
        created_count = 0
        error_count = 0

        for indicator_code, indicator_info in indicators_data.items():
            try:
                self._create_indicator(indicator_code, indicator_info)
                created_count += 1
                if created_count % 50 == 0:
                    self.stdout.write(f'  已处理 {created_count} 个指标...')
            except Exception as e:
                error_count += 1
                if error_count <= 10:  # 只显示前10个错误
                    self.stdout.write(
                        self.style.ERROR(f'  ❌ 创建指标失败: {indicator_code} - {e}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ 指标导入完成！成功: {created_count}, 失败: {error_count}'
            )
        )

    def _create_indicator(self, indicator_code, indicator_data):
        """创建单个指标 - 只使用核心字段"""
        
        # 检查是否已存在
        if Indicator.objects.filter(code=indicator_code).exists():
            return  # 跳过已存在的指标
            
        # 获取分类
        category_name = indicator_data.get('category')
        category = IndicatorCategory.objects.get(code=category_name.upper())

        # 映射频率
        frequency_mapping = {
            'monthly': 'M',
            'weekly': 'W', 
            'daily': 'D',
            'quarterly': 'Q',
            'yearly': 'Y'
        }
        frequency = frequency_mapping.get(indicator_data.get('frequency'), 'M')

        # 映射数据可用性
        availability_mapping = {
            'high': 'high',
            'medium': 'medium',
            'low': 'low',
            'calculated': 'calculated'
        }
        data_availability = availability_mapping.get(
            indicator_data.get('data_availability'), 'medium'
        )

        # 创建指标 - 只使用绝对安全的字段
        indicator = Indicator.objects.create(
            code=indicator_code,
            name=indicator_data.get('name_cn', indicator_code),
            description=indicator_data.get('investment_significance', ''),
            category=category,
            sub_category=indicator_data.get('sub_category', ''),
            sector=indicator_data.get('sector', ''),
            industry=indicator_data.get('indicator_type', ''),
            frequency=frequency,
            lead_lag_status='SYNC',  # 默认同步指标
            unit=indicator_data.get('unit', ''),
            source=indicator_data.get('data_source', 'akshare'),
            api_function=indicator_data.get('api_function', ''),
            data_availability=data_availability,
            calculation_method=indicator_data.get('calculation_method', ''),
            importance_level=min(5, max(1, indicator_data.get('importance_level', 3))),
            implementation_phase=indicator_data.get('implementation_phase', 1),
            investment_significance=indicator_data.get('investment_significance', ''),
            
            # 基础维度标签
            dimension_prosperity=True,
            dimension_fundamental=True,
        )

        return indicator 