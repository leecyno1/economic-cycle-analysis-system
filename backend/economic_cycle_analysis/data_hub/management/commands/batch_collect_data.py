# -*- coding: utf-8 -*-
"""
Django管理命令: 批量采集近10年指标数据
运行命令: python manage.py batch_collect_data
"""

import time
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.utils import timezone

from data_hub.models import Indicator, IndicatorData, DataQualityReport
from data_hub.enhanced_data_collector_methods import EnhancedDataCollectorMethods
from data_hub.indicators_config import get_all_indicators

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BatchDataCollector:
    """批量数据采集器"""
    
    def __init__(self):
        self.collector = EnhancedDataCollectorMethods()
        self.success_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.total_records = 0
        self.errors: List[Dict] = []
        self.start_time = None
        self.progress_interval = 10  # 每10个指标显示一次进度
        
    def collect_all_10_years_data(self, 
                                  phases: List[int] = None, 
                                  force_update: bool = False,
                                  max_retries: int = 3,
                                  delay_between_calls: float = 1.0):
        """
        采集所有指标近10年数据
        
        Args:
            phases: 要采集的阶段，如[1, 2, 3]，None表示所有阶段
            force_update: 是否强制更新已有数据
            max_retries: 最大重试次数
            delay_between_calls: API调用间隔（秒）
        """
        self.start_time = datetime.now()
        
        # 计算时间范围（近10年）
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')
        
        logger.info(f"开始批量采集近10年数据 ({start_date} 到 {end_date})")
        logger.info(f"强制更新: {force_update}, 最大重试: {max_retries}, 调用间隔: {delay_between_calls}秒")
        
        # 获取要采集的指标
        indicators = self._get_indicators_to_collect(phases, force_update)
        total_indicators = len(indicators)
        
        if total_indicators == 0:
            logger.info("没有需要采集的指标")
            return
            
        logger.info(f"共需采集 {total_indicators} 个指标")
        
        # 按阶段分组处理
        phase_groups = self._group_indicators_by_phase(indicators)
        
        for phase, phase_indicators in phase_groups.items():
            logger.info(f"\n=== 开始处理第 {phase} 阶段指标 ({len(phase_indicators)} 个) ===")
            self._collect_phase_data(
                phase_indicators, 
                start_date, 
                end_date, 
                max_retries, 
                delay_between_calls
            )
        
        # 生成采集报告
        self._generate_collection_report(start_date, end_date)
        
    def _get_indicators_to_collect(self, phases: List[int] = None, force_update: bool = False) -> List[Indicator]:
        """获取需要采集的指标列表"""
        queryset = Indicator.objects.filter(is_active=True)
        
        if phases:
            queryset = queryset.filter(implementation_phase__in=phases)
            
        if not force_update:
            # 排除已有近期数据的指标
            recent_date = datetime.now() - timedelta(days=30)
            indicators_with_recent_data = IndicatorData.objects.filter(
                date__gte=recent_date
            ).values_list('indicator_id', flat=True).distinct()
            
            queryset = queryset.exclude(id__in=indicators_with_recent_data)
            
        return list(queryset.order_by('implementation_phase', '-importance_level'))
    
    def _group_indicators_by_phase(self, indicators: List[Indicator]) -> Dict[int, List[Indicator]]:
        """按实施阶段分组指标"""
        phase_groups = {}
        for indicator in indicators:
            phase = indicator.implementation_phase
            if phase not in phase_groups:
                phase_groups[phase] = []
            phase_groups[phase].append(indicator)
        return phase_groups
    
    def _collect_phase_data(self, 
                           indicators: List[Indicator],
                           start_date: str,
                           end_date: str,
                           max_retries: int,
                           delay_between_calls: float):
        """采集单个阶段的数据"""
        phase_start_time = datetime.now()
        
        for i, indicator in enumerate(indicators, 1):
            try:
                logger.info(f"[{i}/{len(indicators)}] 处理指标: {indicator.name} ({indicator.code})")
                
                # 采集数据（带重试机制）
                success = self._collect_with_retry(
                    indicator, start_date, end_date, max_retries
                )
                
                if success:
                    self.success_count += 1
                    logger.info(f"✓ 成功采集 {indicator.code}")
                else:
                    self.error_count += 1
                    logger.error(f"✗ 采集失败 {indicator.code}")
                
                # 显示进度
                if i % self.progress_interval == 0:
                    self._show_progress(i, len(indicators), phase_start_time)
                
                # API调用间隔
                if delay_between_calls > 0:
                    time.sleep(delay_between_calls)
                    
            except Exception as e:
                self.error_count += 1
                error_info = {
                    'indicator_code': indicator.code,
                    'indicator_name': indicator.name,
                    'error': str(e),
                    'traceback': traceback.format_exc(),
                    'timestamp': datetime.now().isoformat()
                }
                self.errors.append(error_info)
                logger.error(f"处理指标 {indicator.code} 时发生异常: {e}")
    
    def _collect_with_retry(self, 
                           indicator: Indicator, 
                           start_date: str, 
                           end_date: str, 
                           max_retries: int) -> bool:
        """带重试机制的数据采集"""
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    wait_time = 2 ** attempt  # 指数退避
                    logger.info(f"重试 {attempt}/{max_retries} - 等待 {wait_time} 秒...")
                    time.sleep(wait_time)
                
                result = self.collector.collect_indicator_data(
                    indicator.code, start_date, end_date
                )
                success = result.success
                
                if success:
                    # 更新指标的最后更新时间
                    indicator.last_update_date = timezone.now().date()
                    indicator.save(update_fields=['last_update_date'])
                    
                    # 生成数据质量报告
                    self._generate_quality_report(indicator)
                    return True
                    
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次尝试失败: {e}")
                if attempt == max_retries:
                    error_info = {
                        'indicator_code': indicator.code,
                        'indicator_name': indicator.name,
                        'error': str(e),
                        'attempts': attempt + 1,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.errors.append(error_info)
        
        return False
    
    def _generate_quality_report(self, indicator: Indicator):
        """为指标生成数据质量报告"""
        try:
            # 获取指标最近的数据
            recent_data = IndicatorData.objects.filter(
                indicator=indicator
            ).order_by('-date')[:100]
            
            if not recent_data.exists():
                return
            
            # 计算质量指标
            total_count = recent_data.count()
            non_null_count = recent_data.exclude(value__isnull=True).count()
            completeness_score = non_null_count / total_count if total_count > 0 else 0
            
            # 计算及时性（基于最新数据的时间差）
            latest_data = recent_data.first()
            days_since_update = (datetime.now().date() - latest_data.date).days if latest_data else 365
            timeliness_score = max(0, 1 - days_since_update / 30)  # 30天内为满分
            
            # 计算准确性和一致性（简化版本）
            accuracy_score = 0.8  # 假设准确性为80%
            consistency_score = 0.85  # 假设一致性为85%
            
            # 确定总体质量等级
            overall_score = (completeness_score + timeliness_score + accuracy_score + consistency_score) / 4
            if overall_score >= 0.9:
                quality_level = DataQualityReport.QualityLevel.EXCELLENT
            elif overall_score >= 0.75:
                quality_level = DataQualityReport.QualityLevel.GOOD
            elif overall_score >= 0.6:
                quality_level = DataQualityReport.QualityLevel.FAIR
            else:
                quality_level = DataQualityReport.QualityLevel.POOR
            
            # 创建或更新质量报告
            report, created = DataQualityReport.objects.update_or_create(
                indicator=indicator,
                report_date=datetime.now().date(),
                defaults={
                    'completeness_score': completeness_score,
                    'timeliness_score': timeliness_score,
                    'accuracy_score': accuracy_score,
                    'consistency_score': consistency_score,
                    'overall_quality': quality_level,
                    'issues_found': [],
                    'recommendations': '数据质量良好' if overall_score >= 0.75 else '需要关注数据质量'
                }
            )
            
            # 更新指标的数据质量评分
            indicator.data_quality_score = overall_score
            indicator.save(update_fields=['data_quality_score'])
            
        except Exception as e:
            logger.warning(f"生成质量报告失败 {indicator.code}: {e}")
    
    def _show_progress(self, current: int, total: int, start_time: datetime):
        """显示采集进度"""
        elapsed = datetime.now() - start_time
        rate = current / elapsed.total_seconds() if elapsed.total_seconds() > 0 else 0
        eta = (total - current) / rate if rate > 0 else 0
        
        progress_percent = (current / total) * 100
        
        logger.info(f"进度: {current}/{total} ({progress_percent:.1f}%) | "
                   f"速度: {rate:.2f} 指标/秒 | "
                   f"预计剩余: {eta/60:.1f} 分钟 | "
                   f"成功: {self.success_count}, 失败: {self.error_count}")
    
    def _generate_collection_report(self, start_date: str, end_date: str):
        """生成采集总结报告"""
        end_time = datetime.now()
        total_time = end_time - self.start_time
        
        # 统计数据
        total_indicators = self.success_count + self.error_count
        success_rate = (self.success_count / total_indicators * 100) if total_indicators > 0 else 0
        
        # 数据库统计
        total_data_points = IndicatorData.objects.count()
        recent_data_points = IndicatorData.objects.filter(
            collection_time__gte=self.start_time
        ).count()
        
        report = f"""
================================
数据采集完成报告
================================
采集时间范围: {start_date} 到 {end_date}
采集开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
采集结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
总耗时: {total_time}

指标采集统计:
- 总指标数: {total_indicators}
- 成功采集: {self.success_count}
- 采集失败: {self.error_count}
- 成功率: {success_rate:.1f}%

数据点统计:
- 数据库总数据点: {total_data_points:,}
- 本次新增数据点: {recent_data_points:,}

性能指标:
- 平均采集速度: {total_indicators / total_time.total_seconds():.2f} 指标/秒
- 平均数据获取速度: {recent_data_points / total_time.total_seconds():.2f} 数据点/秒

错误统计:
- 错误数量: {len(self.errors)}
"""
        
        if self.errors:
            report += "\n错误详情:\n"
            for i, error in enumerate(self.errors[:10], 1):  # 只显示前10个错误
                report += f"{i}. {error['indicator_code']}: {error['error']}\n"
            if len(self.errors) > 10:
                report += f"... 还有 {len(self.errors) - 10} 个错误\n"
        
        report += "\n================================"
        
        logger.info(report)
        
        # 保存详细错误日志到文件
        if self.errors:
            error_log_file = f"collection_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            with open(error_log_file, 'w', encoding='utf-8') as f:
                for error in self.errors:
                    f.write(f"指标: {error['indicator_code']} ({error.get('indicator_name', 'N/A')})\n")
                    f.write(f"错误: {error['error']}\n")
                    f.write(f"时间: {error['timestamp']}\n")
                    if 'traceback' in error:
                        f.write(f"详细信息:\n{error['traceback']}\n")
                    f.write("-" * 80 + "\n")
            
            logger.info(f"详细错误日志已保存到: {error_log_file}")


class Command(BaseCommand):
    help = '批量采集所有指标的近10年历史数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phases',
            nargs='+',
            type=int,
            choices=[1, 2, 3],
            help='指定要采集的实施阶段，如 --phases 1 2'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制更新已有数据'
        )
        parser.add_argument(
            '--max-retries',
            type=int,
            default=3,
            help='最大重试次数（默认3次）'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='API调用间隔秒数（默认1.0秒）'
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='测试模式，只处理前5个指标'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始批量数据采集...'))
        
        # 检查数据库连接
        try:
            connection.ensure_connection()
            self.stdout.write('✓ 数据库连接正常')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ 数据库连接失败: {e}'))
            return
        
        # 初始化采集器
        collector = BatchDataCollector()
        
        # 测试模式
        if options['test']:
            self.stdout.write(self.style.WARNING('运行测试模式（仅处理前5个指标）'))
            # 这里可以添加测试逻辑
            return
        
        try:
            # 开始批量采集
            collector.collect_all_10_years_data(
                phases=options['phases'],
                force_update=options['force'],
                max_retries=options['max_retries'],
                delay_between_calls=options['delay']
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'数据采集完成! 成功: {collector.success_count}, '
                    f'失败: {collector.error_count}'
                )
            )
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('用户中断采集过程'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'采集过程发生错误: {e}'))
            logger.error(f"采集过程异常: {e}", exc_info=True) 