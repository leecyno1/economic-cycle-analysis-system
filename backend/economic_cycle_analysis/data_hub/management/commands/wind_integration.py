# -*- coding: utf-8 -*-
"""
Wind数据源集成管理命令
提供Wind数据源的初始化、同步、数据收集等功能
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from data_hub.wind_integration_service import wind_integration_service
from data_hub.wind_data_collector import WindConnectionConfig
from data_hub.models import Indicator, IndicatorData


class Command(BaseCommand):
    help = 'Wind数据源集成管理命令'

    def add_arguments(self, parser):
        # 子命令
        subparsers = parser.add_subparsers(dest='action', help='操作类型')
        
        # 初始化指标
        init_parser = subparsers.add_parser('init', help='初始化Wind指标到数据库')
        
        # 同步指标
        sync_parser = subparsers.add_parser('sync', help='同步Wind指标与现有指标体系')
        
        # 收集数据
        collect_parser = subparsers.add_parser('collect', help='收集Wind数据')
        collect_parser.add_argument(
            '--indicators',
            type=str,
            help='指标代码列表，用逗号分隔'
        )
        collect_parser.add_argument(
            '--start-date',
            type=str,
            help='开始日期，格式：YYYY-MM-DD'
        )
        collect_parser.add_argument(
            '--end-date',
            type=str,
            help='结束日期，格式：YYYY-MM-DD'
        )
        collect_parser.add_argument(
            '--years',
            type=int,
            default=2,
            help='数据年数（从当前日期向前推算），默认2年'
        )
        collect_parser.add_argument(
            '--force',
            action='store_true',
            help='强制更新已有数据'
        )
        
        # 状态查看
        status_parser = subparsers.add_parser('status', help='查看Wind集成状态')
        
        # 测试连接
        test_parser = subparsers.add_parser('test', help='测试Wind连接')
        test_parser.add_argument(
            '--username',
            type=str,
            default='17600806220',
            help='Wind用户名'
        )
        test_parser.add_argument(
            '--password',
            type=str,
            default='iv19whot',
            help='Wind密码'
        )
        
        # 清理数据
        clean_parser = subparsers.add_parser('clean', help='清理Wind数据')
        clean_parser.add_argument(
            '--confirm',
            action='store_true',
            help='确认删除操作'
        )

    def handle(self, *args, **options):
        action = options.get('action')
        
        if not action:
            self.stdout.write(self.style.ERROR('请指定操作类型'))
            return
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS(f"Wind数据源集成 - {action.upper()}"))
        self.stdout.write("=" * 80)
        
        try:
            if action == 'init':
                self.handle_init()
            elif action == 'sync':
                self.handle_sync()
            elif action == 'collect':
                self.handle_collect(options)
            elif action == 'status':
                self.handle_status()
            elif action == 'test':
                self.handle_test(options)
            elif action == 'clean':
                self.handle_clean(options)
            else:
                self.stdout.write(self.style.ERROR(f'未知操作: {action}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'操作失败: {str(e)}'))
            raise

    def handle_init(self):
        """初始化Wind指标"""
        self.stdout.write("开始初始化Wind指标...")
        
        result = wind_integration_service.initialize_wind_indicators()
        
        if result.success:
            self.stdout.write(self.style.SUCCESS(
                f"✅ Wind指标初始化成功!\n"
                f"   总指标数: {result.total_indicators}\n"
                f"   成功: {result.successful_indicators}\n"
                f"   失败: {result.failed_indicators}\n"
                f"   耗时: {result.execution_time:.2f}秒"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ Wind指标初始化失败!\n"
                f"   失败数: {result.failed_indicators}\n"
                f"   错误: {len(result.errors)} 个"
            ))
            
            # 显示错误详情
            for error in result.errors[:5]:  # 只显示前5个错误
                self.stdout.write(f"   - {error}")

    def handle_sync(self):
        """同步指标"""
        self.stdout.write("开始同步Wind指标与现有指标体系...")
        
        result = wind_integration_service.sync_with_existing_indicators()
        
        if result.success:
            self.stdout.write(self.style.SUCCESS(
                f"✅ 指标同步成功!\n"
                f"   成功同步: {result.successful_indicators}\n"
                f"   失败: {result.failed_indicators}\n"
                f"   耗时: {result.execution_time:.2f}秒"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ 指标同步失败!\n"
                f"   失败数: {result.failed_indicators}"
            ))

    def handle_collect(self, options):
        """收集数据"""
        self.stdout.write("开始收集Wind数据...")
        
        # 解析参数
        indicator_codes = None
        if options.get('indicators'):
            indicator_codes = [code.strip() for code in options['indicators'].split(',')]
        
        # 确定时间范围
        if options.get('start_date') and options.get('end_date'):
            start_date = options['start_date']
            end_date = options['end_date']
        else:
            end_date = datetime.now().strftime('%Y-%m-%d')
            years = options.get('years', 2)
            start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        force_update = options.get('force', False)
        
        self.stdout.write(f"时间范围: {start_date} ~ {end_date}")
        self.stdout.write(f"强制更新: {force_update}")
        
        if indicator_codes:
            self.stdout.write(f"指定指标: {len(indicator_codes)} 个")
        else:
            self.stdout.write("收集所有支持的Wind指标")
        
        # 执行数据收集
        result = wind_integration_service.collect_wind_data_batch(
            indicator_codes=indicator_codes,
            start_date=start_date,
            end_date=end_date,
            force_update=force_update
        )
        
        if result.success:
            self.stdout.write(self.style.SUCCESS(
                f"✅ Wind数据收集成功!\n"
                f"   总指标数: {result.total_indicators}\n"
                f"   成功: {result.successful_indicators}\n"
                f"   失败: {result.failed_indicators}\n"
                f"   总数据点: {result.total_data_points:,}\n"
                f"   耗时: {result.execution_time:.2f}秒"
            ))
            
            # 显示收集效率
            if result.execution_time > 0:
                rate = result.total_data_points / result.execution_time
                self.stdout.write(f"   收集速度: {rate:.1f} 数据点/秒")
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ Wind数据收集失败!\n"
                f"   失败数: {result.failed_indicators}\n"
                f"   错误数: {len(result.errors)}"
            ))
            
            # 显示部分错误
            for error in result.errors[:3]:
                self.stdout.write(f"   - {error.get('indicator_code', 'Unknown')}: {error.get('error', 'Unknown error')}")

    def handle_status(self):
        """查看状态"""
        self.stdout.write("获取Wind集成状态...")
        
        status = wind_integration_service.get_integration_status()
        
        if 'error' in status:
            self.stdout.write(self.style.ERROR(f"❌ 获取状态失败: {status['error']}"))
            return
        
        # 显示指标统计
        wind_indicators = status.get('wind_indicators', {})
        self.stdout.write(self.style.SUCCESS("📊 Wind指标统计:"))
        self.stdout.write(f"   总指标数: {wind_indicators.get('total', 0)}")
        self.stdout.write(f"   活跃指标: {wind_indicators.get('active', 0)}")
        self.stdout.write(f"   API支持: {wind_indicators.get('supported_by_api', 0)}")
        
        # 显示数据统计
        data_points = status.get('data_points', {})
        self.stdout.write(self.style.SUCCESS("\n📈 数据统计:"))
        self.stdout.write(f"   总数据点: {data_points.get('total', 0):,}")
        self.stdout.write(f"   最新数据: {data_points.get('latest_date', 'N/A')}")
        
        # 显示质量统计
        quality = status.get('quality', {})
        self.stdout.write(self.style.SUCCESS("\n🔍 数据质量:"))
        self.stdout.write(f"   优秀: {quality.get('excellent', 0)}")
        self.stdout.write(f"   良好: {quality.get('good', 0)}")
        self.stdout.write(f"   一般: {quality.get('fair', 0)}")
        self.stdout.write(f"   较差: {quality.get('poor', 0)}")
        
        # 显示API统计
        api_stats = status.get('api_stats', {})
        self.stdout.write(self.style.SUCCESS("\n🔌 API统计:"))
        self.stdout.write(f"   总请求: {api_stats.get('total_requests', 0)}")
        self.stdout.write(f"   成功请求: {api_stats.get('successful_requests', 0)}")
        self.stdout.write(f"   失败请求: {api_stats.get('failed_requests', 0)}")
        self.stdout.write(f"   缓存命中: {api_stats.get('cache_hits', 0)}")
        self.stdout.write(f"   缓存未命中: {api_stats.get('cache_misses', 0)}")

    def handle_test(self, options):
        """测试连接"""
        username = options.get('username')
        password = options.get('password')
        
        self.stdout.write(f"测试Wind连接 (用户: {username})...")
        
        # 创建配置
        wind_config = WindConnectionConfig(
            username=username,
            password=password
        )
        
        # 更新服务配置
        wind_integration_service.wind_config = wind_config
        wind_integration_service.wind_collector.config = wind_config
        
        # 测试连接
        test_result = wind_integration_service.test_wind_connectivity()
        
        if test_result.get('connected', False):
            self.stdout.write(self.style.SUCCESS(
                f"✅ Wind连接成功!\n"
                f"   用户: {test_result.get('username', 'N/A')}\n"
                f"   状态: {test_result.get('status', 'N/A')}\n"
                f"   版本: {test_result.get('version', 'N/A')}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ Wind连接失败!\n"
                f"   错误: {test_result.get('error', 'Unknown error')}"
            ))

    def handle_clean(self, options):
        """清理数据"""
        if not options.get('confirm'):
            self.stdout.write(self.style.WARNING(
                "⚠️  此操作将删除所有Wind相关数据!\n"
                "   请使用 --confirm 参数确认删除操作"
            ))
            return
        
        self.stdout.write("开始清理Wind数据...")
        
        try:
            # 获取Wind指标
            wind_indicators = Indicator.objects.filter(source__contains='wind')
            indicator_count = wind_indicators.count()
            
            # 删除相关数据
            data_count = IndicatorData.objects.filter(indicator__in=wind_indicators).count()
            IndicatorData.objects.filter(indicator__in=wind_indicators).delete()
            
            # 删除指标
            wind_indicators.delete()
            
            self.stdout.write(self.style.SUCCESS(
                f"✅ Wind数据清理完成!\n"
                f"   删除指标: {indicator_count} 个\n"
                f"   删除数据点: {data_count:,} 个"
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ 清理失败: {str(e)}")) 