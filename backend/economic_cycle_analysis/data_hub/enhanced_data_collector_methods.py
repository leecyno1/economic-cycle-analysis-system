# -*- coding: utf-8 -*-
"""
增强版数据采集器 - 核心方法
"""

from .enhanced_data_collector import EnhancedDataCollector, CollectionResult
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)


class EnhancedDataCollectorMethods(EnhancedDataCollector):
    """增强版数据采集器的方法扩展"""
    
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
            from .models import Indicator
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
                                config, 
                                start_date: str = None, 
                                end_date: str = None) -> Optional[pd.DataFrame]:
        """从AkShare获取数据"""
        try:
            import akshare as ak
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
    
    def _clean_and_standardize_data(self, data_df: pd.DataFrame, config) -> pd.DataFrame:
        """数据清洗和标准化"""
        try:
            df = data_df.copy()
            
            # 获取日期列和数值列
            date_col = config.get('date_col', '日期')
            value_col = config.get('value_col', '收盘')
            
            # 查找实际的列名
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
            
            # 移除特殊字符并处理倍数
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
    
    def _save_to_database(self, indicator, data_df: pd.DataFrame) -> int:
        """保存数据到数据库"""
        from django.db import transaction, IntegrityError
        from .models import IndicatorData
        
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
                                'confidence_score': 0.9,
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