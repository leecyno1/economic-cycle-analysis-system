#!/usr/bin/env python
"""
收集CPI和半导体相关指标的10年历史数据
"""
import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator, IndicatorData
from data_hub.enhanced_data_collector import EnhancedDataCollector
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def collect_specific_indicators():
    """收集CPI和半导体相关指标的数据"""
    
    # 创建数据收集器
    collector = EnhancedDataCollector()
    
    # 定义时间范围（10年）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)  # 约10年
    
    # 查找CPI相关指标
    cpi_indicators = Indicator.objects.filter(name__icontains='CPI')
    logger.info(f"找到 {cpi_indicators.count()} 个CPI指标")
    
    # 查找半导体相关指标
    semiconductor_indicators = Indicator.objects.filter(name__iregex=r'半导体|芯片|集成电路|晶圆|存储器')
    logger.info(f"找到 {semiconductor_indicators.count()} 个半导体指标")
    
    # 合并指标列表
    all_indicators = list(cpi_indicators) + list(semiconductor_indicators)
    total_indicators = len(all_indicators)
    
    logger.info(f"开始收集 {total_indicators} 个指标的10年历史数据")
    logger.info(f"时间范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")
    
    success_count = 0
    error_count = 0
    
    for i, indicator in enumerate(all_indicators, 1):
        try:
            logger.info(f"[{i}/{total_indicators}] 正在收集: {indicator.name} ({indicator.code})")
            
            # 检查是否已有数据
            existing_count = IndicatorData.objects.filter(indicator=indicator).count()
            logger.info(f"  现有数据点: {existing_count}")
            
            # 尝试收集数据
            result = collector.collect_indicator_data(
                indicator_code=indicator.code,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            
            if result.success:
                new_count = result.records_count
                success_count += 1
                logger.info(f"  ✓ 成功收集 {new_count} 个数据点")
                
                # 显示最新数据样本
                latest_data = IndicatorData.objects.filter(indicator=indicator).order_by('-date')[:3]
                if latest_data:
                    logger.info("  最新数据:")
                    for data in latest_data:
                        logger.info(f"    {data.date}: {data.value}")
            else:
                error_count += 1
                error_msg = result.error_message or '未知错误'
                logger.warning(f"  ✗ 收集失败: {error_msg}")
                
        except Exception as e:
            error_count += 1
            logger.error(f"  ✗ 异常错误: {str(e)}")
        
        # 每5个指标显示进度
        if i % 5 == 0:
            logger.info(f"进度: {i}/{total_indicators} 完成, 成功: {success_count}, 失败: {error_count}")
    
    # 最终统计
    logger.info("=" * 60)
    logger.info("数据收集完成!")
    logger.info(f"总指标数: {total_indicators}")
    logger.info(f"成功收集: {success_count}")
    logger.info(f"收集失败: {error_count}")
    logger.info(f"成功率: {success_count/total_indicators*100:.1f}%")
    
    # 显示各指标的数据统计
    logger.info("\n=== 指标数据统计 ===")
    for indicator in all_indicators:
        data_count = IndicatorData.objects.filter(indicator=indicator).count()
        if data_count > 0:
            latest_date = IndicatorData.objects.filter(indicator=indicator).order_by('-date').first().date
            earliest_date = IndicatorData.objects.filter(indicator=indicator).order_by('date').first().date
            logger.info(f"{indicator.name}: {data_count} 点 ({earliest_date} ~ {latest_date})")
        else:
            logger.info(f"{indicator.name}: 无数据")

if __name__ == "__main__":
    collect_specific_indicators() 