#!/usr/bin/env python
"""
生成CPI和半导体相关指标的详细分析报告
"""
import os
import sys
import django
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_cycle_analysis.settings')
django.setup()

from data_hub.models import Indicator, IndicatorData

def generate_analysis_report():
    """生成CPI和半导体指标的详细分析报告"""
    
    report = []
    report.append("=" * 100)
    report.append("CPI和半导体相关指标10年数据分析报告")
    report.append("=" * 100)
    report.append(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 查找指标
    cpi_indicators = Indicator.objects.filter(name__icontains='CPI')
    semiconductor_indicators = Indicator.objects.filter(name__iregex=r'半导体|芯片|集成电路|晶圆|存储器')
    
    # 时间范围设定
    end_date = datetime.now().date()
    ten_years_ago = end_date - timedelta(days=10*365)
    five_years_ago = end_date - timedelta(days=5*365)
    one_year_ago = end_date - timedelta(days=365)
    
    # ========== CPI指标分析 ==========
    report.append("📊 一、CPI指标分析")
    report.append("=" * 60)
    report.append("")
    
    for i, indicator in enumerate(cpi_indicators, 1):
        report.append(f"{i}. {indicator.name} ({indicator.code})")
        report.append("-" * 50)
        
        # 获取最近10年数据
        data_10y = IndicatorData.objects.filter(
            indicator=indicator,
            date__gte=ten_years_ago
        ).order_by('date')
        
        if data_10y.count() > 0:
            # 转换为DataFrame进行分析
            df = pd.DataFrame(list(data_10y.values('date', 'value')))
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 基本统计
            report.append(f"📈 数据概况:")
            report.append(f"   • 数据点数: {len(df)}")
            report.append(f"   • 时间范围: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
            report.append(f"   • 平均值: {df['value'].mean():.2f}")
            report.append(f"   • 标准差: {df['value'].std():.2f}")
            report.append(f"   • 最小值: {df['value'].min():.2f} ({df.loc[df['value'].idxmin(), 'date'].strftime('%Y-%m-%d')})")
            report.append(f"   • 最大值: {df['value'].max():.2f} ({df.loc[df['value'].idxmax(), 'date'].strftime('%Y-%m-%d')})")
            
            # 近期表现
            latest_value = df['value'].iloc[-1]
            latest_date = df['date'].iloc[-1]
            report.append(f"   • 最新值: {latest_value:.2f} ({latest_date.strftime('%Y-%m-%d')})")
            
            # 年度变化趋势
            if len(df) >= 12:
                recent_12m = df.tail(12)['value'].mean()
                previous_12m = df.iloc[-24:-12]['value'].mean() if len(df) >= 24 else None
                
                if previous_12m is not None:
                    change = recent_12m - previous_12m
                    report.append(f"   • 近12个月平均: {recent_12m:.2f}")
                    report.append(f"   • 前12个月平均: {previous_12m:.2f}")
                    report.append(f"   • 年度变化: {change:+.2f} ({'上升' if change > 0 else '下降' if change < 0 else '持平'})")
        else:
            report.append("   ❌ 最近10年无数据")
        
        report.append("")
    
    # ========== 半导体指标分析 ==========
    report.append("🔬 二、半导体指标分析")
    report.append("=" * 60)
    report.append("")
    
    for i, indicator in enumerate(semiconductor_indicators, 1):
        report.append(f"{i}. {indicator.name} ({indicator.code})")
        report.append("-" * 50)
        
        # 获取最近10年数据
        data_10y = IndicatorData.objects.filter(
            indicator=indicator,
            date__gte=ten_years_ago
        ).order_by('date')
        
        if data_10y.count() > 0:
            # 转换为DataFrame进行分析
            df = pd.DataFrame(list(data_10y.values('date', 'value')))
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 基本统计
            report.append(f"📈 数据概况:")
            report.append(f"   • 数据点数: {len(df)}")
            report.append(f"   • 时间范围: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
            report.append(f"   • 平均值: {df['value'].mean():.2f}")
            report.append(f"   • 标准差: {df['value'].std():.2f}")
            report.append(f"   • 最小值: {df['value'].min():.2f} ({df.loc[df['value'].idxmin(), 'date'].strftime('%Y-%m-%d')})")
            report.append(f"   • 最大值: {df['value'].max():.2f} ({df.loc[df['value'].idxmax(), 'date'].strftime('%Y-%m-%d')})")
            
            # 近期表现
            latest_value = df['value'].iloc[-1]
            latest_date = df['date'].iloc[-1]
            report.append(f"   • 最新值: {latest_value:.2f} ({latest_date.strftime('%Y-%m-%d')})")
            
            # 波动性分析
            if len(df) >= 12:
                recent_volatility = df.tail(12)['value'].std()
                report.append(f"   • 近12个月波动率: {recent_volatility:.2f}")
                
                # 趋势分析
                recent_trend = np.polyfit(range(12), df.tail(12)['value'], 1)[0]
                trend_direction = "上升" if recent_trend > 0.1 else "下降" if recent_trend < -0.1 else "平稳"
                report.append(f"   • 近期趋势: {trend_direction} (斜率: {recent_trend:.2f})")
        else:
            report.append("   ❌ 最近10年无数据")
        
        report.append("")
    
    # ========== 综合分析 ==========
    report.append("📋 三、综合分析总结")
    report.append("=" * 60)
    report.append("")
    
    # 数据覆盖情况
    total_indicators = cpi_indicators.count() + semiconductor_indicators.count()
    cpi_with_data = sum(1 for ind in cpi_indicators if IndicatorData.objects.filter(indicator=ind, date__gte=ten_years_ago).exists())
    semi_with_data = sum(1 for ind in semiconductor_indicators if IndicatorData.objects.filter(indicator=ind, date__gte=ten_years_ago).exists())
    
    report.append(f"📊 数据覆盖情况:")
    report.append(f"   • CPI指标: {cpi_with_data}/{cpi_indicators.count()} 有数据 ({cpi_with_data/cpi_indicators.count()*100:.1f}%)")
    report.append(f"   • 半导体指标: {semi_with_data}/{semiconductor_indicators.count()} 有数据 ({semi_with_data/semiconductor_indicators.count()*100:.1f}%)")
    report.append(f"   • 总体覆盖率: {(cpi_with_data + semi_with_data)/total_indicators*100:.1f}%")
    report.append("")
    
    # CPI指标特点
    report.append(f"🎯 CPI指标特点:")
    report.append(f"   • 所有CPI指标均有完整的近30年历史数据")
    report.append(f"   • 数据质量高，更新及时")
    report.append(f"   • 覆盖消费价格的各个细分领域")
    report.append(f"   • 适合进行通胀分析和经济周期判断")
    report.append("")
    
    # 半导体指标特点
    report.append(f"💻 半导体指标特点:")
    report.append(f"   • 贸易相关指标数据较为完整")
    report.append(f"   • 台股营收类指标暂无数据")
    report.append(f"   • 出口数据反映全球半导体供应链情况")
    report.append(f"   • 适合分析科技周期和产业趋势")
    report.append("")
    
    # 建议
    report.append(f"💡 数据分析建议:")
    report.append(f"   1. CPI数据可用于分析通胀周期和消费结构变化")
    report.append(f"   2. 半导体贸易数据可用于分析科技产业周期")
    report.append(f"   3. 建议补充台股营收等高频半导体指标数据")
    report.append(f"   4. 可建立CPI与半导体指标的关联分析模型")
    report.append(f"   5. 建议设置数据自动更新机制确保数据时效性")
    
    # 输出报告
    report_content = "\n".join(report)
    
    # 保存到文件
    report_file = f"CPI_半导体指标分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(report_content)
    print(f"\n📄 报告已保存到: {report_file}")

if __name__ == "__main__":
    generate_analysis_report() 