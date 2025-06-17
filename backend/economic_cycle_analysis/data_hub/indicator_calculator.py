# -*- coding: utf-8 -*-
"""
经济周期分析系统 - 指标计算器
用于计算基于基础指标的衍生指标

主要功能：
1. 解析计算公式
2. 获取依赖数据
3. 执行计算逻辑
4. 保存计算结果
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.db import transaction
from .models import Indicator, IndicatorData
from .indicators_config_expanded import CALCULATED_INDICATORS_CONFIG, get_calculation_dependencies
import logging

logger = logging.getLogger(__name__)

class IndicatorCalculator:
    """指标计算器类"""
    
    def __init__(self):
        self.calculated_indicators = CALCULATED_INDICATORS_CONFIG["计算指标"]["indicators"]
        self.dependencies = get_calculation_dependencies()
    
    def parse_calculation_expression(self, expression):
        """
        解析计算表达式，提取依赖的指标代码
        
        Args:
            expression (str): 计算表达式，如 "CN_M1_YEARLY - CN_M2_YEARLY"
            
        Returns:
            list: 依赖的指标代码列表
        """
        import re
        # 提取表达式中的指标代码（假设都是大写字母、数字和下划线组成）
        pattern = r'\b[A-Z][A-Z0-9_]*\b'
        indicators = re.findall(pattern, expression)
        return list(set(indicators))  # 去重
    
    def get_indicator_data(self, indicator_code, start_date=None, end_date=None):
        """
        获取指标数据
        
        Args:
            indicator_code (str): 指标代码
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
            
        Returns:
            pandas.Series: 指标数据时间序列
        """
        try:
            indicator = Indicator.objects.get(code=indicator_code)
            data_query = indicator.data_points.all()
            
            if start_date:
                data_query = data_query.filter(date__gte=start_date)
            if end_date:
                data_query = data_query.filter(date__lte=end_date)
                
            data = data_query.order_by('date').values('date', 'value')
            
            if not data:
                logger.warning(f"No data found for indicator: {indicator_code}")
                return pd.Series(dtype=float)
            
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            return df['value']
            
        except Indicator.DoesNotExist:
            logger.error(f"Indicator not found: {indicator_code}")
            return pd.Series(dtype=float)
        except Exception as e:
            logger.error(f"Error getting data for {indicator_code}: {str(e)}")
            return pd.Series(dtype=float)
    
    def evaluate_expression(self, expression, data_dict):
        """
        计算表达式的值
        
        Args:
            expression (str): 计算表达式
            data_dict (dict): 指标数据字典，key为指标代码，value为pandas.Series
            
        Returns:
            pandas.Series: 计算结果时间序列
        """
        try:
            # 安全的表达式求值环境
            safe_dict = {
                '__builtins__': {},
                'np': np,
                'pd': pd,
                'abs': abs,
                'max': max,
                'min': min,
            }
            
            # 添加指标数据到环境中
            safe_dict.update(data_dict)
            
            # 求值表达式
            result = eval(expression, safe_dict)
            
            if isinstance(result, pd.Series):
                return result
            else:
                # 如果结果是标量，转换为Series
                if len(data_dict) > 0:
                    # 使用第一个数据的索引
                    first_series = list(data_dict.values())[0]
                    return pd.Series([result] * len(first_series), index=first_series.index)
                else:
                    return pd.Series([result], index=[datetime.now().date()])
                    
        except Exception as e:
            logger.error(f"Error evaluating expression '{expression}': {str(e)}")
            return pd.Series(dtype=float)
    
    def calculate_indicator(self, calc_indicator_config, start_date=None, end_date=None):
        """
        计算单个衍生指标
        
        Args:
            calc_indicator_config (dict): 计算指标配置
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
            
        Returns:
            pandas.Series: 计算结果
        """
        indicator_code = calc_indicator_config["code"]
        expression = calc_indicator_config["calculation"]
        
        logger.info(f"Calculating indicator: {indicator_code}")
        
        # 解析依赖的指标
        dependent_indicators = self.parse_calculation_expression(expression)
        
        # 获取依赖数据
        data_dict = {}
        for dep_code in dependent_indicators:
            data = self.get_indicator_data(dep_code, start_date, end_date)
            if not data.empty:
                data_dict[dep_code] = data
            else:
                logger.warning(f"No data available for dependency: {dep_code}")
        
        if not data_dict:
            logger.warning(f"No dependency data available for {indicator_code}")
            return pd.Series(dtype=float)
        
        # 对齐时间序列（取交集）
        if len(data_dict) > 1:
            # 找到所有序列的共同时间点
            common_dates = None
            for series in data_dict.values():
                if common_dates is None:
                    common_dates = set(series.index)
                else:
                    common_dates = common_dates.intersection(set(series.index))
            
            # 对齐所有序列到共同时间点
            if common_dates:
                common_dates = sorted(list(common_dates))
                for code, series in data_dict.items():
                    data_dict[code] = series.reindex(common_dates)
        
        # 计算表达式
        result = self.evaluate_expression(expression, data_dict)
        
        # 清理无效值
        result = result.dropna()
        
        logger.info(f"Calculated {len(result)} data points for {indicator_code}")
        return result
    
    def save_calculated_data(self, indicator_code, data_series):
        """
        保存计算结果到数据库
        
        Args:
            indicator_code (str): 指标代码
            data_series (pandas.Series): 计算结果数据
        """
        try:
            indicator = Indicator.objects.get(code=indicator_code)
            
            with transaction.atomic():
                # 删除已存在的数据（可选，避免重复）
                IndicatorData.objects.filter(indicator=indicator).delete()
                
                # 批量创建新数据
                data_objects = []
                for date, value in data_series.items():
                    if pd.notna(value):  # 跳过NaN值
                        data_objects.append(IndicatorData(
                            indicator=indicator,
                            date=date.date() if hasattr(date, 'date') else date,
                            value=float(value)
                        ))
                
                if data_objects:
                    IndicatorData.objects.bulk_create(data_objects, batch_size=1000)
                    logger.info(f"Saved {len(data_objects)} data points for {indicator_code}")
                else:
                    logger.warning(f"No valid data to save for {indicator_code}")
                    
        except Indicator.DoesNotExist:
            logger.error(f"Indicator not found for saving: {indicator_code}")
        except Exception as e:
            logger.error(f"Error saving data for {indicator_code}: {str(e)}")
    
    def create_calculated_indicators(self):
        """
        在数据库中创建计算指标的Indicator记录
        """
        from .models import IndicatorCategory
        
        # 获取或创建"计算指标"分类
        calc_category, created = IndicatorCategory.objects.get_or_create(
            name="计算指标",
            defaults={"description": "基于现有指标计算的衍生指标"}
        )
        
        if created:
            logger.info("Created new category: 计算指标")
        
        # 创建计算指标
        for calc_config in self.calculated_indicators:
            indicator, created = Indicator.objects.get_or_create(
                code=calc_config["code"],
                defaults={
                    "name": calc_config["name"],
                    "category": calc_category,
                    "frequency": calc_config["frequency"],
                    "lead_lag_status": calc_config["lead_lag"],
                    "source": "Calculated",
                    "description": calc_config.get("description", "")
                }
            )
            
            if created:
                logger.info(f"Created calculated indicator: {calc_config['code']}")
            else:
                logger.info(f"Calculated indicator already exists: {calc_config['code']}")
    
    def calculate_all_indicators(self, start_date=None, end_date=None):
        """
        计算所有计算指标
        
        Args:
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
        """
        logger.info("Starting calculation of all indicators...")
        
        # 首先确保计算指标在数据库中存在
        self.create_calculated_indicators()
        
        # 按依赖关系排序（简单实现：先计算依赖少的）
        # 这里简化处理，实际可以实现拓扑排序
        sorted_indicators = sorted(
            self.calculated_indicators,
            key=lambda x: len(self.parse_calculation_expression(x["calculation"]))
        )
        
        success_count = 0
        error_count = 0
        
        for calc_config in sorted_indicators:
            try:
                result = self.calculate_indicator(calc_config, start_date, end_date)
                if not result.empty:
                    self.save_calculated_data(calc_config["code"], result)
                    success_count += 1
                else:
                    logger.warning(f"No data calculated for {calc_config['code']}")
                    error_count += 1
            except Exception as e:
                logger.error(f"Failed to calculate {calc_config['code']}: {str(e)}")
                error_count += 1
        
        logger.info(f"Calculation completed. Success: {success_count}, Errors: {error_count}")
        return success_count, error_count
    
    def update_indicator(self, indicator_code, start_date=None, end_date=None):
        """
        更新单个计算指标
        
        Args:
            indicator_code (str): 指标代码
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
        """
        # 找到对应的配置
        calc_config = None
        for config in self.calculated_indicators:
            if config["code"] == indicator_code:
                calc_config = config
                break
        
        if not calc_config:
            logger.error(f"Calculated indicator config not found: {indicator_code}")
            return False
        
        try:
            result = self.calculate_indicator(calc_config, start_date, end_date)
            if not result.empty:
                self.save_calculated_data(indicator_code, result)
                logger.info(f"Successfully updated {indicator_code}")
                return True
            else:
                logger.warning(f"No data calculated for {indicator_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to update {indicator_code}: {str(e)}")
            return False

# 便捷函数
def calculate_all_indicators(start_date=None, end_date=None):
    """
    计算所有指标的便捷函数
    """
    calculator = IndicatorCalculator()
    return calculator.calculate_all_indicators(start_date, end_date)

def update_calculated_indicator(indicator_code, start_date=None, end_date=None):
    """
    更新单个计算指标的便捷函数
    """
    calculator = IndicatorCalculator()
    return calculator.update_indicator(indicator_code, start_date, end_date) 