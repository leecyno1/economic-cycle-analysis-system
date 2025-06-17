# -*- coding: utf-8 -*-
"""
Wind数据批量收集管理命令
支持指定指标、时间范围的Wind数据采集
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from data_hub.wind_data_collector import WindDataCollector, WindConnectionConfig
from data_hub.models import Indicator, IndicatorData, DataQualityReport


class Command(BaseCommand):
    help = 'Wind数据批量收集命令'

    def add_arguments(self, parser):
        parser.add_argument(
            '--indicators',
            type=str,
            help='指标代码列表，用逗号分隔。如果不指定，将收集所有支持的Wind指标'
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
            '--years',
            type=int,
            default=10,
            help='数据年数（从当前日期向前推算），默认10年'
        )
        
        parser.add_argument(
            '--test-connection',
            action='store_true',
            help='仅测试Wind连接，不收集数据'
        )
        
        parser.add_argument(
            '--create-missing',
            action='store_true',
            help='自动创建数据库中不存在的指标'
        )
        
        parser.add_argument(
            '--username',
            type=str,
            default='17600806220',
            help='Wind用户名'
        )
        
        parser.add_argument(
            '--password',
            type=str,
            default='iv19whot',
            help='Wind密码'
        )

    def handle(self, *args, **options):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("Wind数据批量收集开始"))
        self.stdout.write("=" * 80)

        # 创建Wind配置
        wind_config = WindConnectionConfig(
            username=options['username'],
            password=options['password']
        )
        
        # 创建Wind数据收集器
        collector = WindDataCollector(wind_config)
        
        # 测试连接
        if options['test_connection']:
            self.test_wind_connection(collector)
            return
        
        # 确定时间范围
        if options['start_date'] and options['end_date']:
            start_date = options['start_date']
            end_date = options['end_date']
        else:
            end_date = datetime.now().strftime('%Y-%m-%d')
            years = options['years']
            start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        self.stdout.write(f"时间范围: {start_date} ~ {end_date}")
        
        # 确定要收集的指标
        if options['indicators']:
            indicator_codes = [code.strip() for code in options['indicators'].split(',')]
        else:
            # 收集所有支持的Wind指标
            indicator_codes = collector.get_supported_indicators()
        
        self.stdout.write(f"准备收集 {len(indicator_codes)} 个Wind指标")
        
        # 统计变量
        success_count = 0
        error_count = 0
        total_records = 0
        
        # 收集数据
        for i, indicator_code in enumerate(indicator_codes, 1):
            self.stdout.write(f"\n[{i}/{len(indicator_codes)}] 处理指标: {indicator_code}")
            
            try:
                # 检查指标是否存在
                try:
                    indicator = Indicator.objects.get(code=indicator_code)
                except Indicator.DoesNotExist:
                    if options['create_missing']:
                        # 自动创建指标
                        wind_mapping = collector.wind_mappings.get(indicator_code, {})
                        indicator = Indicator.objects.create(
                            code=indicator_code,
                            name=wind_mapping.get('description', indicator_code),
                            description=f"Wind数据库指标: {wind_mapping.get('description', indicator_code)}",
                            category='wind',
                            frequency=wind_mapping.get('frequency', 'D'),
                            unit='',
                            source='wind',
                            phase=1
                        )
                        self.stdout.write(f"  📝 自动创建指标: {indicator_code}")
                    else:
                        self.stdout.write(f"  ❌ 指标不存在: {indicator_code}")
                        error_count += 1
                        continue
                
                # 显示现有数据数量
                existing_count = IndicatorData.objects.filter(indicator=indicator).count()
                self.stdout.write(f"  现有数据: {existing_count} 条")
                
                # 收集数据
                result = collector.collect_indicator_data(indicator_code, start_date, end_date)
                
                if result.success:
                    success_count += 1
                    total_records += result.records_count
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✅ 成功收集 {result.records_count} 条数据"
                    ))
                    self.stdout.write(f"  📅 数据范围: {result.data_range[0]} ~ {result.data_range[1]}")
                    self.stdout.write(f"  🔗 Wind代码: {result.wind_code}")
                    
                    # 显示最新数据样本
                    latest_data = IndicatorData.objects.filter(
                        indicator=indicator
                    ).order_by('-date')[:3]
                    
                    if latest_data:
                        self.stdout.write("  📊 最新数据:")
                        for data in latest_data:
                            self.stdout.write(f"    {data.date}: {data.value:.4f}")
                            
                else:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(
                        f"  ❌ 收集失败: {result.error_message}"
                    ))
                    if result.error_code:
                        self.stdout.write(f"  🔢 错误代码: {result.error_code}")
                
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f"  ❌ 异常错误: {str(e)}"))
            
            # 每5个指标显示一次进度
            if i % 5 == 0:
                self.stdout.write(f"\n📊 进度: {i}/{len(indicator_codes)} 完成, 成功: {success_count}, 失败: {error_count}")
        
        # 断开Wind连接
        collector.disconnect()
        
        # 生成质量报告
        self.generate_quality_report(start_date, end_date, success_count, error_count, total_records)
        
        # 最终统计
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("Wind数据收集完成!"))
        self.stdout.write("=" * 80)
        self.stdout.write(f"总指标数: {len(indicator_codes)}")
        self.stdout.write(f"成功收集: {success_count}")
        self.stdout.write(f"收集失败: {error_count}")
        self.stdout.write(f"成功率: {success_count/len(indicator_codes)*100:.1f}%")
        self.stdout.write(f"总数据条数: {total_records:,}")
        self.stdout.write("=" * 80)

    def test_wind_connection(self, collector):
        """测试Wind连接"""
        self.stdout.write("🔍 测试Wind连接...")
        
        connection_result = collector.test_connection()
        
        if connection_result['connected']:
            self.stdout.write(self.style.SUCCESS("✅ Wind连接成功!"))
            self.stdout.write(f"Wind版本: {connection_result.get('wind_version', '未知')}")
            self.stdout.write(f"数据测试: {connection_result.get('test_data', '未测试')}")
            
            # 显示支持的指标统计
            supported_indicators = collector.get_supported_indicators()
            self.stdout.write(f"\n📊 支持的指标数量: {len(supported_indicators)}")
            
            # 按类型统计
            mappings = collector.wind_mappings
            categories = {}
            for code, config in mappings.items():
                data_type = config['data_type']
                categories[data_type] = categories.get(data_type, 0) + 1
            
            self.stdout.write("📈 指标类型分布:")
            for category, count in categories.items():
                self.stdout.write(f"  • {category}: {count}个")
                
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ Wind连接失败: {connection_result['error_message']}"
            ))
        
        collector.disconnect()

    def generate_quality_report(self, start_date, end_date, success_count, error_count, total_records):
        """生成数据质量报告"""
        try:
            # 创建质量报告
            report = DataQualityReport.objects.create(
                report_type='wind_batch_collection',
                start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
                end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
                total_indicators=success_count + error_count,
                successful_collections=success_count,
                failed_collections=error_count,
                total_data_points=total_records,
                data_quality_score=success_count/(success_count + error_count)*100 if (success_count + error_count) > 0 else 0,
                issues_found=error_count,
                recommendations=f"Wind数据批量收集完成，成功率: {success_count/(success_count + error_count)*100:.1f}%",
                generated_at=timezone.now()
            )
            
            self.stdout.write(f"\n📋 质量报告ID: {report.id}")
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"生成质量报告失败: {str(e)}")) 