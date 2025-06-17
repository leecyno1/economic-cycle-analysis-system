# -*- coding: utf-8 -*-
"""
Wind数据源集成服务
统一管理Wind数据的采集、更新、监控和质量评估
与现有的1064指标体系无缝集成
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json

from django.db import transaction, IntegrityError
from django.utils import timezone
from django.core.cache import cache

from .models import Indicator, IndicatorData, DataQualityReport, IndicatorCategory
from .wind_data_collector import WindDataCollector, WindConnectionConfig, WindCollectionResult
from .indicators_config import get_all_indicators

# 配置日志
logger = logging.getLogger(__name__)


@dataclass
class WindIntegrationConfig:
    """Wind集成配置"""
    auto_create_indicators: bool = True
    quality_check_enabled: bool = True
    cache_enabled: bool = True
    batch_size: int = 50
    retry_count: int = 3
    data_validation: bool = True


@dataclass
class WindIntegrationResult:
    """Wind集成结果"""
    success: bool
    total_indicators: int = 0
    successful_indicators: int = 0
    failed_indicators: int = 0
    total_data_points: int = 0
    errors: List[Dict] = None
    execution_time: float = 0.0
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class WindIntegrationService:
    """Wind数据源集成服务"""
    
    def __init__(self, wind_config: WindConnectionConfig = None, 
                 integration_config: WindIntegrationConfig = None):
        self.wind_config = wind_config or WindConnectionConfig()
        self.integration_config = integration_config or WindIntegrationConfig()
        self.wind_collector = WindDataCollector(self.wind_config)
        
        # 缓存键前缀
        self.cache_prefix = "wind_integration"
        
        # 统计计数器
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def initialize_wind_indicators(self) -> WindIntegrationResult:
        """初始化Wind指标到数据库"""
        start_time = datetime.now()
        result = WindIntegrationResult(success=False)
        
        try:
            logger.info("开始初始化Wind指标...")
            
            # 获取Wind指标映射
            wind_mappings = self.wind_collector.wind_mappings
            result.total_indicators = len(wind_mappings)
            
            created_count = 0
            updated_count = 0
            
            for indicator_code, config in wind_mappings.items():
                try:
                    # 使用新的创建或更新方法
                    success = self._create_or_update_indicator(indicator_code, config)
                    
                    if success:
                        result.successful_indicators += 1
                        # 检查是否是新创建的
                        try:
                            indicator = Indicator.objects.get(code=indicator_code)
                            if indicator.created_at.date() == timezone.now().date():
                                created_count += 1
                                logger.info(f"创建新指标: {indicator_code}")
                            else:
                                updated_count += 1
                                logger.info(f"更新指标: {indicator_code}")
                        except:
                            updated_count += 1
                    else:
                        result.failed_indicators += 1
                    
                except Exception as e:
                    result.failed_indicators += 1
                    error_info = {
                        'indicator_code': indicator_code,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }
                    result.errors.append(error_info)
                    logger.error(f"处理指标 {indicator_code} 时出错: {e}")
            
            result.success = result.failed_indicators == 0
            result.execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Wind指标初始化完成: 创建 {created_count} 个, 更新 {updated_count} 个")
            
        except Exception as e:
            logger.error(f"Wind指标初始化失败: {e}")
            result.errors.append({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        return result
    
    def collect_wind_data_batch(self, 
                               indicator_codes: List[str] = None,
                               start_date: str = None,
                               end_date: str = None,
                               force_update: bool = False) -> WindIntegrationResult:
        """批量收集Wind数据"""
        start_time = datetime.now()
        result = WindIntegrationResult(success=False)
        
        try:
            # 连接Wind数据库
            if not self.wind_collector.connect():
                raise Exception("无法连接到Wind数据库")
            
            # 确定要收集的指标
            if indicator_codes is None:
                indicator_codes = list(self.wind_collector.wind_mappings.keys())
            
            result.total_indicators = len(indicator_codes)
            
            # 确定时间范围
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            logger.info(f"开始批量收集Wind数据: {len(indicator_codes)} 个指标, 时间范围: {start_date} ~ {end_date}")
            
            # 分批处理
            batch_size = self.integration_config.batch_size
            for i in range(0, len(indicator_codes), batch_size):
                batch_codes = indicator_codes[i:i + batch_size]
                batch_result = self._process_indicator_batch(
                    batch_codes, start_date, end_date, force_update
                )
                
                # 累积结果
                result.successful_indicators += batch_result.successful_indicators
                result.failed_indicators += batch_result.failed_indicators
                result.total_data_points += batch_result.total_data_points
                result.errors.extend(batch_result.errors)
                
                logger.info(f"批次 {i//batch_size + 1} 完成: {batch_result.successful_indicators}/{len(batch_codes)} 成功")
            
            result.success = result.failed_indicators == 0
            result.execution_time = (datetime.now() - start_time).total_seconds()
            
            # 生成数据质量报告
            if self.integration_config.quality_check_enabled:
                self._generate_batch_quality_report(indicator_codes, start_date, end_date)
            
        except Exception as e:
            logger.error(f"批量收集Wind数据失败: {e}")
            result.errors.append({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        finally:
            # 断开Wind连接
            self.wind_collector.disconnect()
        
        return result
    
    def _process_indicator_batch(self, 
                                indicator_codes: List[str],
                                start_date: str,
                                end_date: str,
                                force_update: bool) -> WindIntegrationResult:
        """处理指标批次"""
        batch_result = WindIntegrationResult(success=True)
        
        for indicator_code in indicator_codes:
            try:
                # 检查缓存
                if not force_update and self.integration_config.cache_enabled:
                    cache_key = f"{self.cache_prefix}:{indicator_code}:{start_date}:{end_date}"
                    cached_result = cache.get(cache_key)
                    if cached_result:
                        self.stats['cache_hits'] += 1
                        batch_result.successful_indicators += 1
                        continue
                    else:
                        self.stats['cache_misses'] += 1
                
                # 收集数据
                collection_result = self.wind_collector.collect_indicator_data(
                    indicator_code, start_date, end_date
                )
                
                if collection_result.success:
                    batch_result.successful_indicators += 1
                    batch_result.total_data_points += collection_result.records_count
                    
                    # 缓存结果
                    if self.integration_config.cache_enabled:
                        cache_key = f"{self.cache_prefix}:{indicator_code}:{start_date}:{end_date}"
                        cache.set(cache_key, True, timeout=3600)  # 缓存1小时
                    
                    logger.debug(f"成功收集 {indicator_code}: {collection_result.records_count} 条数据")
                else:
                    batch_result.failed_indicators += 1
                    batch_result.errors.append({
                        'indicator_code': indicator_code,
                        'error': collection_result.error_message,
                        'wind_code': collection_result.wind_code,
                        'timestamp': datetime.now().isoformat()
                    })
                    logger.warning(f"收集失败 {indicator_code}: {collection_result.error_message}")
                
                self.stats['total_requests'] += 1
                if collection_result.success:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
                
            except Exception as e:
                batch_result.failed_indicators += 1
                batch_result.errors.append({
                    'indicator_code': indicator_code,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                logger.error(f"处理指标 {indicator_code} 时出错: {e}")
        
        return batch_result
    
    def sync_with_existing_indicators(self) -> WindIntegrationResult:
        """与现有1064指标体系同步"""
        start_time = datetime.now()
        result = WindIntegrationResult(success=False)
        
        try:
            logger.info("开始与现有指标体系同步...")
            
            # 获取现有指标
            existing_indicators = get_all_indicators()
            wind_mappings = self.wind_collector.wind_mappings
            
            sync_count = 0
            create_count = 0
            
            # 检查现有指标是否有对应的Wind数据源
            for indicator_config in existing_indicators:
                indicator_code = indicator_config['code']
                
                # 寻找匹配的Wind指标
                matched_wind_code = self._find_matching_wind_indicator(indicator_config)
                
                if matched_wind_code:
                    try:
                        # 更新指标的数据源信息
                        indicator = Indicator.objects.get(code=indicator_code)
                        
                        # 添加Wind作为辅助数据源
                        if 'wind' not in indicator.source:
                            indicator.source = f"{indicator.source},wind"
                            indicator.calculation_method += f" | Wind API: {matched_wind_code}"
                            indicator.save(update_fields=['source', 'calculation_method'])
                            sync_count += 1
                            logger.info(f"同步指标 {indicator_code} 到Wind数据源")
                    
                    except Indicator.DoesNotExist:
                        logger.warning(f"指标 {indicator_code} 在数据库中不存在")
            
            # 为没有对应现有指标的Wind指标创建新记录
            existing_codes = {config['code'] for config in existing_indicators}
            for wind_code in wind_mappings.keys():
                if wind_code not in existing_codes:
                    # 创建新的Wind指标
                    wind_config = wind_mappings[wind_code]
                    try:
                        wind_category = self._get_or_create_wind_category()
                        
                        Indicator.objects.create(
                            code=wind_code,
                            name=wind_config['description'],
                            description=f"Wind专属指标: {wind_config['description']}",
                            category=wind_category,
                            frequency=wind_config['frequency'],
                            unit=self._determine_unit(wind_config),
                            source='wind',
                            implementation_phase=2,  # 作为扩展指标
                            importance_level=3,
                            dimension=wind_config.get('dimension', '基本面'),
                            industry=wind_config.get('industry', '未分类'),
                            calculation_method=f"Wind API: {wind_config['wind_code']}",
                            data_type=wind_config['data_type'],
                            is_active=True
                        )
                        create_count += 1
                        logger.info(f"创建Wind专属指标: {wind_code}")
                        
                    except IntegrityError:
                        logger.warning(f"Wind指标 {wind_code} 已存在")
            
            result.successful_indicators = sync_count + create_count
            result.success = True
            result.execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"指标同步完成: 同步 {sync_count} 个, 创建 {create_count} 个")
            
        except Exception as e:
            logger.error(f"指标同步失败: {e}")
            result.errors.append({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        return result
    
    def _find_matching_wind_indicator(self, indicator_config: Dict) -> Optional[str]:
        """为现有指标寻找匹配的Wind数据源"""
        indicator_name = indicator_config.get('name', '').lower()
        indicator_desc = indicator_config.get('description', '').lower()
        
        # 关键词匹配规则
        matching_rules = {
            'cpi': 'WIND_CPI_YOY',
            'ppi': 'WIND_PPI_YOY',
            'gdp': 'WIND_GDP_YOY',
            'pmi': 'WIND_PMI_MFG',
            'm2': 'WIND_M2_YOY',
            '沪深300': 'WIND_CSI300',
            '上证': 'WIND_SSE_COMP',
            '深证': 'WIND_SZSE_COMP',
            '创业板': 'WIND_GEM',
            '国债': 'WIND_10Y_TREASURY',
            'shibor': 'WIND_SHIBOR_1M',
            '原油': 'WIND_CRUDE_OIL',
            '铜': 'WIND_COPPER',
            '美元': 'WIND_USD_CNY',
            '欧元': 'WIND_EUR_CNY',
            '房价': 'WIND_HOUSE_PRICE_70',
            '出口': 'WIND_EXPORT_YOY',
            '进口': 'WIND_IMPORT_YOY',
            '工业增加值': 'WIND_INDUSTRIAL_PROD',
            '消费': 'WIND_RETAIL_SALES',
            '固定资产投资': 'WIND_FAI_YTD',
            '失业率': 'WIND_URBAN_UNEMPLOYMENT'
        }
        
        # 检查匹配
        for keyword, wind_code in matching_rules.items():
            if keyword in indicator_name or keyword in indicator_desc:
                return self.wind_collector.wind_mappings[wind_code]['wind_code']
        
        return None
    
    def _get_or_create_wind_category(self) -> IndicatorCategory:
        """获取或创建Wind分类"""
        category, created = IndicatorCategory.objects.get_or_create(
            code='wind',
            defaults={
                'name': 'Wind数据源',
                'description': 'Wind金融终端数据源指标',
                'parent': None,
                'level': 1,
                'sort_order': 100
            }
        )
        return category
    
    def _determine_unit(self, config: Dict) -> str:
        """确定指标单位"""
        description = config.get('description', '').lower()
        
        if '%' in description or '同比' in description or '环比' in description:
            return '%'
        elif '指数' in description:
            return '点'
        elif '价格' in description:
            return '元'
        elif '汇率' in description:
            return ''
        elif '万亿' in description:
            return '万亿元'
        elif '亿' in description:
            return '亿元'
        else:
            return ''
    
    def _determine_importance(self, config: Dict) -> int:
        """确定指标重要性级别"""
        data_type = config.get('data_type', '')
        
        if data_type in ['macro', 'index']:
            return 1  # 高重要性
        elif data_type in ['bond', 'commodity', 'fx']:
            return 2  # 中重要性
        else:
            return 3  # 低重要性
    
    def _generate_batch_quality_report(self, 
                                     indicator_codes: List[str],
                                     start_date: str,
                                     end_date: str):
        """生成批量质量报告"""
        try:
            logger.info("生成Wind数据质量报告...")
            
            for indicator_code in indicator_codes:
                try:
                    indicator = Indicator.objects.get(code=indicator_code)
                    
                    # 获取数据
                    data_count = IndicatorData.objects.filter(
                        indicator=indicator,
                        date__gte=start_date,
                        date__lte=end_date
                    ).count()
                    
                    if data_count > 0:
                        # 计算质量评分
                        completeness_score = min(1.0, data_count / 365)  # 假设期望每日数据
                        timeliness_score = 1.0  # Wind数据通常很及时
                        accuracy_score = 0.95  # Wind数据准确性很高
                        consistency_score = 0.9  # 一致性较好
                        
                        overall_score = (completeness_score + timeliness_score + 
                                       accuracy_score + consistency_score) / 4
                        
                        # 确定质量等级
                        if overall_score >= 0.9:
                            quality_level = DataQualityReport.QualityLevel.EXCELLENT
                        elif overall_score >= 0.75:
                            quality_level = DataQualityReport.QualityLevel.GOOD
                        elif overall_score >= 0.6:
                            quality_level = DataQualityReport.QualityLevel.FAIR
                        else:
                            quality_level = DataQualityReport.QualityLevel.POOR
                        
                        # 创建质量报告
                        DataQualityReport.objects.update_or_create(
                            indicator=indicator,
                            report_date=timezone.now().date(),
                            defaults={
                                'completeness_score': completeness_score,
                                'timeliness_score': timeliness_score,
                                'accuracy_score': accuracy_score,
                                'consistency_score': consistency_score,
                                'overall_quality': quality_level,
                                'issues_found': [],
                                'recommendations': 'Wind数据质量优秀' if overall_score >= 0.8 else '数据质量需要关注'
                            }
                        )
                        
                        # 更新指标质量评分
                        indicator.data_quality_score = overall_score
                        indicator.save(update_fields=['data_quality_score'])
                
                except Indicator.DoesNotExist:
                    logger.warning(f"指标 {indicator_code} 不存在，跳过质量报告")
                except Exception as e:
                    logger.error(f"生成指标 {indicator_code} 质量报告时出错: {e}")
        
        except Exception as e:
            logger.error(f"生成批量质量报告失败: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """获取集成状态"""
        try:
            # 统计Wind指标数量
            wind_indicators = Indicator.objects.filter(source__contains='wind')
            total_wind_indicators = wind_indicators.count()
            active_wind_indicators = wind_indicators.filter(is_active=True).count()
            
            # 统计Wind数据点
            wind_data_points = IndicatorData.objects.filter(
                indicator__in=wind_indicators
            ).count()
            
            # 最近数据时间
            latest_data = IndicatorData.objects.filter(
                indicator__in=wind_indicators
            ).order_by('-date').first()
            
            latest_date = latest_data.date if latest_data else None
            
            # 数据质量统计
            quality_reports = DataQualityReport.objects.filter(
                indicator__in=wind_indicators
            )
            
            quality_stats = {
                'excellent': quality_reports.filter(overall_quality='excellent').count(),
                'good': quality_reports.filter(overall_quality='good').count(),
                'fair': quality_reports.filter(overall_quality='fair').count(),
                'poor': quality_reports.filter(overall_quality='poor').count()
            }
            
            return {
                'wind_indicators': {
                    'total': total_wind_indicators,
                    'active': active_wind_indicators,
                    'supported_by_api': len(self.wind_collector.wind_mappings)
                },
                'data_points': {
                    'total': wind_data_points,
                    'latest_date': latest_date.isoformat() if latest_date else None
                },
                'quality': quality_stats,
                'api_stats': self.stats,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取集成状态失败: {e}")
            return {'error': str(e)}
    
    def test_wind_connectivity(self) -> Dict[str, Any]:
        """测试Wind连接"""
        return self.wind_collector.test_connection()

    def _create_or_update_indicator(self, indicator_code: str, indicator_info: Dict[str, Any]) -> bool:
        """创建或更新指标"""
        try:
            # 映射Wind指标信息到模型字段
            mapped_data = self._map_wind_indicator_to_model(indicator_info)
            
            # 获取或创建指标分类
            category, _ = IndicatorCategory.objects.get_or_create(
                code=mapped_data.get('category_code', 'WIND'),
                defaults={
                    'name': mapped_data.get('category_name', 'Wind数据源'),
                    'description': 'Wind金融终端数据源指标',
                    'level': 1,
                    'is_active': True
                }
            )
            
            # 创建或更新指标
            indicator, created = Indicator.objects.update_or_create(
                code=indicator_code,
                defaults={
                    'name': mapped_data['name'],
                    'name_en': mapped_data.get('name_en'),
                    'description': mapped_data.get('description'),
                    'category': category,
                    'sub_category': mapped_data.get('sub_category'),
                    'sector': mapped_data.get('sector'),
                    'industry': mapped_data.get('industry'),
                    'frequency': mapped_data.get('frequency', 'M'),
                    'lead_lag_status': mapped_data.get('lead_lag_status', 'SYNC'),
                    'unit': mapped_data.get('unit'),
                    'source': f"wind:{mapped_data.get('wind_code', '')}",
                    'api_function': mapped_data.get('api_function'),
                    'data_availability': mapped_data.get('data_availability', 'medium'),
                    'importance_level': mapped_data.get('importance_level', 3),
                    'implementation_phase': mapped_data.get('implementation_phase', 2),
                    'investment_significance': mapped_data.get('investment_significance'),
                    'is_active': True,
                    'metadata': {
                        'wind_code': mapped_data.get('wind_code'),
                        'data_type': mapped_data.get('data_type'),
                        'original_dimension': mapped_data.get('dimension'),
                        'wind_integration_version': '1.0'
                    },
                    # 设置维度字段
                    **self._get_dimension_mapping(mapped_data.get('dimension'))
                }
            )
            
            action = "创建" if created else "更新"
            logger.info(f"{action}指标: {indicator_code}")
            return True
            
        except Exception as e:
            logger.error(f"处理指标 {indicator_code} 时出错: {str(e)}")
            return False

    def _map_wind_indicator_to_model(self, indicator_info: Dict[str, Any]) -> Dict[str, Any]:
        """将Wind指标信息映射到模型字段"""
        # 基础映射
        mapped_data = {
            'name': indicator_info.get('description', ''),
            'name_en': indicator_info.get('name_en'),
            'description': indicator_info.get('description', ''),
            'wind_code': indicator_info.get('wind_code'),
            'data_type': indicator_info.get('data_type', 'macro'),
            'dimension': indicator_info.get('dimension', '景气指数'),
            'frequency': self._map_frequency(indicator_info.get('frequency', 'M')),
            'unit': indicator_info.get('unit'),
            'industry': indicator_info.get('industry', '宏观经济'),
        }
        
        # 根据data_type设置分类信息
        data_type = indicator_info.get('data_type', 'macro')
        if data_type == 'macro':
            mapped_data.update({
                'category_code': 'MACRO',
                'category_name': '宏观经济指标',
                'sector': '宏观经济',
                'lead_lag_status': 'LEAD',
                'importance_level': 4
            })
        elif data_type == 'market':
            mapped_data.update({
                'category_code': 'MARKET',
                'category_name': '市场指标',
                'sector': '金融市场',
                'lead_lag_status': 'SYNC',
                'importance_level': 3
            })
        elif data_type == 'industry':
            mapped_data.update({
                'category_code': 'INDUSTRY',
                'category_name': '行业指标',
                'sector': indicator_info.get('industry', '行业'),
                'lead_lag_status': 'SYNC',
                'importance_level': 3
            })
        elif data_type == 'commodity':
            mapped_data.update({
                'category_code': 'COMMODITY',
                'category_name': '大宗商品',
                'sector': '大宗商品',
                'lead_lag_status': 'LEAD',
                'importance_level': 3
            })
        else:
            mapped_data.update({
                'category_code': 'WIND_OTHER',
                'category_name': 'Wind其他指标',
                'sector': '其他',
                'lead_lag_status': 'SYNC',
                'importance_level': 2
            })
        
        return mapped_data

    def _get_dimension_mapping(self, dimension: str) -> Dict[str, bool]:
        """将维度名称映射到模型的布尔字段"""
        dimension_mapping = {
            '景气指数': {'dimension_prosperity': True},
            '景气度': {'dimension_prosperity': True},
            '估值': {'dimension_valuation': True},
            '拥挤度': {'dimension_crowdedness': True},
            '技术面': {'dimension_technical': True},
            '基本面': {'dimension_fundamental': True},
            '动量': {'dimension_momentum': True},
            '情绪': {'dimension_sentiment': True},
            '流动性': {'dimension_liquidity': True},
            '波动率': {'dimension_volatility': True},
            '相关性': {'dimension_correlation': True},
            '季节性': {'dimension_seasonality': True},
            '政策敏感度': {'dimension_policy': True},
            '供应链': {'dimension_supply_chain': True},
            '创新': {'dimension_innovation': True},
            'ESG': {'dimension_esg': True},
            '风险': {'dimension_risk': True},
        }
        
        # 默认返回空字典（所有维度为False）
        result = {}
        
        # 如果找到匹配的维度，设置对应字段为True
        if dimension and dimension in dimension_mapping:
            result.update(dimension_mapping[dimension])
        else:
            # 如果没有找到匹配，默认设置为景气度维度
            result['dimension_prosperity'] = True
            
        return result

    def _map_frequency(self, wind_frequency: str) -> str:
        """映射频率代码"""
        frequency_mapping = {
            'D': 'D',  # 日度
            'W': 'W',  # 周度
            'M': 'M',  # 月度
            'Q': 'Q',  # 季度
            'Y': 'Y',  # 年度
            'A': 'Y',  # 年度（另一种表示）
        }
        
        return frequency_mapping.get(wind_frequency, 'M')


# 全局Wind集成服务实例
wind_integration_service = WindIntegrationService() 