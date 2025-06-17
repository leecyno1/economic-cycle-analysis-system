# -*- coding: utf-8 -*-
"""
WindAPI数据采集模块
专业的Wind金融数据终端接口集成
支持宏观经济、股票、债券、期货等多种金融数据
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple, Union
from dataclasses import dataclass
import os
import sys

from django.db import transaction, IntegrityError
from django.utils import timezone
from .models import Indicator, IndicatorData, DataQualityReport

# WindPy导入
try:
    from WindPy import w
    WIND_AVAILABLE = True
except ImportError:
    WIND_AVAILABLE = False
    w = None

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WindConnectionConfig:
    """Wind连接配置"""
    username: str = "17600806220"
    password: str = "iv19whot"
    server: str = ""  # 可选服务器地址
    timeout: int = 60  # 超时时间（秒）


@dataclass
class WindCollectionResult:
    """Wind数据采集结果"""
    success: bool
    records_count: int = 0
    error_message: str = ""
    data_range: Tuple[str, str] = ("", "")
    wind_code: str = ""
    error_code: int = 0


class WindDataCollector:
    """Wind数据采集器"""
    
    def __init__(self, config: WindConnectionConfig = None):
        self.config = config or WindConnectionConfig()
        self.connected = False
        self.w = w
        
        # Wind代码映射表
        self.wind_mappings = self._build_wind_mappings()
        
        # 数据标准化规则
        self.standardization_rules = self._build_standardization_rules()
    
    def connect(self) -> bool:
        """连接到Wind数据库"""
        if not WIND_AVAILABLE:
            logger.error("WindPy未安装，请先安装: pip install WindPy")
            return False
        
        try:
            # 启动Wind接口
            result = self.w.start()
            
            if result.ErrorCode == 0:
                self.connected = True
                logger.info("Wind数据库连接成功")
                
                # 登录验证
                login_result = self.w.logon(self.config.username, self.config.password)
                if hasattr(login_result, 'ErrorCode') and login_result.ErrorCode == 0:
                    logger.info(f"Wind用户登录成功: {self.config.username}")
                else:
                    logger.warning("Wind登录状态未明确，但连接已建立")
                
                return True
            else:
                logger.error(f"Wind数据库连接失败，错误代码: {result.ErrorCode}")
                return False
                
        except Exception as e:
            logger.error(f"Wind连接异常: {str(e)}")
            return False
    
    def disconnect(self):
        """断开Wind连接"""
        if self.connected and self.w:
            try:
                self.w.stop()
                self.connected = False
                logger.info("Wind数据库连接已断开")
            except Exception as e:
                logger.error(f"断开Wind连接时出错: {str(e)}")
    
    def _build_wind_mappings(self) -> Dict[str, Dict]:
        """构建Wind代码映射表"""
        return {
            # ===== 宏观经济指标 =====
            'WIND_CPI_YOY': {
                'wind_code': 'M0000612',  # CPI当月同比
                'data_type': 'macro',
                'frequency': 'M',
                'description': 'CPI当月同比(%)',
                'dimension': '景气指数',
                'industry': '宏观经济'
            },
            'WIND_CPI_MOM': {
                'wind_code': 'M0000613',  # CPI当月环比
                'data_type': 'macro',
                'frequency': 'M',
                'description': 'CPI当月环比(%)',
                'dimension': '景气指数',
                'industry': '宏观经济'
            },
            'WIND_PPI_YOY': {
                'wind_code': 'M0001227',  # PPI当月同比
                'data_type': 'macro',
                'frequency': 'M',
                'description': 'PPI当月同比(%)',
                'dimension': '景气指数',
                'industry': '宏观经济'
            },
            'WIND_GDP_YOY': {
                'wind_code': 'M0000545',  # GDP当季同比
                'data_type': 'macro',
                'frequency': 'Q',
                'description': 'GDP当季同比(%)',
                'dimension': '景气指数',
                'industry': '宏观经济'
            },
            'WIND_M2_YOY': {
                'wind_code': 'M0001380',  # M2同比增长
                'data_type': 'macro',
                'frequency': 'M',
                'description': 'M2同比增长(%)',
                'dimension': '流动性',
                'industry': '宏观经济'
            },
            'WIND_PMI_MFG': {
                'wind_code': 'M0017126',  # 制造业PMI
                'data_type': 'macro',
                'frequency': 'M',
                'description': '制造业PMI',
                'dimension': '景气指数',
                'industry': '制造业'
            },
            'WIND_PMI_NON_MFG': {
                'wind_code': 'M0017127',  # 非制造业PMI
                'data_type': 'macro',
                'frequency': 'M',
                'description': '非制造业PMI',
                'dimension': '景气指数',
                'industry': '服务业'
            },
            
            # ===== 股票指数 =====
            'WIND_CSI300': {
                'wind_code': '000300.SH',  # 沪深300指数
                'data_type': 'index',
                'frequency': 'D',
                'description': '沪深300指数',
                'dimension': '技术面',
                'industry': '股票市场'
            },
            'WIND_SSE_COMP': {
                'wind_code': '000001.SH',  # 上证综指
                'data_type': 'index',
                'frequency': 'D',
                'description': '上证综合指数',
                'dimension': '技术面',
                'industry': '股票市场'
            },
            'WIND_SZSE_COMP': {
                'wind_code': '399001.SZ',  # 深证成指
                'data_type': 'index',
                'frequency': 'D',
                'description': '深证成份指数',
                'dimension': '技术面',
                'industry': '股票市场'
            },
            'WIND_GEM': {
                'wind_code': '399006.SZ',  # 创业板指数
                'data_type': 'index',
                'frequency': 'D',
                'description': '创业板指数',
                'dimension': '技术面',
                'industry': '股票市场'
            },
            
            # ===== 债券利率 =====
            'WIND_10Y_TREASURY': {
                'wind_code': 'M1004263',  # 10年期国债收益率
                'data_type': 'bond',
                'frequency': 'D',
                'description': '10年期国债收益率(%)',
                'dimension': '流动性',
                'industry': '债券市场'
            },
            'WIND_1Y_TREASURY': {
                'wind_code': 'M1004260',  # 1年期国债收益率
                'data_type': 'bond',
                'frequency': 'D',
                'description': '1年期国债收益率(%)',
                'dimension': '流动性',
                'industry': '债券市场'
            },
            'WIND_SHIBOR_1M': {
                'wind_code': 'M0017142',  # 1个月SHIBOR
                'data_type': 'bond',
                'frequency': 'D',
                'description': '1个月SHIBOR(%)',
                'dimension': '流动性',
                'industry': '债券市场'
            },
            
            # ===== 行业指数 =====
            'WIND_CSI_CONSUMER': {
                'wind_code': '000932.SH',  # 中证消费指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证消费指数',
                'dimension': '技术面',
                'industry': '消费'
            },
            'WIND_CSI_FINANCE': {
                'wind_code': '000934.SH',  # 中证金融指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证金融指数',
                'dimension': '技术面',
                'industry': '金融'
            },
            'WIND_CSI_MATERIAL': {
                'wind_code': '000935.SH',  # 中证材料指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证材料指数',
                'dimension': '技术面',
                'industry': '材料'
            },
            'WIND_CSI_ENERGY': {
                'wind_code': '000936.SH',  # 中证能源指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证能源指数',
                'dimension': '技术面',
                'industry': '能源'
            },
            'WIND_CSI_HEALTHCARE': {
                'wind_code': '000933.SH',  # 中证医药指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证医药指数',
                'dimension': '技术面',
                'industry': '医药'
            },
            'WIND_CSI_TECH': {
                'wind_code': '000937.SH',  # 中证科技指数
                'data_type': 'industry_index',
                'frequency': 'D',
                'description': '中证科技指数',
                'dimension': '技术面',
                'industry': 'TMT'
            },
            
            # ===== 商品期货 =====
            'WIND_CRUDE_OIL': {
                'wind_code': 'SC.INE',  # 原油期货主力合约
                'data_type': 'commodity',
                'frequency': 'D',
                'description': '原油期货价格',
                'dimension': '基本面',
                'industry': '能源'
            },
            'WIND_COPPER': {
                'wind_code': 'CU.SHF',  # 沪铜期货主力合约
                'data_type': 'commodity',
                'frequency': 'D',
                'description': '铜期货价格',
                'dimension': '基本面',
                'industry': '有色金属'
            },
            'WIND_STEEL_REBAR': {
                'wind_code': 'RB.SHF',  # 螺纹钢期货主力合约
                'data_type': 'commodity',
                'frequency': 'D',
                'description': '螺纹钢期货价格',
                'dimension': '基本面',
                'industry': '钢铁'
            },
            'WIND_CORN': {
                'wind_code': 'C.DCE',  # 玉米期货主力合约
                'data_type': 'commodity',
                'frequency': 'D',
                'description': '玉米期货价格',
                'dimension': '基本面',
                'industry': '农业'
            },
            
            # ===== 外汇汇率 =====
            'WIND_USD_CNY': {
                'wind_code': 'USDCNY.EX',  # 美元兑人民币即期汇率
                'data_type': 'fx',
                'frequency': 'D',
                'description': '美元兑人民币汇率',
                'dimension': '流动性',
                'industry': '外汇'
            },
            'WIND_EUR_CNY': {
                'wind_code': 'EURCNY.EX',  # 欧元兑人民币即期汇率
                'data_type': 'fx',
                'frequency': 'D',
                'description': '欧元兑人民币汇率',
                'dimension': '流动性',
                'industry': '外汇'
            },
            
            # ===== 房地产指标 =====
            'WIND_HOUSE_PRICE_70': {
                'wind_code': 'M0041652',  # 70个大中城市房价指数
                'data_type': 'real_estate',
                'frequency': 'M',
                'description': '70个大中城市房价指数',
                'dimension': '基本面',
                'industry': '房地产'
            },
            'WIND_LAND_PREMIUM': {
                'wind_code': 'M0041653',  # 土地成交溢价率
                'data_type': 'real_estate',
                'frequency': 'M',
                'description': '土地成交溢价率(%)',
                'dimension': '基本面',
                'industry': '房地产'
            },
            
            # ===== 社会融资指标 =====
            'WIND_SOCIAL_FINANCING': {
                'wind_code': 'M0017142',  # 社会融资规模存量
                'data_type': 'finance',
                'frequency': 'M',
                'description': '社会融资规模存量(万亿元)',
                'dimension': '流动性',
                'industry': '金融'
            },
            'WIND_NEW_LOANS': {
                'wind_code': 'M0001385',  # 新增人民币贷款
                'data_type': 'finance',
                'frequency': 'M',
                'description': '新增人民币贷款(亿元)',
                'dimension': '流动性',
                'industry': '金融'
            },
            
            # ===== 进出口贸易 =====
            'WIND_EXPORT_YOY': {
                'wind_code': 'M0000607',  # 出口金额当月同比
                'data_type': 'trade',
                'frequency': 'M',
                'description': '出口金额当月同比(%)',
                'dimension': '基本面',
                'industry': '对外贸易'
            },
            'WIND_IMPORT_YOY': {
                'wind_code': 'M0000608',  # 进口金额当月同比
                'data_type': 'trade',
                'frequency': 'M',
                'description': '进口金额当月同比(%)',
                'dimension': '基本面',
                'industry': '对外贸易'
            },
            
            # ===== 工业生产指标 =====
            'WIND_INDUSTRIAL_PROD': {
                'wind_code': 'M0000564',  # 工业增加值当月同比
                'data_type': 'industrial',
                'frequency': 'M',
                'description': '工业增加值当月同比(%)',
                'dimension': '景气指数',
                'industry': '工业'
            },
            'WIND_ELECTRICITY_PROD': {
                'wind_code': 'M0000565',  # 发电量当月同比
                'data_type': 'industrial',
                'frequency': 'M',
                'description': '发电量当月同比(%)',
                'dimension': '景气指数',
                'industry': '电力'
            },
            
            # ===== 消费指标 =====
            'WIND_RETAIL_SALES': {
                'wind_code': 'M0000566',  # 社会消费品零售总额当月同比
                'data_type': 'consumption',
                'frequency': 'M',
                'description': '社会消费品零售总额当月同比(%)',
                'dimension': '景气指数',
                'industry': '消费'
            },
            'WIND_AUTO_SALES': {
                'wind_code': 'M0000567',  # 汽车销量当月同比
                'data_type': 'consumption',
                'frequency': 'M',
                'description': '汽车销量当月同比(%)',
                'dimension': '景气指数',
                'industry': '汽车'
            },
            
            # ===== 投资指标 =====
            'WIND_FAI_YTD': {
                'wind_code': 'M0000570',  # 固定资产投资完成额累计同比
                'data_type': 'investment',
                'frequency': 'M',
                'description': '固定资产投资完成额累计同比(%)',
                'dimension': '景气指数',
                'industry': '投资'
            },
            'WIND_REAL_ESTATE_INV': {
                'wind_code': 'M0000571',  # 房地产开发投资完成额累计同比
                'data_type': 'investment',
                'frequency': 'M',
                'description': '房地产开发投资完成额累计同比(%)',
                'dimension': '景气指数',
                'industry': '房地产'
            },
            
            # ===== 就业指标 =====
            'WIND_URBAN_UNEMPLOYMENT': {
                'wind_code': 'M0000572',  # 城镇调查失业率
                'data_type': 'employment',
                'frequency': 'M',
                'description': '城镇调查失业率(%)',
                'dimension': '景气指数',
                'industry': '劳动力市场'
            },
            
            # ===== 波动率指标 =====
            'WIND_VIX_CHINA': {
                'wind_code': 'CVIX.SH',  # 中国波指
                'data_type': 'volatility',
                'frequency': 'D',
                'description': '中国波指',
                'dimension': '波动率',
                'industry': '股票市场'
            },
            
            # ===== ESG指标 =====
            'WIND_CSI_ESG': {
                'wind_code': '931151.CSI',  # 中证ESG指数
                'data_type': 'esg',
                'frequency': 'D',
                'description': '中证ESG指数',
                'dimension': 'ESG',
                'industry': 'ESG'
            }
        }
    
    def _build_standardization_rules(self) -> Dict[str, Dict]:
        """构建数据标准化规则"""
        return {
            'date_formats': [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y.%m.%d',
                '%Y%m%d'
            ],
            'value_cleaning': {
                'replace_values': {
                    'nan': None,
                    'NaN': None,
                    'NULL': None,
                    '--': None,
                    '': None
                }
            }
        }
    
    def collect_indicator_data(self, 
                             indicator_code: str, 
                             start_date: str = None, 
                             end_date: str = None) -> WindCollectionResult:
        """
        采集单个指标的Wind数据
        
        Args:
            indicator_code: 指标代码
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            
        Returns:
            WindCollectionResult: 采集结果
        """
        if not self.connected:
            if not self.connect():
                return WindCollectionResult(
                    success=False,
                    error_message="无法连接到Wind数据库"
                )
        
        try:
            # 从数据库获取指标信息
            indicator = Indicator.objects.get(code=indicator_code)
            logger.info(f"开始采集Wind指标: {indicator.name} ({indicator_code})")
            
            # 获取Wind代码配置
            if indicator_code not in self.wind_mappings:
                return WindCollectionResult(
                    success=False,
                    error_message=f"未找到指标 {indicator_code} 的Wind映射配置"
                )
            
            config = self.wind_mappings[indicator_code]
            wind_code = config['wind_code']
            
            # 调用Wind API获取数据
            data_df = self._fetch_data_from_wind(config, start_date, end_date)
            
            if data_df is None or data_df.empty:
                return WindCollectionResult(
                    success=False,
                    error_message=f"指标 {indicator_code} 未获取到Wind数据",
                    wind_code=wind_code
                )
            
            # 数据清洗和标准化
            cleaned_data = self._clean_and_standardize_data(data_df, config)
            
            if cleaned_data.empty:
                return WindCollectionResult(
                    success=False,
                    error_message=f"指标 {indicator_code} 清洗后数据为空",
                    wind_code=wind_code
                )
            
            # 保存到数据库
            saved_count = self._save_to_database(indicator, cleaned_data)
            
            # 计算数据范围
            data_range = (
                cleaned_data['date'].min().strftime('%Y-%m-%d'),
                cleaned_data['date'].max().strftime('%Y-%m-%d')
            )
            
            logger.info(f"指标 {indicator_code} 成功保存 {saved_count} 条Wind数据")
            
            return WindCollectionResult(
                success=True,
                records_count=saved_count,
                data_range=data_range,
                wind_code=wind_code
            )
            
        except Exception as e:
            error_msg = f"采集Wind指标 {indicator_code} 时出错: {str(e)}"
            logger.error(error_msg)
            return WindCollectionResult(
                success=False,
                error_message=error_msg
            )
    
    def _fetch_data_from_wind(self, 
                             config: Dict, 
                             start_date: str = None, 
                             end_date: str = None) -> Optional[pd.DataFrame]:
        """
        从Wind获取数据
        
        Args:
            config: Wind代码配置
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 获取的数据
        """
        try:
            wind_code = config['wind_code']
            data_type = config['data_type']
            frequency = config['frequency']
            
            # 设置默认日期范围
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=10*365)).strftime('%Y-%m-%d')
            
            logger.info(f"调用Wind API: {wind_code}, 时间范围: {start_date} ~ {end_date}")
            
            # 根据数据类型选择不同的Wind函数
            if data_type in ['macro']:
                # 宏观数据使用wsd函数
                result = self.w.edb(wind_code, start_date, end_date)
            elif data_type in ['index', 'industry', 'us_index']:
                # 指数数据使用wsd函数
                result = self.w.wsd(wind_code, "close", start_date, end_date)
            elif data_type in ['bond']:
                # 债券数据
                if wind_code.startswith('M'):  # 宏观类债券数据
                    result = self.w.edb(wind_code, start_date, end_date)
                else:
                    result = self.w.wsd(wind_code, "close", start_date, end_date)
            elif data_type in ['commodity']:
                # 商品期货数据
                result = self.w.wsd(wind_code, "close", start_date, end_date)
            elif data_type in ['fx']:
                # 外汇数据
                result = self.w.wsd(wind_code, "close", start_date, end_date)
            else:
                logger.error(f"不支持的数据类型: {data_type}")
                return None
            
            # 检查返回结果
            if result.ErrorCode != 0:
                logger.error(f"Wind API调用失败，错误代码: {result.ErrorCode}")
                return None
            
            # 转换为DataFrame
            if hasattr(result, 'Data') and hasattr(result, 'Times'):
                if result.Data and result.Times:
                    df = pd.DataFrame({
                        'date': result.Times,
                        'value': result.Data[0] if isinstance(result.Data[0], list) else result.Data
                    })
                    logger.info(f"成功获取 {len(df)} 条Wind数据")
                    return df
                else:
                    logger.warning("Wind返回数据为空")
                    return None
            else:
                logger.error("Wind返回结果格式异常")
                return None
                
        except Exception as e:
            logger.error(f"调用Wind API失败: {str(e)}")
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
            
            # 确保有date和value列
            if 'date' not in df.columns or 'value' not in df.columns:
                logger.error("数据缺少必要的date或value列")
                return pd.DataFrame()
            
            # 清洗日期列
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 清洗数值列
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            # 删除无效数据
            df = df.dropna(subset=['date', 'value'])
            
            # 按日期排序
            df = df.sort_values('date')
            
            # 去重（保留最新的值）
            df = df.drop_duplicates(subset=['date'], keep='last')
            
            return df
            
        except Exception as e:
            logger.error(f"Wind数据清洗失败: {str(e)}")
            return pd.DataFrame()
    
    def _save_to_database(self, indicator: Indicator, data_df: pd.DataFrame) -> int:
        """
        保存数据到数据库
        
        Args:
            indicator: 指标对象
            data_df: 清洗后的数据
            
        Returns:
            int: 保存的记录数
        """
        try:
            saved_count = 0
            
            with transaction.atomic():
                for _, row in data_df.iterrows():
                    try:
                        data_point, created = IndicatorData.objects.get_or_create(
                            indicator=indicator,
                            date=row['date'],
                            defaults={
                                'value': float(row['value']),
                                'source': 'wind',
                                'created_at': timezone.now(),
                                'updated_at': timezone.now()
                            }
                        )
                        
                        if not created:
                            # 更新现有数据
                            data_point.value = float(row['value'])
                            data_point.source = 'wind'
                            data_point.updated_at = timezone.now()
                            data_point.save()
                        
                        saved_count += 1
                        
                    except (ValueError, TypeError) as e:
                        logger.warning(f"跳过无效数据点 {row['date']}: {row['value']} - {str(e)}")
                        continue
                    except IntegrityError as e:
                        logger.warning(f"数据完整性错误 {row['date']}: {str(e)}")
                        continue
            
            return saved_count
            
        except Exception as e:
            logger.error(f"保存Wind数据到数据库失败: {str(e)}")
            return 0
    
    def get_supported_indicators(self) -> List[str]:
        """获取支持的指标列表"""
        return list(self.wind_mappings.keys())
    
    def validate_indicator_support(self, indicator_code: str) -> Tuple[bool, str]:
        """验证指标是否支持"""
        if indicator_code in self.wind_mappings:
            config = self.wind_mappings[indicator_code]
            return True, f"支持Wind代码: {config['wind_code']} - {config['description']}"
        else:
            return False, f"不支持的指标代码: {indicator_code}"
    
    def test_connection(self) -> Dict[str, Any]:
        """测试Wind连接"""
        result = {
            'connected': False,
            'error_message': '',
            'wind_version': '',
            'user_info': {}
        }
        
        try:
            if not WIND_AVAILABLE:
                result['error_message'] = "WindPy未安装"
                return result
            
            if self.connect():
                result['connected'] = True
                
                # 获取Wind版本信息
                try:
                    version_info = self.w.getVersionInfo()
                    result['wind_version'] = str(version_info)
                except:
                    result['wind_version'] = "未知版本"
                
                # 测试简单数据获取
                try:
                    test_result = self.w.edb("M0000612", "2024-01-01", "2024-01-31")  # 测试CPI数据
                    if test_result.ErrorCode == 0:
                        result['test_data'] = "数据获取测试成功"
                    else:
                        result['test_data'] = f"数据获取测试失败，错误代码: {test_result.ErrorCode}"
                except Exception as e:
                    result['test_data'] = f"数据获取测试异常: {str(e)}"
                    
            else:
                result['error_message'] = "Wind连接失败"
                
        except Exception as e:
            result['error_message'] = f"连接测试异常: {str(e)}"
        
        return result
    
    def __del__(self):
        """析构函数，确保断开连接"""
        if hasattr(self, 'connected') and self.connected:
            self.disconnect() 