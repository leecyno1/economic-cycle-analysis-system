# -*- coding: utf-8 -*-
"""
数据采集模块
使用 AkShare 从各数据源采集指标的时间序列数据
"""

import logging
import pandas as pd
import akshare as ak
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from django.db import transaction
from .models import Indicator, IndicatorData
from .indicators_config import get_all_indicators

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """数据采集器类"""
    
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.errors = []
    
    def collect_indicator_data(self, indicator_code: str, start_date: str = None, end_date: str = None) -> bool:
        """
        采集单个指标的数据
        
        Args:
            indicator_code: 指标代码
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            
        Returns:
            bool: 采集是否成功
        """
        try:
            # 从数据库获取指标信息
            indicator = Indicator.objects.get(code=indicator_code)
            logger.info(f"开始采集指标: {indicator.name} ({indicator_code})")
            
            # 从指标配置中获取对应的akshare函数
            akshare_func_name = self._get_akshare_function(indicator_code)
            if not akshare_func_name:
                raise ValueError(f"未找到指标 {indicator_code} 对应的 AkShare 函数")
            
            # 调用对应的 AkShare 函数获取数据
            data_df = self._fetch_data_from_akshare(akshare_func_name, start_date, end_date)
            
            if data_df is None or data_df.empty:
                logger.warning(f"指标 {indicator_code} 未获取到数据")
                return False
            
            # 数据清洗和标准化
            cleaned_data = self._clean_and_standardize_data(data_df, indicator)
            
            if cleaned_data.empty:
                logger.warning(f"指标 {indicator_code} 清洗后数据为空")
                return False
            
            # 保存到数据库
            saved_count = self._save_to_database(indicator, cleaned_data)
            logger.info(f"指标 {indicator_code} 成功保存 {saved_count} 条数据")
            
            self.success_count += 1
            return True
            
        except Exception as e:
            error_msg = f"采集指标 {indicator_code} 时出错: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            self.error_count += 1
            return False
    
    def collect_all_indicators(self, start_date: str = None, end_date: str = None):
        """
        采集所有指标的数据
        
        Args:
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
        """
        logger.info("开始采集所有指标数据...")
        
        # 设置默认日期范围（过去1年）
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        logger.info(f"数据采集时间范围: {start_date} 到 {end_date}")
        
        # 获取所有指标
        indicators = Indicator.objects.all()
        total_indicators = indicators.count()
        logger.info(f"共需采集 {total_indicators} 个指标")
        
        for i, indicator in enumerate(indicators, 1):
            logger.info(f"进度: [{i}/{total_indicators}] 正在处理 {indicator.name}")
            self.collect_indicator_data(indicator.code, start_date, end_date)
        
        # 输出采集结果统计
        logger.info(f"""
        数据采集完成！
        成功: {self.success_count} 个指标
        失败: {self.error_count} 个指标
        总计: {total_indicators} 个指标
        """)
        
        if self.errors:
            logger.error("采集过程中的错误:")
            for error in self.errors:
                logger.error(f"  - {error}")
    
    def _get_akshare_function(self, indicator_code: str) -> Optional[str]:
        """根据指标代码获取对应的 AkShare 函数名"""
        all_indicators = get_all_indicators()
        for indicator in all_indicators:
            if indicator['code'] == indicator_code:
                return indicator['akshare_func']
        return None
    
    def _fetch_data_from_akshare(self, func_name: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
        """
        从 AkShare 获取数据
        
        Args:
            func_name: AkShare函数名
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 获取的数据
        """
        try:
            # 获取 AkShare 函数
            akshare_func = getattr(ak, func_name)
            
            # 根据函数类型调用（有些函数需要参数，有些不需要）
            if func_name in ['macro_china_cpi_monthly', 'macro_china_gdp_yearly', 'macro_usa_cpi_monthly']:
                # 宏观数据函数通常不需要日期参数
                data_df = akshare_func()
            elif func_name in ['index_zh_a_hist']:
                # 指数历史数据需要symbol参数
                # 这里需要根据具体指标映射到对应的symbol
                symbol = self._get_symbol_for_index_func(func_name)
                data_df = akshare_func(symbol=symbol, period="daily", start_date=start_date, end_date=end_date)
            else:
                # 大部分函数可以直接调用
                data_df = akshare_func()
            
            return data_df
            
        except Exception as e:
            logger.error(f"调用 AkShare 函数 {func_name} 失败: {str(e)}")
            return None
    
    def _get_symbol_for_index_func(self, func_name: str) -> str:
        """为指数函数获取默认的symbol参数"""
        # 这是一个简化的映射，实际使用中需要更详细的配置
        if func_name == 'index_zh_a_hist':
            return '000001'  # 上证指数
        return '000001'
    
    def _clean_and_standardize_data(self, data_df: pd.DataFrame, indicator: Indicator) -> pd.DataFrame:
        """
        数据清洗和标准化
        
        Args:
            data_df: 原始数据
            indicator: 指标对象
            
        Returns:
            pd.DataFrame: 清洗后的数据，包含 date 和 value 列
        """
        try:
            # 复制数据避免修改原始数据
            df = data_df.copy()
            
            # 根据不同的数据源格式进行标准化
            # 大多数 AkShare 数据都有日期列和数值列，但列名可能不同
            
            # 尝试识别日期列
            date_column = None
            possible_date_columns = ['日期', 'date', '时间', 'time', 'Date', 'Time']
            for col in possible_date_columns:
                if col in df.columns:
                    date_column = col
                    break
            
            if date_column is None:
                # 如果没有明确的日期列，使用索引
                if df.index.name in ['date', '日期'] or pd.api.types.is_datetime64_any_dtype(df.index):
                    df = df.reset_index()
                    date_column = df.columns[0]
                else:
                    raise ValueError("无法识别日期列")
            
            # 尝试识别数值列
            value_column = None
            possible_value_columns = ['当前值', '现值', 'value', 'close', '收盘价', '数值', 'current', 'actual']
            for col in possible_value_columns:
                if col in df.columns:
                    value_column = col
                    break
            
            if value_column is None:
                # 如果没有明确的数值列，尝试找到第一个数字列
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_columns) > 0:
                    value_column = numeric_columns[0]
                else:
                    raise ValueError("无法识别数值列")
            
            # 创建标准化的DataFrame
            result_df = pd.DataFrame()
            result_df['date'] = pd.to_datetime(df[date_column])
            result_df['value'] = pd.to_numeric(df[value_column], errors='coerce')
            
            # 删除空值
            result_df = result_df.dropna()
            
            # 按日期排序
            result_df = result_df.sort_values('date')
            
            # 去重（保留最新数据）
            result_df = result_df.drop_duplicates(subset=['date'], keep='last')
            
            logger.info(f"数据清洗完成，共 {len(result_df)} 条有效数据")
            return result_df
            
        except Exception as e:
            logger.error(f"数据清洗失败: {str(e)}")
            return pd.DataFrame()
    
    def _save_to_database(self, indicator: Indicator, data_df: pd.DataFrame) -> int:
        """
        将数据保存到数据库
        
        Args:
            indicator: 指标对象
            data_df: 要保存的数据，包含 date 和 value 列
            
        Returns:
            int: 保存的数据条数
        """
        saved_count = 0
        
        try:
            with transaction.atomic():
                for _, row in data_df.iterrows():
                    # 使用 update_or_create 来避免重复数据
                    indicator_data, created = IndicatorData.objects.update_or_create(
                        indicator=indicator,
                        date=row['date'].date(),
                        defaults={'value': float(row['value'])}
                    )
                    
                    if created:
                        saved_count += 1
                
        except Exception as e:
            logger.error(f"保存数据到数据库失败: {str(e)}")
            
        return saved_count

def collect_sample_data():
    """采集样本数据 - 用于测试"""
    collector = DataCollector()
    
    # 先采集几个重要的宏观指标进行测试
    test_indicators = [
        'CN_CPI_MONTHLY',     # 中国CPI月率
        'CN_M2_YEARLY',       # M2货币供应量年率
        'US_CPI_MONTHLY',     # 美国CPI月率
    ]
    
    logger.info("开始采集样本数据...")
    for indicator_code in test_indicators:
        collector.collect_indicator_data(indicator_code)
    
    logger.info(f"样本数据采集完成！成功: {collector.success_count}, 失败: {collector.error_count}")

if __name__ == "__main__":
    # 运行样本数据采集
    collect_sample_data() 