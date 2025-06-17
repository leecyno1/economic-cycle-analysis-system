# -*- coding: utf-8 -*-
"""
增强版数据采集模块
专门针对1,064个指标体系的专业数据采集器
支持多种数据源和复杂的数据处理逻辑
"""

import logging
import pandas as pd
import akshare as ak
import numpy as np
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

from django.db import transaction, IntegrityError
from django.utils import timezone
from .models import Indicator, IndicatorData, DataQualityReport

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CollectionResult:
    """数据采集结果"""
    success: bool
    records_count: int = 0
    error_message: str = ""
    data_range: Tuple[str, str] = ("", "")
    api_function: str = ""


class EnhancedDataCollector:
    """增强版数据采集器"""
    
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.errors = []
        
        # AkShare函数映射表 - 支持1,064个指标
        self.akshare_mappings = self._build_comprehensive_mappings()
        
        # 加载自动生成的映射配置
        self._load_enhanced_mappings()
        
        # 数据标准化规则
        self.standardization_rules = self._build_standardization_rules()
    
    def _load_enhanced_mappings(self):
        """加载自动生成的增强映射配置"""
        try:
            from .enhanced_mapping_config import ENHANCED_AKSHARE_MAPPINGS, MAPPING_STATS
            
            # 合并自动生成的映射
            self.akshare_mappings.update(ENHANCED_AKSHARE_MAPPINGS)
            
            logger.info(f"已加载 {MAPPING_STATS['total_indicators']} 个自动映射配置")
            logger.info(f"映射覆盖率: {MAPPING_STATS['coverage_rate']:.1f}%")
            logger.info(f"生成时间: {MAPPING_STATS['generation_time']}")
            
        except ImportError:
            logger.warning("未找到增强映射配置文件，请先运行指标映射更新器")
    
    def _build_comprehensive_mappings(self) -> Dict[str, Dict]:
        """构建全面的AkShare函数映射表"""
        return {
            # ===== 宏观经济指标 =====
            'CN_CPI_MONTHLY': {
                'func': 'macro_china_cpi_monthly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_CPI_YEARLY': {
                'func': 'macro_china_cpi_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_CPI_MONTHLY': {
                'func': 'macro_usa_cpi_monthly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # PPI相关
            'CN_PPI_YEARLY': {
                'func': 'macro_china_ppi_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # 货币供应量
            'CN_M1_YEARLY': {
                'func': 'macro_china_m1_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_M2_YEARLY': {
                'func': 'macro_china_m2_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # PMI指标
            'CN_PMI_MFG': {
                'func': 'macro_china_pmi_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_PMI_NON_MFG': {
                'func': 'macro_china_non_man_pmi',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_PMI_CAIXIN_MFG': {
                'func': 'index_pmi_man_cx',
                'params': {},
                'date_col': '日期',
                'value_col': '数值',
                'data_type': 'index',
                'frequency': 'M'
            },
            
            # GDP相关
            'CN_GDP_YEARLY': {
                'func': 'macro_china_gdp_yearly',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'Q'
            },
            'CN_INDUSTRIAL_ADDED_VALUE': {
                'func': 'macro_china_industrial_added_value',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # 贸易数据
            'CN_EXPORTS_YOY': {
                'func': 'macro_china_exports_yoy',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_IMPORTS_YOY': {
                'func': 'macro_china_imports_yoy',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_TRADE_BALANCE': {
                'func': 'macro_china_trade_balance',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_FDI': {
                'func': 'macro_china_fdi',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # 社融与信贷
            'CN_SOCIAL_FINANCING': {
                'func': 'macro_china_shrzgm',
                'params': {},
                'date_col': '日期',
                'value_col': '社会融资规模存量',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_NEW_RMB_LOAN': {
                'func': 'macro_rmb_loan',
                'params': {},
                'date_col': '月份',
                'value_col': '新增人民币贷款',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'CN_NEW_FINANCIAL_CREDIT': {
                'func': 'macro_china_new_financial_credit',
                'params': {},
                'date_col': '月份',
                'value_col': '当月',
                'data_type': 'macro',
                'frequency': 'M'
            },
            
            # 利率指标
            'CN_SHIBOR': {
                'func': 'macro_china_shibor_all',
                'params': {},
                'date_col': '日期',
                'value_col': 'Shibor隔夜',
                'data_type': 'rate',
                'frequency': 'D'
            },
            'CN_LPR': {
                'func': 'rate_interbank',
                'params': {},
                'date_col': '日期',
                'value_col': '1年期LPR',
                'data_type': 'rate',
                'frequency': 'M'
            },
            
            # ===== 美国经济指标 =====
            'US_UNEMPLOYMENT': {
                'func': 'macro_usa_unemployment_rate',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_PMI_MFG': {
                'func': 'macro_usa_pmi',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_INITIAL_JOBLESS': {
                'func': 'macro_usa_initial_jobless',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'W'
            },
            'US_ADP_EMPLOYMENT': {
                'func': 'macro_usa_adp_employment',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_DURABLE_GOODS': {
                'func': 'macro_usa_durable_goods_orders',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_RETAIL_SALES': {
                'func': 'macro_usa_retail_sales',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_EXIST_HOME_SALES': {
                'func': 'macro_usa_exist_home_sales',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_HOUSE_STARTS': {
                'func': 'macro_usa_house_starts',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_MICHIGAN_SENTIMENT': {
                'func': 'macro_usa_michigan_consumer_sentiment',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_LMCI': {
                'func': 'macro_usa_lmci',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'US_EIA_CRUDE': {
                'func': 'macro_usa_eia_crude_rate',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'commodity',
                'frequency': 'W'
            },
            'US_API_CRUDE': {
                'func': 'macro_usa_api_crude_stock',
                'params': {},
                'date_col': '日期',
                'value_col': '今值',
                'data_type': 'commodity',
                'frequency': 'W'
            },
            
            # ===== 股票指数 =====
            'SSE_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '000001', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            'SZSE_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '399001', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            'CHINEXT_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '399006', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            'CSI300_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '000300', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            'CSI500_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '000905', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            'SSE50_INDEX': {
                'func': 'index_zh_a_hist',
                'params': {'symbol': '000016', 'period': 'daily'},
                'date_col': '日期',
                'value_col': '收盘',
                'data_type': 'index',
                'frequency': 'D'
            },
            
            # ===== 资金流数据 =====
            'NORTHBOUND_CAPITAL': {
                'func': 'stock_connect_hist_sina',
                'params': {},
                'date_col': '日期',
                'value_col': '北向资金',
                'data_type': 'capital_flow',
                'frequency': 'D'
            },
            'SOUTHBOUND_CAPITAL': {
                'func': 'stock_connect_hist_sina',
                'params': {},
                'date_col': '日期',
                'value_col': '南向资金',
                'data_type': 'capital_flow',
                'frequency': 'D'
            },
            
            # ===== 估值指标 =====
            'A_SHARE_PE': {
                'func': 'stock_zh_valuation_baidu',
                'params': {},
                'date_col': '日期',
                'value_col': 'PE',
                'data_type': 'valuation',
                'frequency': 'D'
            },
            'A_SHARE_PB': {
                'func': 'stock_zh_valuation_baidu',
                'params': {},
                'date_col': '日期',
                'value_col': 'PB',
                'data_type': 'valuation',
                'frequency': 'D'
            },
            
            # ===== 政策相关 =====
            'CN_BOND_10Y': {
                'func': 'bond_zh_us_rate',
                'params': {},
                'date_col': '日期',
                'value_col': '中国国债收益率10年',
                'data_type': 'bond',
                'frequency': 'D'
            },
            'CN_BOND_1Y': {
                'func': 'bond_zh_us_rate',
                'params': {},
                'date_col': '日期',
                'value_col': '中国国债收益率1年',
                'data_type': 'bond',
                'frequency': 'D'
            },
            'CN_BOND_5Y': {
                'func': 'bond_zh_us_rate',
                'params': {},
                'date_col': '日期',
                'value_col': '中国国债收益率5年',
                'data_type': 'bond',
                'frequency': 'D'
            },
            'CN_RRR': {
                'func': 'tool_china_rrr',
                'params': {},
                'date_col': '日期',
                'value_col': '存款准备金率',
                'data_type': 'policy',
                'frequency': 'M'
            },
            
            # ===== 大宗商品 =====
            'GOLD_PRICE': {
                'func': 'macro_cons_gold',
                'params': {},
                'date_col': '日期',
                'value_col': '库存总量',
                'data_type': 'commodity',
                'frequency': 'D'
            },
            'LME_STOCK': {
                'func': 'macro_euro_lme_stock',
                'params': {},
                'date_col': '日期',
                'value_col': '库存',
                'data_type': 'commodity',
                'frequency': 'D'
            },
            
            # ===== 情绪指标 =====
            'VIX_INDEX': {
                'func': 'index_vix',
                'params': {},
                'date_col': '日期',
                'value_col': '收盘价',
                'data_type': 'sentiment',
                'frequency': 'D'
            },
            
            # ===== 全球市场 =====
            'GLOBAL_INDICES': {
                'func': 'index_global_spot_em',
                'params': {},
                'date_col': '日期',
                'value_col': '最新价',
                'data_type': 'global_index',
                'frequency': 'D'
            },
            'HK_INDICES': {
                'func': 'stock_hk_index_spot_sina',
                'params': {},
                'date_col': '日期',
                'value_col': '现价',
                'data_type': 'hk_index',
                'frequency': 'D'
            }
        }
    
    def _build_standardization_rules(self) -> Dict[str, Dict]:
        """构建数据标准化规则"""
        return {
            'date_formats': [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y年%m月%d日',
                '%Y-%m',
                '%Y年%m月',
                '%Y'
            ],
            'numeric_cleaning': {
                'remove_chars': ['%', '万', '亿', '千', ',', '，'],
                'multipliers': {
                    '万': 10000,
                    '亿': 100000000,
                    '千': 1000
                }
            },
            'null_values': ['--', '-', 'N/A', 'n/a', '', '无数据', '暂无']
        }
    
    def collect_indicator_data(self, 
                             indicator_code: str, 
                             start_date: str = None, 
                             end_date: str = None) -> CollectionResult:
        """
        采集单个指标的数据
        
        Args:
            indicator_code: 指标代码
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            
        Returns:
            CollectionResult: 采集结果
        """
        try:
            # 从数据库获取指标信息
            indicator = Indicator.objects.get(code=indicator_code)
            logger.info(f"开始采集指标: {indicator.name} ({indicator_code})")
            
            # 获取AkShare函数配置
            if indicator_code not in self.akshare_mappings:
                return CollectionResult(
                    success=False,
                    error_message=f"未找到指标 {indicator_code} 的AkShare映射配置"
                )
            
            config = self.akshare_mappings[indicator_code]
            
            # 调用AkShare函数获取数据
            data_df = self._fetch_data_from_akshare(config, start_date, end_date)
            
            if data_df is None or data_df.empty:
                return CollectionResult(
                    success=False,
                    error_message=f"指标 {indicator_code} 未获取到数据"
                )
            
            # 数据清洗和标准化
            cleaned_data = self._clean_and_standardize_data(data_df, config)
            
            if cleaned_data.empty:
                return CollectionResult(
                    success=False,
                    error_message=f"指标 {indicator_code} 清洗后数据为空"
                )
            
            # 保存到数据库
            saved_count = self._save_to_database(indicator, cleaned_data)
            
            # 计算数据范围
            data_range = (
                cleaned_data['date'].min().strftime('%Y-%m-%d'),
                cleaned_data['date'].max().strftime('%Y-%m-%d')
            )
            
            logger.info(f"指标 {indicator_code} 成功保存 {saved_count} 条数据")
            
            return CollectionResult(
                success=True,
                records_count=saved_count,
                data_range=data_range,
                api_function=config['func']
            )
            
        except Exception as e:
            error_msg = f"采集指标 {indicator_code} 时出错: {str(e)}"
            logger.error(error_msg)
            return CollectionResult(
                success=False,
                error_message=error_msg
            )
    
    def _fetch_data_from_akshare(self, 
                                config: Dict, 
                                start_date: str = None, 
                                end_date: str = None) -> Optional[pd.DataFrame]:
        """
        从AkShare获取数据
        
        Args:
            config: AkShare函数配置
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 获取的数据
        """
        try:
            func_name = config['func']
            params = config.get('params', {}).copy()
            
            # 获取AkShare函数
            akshare_func = getattr(ak, func_name)
            
            # 根据函数类型添加日期参数
            if func_name in ['index_zh_a_hist'] and start_date and end_date:
                params['start_date'] = start_date.replace('-', '')
                params['end_date'] = end_date.replace('-', '')
            
            # 调用AkShare函数
            logger.info(f"调用 {func_name} 函数，参数: {params}")
            data_df = akshare_func(**params)
            
            logger.info(f"成功获取 {len(data_df) if data_df is not None else 0} 条数据")
            return data_df
            
        except Exception as e:
            logger.error(f"调用AkShare函数 {config['func']} 失败: {str(e)}")
            return None
    
    def _clean_and_standardize_data(self, 
                                   data_df: pd.DataFrame, 
                                   config: Dict) -> pd.DataFrame:
        """
        数据清洗和标准化
        
        Args:
            data_df: 原始数据
            config: 配置信息
            
        Returns:
            pd.DataFrame: 清洗后的数据，包含 date 和 value 列
        """
        try:
            df = data_df.copy()
            
            # 获取日期列和数值列
            date_col = config.get('date_col', '日期')
            value_col = config.get('value_col', '收盘')
            
            # 查找实际的列名（处理列名可能的变化）
            actual_date_col = self._find_column(df, [date_col, '日期', 'date', 'Date', '时间'])
            actual_value_col = self._find_column(df, [value_col, '数值', 'value', 'Value', '今值', '收盘', '最新价'])
            
            if actual_date_col is None:
                logger.warning(f"未找到日期列，尝试使用索引")
                if df.index.name == '日期' or pd.api.types.is_datetime64_any_dtype(df.index):
                    df = df.reset_index()
                    actual_date_col = df.columns[0]
                else:
                    raise ValueError("无法确定日期列")
            
            if actual_value_col is None:
                logger.warning(f"未找到数值列 {value_col}，使用第一个数值列")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    actual_value_col = numeric_cols[0]
                else:
                    raise ValueError("无法确定数值列")
            
            # 提取必要的列
            result_df = df[[actual_date_col, actual_value_col]].copy()
            result_df.columns = ['date', 'value']
            
            # 清洗日期列
            result_df['date'] = self._clean_date_column(result_df['date'])
            
            # 清洗数值列
            result_df['value'] = self._clean_numeric_column(result_df['value'])
            
            # 删除无效数据
            result_df = result_df.dropna(subset=['date', 'value'])
            
            # 按日期排序
            result_df = result_df.sort_values('date')
            
            # 去重（保留最新的值）
            result_df = result_df.drop_duplicates(subset=['date'], keep='last')
            
            return result_df
            
        except Exception as e:
            logger.error(f"数据清洗失败: {str(e)}")
            return pd.DataFrame()
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """查找列名"""
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    def _clean_date_column(self, date_series: pd.Series) -> pd.Series:
        """清洗日期列"""
        def parse_date(date_str):
            if pd.isna(date_str):
                return None
            
            # 如果已经是datetime类型
            if isinstance(date_str, (pd.Timestamp, datetime)):
                return date_str.date() if hasattr(date_str, 'date') else date_str
            
            date_str = str(date_str).strip()
            
            # 尝试多种日期格式
            for fmt in self.standardization_rules['date_formats']:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            
            # 使用pandas的to_datetime作为后备
            try:
                return pd.to_datetime(date_str).date()
            except:
                logger.warning(f"无法解析日期: {date_str}")
                return None
        
        return date_series.apply(parse_date)
    
    def _clean_numeric_column(self, value_series: pd.Series) -> pd.Series:
        """清洗数值列"""
        def parse_numeric(value):
            if pd.isna(value):
                return None
            
            # 如果已经是数值类型
            if isinstance(value, (int, float)):
                return float(value) if not np.isnan(value) else None
            
            value_str = str(value).strip()
            
            # 检查是否为空值
            if value_str in self.standardization_rules['null_values']:
                return None
            
            # 移除特殊字符
            for char in self.standardization_rules['numeric_cleaning']['remove_chars']:
                if char in value_str:
                    multiplier = self.standardization_rules['numeric_cleaning']['multipliers'].get(char, 1)
                    value_str = value_str.replace(char, '')
                    try:
                        return float(value_str) * multiplier
                    except ValueError:
                        continue
            
            # 尝试直接转换
            try:
                return float(value_str)
            except ValueError:
                logger.warning(f"无法解析数值: {value}")
                return None
        
        return value_series.apply(parse_numeric)
    
    def _save_to_database(self, indicator: Indicator, data_df: pd.DataFrame) -> int:
        """
        保存数据到数据库
        
        Args:
            indicator: 指标对象
            data_df: 清洗后的数据
            
        Returns:
            int: 保存的记录数
        """
        saved_count = 0
        
        try:
            with transaction.atomic():
                for _, row in data_df.iterrows():
                    try:
                        # 创建或更新数据记录
                        data_point, created = IndicatorData.objects.update_or_create(
                            indicator=indicator,
                            date=row['date'],
                            defaults={
                                'value': row['value'],
                                'source_system': 'AkShare',
                                'is_estimated': False,
                                'confidence_score': 0.9,  # 默认置信度
                                'raw_value': row['value'],
                                'calculated_value': row['value']
                            }
                        )
                        
                        if created:
                            saved_count += 1
                            
                    except IntegrityError as e:
                        logger.warning(f"保存数据点失败 {indicator.code} {row['date']}: {e}")
                        continue
                
                logger.info(f"成功保存 {saved_count} 条新数据到数据库")
                
        except Exception as e:
            logger.error(f"保存数据到数据库失败: {str(e)}")
            
        return saved_count
    
    def get_supported_indicators(self) -> List[str]:
        """获取支持的指标列表"""
        return list(self.akshare_mappings.keys())
    
    def validate_indicator_support(self, indicator_code: str) -> Tuple[bool, str]:
        """验证指标是否支持"""
        if indicator_code in self.akshare_mappings:
            config = self.akshare_mappings[indicator_code]
            return True, f"支持，使用函数: {config['func']}"
        else:
            return False, "不支持，需要添加AkShare映射配置" 