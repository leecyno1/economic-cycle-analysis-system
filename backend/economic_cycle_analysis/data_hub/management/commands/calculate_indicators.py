# -*- coding: utf-8 -*-
"""
Django管理命令：计算扩充指标
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from data_hub.indicator_calculator import IndicatorCalculator
from data_hub.indicators_config_expanded import get_enhanced_category_summary

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '计算基于现有指标的扩充指标（如M1-M2剪刀差、收益率曲线斜率等）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--indicator',
            type=str,
            help='指定要计算的指标代码，如不指定则计算所有计算指标'
        )
        
        parser.add_argument(
            '--start-date',
            type=str,
            help='开始日期 (YYYY-MM-DD格式)'
        )
        
        parser.add_argument(
            '--end-date',
            type=str,
            help='结束日期 (YYYY-MM-DD格式)'
        )
        
        parser.add_argument(
            '--list-indicators',
            action='store_true',
            help='列出所有可计算的指标'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅运行计算但不保存结果'
        )

    def handle(self, *args, **options):
        # 设置日志级别
        if options['verbosity'] >= 2:
            logger.setLevel(logging.DEBUG)
        elif options['verbosity'] >= 1:
            logger.setLevel(logging.INFO)

        calculator = IndicatorCalculator()

        # 列出指标选项
        if options['list_indicators']:
            self.list_indicators(calculator)
            return

        # 解析日期
        start_date = None
        end_date = None
        
        if options['start_date']:
            try:
                start_date = datetime.strptime(options['start_date'], '%Y-%m-%d').date()
            except ValueError:
                raise CommandError(f"Invalid start date format: {options['start_date']}")
        
        if options['end_date']:
            try:
                end_date = datetime.strptime(options['end_date'], '%Y-%m-%d').date()
            except ValueError:
                raise CommandError(f"Invalid end date format: {options['end_date']}")

        self.stdout.write(
            self.style.SUCCESS('=== 经济周期分析系统 - 扩充指标计算 ===')
        )

        # 显示计算范围
        if start_date or end_date:
            self.stdout.write(f"计算时间范围: {start_date or '开始'} 到 {end_date or '现在'}")
        else:
            self.stdout.write("计算时间范围: 全部历史数据")

        if options['dry_run']:
            self.stdout.write(self.style.WARNING("*** 干运行模式：不会保存计算结果 ***"))

        # 计算指定指标或所有指标
        if options['indicator']:
            self.calculate_single_indicator(
                calculator, 
                options['indicator'], 
                start_date, 
                end_date,
                options['dry_run']
            )
        else:
            self.calculate_all_indicators(
                calculator, 
                start_date, 
                end_date,
                options['dry_run']
            )

    def list_indicators(self, calculator):
        """列出所有可计算的指标"""
        self.stdout.write(self.style.SUCCESS('=== 可计算的扩充指标列表 ==='))
        
        # 显示指标体系统计
        summary = get_enhanced_category_summary()
        self.stdout.write("\n📊 指标体系统计:")
        for category, info in summary.items():
            if category == "总计":
                self.stdout.write(
                    self.style.SUCCESS(f"  {category}: {info['count']}个指标")
                )
            else:
                self.stdout.write(f"  {category}: {info['count']}个指标")
        
        # 显示计算指标详情
        self.stdout.write("\n🔧 计算指标详情:")
        for i, indicator in enumerate(calculator.calculated_indicators, 1):
            self.stdout.write(f"  {i:2d}. {indicator['code']}")
            self.stdout.write(f"      名称: {indicator['name']}")
            self.stdout.write(f"      公式: {indicator['calculation']}")
            self.stdout.write(f"      描述: {indicator.get('description', '无')}")
            self.stdout.write(f"      频率: {indicator['frequency']}")
            
            # 显示依赖关系
            deps = calculator.parse_calculation_expression(indicator['calculation'])
            self.stdout.write(f"      依赖: {', '.join(deps)}")
            self.stdout.write("")

    def calculate_single_indicator(self, calculator, indicator_code, start_date, end_date, dry_run):
        """计算单个指标"""
        self.stdout.write(f"\n🎯 计算指标: {indicator_code}")
        
        # 找到指标配置
        calc_config = None
        for config in calculator.calculated_indicators:
            if config["code"] == indicator_code:
                calc_config = config
                break
        
        if not calc_config:
            raise CommandError(f"指标代码不存在: {indicator_code}")
        
        self.stdout.write(f"名称: {calc_config['name']}")
        self.stdout.write(f"公式: {calc_config['calculation']}")
        
        try:
            if not dry_run:
                # 确保计算指标在数据库中存在
                calculator.create_calculated_indicators()
            
            # 执行计算
            result = calculator.calculate_indicator(calc_config, start_date, end_date)
            
            if not result.empty:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ 计算成功，共{len(result)}个数据点")
                )
                
                # 显示最近5个数据点
                self.stdout.write("最近数据点:")
                for date, value in result.tail(5).items():
                    self.stdout.write(f"  {date}: {value:.6f}")
                
                if not dry_run:
                    calculator.save_calculated_data(indicator_code, result)
                    self.stdout.write("✅ 数据已保存到数据库")
                else:
                    self.stdout.write("⚠️  干运行模式：数据未保存")
            else:
                self.stdout.write(
                    self.style.ERROR("❌ 计算失败：无可用数据")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ 计算失败：{str(e)}")
            )

    def calculate_all_indicators(self, calculator, start_date, end_date, dry_run):
        """计算所有指标"""
        self.stdout.write("\n🔄 开始计算所有扩充指标...")
        
        total_indicators = len(calculator.calculated_indicators)
        self.stdout.write(f"总共需要计算 {total_indicators} 个指标")
        
        try:
            if not dry_run:
                # 确保计算指标在数据库中存在
                calculator.create_calculated_indicators()
                self.stdout.write("✅ 计算指标定义已更新")
            
            success_count = 0
            error_count = 0
            
            # 按依赖关系排序
            sorted_indicators = sorted(
                calculator.calculated_indicators,
                key=lambda x: len(calculator.parse_calculation_expression(x["calculation"]))
            )
            
            for i, calc_config in enumerate(sorted_indicators, 1):
                indicator_code = calc_config["code"]
                self.stdout.write(f"\n[{i:2d}/{total_indicators}] 计算 {indicator_code}")
                
                try:
                    result = calculator.calculate_indicator(calc_config, start_date, end_date)
                    
                    if not result.empty:
                        self.stdout.write(f"  ✅ 成功，{len(result)}个数据点")
                        
                        if not dry_run:
                            calculator.save_calculated_data(indicator_code, result)
                        
                        success_count += 1
                    else:
                        self.stdout.write(f"  ⚠️  无数据")
                        error_count += 1
                        
                except Exception as e:
                    self.stdout.write(f"  ❌ 失败：{str(e)}")
                    error_count += 1
            
            # 显示结果统计
            self.stdout.write("\n" + "="*50)
            self.stdout.write(self.style.SUCCESS(f"✅ 计算完成！"))
            self.stdout.write(f"成功: {success_count} 个指标")
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f"失败: {error_count} 个指标"))
            
            if dry_run:
                self.stdout.write(self.style.WARNING("⚠️  干运行模式：所有数据均未保存"))
            else:
                self.stdout.write("💾 所有成功计算的数据已保存到数据库")
                
        except Exception as e:
            raise CommandError(f"计算过程中发生错误：{str(e)}")

    def get_calculation_summary(self, calculator):
        """获取计算摘要信息"""
        from data_hub.models import Indicator, IndicatorData
        
        summary = {}
        
        for calc_config in calculator.calculated_indicators:
            code = calc_config["code"]
            try:
                indicator = Indicator.objects.get(code=code)
                data_count = IndicatorData.objects.filter(indicator=indicator).count()
                
                if data_count > 0:
                    latest_data = IndicatorData.objects.filter(
                        indicator=indicator
                    ).order_by('-date').first()
                    
                    summary[code] = {
                        'name': calc_config['name'],
                        'data_count': data_count,
                        'latest_date': latest_data.date if latest_data else None,
                        'latest_value': latest_data.value if latest_data else None
                    }
                else:
                    summary[code] = {
                        'name': calc_config['name'],
                        'data_count': 0,
                        'latest_date': None,
                        'latest_value': None
                    }
                    
            except Indicator.DoesNotExist:
                summary[code] = {
                    'name': calc_config['name'],
                    'data_count': 0,
                    'latest_date': None,
                    'latest_value': None,
                    'status': 'not_created'
                }
        
        return summary 