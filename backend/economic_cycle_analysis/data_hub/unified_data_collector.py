# -*- coding: utf-8 -*-
"""
统一数据收集器
集成AkShare和Wind数据源，提供统一的数据采集接口
支持智能数据源选择和优先级策略
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from django.db import transaction, IntegrityError
from django.utils import timezone
from .models import Indicator, IndicatorData, DataQualityReport

# 导入各数据源收集器
from .enhanced_data_collector import EnhancedDataCollector, CollectionResult
from .wind_data_collector import WindDataCollector, WindConnectionConfig, WindCollectionResult

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSource(Enum):
    """数据源枚举"""
    AKSHARE = "akshare"
    WIND = "wind"
    AUTO = "auto"  # 自动选择


@dataclass
class UnifiedCollectionResult:
    """统一数据采集结果"""
    success: bool
    records_count: int = 0
    error_message: str = ""
    data_range: Tuple[str, str] = ("", "")
    data_source: str = ""
    api_function: str = ""
    wind_code: str = ""
    akshare_function: str = ""


class UnifiedDataCollector:
    """统一数据收集器"""
    
    def __init__(self, wind_config: WindConnectionConfig = None):
        # 初始化各数据源收集器
        self.akshare_collector = EnhancedDataCollector()
        self.wind_collector = WindDataCollector(wind_config) if wind_config else None
        
        # 数据源优先级策略
        self.source_priority = self._build_source_priority()
        
        # 支持的指标映射
        self.unified_mappings = self._build_unified_mappings()
    
    def _build_source_priority(self) -> Dict[str, List[DataSource]]:
        """构建数据源优先级策略"""
        return {
            # 宏观经济指标：优先使用Wind，备选AkShare
            'macro': [DataSource.WIND, DataSource.AKSHARE],
            
            # 股票指数：优先使用Wind
            'index': [DataSource.WIND, DataSource.AKSHARE],
            'industry': [DataSource.WIND, DataSource.AKSHARE],
            'us_index': [DataSource.WIND, DataSource.AKSHARE],
            
            # 债券利率：优先使用Wind
            'bond': [DataSource.WIND, DataSource.AKSHARE],
            
            # 商品期货：优先使用Wind
            'commodity': [DataSource.WIND, DataSource.AKSHARE],
            
            # 外汇：优先使用Wind
            'fx': [DataSource.WIND, DataSource.AKSHARE],
            
            # 默认：自动选择
            'default': [DataSource.WIND, DataSource.AKSHARE]
        }
    
    def _build_unified_mappings(self) -> Dict[str, Dict]:
        """构建统一指标映射"""
        unified_mappings = {}
        
        # 添加AkShare映射
        if hasattr(self.akshare_collector, 'akshare_mappings'):
            for code, config in self.akshare_collector.akshare_mappings.items():
                unified_mappings[code] = {
                    'sources': {DataSource.AKSHARE: config},
                    'primary_source': DataSource.AKSHARE,
                    'data_type': config.get('data_type', 'unknown')
                }
        
        # 添加Wind映射
        if self.wind_collector and hasattr(self.wind_collector, 'wind_mappings'):
            for code, config in self.wind_collector.wind_mappings.items():
                if code in unified_mappings:
                    # 如果已存在，添加Wind作为备选数据源
                    unified_mappings[code]['sources'][DataSource.WIND] = config
                else:
                    # 新增Wind指标
                    unified_mappings[code] = {
                        'sources': {DataSource.WIND: config},
                        'primary_source': DataSource.WIND,
                        'data_type': config.get('data_type', 'unknown')
                    }
        
        # 设置数据源优先级
        for code, mapping in unified_mappings.items():
            data_type = mapping['data_type']
            priority = self.source_priority.get(data_type, self.source_priority['default'])
            
            # 根据优先级和可用性确定主数据源
            for source in priority:
                if source in mapping['sources']:
                    mapping['primary_source'] = source
                    break
        
        return unified_mappings
    
    def collect_indicator_data(self, 
                             indicator_code: str, 
                             start_date: str = None, 
                             end_date: str = None,
                             data_source: DataSource = DataSource.AUTO) -> UnifiedCollectionResult:
        """
        统一数据采集接口
        
        Args:
            indicator_code: 指标代码
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            data_source: 指定数据源，默认自动选择
            
        Returns:
            UnifiedCollectionResult: 采集结果
        """
        try:
            # 从数据库获取指标信息
            indicator = Indicator.objects.get(code=indicator_code)
            logger.info(f"开始统一采集指标: {indicator.name} ({indicator_code})")
            
            # 获取指标映射配置
            if indicator_code not in self.unified_mappings:
                return UnifiedCollectionResult(
                    success=False,
                    error_message=f"未找到指标 {indicator_code} 的数据源映射配置"
                )
            
            mapping = self.unified_mappings[indicator_code]
            
            # 确定数据源
            if data_source == DataSource.AUTO:
                # 自动选择主数据源
                selected_source = mapping['primary_source']
            else:
                # 使用指定数据源
                if data_source not in mapping['sources']:
                    return UnifiedCollectionResult(
                        success=False,
                        error_message=f"指标 {indicator_code} 不支持数据源 {data_source.value}"
                    )
                selected_source = data_source
            
            logger.info(f"选择数据源: {selected_source.value}")
            
            # 尝试主数据源
            result = self._collect_from_source(
                indicator_code, selected_source, start_date, end_date
            )
            
            if result.success:
                return result
            
            # 如果主数据源失败，尝试备选数据源
            logger.warning(f"主数据源 {selected_source.value} 失败，尝试备选数据源")
            
            data_type = mapping['data_type']
            priority = self.source_priority.get(data_type, self.source_priority['default'])
            
            for backup_source in priority:
                if backup_source != selected_source and backup_source in mapping['sources']:
                    logger.info(f"尝试备选数据源: {backup_source.value}")
                    
                    result = self._collect_from_source(
                        indicator_code, backup_source, start_date, end_date
                    )
                    
                    if result.success:
                        return result
            
            # 所有数据源都失败
            return UnifiedCollectionResult(
                success=False,
                error_message=f"所有可用数据源都失败，指标: {indicator_code}"
            )
            
        except Exception as e:
            error_msg = f"统一采集指标 {indicator_code} 时出错: {str(e)}"
            logger.error(error_msg)
            return UnifiedCollectionResult(
                success=False,
                error_message=error_msg
            )
    
    def _collect_from_source(self, 
                           indicator_code: str, 
                           source: DataSource, 
                           start_date: str = None, 
                           end_date: str = None) -> UnifiedCollectionResult:
        """
        从指定数据源收集数据
        
        Args:
            indicator_code: 指标代码
            source: 数据源
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            UnifiedCollectionResult: 采集结果
        """
        try:
            if source == DataSource.AKSHARE:
                # 使用AkShare收集器
                akshare_result = self.akshare_collector.collect_indicator_data(
                    indicator_code, start_date, end_date
                )
                
                return UnifiedCollectionResult(
                    success=akshare_result.success,
                    records_count=akshare_result.records_count,
                    error_message=akshare_result.error_message,
                    data_range=akshare_result.data_range,
                    data_source="akshare",
                    akshare_function=akshare_result.api_function
                )
                
            elif source == DataSource.WIND:
                # 使用Wind收集器
                if not self.wind_collector:
                    return UnifiedCollectionResult(
                        success=False,
                        error_message="Wind收集器未初始化"
                    )
                
                wind_result = self.wind_collector.collect_indicator_data(
                    indicator_code, start_date, end_date
                )
                
                return UnifiedCollectionResult(
                    success=wind_result.success,
                    records_count=wind_result.records_count,
                    error_message=wind_result.error_message,
                    data_range=wind_result.data_range,
                    data_source="wind",
                    wind_code=wind_result.wind_code
                )
            
            else:
                return UnifiedCollectionResult(
                    success=False,
                    error_message=f"不支持的数据源: {source.value}"
                )
                
        except Exception as e:
            return UnifiedCollectionResult(
                success=False,
                error_message=f"从数据源 {source.value} 收集数据时出错: {str(e)}"
            )
    
    def get_supported_indicators(self) -> Dict[str, Dict]:
        """获取所有支持的指标信息"""
        supported = {}
        
        for code, mapping in self.unified_mappings.items():
            supported[code] = {
                'primary_source': mapping['primary_source'].value,
                'available_sources': [source.value for source in mapping['sources'].keys()],
                'data_type': mapping['data_type']
            }
        
        return supported
    
    def validate_indicator_support(self, indicator_code: str) -> Tuple[bool, str]:
        """验证指标是否支持"""
        if indicator_code in self.unified_mappings:
            mapping = self.unified_mappings[indicator_code]
            sources = [source.value for source in mapping['sources'].keys()]
            return True, f"支持数据源: {', '.join(sources)} (主: {mapping['primary_source'].value})"
        else:
            return False, f"不支持的指标代码: {indicator_code}"
    
    def get_data_source_statistics(self) -> Dict[str, Any]:
        """获取数据源统计信息"""
        stats = {
            'total_indicators': len(self.unified_mappings),
            'by_source': {},
            'by_data_type': {},
            'dual_source_indicators': 0
        }
        
        # 按数据源统计
        for mapping in self.unified_mappings.values():
            for source in mapping['sources'].keys():
                source_name = source.value
                if source_name not in stats['by_source']:
                    stats['by_source'][source_name] = 0
                stats['by_source'][source_name] += 1
            
            # 双数据源指标统计
            if len(mapping['sources']) > 1:
                stats['dual_source_indicators'] += 1
        
        # 按数据类型统计
        for mapping in self.unified_mappings.values():
            data_type = mapping['data_type']
            if data_type not in stats['by_data_type']:
                stats['by_data_type'][data_type] = 0
            stats['by_data_type'][data_type] += 1
        
        return stats
    
    def test_all_connections(self) -> Dict[str, Dict]:
        """测试所有数据源连接"""
        results = {}
        
        # 测试AkShare
        try:
            # AkShare通常不需要特殊连接测试
            results['akshare'] = {
                'available': True,
                'error_message': '',
                'supported_indicators': len(self.akshare_collector.akshare_mappings)
            }
        except Exception as e:
            results['akshare'] = {
                'available': False,
                'error_message': str(e),
                'supported_indicators': 0
            }
        
        # 测试Wind
        if self.wind_collector:
            wind_test = self.wind_collector.test_connection()
            results['wind'] = {
                'available': wind_test['connected'],
                'error_message': wind_test.get('error_message', ''),
                'wind_version': wind_test.get('wind_version', ''),
                'supported_indicators': len(self.wind_collector.wind_mappings)
            }
        else:
            results['wind'] = {
                'available': False,
                'error_message': 'Wind收集器未初始化',
                'supported_indicators': 0
            }
        
        return results
    
    def cleanup_connections(self):
        """清理所有连接"""
        if self.wind_collector:
            self.wind_collector.disconnect()
        
        logger.info("所有数据源连接已清理") 