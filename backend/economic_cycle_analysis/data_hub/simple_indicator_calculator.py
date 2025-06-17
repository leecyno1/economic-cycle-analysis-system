# -*- coding: utf-8 -*-
"""
简化版指标计算器 - 基于现有数据的计算指标
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.db import transaction
from .models import Indicator, IndicatorData, IndicatorCategory
from .indicators_config_simple_calc import get_simple_calc_indicators, get_executable_calc_indicators
import logging

logger = logging.getLogger(__name__)

class SimpleIndicatorCalculator:
    """简化版指标计算器"""
    
    def __init__(self):
        self.simple_indicators = get_simple_calc_indicators()
    
    def check_data_availability(self):
        """检查数据可用性"""
        from .indicators_config_simple_calc import get_available_base_indicators
        
        analysis = get_available_base_indicators()
        executable = get_executable_calc_indicators()
        
        return {
            'total_calc_indicators': len(self.simple_indicators),
            'executable_indicators': len(executable),
            'available_base_count': analysis['available_count'],
            'missing_base_count': analysis['missing_count'],
            'available_base': analysis['available'],
            'missing_base': analysis['missing'],
            'executable_list': executable
        }
    
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
    
    def calculate_simple_indicator(self, calc_config, start_date=None, end_date=None):
        """计算单个简化指标"""
        indicator_code = calc_config["code"]
        expression = calc_config["calculation"]
        
        logger.info(f"Calculating simple indicator: {indicator_code}")
        
        # 解析依赖
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
                for code, series in data_dict.items():
                    data_dict[code] = series.reindex(common_dates)
        
        # 计算表达式
        result = self.evaluate_expression_safe(expression, data_dict)
        
        # 清理无效值
        result = result.dropna()
        
        logger.info(f"Calculated {len(result)} data points for {indicator_code}")
        return result
    
    def create_simple_calc_indicators(self):
        """创建简化计算指标的数据库记录"""
        # 获取或创建分类
        calc_category, created = IndicatorCategory.objects.get_or_create(
            name="简化计算指标",
            defaults={"description": "基于现有指标计算的简化版衍生指标"}
        )
        
        if created:
            logger.info("Created new category: 简化计算指标")
        
        # 创建指标
        for calc_config in self.simple_indicators:
            indicator, created = Indicator.objects.get_or_create(
                code=calc_config["code"],
                defaults={
                    "name": calc_config["name"],
                    "category": calc_category,
                    "frequency": calc_config["frequency"],
                    "lead_lag_status": calc_config["lead_lag"],
                    "source": "SimpleCalculated",
                    "description": calc_config.get("description", "")
                }
            )
            
            if created:
                logger.info(f"Created simple calc indicator: {calc_config['code']}")
    
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
                    if pd.notna(value):
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
    
    def test_calculations(self, dry_run=True):
        """测试所有可执行的计算"""
        logger.info("Testing simple indicator calculations...")
        
        availability = self.check_data_availability()
        executable_indicators = availability['executable_list']
        
        if not executable_indicators:
            logger.warning("No executable indicators found")
            return {'success': 0, 'error': 0, 'details': []}
        
        if not dry_run:
            self.create_simple_calc_indicators()
        
        results = []
        success_count = 0
        error_count = 0
        
        for calc_config in executable_indicators:
            try:
                result = self.calculate_simple_indicator(calc_config)
                
                if not result.empty:
                    details = {
                        'code': calc_config['code'],
                        'name': calc_config['name'],
                        'data_points': len(result),
                        'date_range': f"{result.index.min().date()} to {result.index.max().date()}",
                        'sample_values': result.tail(3).to_dict(),
                        'status': 'success'
                    }
                    
                    if not dry_run:
                        self.save_calculated_data(calc_config['code'], result)
                        details['saved'] = True
                    
                    results.append(details)
                    success_count += 1
                else:
                    results.append({
                        'code': calc_config['code'],
                        'name': calc_config['name'],
                        'status': 'no_data'
                    })
                    error_count += 1
                    
            except Exception as e:
                results.append({
                    'code': calc_config['code'],
                    'name': calc_config['name'],
                    'status': 'error',
                    'error': str(e)
                })
                error_count += 1
        
        return {
            'success': success_count,
            'error': error_count,
            'details': results,
            'availability': availability
        }

def test_simple_calculations(dry_run=True):
    """便捷测试函数"""
    calculator = SimpleIndicatorCalculator()
    return calculator.test_calculations(dry_run=dry_run) 