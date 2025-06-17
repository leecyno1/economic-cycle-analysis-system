# -*- coding: utf-8 -*-
"""
现实版指标计算器 - 基于实际有数据的指标
"""

import pandas as pd
import numpy as np
from datetime import datetime
from django.db import transaction
from .models import Indicator, IndicatorData, IndicatorCategory
from .indicators_config_realistic import (
    get_realistic_calc_indicators, 
    check_realistic_data_availability,
    get_executable_realistic_indicators
)
import logging

logger = logging.getLogger(__name__)

class RealisticIndicatorCalculator:
    """现实版指标计算器"""
    
    def __init__(self):
        self.realistic_indicators = get_realistic_calc_indicators()
    
    def get_indicator_data(self, indicator_code, start_date=None, end_date=None):
        """获取指标数据"""
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
    
    def parse_calculation_expression(self, expression):
        """解析计算表达式"""
        import re
        pattern = r'\b[A-Z][A-Z0-9_]*\b'
        indicators = re.findall(pattern, expression)
        return list(set(indicators))
    
    def evaluate_expression_safe(self, expression, data_dict):
        """安全计算表达式"""
        try:
            # 安全的计算环境
            safe_dict = {
                '__builtins__': {},
                'np': np,
                'pd': pd,
                'abs': abs,
                'max': max,
                'min': min,
            }
            
            # 添加指标数据
            safe_dict.update(data_dict)
            
            # 计算表达式
            result = eval(expression, safe_dict)
            
            if isinstance(result, pd.Series):
                return result
            else:
                # 标量结果转为Series
                if len(data_dict) > 0:
                    first_series = list(data_dict.values())[0]
                    return pd.Series([result] * len(first_series), index=first_series.index)
                else:
                    return pd.Series([result], index=[datetime.now().date()])
                    
        except Exception as e:
            logger.error(f"Error evaluating expression '{expression}': {str(e)}")
            return pd.Series(dtype=float)
    
    def calculate_realistic_indicator(self, calc_config, start_date=None, end_date=None):
        """计算现实版指标"""
        indicator_code = calc_config["code"]
        expression = calc_config["calculation"]
        
        logger.info(f"Calculating realistic indicator: {indicator_code}")
        
        # 解析依赖
        dependent_indicators = self.parse_calculation_expression(expression)
        
        # 获取依赖数据
        data_dict = {}
        for dep_code in dependent_indicators:
            data = self.get_indicator_data(dep_code, start_date, end_date)
            if not data.empty:
                data_dict[dep_code] = data
                logger.info(f"Loaded {len(data)} data points for {dep_code}")
            else:
                logger.warning(f"No data available for dependency: {dep_code}")
                return pd.Series(dtype=float)
        
        if not data_dict:
            logger.warning(f"No dependency data available for {indicator_code}")
            return pd.Series(dtype=float)
        
        # 对齐时间序列
        if len(data_dict) > 1:
            common_dates = None
            for series in data_dict.values():
                if common_dates is None:
                    common_dates = set(series.index)
                else:
                    common_dates = common_dates.intersection(set(series.index))
            
            if common_dates:
                common_dates = sorted(list(common_dates))
                logger.info(f"Found {len(common_dates)} common dates")
                for code, series in data_dict.items():
                    data_dict[code] = series.reindex(common_dates)
        
        # 计算表达式
        result = self.evaluate_expression_safe(expression, data_dict)
        
        # 清理无效值
        result = result.dropna()
        
        logger.info(f"Calculated {len(result)} data points for {indicator_code}")
        return result
    
    def create_realistic_calc_indicators(self):
        """创建现实版计算指标的数据库记录"""
        # 获取或创建分类
        calc_category, created = IndicatorCategory.objects.get_or_create(
            name="现实计算指标",
            defaults={"description": "基于实际有数据指标计算的衍生指标"}
        )
        
        if created:
            logger.info("Created new category: 现实计算指标")
        
        # 创建指标
        for calc_config in self.realistic_indicators:
            indicator, created = Indicator.objects.get_or_create(
                code=calc_config["code"],
                defaults={
                    "name": calc_config["name"],
                    "category": calc_category,
                    "frequency": calc_config["frequency"],
                    "lead_lag_status": calc_config["lead_lag"],
                    "source": "RealisticCalculated",
                    "description": calc_config.get("description", "")
                }
            )
            
            if created:
                logger.info(f"Created realistic calc indicator: {calc_config['code']}")
    
    def save_calculated_data(self, indicator_code, data_series):
        """保存计算结果"""
        try:
            indicator = Indicator.objects.get(code=indicator_code)
            
            with transaction.atomic():
                # 删除已存在的数据
                IndicatorData.objects.filter(indicator=indicator).delete()
                
                # 批量创建新数据
                data_objects = []
                for date, value in data_series.items():
                    if pd.notna(value) and not np.isinf(value):  # 排除NaN和无穷值
                        data_objects.append(IndicatorData(
                            indicator=indicator,
                            date=date.date() if hasattr(date, 'date') else date,
                            value=float(value)
                        ))
                
                if data_objects:
                    IndicatorData.objects.bulk_create(data_objects, batch_size=1000)
                    logger.info(f"Saved {len(data_objects)} data points for {indicator_code}")
                    
        except Exception as e:
            logger.error(f"Error saving data for {indicator_code}: {str(e)}")
    
    def calculate_all_realistic_indicators(self, dry_run=True, start_date=None, end_date=None):
        """计算所有现实版指标"""
        logger.info("Starting calculation of all realistic indicators...")
        
        # 检查数据可用性
        availability = check_realistic_data_availability()
        if not availability['all_available']:
            logger.error("Not all required base indicators are available")
            return {'success': 0, 'error': 0, 'details': [], 'availability': availability}
        
        executable_indicators = get_executable_realistic_indicators()
        
        if not dry_run:
            self.create_realistic_calc_indicators()
        
        results = []
        success_count = 0
        error_count = 0
        
        for calc_config in executable_indicators:
            try:
                result = self.calculate_realistic_indicator(calc_config, start_date, end_date)
                
                if not result.empty:
                    details = {
                        'code': calc_config['code'],
                        'name': calc_config['name'],
                        'data_points': len(result),
                        'date_range': f"{result.index.min().date()} to {result.index.max().date()}",
                        'sample_values': result.tail(5).to_dict(),
                        'statistics': {
                            'mean': float(result.mean()),
                            'std': float(result.std()),
                            'min': float(result.min()),
                            'max': float(result.max())
                        },
                        'status': 'success'
                    }
                    
                    if not dry_run:
                        self.save_calculated_data(calc_config['code'], result)
                        details['saved'] = True
                    
                    results.append(details)
                    success_count += 1
                    logger.info(f"Successfully calculated {calc_config['code']}")
                else:
                    results.append({
                        'code': calc_config['code'],
                        'name': calc_config['name'],
                        'status': 'no_data'
                    })
                    error_count += 1
                    logger.warning(f"No data calculated for {calc_config['code']}")
                    
            except Exception as e:
                results.append({
                    'code': calc_config['code'],
                    'name': calc_config['name'],
                    'status': 'error',
                    'error': str(e)
                })
                error_count += 1
                logger.error(f"Failed to calculate {calc_config['code']}: {str(e)}")
        
        return {
            'success': success_count,
            'error': error_count,
            'details': results,
            'availability': availability
        }

def calculate_realistic_indicators(dry_run=True, start_date=None, end_date=None):
    """便捷计算函数"""
    calculator = RealisticIndicatorCalculator()
    return calculator.calculate_all_realistic_indicators(dry_run=dry_run, start_date=start_date, end_date=end_date) 