# -*- coding: utf-8 -*-
"""
Django管理命令: 采集指标数据
运行命令: python manage.py collect_data
"""

from django.core.management.base import BaseCommand
from data_hub.data_collector import DataCollector


class Command(BaseCommand):
    help = '从AkShare采集指标的时间序列数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--indicator',
            type=str,
            help='指定要采集的指标代码，不指定则采集样本数据'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            help='开始日期，格式：YYYY-MM-DD'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            help='结束日期，格式：YYYY-MM-DD'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='采集所有指标数据（注意：这可能需要很长时间）'
        )

    def handle(self, *args, **options):
        collector = DataCollector()
        
        if options['all']:
            # 采集所有指标
            self.stdout.write('开始采集所有指标数据...')
            collector.collect_all_indicators(
                start_date=options['start_date'],
                end_date=options['end_date']
            )
        elif options['indicator']:
            # 采集指定指标
            indicator_code = options['indicator']
            self.stdout.write(f'开始采集指标: {indicator_code}')
            success = collector.collect_indicator_data(
                indicator_code=indicator_code,
                start_date=options['start_date'],
                end_date=options['end_date']
            )
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'指标 {indicator_code} 采集成功!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'指标 {indicator_code} 采集失败!')
                )
        else:
            # 采集样本数据
            self.stdout.write('开始采集样本数据...')
            
            # 样本指标列表
            sample_indicators = [
                'CN_CPI_MONTHLY',     # 中国CPI月率
                'CN_M2_YEARLY',       # M2货币供应量年率
                'US_CPI_MONTHLY',     # 美国CPI月率
            ]
            
            for indicator_code in sample_indicators:
                self.stdout.write(f'正在采集: {indicator_code}')
                collector.collect_indicator_data(
                    indicator_code=indicator_code,
                    start_date=options['start_date'],
                    end_date=options['end_date']
                )
        
        # 输出采集结果
        self.stdout.write(
            self.style.SUCCESS(
                f'数据采集完成! 成功: {collector.success_count}, 失败: {collector.error_count}'
            )
        )
        
        if collector.errors:
            self.stdout.write(self.style.WARNING('采集过程中的错误:'))
            for error in collector.errors:
                self.stdout.write(f'  - {error}') 