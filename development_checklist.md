# 经济周期分析系统开发检查清单

## 第一阶段：核心指标
**目标：** 230个指标
**周期：** 3-4周
**重点：** TMT、周期、消费行业主要指标
**交付：** 基础数据获取和存储

### 优先指标列表
- [ ] 通信设备制造业PPI (`TMT_COMM_OPTICAL_MODULE_PPI`)
  - 数据源: akshare
  - API函数: macro_china_ppi
  - 数据可用性: high
  - 重要程度: ★★★★
- [ ] 集成电路产量 (`TMT_ELEC_IC_PRODUCTION`)
  - 数据源: akshare
  - API函数: macro_china_industrial_production_yoy
  - 数据可用性: high
  - 重要程度: ★★★★★
- [ ] 纯碱产量 (`CYCLE_CHEM_SODA_ASH_PRODUCTION`)
  - 数据源: akshare
  - API函数: macro_china_industrial_production_yoy
  - 数据可用性: high
  - 重要程度: ★★★★
- [ ] 环渤海动力煤价格 (`CYCLE_COAL_THERMAL_PRICE`)
  - 数据源: akshare
  - API函数: energy_oil_hist
  - 数据可用性: high
  - 重要程度: ★★★★★
- [ ] 快递业务量 (`CYCLE_TRANSPORT_EXPRESS_DELIVERY`)
  - 数据源: akshare
  - API函数: macro_china_postal_telecommunicational
  - 数据可用性: high
  - 重要程度: ★★★★
- [ ] 稻米价格 (`CONSUMER_AGRI_RICE_PRICE`)
  - 数据源: akshare
  - API函数: futures_main_sina
  - 数据可用性: high
  - 重要程度: ★★★★
- [ ] 挖掘机销量 (`MFG_MACHINERY_EXCAVATOR_SALES`)
  - 数据源: calculated
  - API函数: macro_china_industrial_production_yoy
  - 数据可用性: medium
  - 重要程度: ★★★★★

## 第二阶段：扩展指标
**目标：** 834个指标
**周期：** 4-5周
**重点：** 完善各行业指标体系
**交付：** 完整的行业指标数据库

### 优先指标列表
- [ ] 笔记本电脑销量 (`TMT_ELEC_LAPTOP_SALES`)
  - 数据源: calculated
  - API函数: macro_china_retail_total
  - 数据可用性: medium
  - 重要程度: ★★★
- [ ] 化学农药原药产量 (`CYCLE_CHEM_PESTICIDE_PRODUCTION`)
  - 数据源: akshare
  - API函数: macro_china_industrial_production_yoy
  - 数据可用性: high
  - 重要程度: ★★★
- [ ] 零食坚果特产销售额 (`CONSUMER_FOOD_SNACK_SALES`)
  - 数据源: calculated
  - API函数: macro_china_retail_total
  - 数据可用性: medium
  - 重要程度: ★★★
- [ ] 起重机销量 (`MFG_MACHINERY_CRANE_SALES`)
  - 数据源: calculated
  - API函数: macro_china_industrial_production_yoy
  - 数据可用性: medium
  - 重要程度: ★★★★
- [ ] 电力工程投资完成额 (`MFG_POWER_INVESTMENT`)
  - 数据源: akshare
  - API函数: macro_china_fixed_asset_investment
  - 数据可用性: high
  - 重要程度: ★★★
- [ ] 医疗保健CPI (`PHARMA_HEALTHCARE_CPI`)
  - 数据源: akshare
  - API函数: macro_china_cpi
  - 数据可用性: high
  - 重要程度: ★★★
- [ ] 原保险保费收入 (`FINANCE_INSURANCE_PREMIUM`)
  - 数据源: akshare
  - API函数: macro_china_insurance
  - 数据可用性: high
  - 重要程度: ★★★

## 第三阶段：增强指标
**目标：** 144个指标
**周期：** 3-4周
**重点：** 计算指标和综合指数
**交付：** 完整的指标分析系统

### 优先指标列表
- [ ] 印刷业用电量 (`CONSUMER_LIGHT_PRINTING_ELECTRICITY`)
  - 数据源: calculated
  - API函数: energy_oil_detail
  - 数据可用性: medium
  - 重要程度: ★★
- [ ] TMT行业景气度指数 (`CALC_TMT_PROSPERITY_INDEX`)
  - 数据源: calculated
  - API函数: weighted_composite
  - 数据可用性: 依赖组成指标
  - 重要程度: ★★★★★
- [ ] 周期行业景气度指数 (`CALC_CYCLICAL_PROSPERITY_INDEX`)
  - 数据源: calculated
  - API函数: weighted_composite
  - 数据可用性: 依赖组成指标
  - 重要程度: ★★★★★
- [ ] 建筑产业链指数 (`CALC_SUPPLY_CHAIN_CONSTRUCTION`)
  - 数据源: calculated
  - API函数: supply_chain_composite
  - 数据可用性: 依赖组成指标
  - 重要程度: ★★★★
- [ ] 行业价格传导指数 (`CALC_PRICE_TRANSMISSION_INDEX`)
  - 数据源: calculated
  - API函数: price_transmission_composite
  - 数据可用性: 依赖组成指标
  - 重要程度: ★★★★
