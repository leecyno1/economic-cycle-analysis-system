# -*- coding: utf-8 -*-
"""
Django管理命令：导入指标字典
从indicators_dictionary.json文件导入1,064个指标定义到数据库
"""

import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth.models import User
from data_hub.models import IndicatorCategory, Indicator


class Command(BaseCommand):
    help = '从indicators_dictionary.json导入指标字典到数据库'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='指标字典JSON文件路径，默认为项目根目录下的indicators_dictionary.json',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清空现有数据后导入',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 开始导入指标字典...')
        )

        # 确定JSON文件路径
        if options['file']:
            json_file_path = options['file']
        else:
            # 默认路径：项目根目录
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

        # 清空现有数据（可选）
        if options['clear']:
            self.stdout.write('🗑️  清空现有数据...')
            with transaction.atomic():
                Indicator.objects.all().delete()
                IndicatorCategory.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ 清空完成'))

        # 开始导入
        try:
            with transaction.atomic():
                self._import_categories(data)
                self._import_indicators(data)
                self._import_composite_indicators(data)
        except Exception as e:
            raise CommandError(f'导入过程中出错: {e}')

        self.stdout.write(
            self.style.SUCCESS('🎉 指标字典导入完成！')
        )

    def _import_categories(self, data):
        """导入指标分类"""
        self.stdout.write('📂 导入指标分类...')
        
        # 从indicators数据中提取分类信息
        indicators_data = data.get('indicators', {})
        categories = set()
        
        # 收集所有分类
        for indicator_code, indicator_info in indicators_data.items():
            category = indicator_info.get('category')
            if category:
                categories.add(category)
        
        created_count = 0

        # 创建分类
        for category_name in categories:
            category, created = IndicatorCategory.objects.get_or_create(
                code=category_name.upper(),
                defaults={
                    'name': category_name,
                    'description': f'{category_name}行业指标分类',
                    'level': 1,
                    'sort_order': 0,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  + 创建分类: {category.name}')

        self.stdout.write(
            self.style.SUCCESS(f'✅ 分类导入完成，共创建 {created_count} 个分类')
        )

    def _import_indicators(self, data):
        """导入指标"""
        self.stdout.write('📊 导入指标...')
        
        indicators_data = data.get('indicators', {})
        created_count = 0
        error_count = 0

        for indicator_code, indicator_info in indicators_data.items():
            try:
                self._create_indicator(indicator_code, indicator_info)
                created_count += 1
                if created_count % 100 == 0:
                    self.stdout.write(f'  已处理 {created_count} 个指标...')
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ❌ 创建指标失败: {indicator_code} - {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ 指标导入完成！成功: {created_count}, 失败: {error_count}'
            )
        )

    def _create_indicator(self, indicator_code, indicator_data):
        """创建单个指标"""
        # 获取分类
        category_name = indicator_data.get('category')
        try:
            category = IndicatorCategory.objects.get(code=category_name.upper())
        except IndicatorCategory.DoesNotExist:
            # 如果分类不存在，创建一个默认分类
            category = IndicatorCategory.objects.create(
                code=category_name.upper(),
                name=category_name,
                level=1
            )

        # 映射数据可用性
        availability_mapping = {
            'high': 'high',
            'medium': 'medium', 
            'low': 'low',
            '计算': 'calculated',
            'calculated': 'calculated'
        }
        data_availability = availability_mapping.get(
            indicator_data.get('data_availability'), 'medium'
        )

        # 映射频率
        frequency_mapping = {
            'monthly': 'M',
            'weekly': 'W',
            'daily': 'D',
            'quarterly': 'Q',
            'yearly': 'Y'
        }
        frequency = frequency_mapping.get(
            indicator_data.get('frequency'), 'M'
        )

        # 创建指标
        indicator, created = Indicator.objects.get_or_create(
            code=indicator_code,
            defaults={
                'name': indicator_data.get('name_cn', ''),
                'description': indicator_data.get('investment_significance'),
                'category': category,
                'sub_category': indicator_data.get('sub_category'),
                'sector': indicator_data.get('sector'),
                'industry': indicator_data.get('indicator_type'),
                'frequency': frequency,
                'lead_lag_status': 'SYNC',  # 默认同步指标
                'unit': indicator_data.get('unit'),
                'source': indicator_data.get('data_source', 'akshare'),
                'api_function': indicator_data.get('api_function'),
                'data_availability': data_availability,
                'calculation_method': indicator_data.get('calculation_method'),
                'importance_level': indicator_data.get('importance_level', 3),
                'implementation_phase': indicator_data.get('implementation_phase', 1),
                'investment_significance': indicator_data.get('investment_significance'),
                
                # 先设置基础维度标签
                'dimension_prosperity': True,  # 大部分指标都与景气度相关
                'dimension_fundamental': True,  # 基本面指标
            }
        )

        return indicator

    def _import_composite_indicators(self, data):
        """导入复合指标"""
        self.stdout.write('🔗 导入复合指标...')
        
        # 目前JSON中没有复合指标定义，跳过
        self.stdout.write('  暂无复合指标定义，跳过此步骤')
        
        self.stdout.write(
            self.style.SUCCESS('✅ 复合指标导入完成')
        ) 