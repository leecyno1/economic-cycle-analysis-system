# -*- coding: utf-8 -*-
"""
Django管理命令: 初始化指标数据
运行命令: python manage.py init_indicators
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from data_hub.models import IndicatorCategory, Indicator
from data_hub.indicators_config import INDICATORS_CONFIG


class Command(BaseCommand):
    help = '初始化指标类别和指标数据到数据库'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化指标数据...')
        
        try:
            with transaction.atomic():
                # 清空现有数据(可选,谨慎使用)
                # IndicatorCategory.objects.all().delete()
                # Indicator.objects.all().delete()
                
                categories_created = 0
                indicators_created = 0
                
                for category_name, category_data in INDICATORS_CONFIG.items():
                    # 创建或获取指标类别
                    category, created = IndicatorCategory.objects.get_or_create(
                        name=category_name,
                        defaults={'description': category_data['description']}
                    )
                    
                    if created:
                        categories_created += 1
                        self.stdout.write(f'创建类别: {category_name}')
                    
                    # 创建该类别下的所有指标
                    for indicator_data in category_data['indicators']:
                        indicator, created = Indicator.objects.get_or_create(
                            code=indicator_data['code'],
                            defaults={
                                'name': indicator_data['name'],
                                'category': category,
                                'frequency': indicator_data['frequency'],
                                'lead_lag_status': indicator_data['lead_lag'],
                                'source': f"AkShare - {indicator_data['akshare_func']}",
                                'description': f"通过AkShare的{indicator_data['akshare_func']}函数获取"
                            }
                        )
                        
                        if created:
                            indicators_created += 1
                            self.stdout.write(f'  - 创建指标: {indicator_data["name"]} ({indicator_data["code"]})')
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'指标初始化完成! 创建了 {categories_created} 个类别, {indicators_created} 个指标'
                    )
                )
                
                # 打印统计信息
                total_categories = IndicatorCategory.objects.count()
                total_indicators = Indicator.objects.count()
                self.stdout.write(f'数据库中共有 {total_categories} 个类别, {total_indicators} 个指标')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'初始化失败: {str(e)}')
            ) 