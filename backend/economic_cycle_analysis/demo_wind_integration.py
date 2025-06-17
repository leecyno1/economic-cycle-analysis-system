#!/usr/bin/env python
"""
Wind数据源集成演示
展示WindAPI数据收集器的功能和接口
在macOS环境下使用模拟数据演示
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

from data_hub.models import Indicator, IndicatorData, IndicatorCategory
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockWindDataCollector:
    """模拟Wind数据收集器 - 用于演示"""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connected = False
        
        # Wind指标映射配置
        self.wind_mappings = {
            'WIND_CPI_YOY': {
                'wind_code': 'M0000612',
                'description': 'CPI当月同比(%)',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'WIND_PPI_YOY': {
                'wind_code': 'M0001227',
                'description': 'PPI当月同比(%)',
                'data_type': 'macro',
                'frequency': 'M'
            },
            'WIND_CSI300': {
                'wind_code': '000300.SH',
                'description': '沪深300指数',
                'data_type': 'index',
                'frequency': 'D'
            },
            'WIND_10Y_TREASURY': {
                'wind_code': 'M1004263',
                'description': '10年期国债收益率(%)',
                'data_type': 'bond',
                'frequency': 'D'
            },
            'WIND_PMI_MFG': {
                'wind_code': 'M0017126',
                'description': '制造业PMI',
                'data_type': 'macro',
                'frequency': 'M'
            }
        }
    
    def connect(self):
        """模拟连接"""
        print(f"🔗 模拟连接Wind数据库...")
        print(f"   用户名: {self.username}")
        print(f"   密码: {'*' * len(self.password)}")
        self.connected = True
        return True
    
    def test_connection(self):
        """测试连接"""
        if not self.connected:
            self.connect()
        
        return {
            'connected': True,
            'wind_version': 'MockWind v1.0 (演示版)',
            'test_data': '模拟数据获取成功',
            'error_message': ''
        }
    
    def collect_indicator_data(self, indicator_code, start_date=None, end_date=None):
        """模拟数据收集"""
        if not self.connected:
            self.connect()
        
        print(f"📊 模拟收集Wind指标: {indicator_code}")
        
        # 检查指标是否支持
        if indicator_code not in self.wind_mappings:
            return {
                'success': False,
                'error_message': f'不支持的指标: {indicator_code}',
                'records_count': 0
            }
        
        config = self.wind_mappings[indicator_code]
        
        # 生成模拟数据
        mock_data = self._generate_mock_data(config, start_date, end_date)
        
        # 保存到数据库
        try:
            indicator = Indicator.objects.get(code=indicator_code)
        except Indicator.DoesNotExist:
            # 获取或创建Wind演示分类
            wind_category, _ = IndicatorCategory.objects.get_or_create(
                code='wind_demo',
                defaults={
                    'name': 'Wind演示',
                    'description': 'Wind数据源演示分类',
                    'level': 1
                }
            )
            
            # 创建指标
            indicator = Indicator.objects.create(
                code=indicator_code,
                name=config['description'],
                description=f"Wind数据库指标: {config['description']}",
                category=wind_category,
                frequency=config['frequency'],
                unit='%' if 'YOY' in indicator_code or 'PMI' in indicator_code else '',
                source='wind_mock',
                implementation_phase=1
            )
        
        saved_count = self._save_mock_data(indicator, mock_data)
        
        return {
            'success': True,
            'records_count': saved_count,
            'data_range': (mock_data['date'].min().strftime('%Y-%m-%d'), 
                          mock_data['date'].max().strftime('%Y-%m-%d')),
            'wind_code': config['wind_code'],
            'error_message': ''
        }
    
    def _generate_mock_data(self, config, start_date=None, end_date=None):
        """生成模拟数据"""
        if not end_date:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        if not start_date:
            start_date = end_date - timedelta(days=365*2)  # 2年数据
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        # 根据频率生成日期序列
        if config['frequency'] == 'M':
            # 月度数据
            dates = pd.date_range(start=start_date, end=end_date, freq='ME')
        else:
            # 日度数据
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 根据指标类型生成不同的模拟数据
        data_type = config['data_type']
        wind_code = config['wind_code']
        
        if 'CPI' in wind_code:
            # CPI数据：1-4%波动
            base_value = 2.5
            values = base_value + np.random.normal(0, 0.5, len(dates))
            values = np.clip(values, 0.5, 5.0)
        elif 'PPI' in wind_code:
            # PPI数据：-2%到6%波动
            base_value = 2.0
            values = base_value + np.random.normal(0, 1.0, len(dates))
            values = np.clip(values, -3.0, 8.0)
        elif 'PMI' in wind_code:
            # PMI数据：45-55波动
            base_value = 50.0
            values = base_value + np.random.normal(0, 2.0, len(dates))
            values = np.clip(values, 45.0, 55.0)
        elif data_type == 'index':
            # 股票指数：基于基数增长
            base_value = 3000.0
            returns = np.random.normal(0.0005, 0.02, len(dates))  # 日收益率
            values = [base_value]
            for ret in returns[1:]:
                values.append(values[-1] * (1 + ret))
            values = np.array(values)
        elif data_type == 'bond':
            # 债券收益率：2-5%波动
            base_value = 3.5
            values = base_value + np.random.normal(0, 0.3, len(dates))
            values = np.clip(values, 1.5, 6.0)
        else:
            # 默认数据
            values = np.random.normal(100, 10, len(dates))
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def _save_mock_data(self, indicator, data_df):
        """保存模拟数据到数据库"""
        saved_count = 0
        
        for _, row in data_df.iterrows():
            data_point, created = IndicatorData.objects.get_or_create(
                indicator=indicator,
                date=row['date'].date(),
                defaults={
                    'value': float(row['value']),
                    'source': 'wind_mock',
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            )
            
            if not created:
                data_point.value = float(row['value'])
                data_point.source = 'wind_mock'
                data_point.updated_at = datetime.now()
                data_point.save()
            
            saved_count += 1
        
        return saved_count
    
    def get_supported_indicators(self):
        """获取支持的指标列表"""
        return list(self.wind_mappings.keys())
    
    def disconnect(self):
        """断开连接"""
        self.connected = False
        print("🔌 模拟断开Wind连接")

def demo_wind_integration():
    """演示Wind数据源集成"""
    
    print("=" * 80)
    print("Wind数据源集成演示")
    print("=" * 80)
    print("注意：这是在macOS环境下的模拟演示")
    print("实际生产环境中需要安装WindPy并在Windows环境下运行")
    print("=" * 80)
    
    # 创建模拟Wind收集器
    collector = MockWindDataCollector(
        username="17600806220",
        password="iv19whot"
    )
    
    # 测试连接
    print("\n🔍 测试Wind连接...")
    connection_result = collector.test_connection()
    
    if connection_result['connected']:
        print("✅ Wind连接成功!")
        print(f"   版本信息: {connection_result['wind_version']}")
        print(f"   数据测试: {connection_result['test_data']}")
    else:
        print(f"❌ Wind连接失败: {connection_result['error_message']}")
        return
    
    # 显示支持的指标
    print(f"\n📊 支持的Wind指标:")
    supported_indicators = collector.get_supported_indicators()
    print(f"   总计: {len(supported_indicators)} 个指标")
    
    for code in supported_indicators:
        config = collector.wind_mappings[code]
        print(f"   • {code}: {config['description']} ({config['wind_code']})")
    
    # 演示数据收集
    print(f"\n🔄 演示数据收集...")
    
    # 设置时间范围
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')  # 2年数据
    
    print(f"   时间范围: {start_date} ~ {end_date}")
    
    # 收集几个关键指标的数据
    demo_indicators = ['WIND_CPI_YOY', 'WIND_CSI300', 'WIND_10Y_TREASURY']
    
    for indicator_code in demo_indicators:
        print(f"\n   📈 收集指标: {indicator_code}")
        
        result = collector.collect_indicator_data(indicator_code, start_date, end_date)
        
        if result['success']:
            print(f"     ✅ 成功收集 {result['records_count']} 条数据")
            print(f"     📅 数据范围: {result['data_range'][0]} ~ {result['data_range'][1]}")
            print(f"     🔗 Wind代码: {result['wind_code']}")
            
            # 显示最新数据样本
            try:
                indicator = Indicator.objects.get(code=indicator_code)
                latest_data = IndicatorData.objects.filter(
                    indicator=indicator
                ).order_by('-date')[:5]
                
                if latest_data:
                    print(f"     📊 最新数据样本:")
                    for data in latest_data:
                        print(f"       {data.date}: {data.value:.4f}")
            except:
                pass
                
        else:
            print(f"     ❌ 收集失败: {result['error_message']}")
    
    # 断开连接
    collector.disconnect()
    
    # 显示数据库状态
    print(f"\n📋 数据库状态更新:")
    wind_indicators = Indicator.objects.filter(source__in=['wind_mock', 'wind'])
    print(f"   Wind指标数量: {wind_indicators.count()}")
    
    total_wind_data = IndicatorData.objects.filter(
        indicator__in=wind_indicators
    ).count()
    print(f"   Wind数据点数量: {total_wind_data:,}")
    
    print("\n" + "=" * 80)
    print("Wind数据源集成演示完成!")
    print("=" * 80)
    print("\n💡 实际部署说明:")
    print("1. 在Windows环境下安装Wind客户端")
    print("2. 安装WindPy: pip install WindPy")
    print("3. 使用真实的Wind数据收集器替换模拟器")
    print("4. 配置定时任务进行数据更新")
    print("5. 集成到现有的AkShare数据采集流程中")

if __name__ == "__main__":
    demo_wind_integration() 