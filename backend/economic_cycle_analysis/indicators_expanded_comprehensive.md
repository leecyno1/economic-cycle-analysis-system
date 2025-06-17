# 经济周期分析系统 - 指标扩充方案 2024

## 扩充目标

基于您的要求，我们将在现有指标基础上新增以下四个方面的指标：

1. **沪深300波动率指数（IVIX）**
2. **申万1级33个行业的核心指标**（每个行业3个左右）
3. **克强指数相关指标**（工业用电量、铁路货运量、银行贷款发放量、就业数据等）
4. **深入挖掘指标**（就业、北向、南向、VLCC等相关数据）

## 一、沪深300波动率指数（IVIX）

| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_IVIX | 沪深300波动率指数 | CSI 300 Volatility Index | AkShare | 日度 | ✅ 可获得 |

## 二、申万一级行业指标（31个行业 × 3个指标 = 93个指标）

### 2.1 农林牧渔
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_AGRICULTURE_INDEX | 申万农林牧渔指数 | SW Agriculture Index | AkShare |
| SW_AGRICULTURE_PE | 申万农林牧渔PE | SW Agriculture PE Ratio | AkShare |
| SW_AGRICULTURE_PB | 申万农林牧渔PB | SW Agriculture PB Ratio | AkShare |

### 2.2 基础化工
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_CHEMICAL_INDEX | 申万基础化工指数 | SW Chemical Index | AkShare |
| SW_CHEMICAL_PE | 申万基础化工PE | SW Chemical PE Ratio | AkShare |
| SW_CHEMICAL_PB | 申万基础化工PB | SW Chemical PB Ratio | AkShare |

### 2.3 钢铁
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_STEEL_INDEX | 申万钢铁指数 | SW Steel Index | AkShare |
| SW_STEEL_PE | 申万钢铁PE | SW Steel PE Ratio | AkShare |
| SW_STEEL_PB | 申万钢铁PB | SW Steel PB Ratio | AkShare |

### 2.4 有色金属
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_NONFERROUS_INDEX | 申万有色金属指数 | SW Non-ferrous Metals Index | AkShare |
| SW_NONFERROUS_PE | 申万有色金属PE | SW Non-ferrous Metals PE Ratio | AkShare |
| SW_NONFERROUS_PB | 申万有色金属PB | SW Non-ferrous Metals PB Ratio | AkShare |

### 2.5 电子
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_ELECTRONICS_INDEX | 申万电子指数 | SW Electronics Index | AkShare |
| SW_ELECTRONICS_PE | 申万电子PE | SW Electronics PE Ratio | AkShare |
| SW_ELECTRONICS_PB | 申万电子PB | SW Electronics PB Ratio | AkShare |

### 2.6 家用电器
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_APPLIANCES_INDEX | 申万家用电器指数 | SW Home Appliances Index | AkShare |
| SW_APPLIANCES_PE | 申万家用电器PE | SW Home Appliances PE Ratio | AkShare |
| SW_APPLIANCES_PB | 申万家用电器PB | SW Home Appliances PB Ratio | AkShare |

### 2.7 食品饮料
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_FOOD_BEVERAGE_INDEX | 申万食品饮料指数 | SW Food & Beverage Index | AkShare |
| SW_FOOD_BEVERAGE_PE | 申万食品饮料PE | SW Food & Beverage PE Ratio | AkShare |
| SW_FOOD_BEVERAGE_PB | 申万食品饮料PB | SW Food & Beverage PB Ratio | AkShare |

### 2.8 纺织服饰
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_TEXTILE_INDEX | 申万纺织服饰指数 | SW Textile & Apparel Index | AkShare |
| SW_TEXTILE_PE | 申万纺织服饰PE | SW Textile & Apparel PE Ratio | AkShare |
| SW_TEXTILE_PB | 申万纺织服饰PB | SW Textile & Apparel PB Ratio | AkShare |

### 2.9 轻工制造
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_LIGHT_INDUSTRY_INDEX | 申万轻工制造指数 | SW Light Industry Index | AkShare |
| SW_LIGHT_INDUSTRY_PE | 申万轻工制造PE | SW Light Industry PE Ratio | AkShare |
| SW_LIGHT_INDUSTRY_PB | 申万轻工制造PB | SW Light Industry PB Ratio | AkShare |

### 2.10 医药生物
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_PHARMACEUTICAL_INDEX | 申万医药生物指数 | SW Pharmaceutical Index | AkShare |
| SW_PHARMACEUTICAL_PE | 申万医药生物PE | SW Pharmaceutical PE Ratio | AkShare |
| SW_PHARMACEUTICAL_PB | 申万医药生物PB | SW Pharmaceutical PB Ratio | AkShare |

### 2.11 公用事业
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_UTILITIES_INDEX | 申万公用事业指数 | SW Utilities Index | AkShare |
| SW_UTILITIES_PE | 申万公用事业PE | SW Utilities PE Ratio | AkShare |
| SW_UTILITIES_PB | 申万公用事业PB | SW Utilities PB Ratio | AkShare |

### 2.12 交通运输
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_TRANSPORTATION_INDEX | 申万交通运输指数 | SW Transportation Index | AkShare |
| SW_TRANSPORTATION_PE | 申万交通运输PE | SW Transportation PE Ratio | AkShare |
| SW_TRANSPORTATION_PB | 申万交通运输PB | SW Transportation PB Ratio | AkShare |

### 2.13 房地产
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_REAL_ESTATE_INDEX | 申万房地产指数 | SW Real Estate Index | AkShare |
| SW_REAL_ESTATE_PE | 申万房地产PE | SW Real Estate PE Ratio | AkShare |
| SW_REAL_ESTATE_PB | 申万房地产PB | SW Real Estate PB Ratio | AkShare |

### 2.14 商贸零售
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_RETAIL_INDEX | 申万商贸零售指数 | SW Retail Index | AkShare |
| SW_RETAIL_PE | 申万商贸零售PE | SW Retail PE Ratio | AkShare |
| SW_RETAIL_PB | 申万商贸零售PB | SW Retail PB Ratio | AkShare |

### 2.15 社会服务
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_SOCIAL_SERVICE_INDEX | 申万社会服务指数 | SW Social Service Index | AkShare |
| SW_SOCIAL_SERVICE_PE | 申万社会服务PE | SW Social Service PE Ratio | AkShare |
| SW_SOCIAL_SERVICE_PB | 申万社会服务PB | SW Social Service PB Ratio | AkShare |

### 2.16 综合
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_COMPREHENSIVE_INDEX | 申万综合指数 | SW Comprehensive Index | AkShare |
| SW_COMPREHENSIVE_PE | 申万综合PE | SW Comprehensive PE Ratio | AkShare |
| SW_COMPREHENSIVE_PB | 申万综合PB | SW Comprehensive PB Ratio | AkShare |

### 2.17 建筑材料
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_BUILDING_MATERIALS_INDEX | 申万建筑材料指数 | SW Building Materials Index | AkShare |
| SW_BUILDING_MATERIALS_PE | 申万建筑材料PE | SW Building Materials PE Ratio | AkShare |
| SW_BUILDING_MATERIALS_PB | 申万建筑材料PB | SW Building Materials PB Ratio | AkShare |

### 2.18 建筑装饰
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_CONSTRUCTION_INDEX | 申万建筑装饰指数 | SW Construction Index | AkShare |
| SW_CONSTRUCTION_PE | 申万建筑装饰PE | SW Construction PE Ratio | AkShare |
| SW_CONSTRUCTION_PB | 申万建筑装饰PB | SW Construction PB Ratio | AkShare |

### 2.19 电力设备
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_POWER_EQUIPMENT_INDEX | 申万电力设备指数 | SW Power Equipment Index | AkShare |
| SW_POWER_EQUIPMENT_PE | 申万电力设备PE | SW Power Equipment PE Ratio | AkShare |
| SW_POWER_EQUIPMENT_PB | 申万电力设备PB | SW Power Equipment PB Ratio | AkShare |

### 2.20 机械设备
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_MACHINERY_INDEX | 申万机械设备指数 | SW Machinery Index | AkShare |
| SW_MACHINERY_PE | 申万机械设备PE | SW Machinery PE Ratio | AkShare |
| SW_MACHINERY_PB | 申万机械设备PB | SW Machinery PB Ratio | AkShare |

### 2.21 国防军工
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_DEFENSE_INDEX | 申万国防军工指数 | SW Defense Index | AkShare |
| SW_DEFENSE_PE | 申万国防军工PE | SW Defense PE Ratio | AkShare |
| SW_DEFENSE_PB | 申万国防军工PB | SW Defense PB Ratio | AkShare |

### 2.22 汽车
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_AUTOMOTIVE_INDEX | 申万汽车指数 | SW Automotive Index | AkShare |
| SW_AUTOMOTIVE_PE | 申万汽车PE | SW Automotive PE Ratio | AkShare |
| SW_AUTOMOTIVE_PB | 申万汽车PB | SW Automotive PB Ratio | AkShare |

### 2.23 计算机
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_COMPUTER_INDEX | 申万计算机指数 | SW Computer Index | AkShare |
| SW_COMPUTER_PE | 申万计算机PE | SW Computer PE Ratio | AkShare |
| SW_COMPUTER_PB | 申万计算机PB | SW Computer PB Ratio | AkShare |

### 2.24 传媒
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_MEDIA_INDEX | 申万传媒指数 | SW Media Index | AkShare |
| SW_MEDIA_PE | 申万传媒PE | SW Media PE Ratio | AkShare |
| SW_MEDIA_PB | 申万传媒PB | SW Media PB Ratio | AkShare |

### 2.25 通信
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_TELECOM_INDEX | 申万通信指数 | SW Telecom Index | AkShare |
| SW_TELECOM_PE | 申万通信PE | SW Telecom PE Ratio | AkShare |
| SW_TELECOM_PB | 申万通信PB | SW Telecom PB Ratio | AkShare |

### 2.26 银行
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_BANKING_INDEX | 申万银行指数 | SW Banking Index | AkShare |
| SW_BANKING_PE | 申万银行PE | SW Banking PE Ratio | AkShare |
| SW_BANKING_PB | 申万银行PB | SW Banking PB Ratio | AkShare |

### 2.27 非银金融
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_NONBANK_FINANCE_INDEX | 申万非银金融指数 | SW Non-bank Finance Index | AkShare |
| SW_NONBANK_FINANCE_PE | 申万非银金融PE | SW Non-bank Finance PE Ratio | AkShare |
| SW_NONBANK_FINANCE_PB | 申万非银金融PB | SW Non-bank Finance PB Ratio | AkShare |

### 2.28 煤炭
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_COAL_INDEX | 申万煤炭指数 | SW Coal Index | AkShare |
| SW_COAL_PE | 申万煤炭PE | SW Coal PE Ratio | AkShare |
| SW_COAL_PB | 申万煤炭PB | SW Coal PB Ratio | AkShare |

### 2.29 石油石化
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_PETROCHEMICAL_INDEX | 申万石油石化指数 | SW Petrochemical Index | AkShare |
| SW_PETROCHEMICAL_PE | 申万石油石化PE | SW Petrochemical PE Ratio | AkShare |
| SW_PETROCHEMICAL_PB | 申万石油石化PB | SW Petrochemical PB Ratio | AkShare |

### 2.30 环保
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_ENVIRONMENTAL_INDEX | 申万环保指数 | SW Environmental Index | AkShare |
| SW_ENVIRONMENTAL_PE | 申万环保PE | SW Environmental PE Ratio | AkShare |
| SW_ENVIRONMENTAL_PB | 申万环保PB | SW Environmental PB Ratio | AkShare |

### 2.31 美容护理
| 指标代码 | 中文名称 | 英文名称 | 数据源 |
|---------|---------|---------|--------|
| SW_BEAUTY_INDEX | 申万美容护理指数 | SW Beauty & Personal Care Index | AkShare |
| SW_BEAUTY_PE | 申万美容护理PE | SW Beauty & Personal Care PE Ratio | AkShare |
| SW_BEAUTY_PB | 申万美容护理PB | SW Beauty & Personal Care PB Ratio | AkShare |

## 三、克强指数相关指标（15个指标）

### 3.1 传统克强指数
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_ELECTRICITY_CONSUMPTION | 全社会用电量 | Total Electricity Consumption | 国家统计局 | 月度 | ✅ 可获得 |
| CN_RAILWAY_FREIGHT | 铁路货运量 | Railway Freight Volume | 国家统计局 | 月度 | ✅ 可获得 |
| CN_BANK_LOANS | 银行贷款发放量 | Bank Loan Disbursement | 央行 | 月度 | ✅ 可获得 |

### 3.2 新克强指数
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_URBAN_EMPLOYMENT | 城镇新增就业人数 | Urban New Employment | 人社部 | 月度 | ✅ 可获得 |
| CN_DISPOSABLE_INCOME | 居民人均可支配收入 | Per Capita Disposable Income | 国家统计局 | 季度 | ✅ 可获得 |
| CN_ENERGY_INTENSITY | 单位GDP能耗 | Energy Intensity per GDP | 国家统计局 | 季度 | ✅ 可获得 |

### 3.3 扩展克强指数
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_INDUSTRIAL_ELECTRICITY | 工业用电量 | Industrial Electricity Consumption | 国家统计局 | 月度 | ✅ 可获得 |
| CN_HIGHWAY_FREIGHT | 公路货运量 | Highway Freight Volume | 交通部 | 月度 | ✅ 可获得 |
| CN_WATERWAY_FREIGHT | 水路货运量 | Waterway Freight Volume | 交通部 | 月度 | ✅ 可获得 |
| CN_AVIATION_FREIGHT | 民航货运量 | Aviation Freight Volume | 民航局 | 月度 | ✅ 可获得 |
| CN_EXPRESS_DELIVERY | 快递业务量 | Express Delivery Volume | 邮政局 | 月度 | ✅ 可获得 |
| CN_MOBILE_PAYMENT | 移动支付交易额 | Mobile Payment Volume | 央行 | 月度 | ✅ 可获得 |
| CN_INTERNET_USERS | 互联网用户数 | Internet Users | 工信部 | 季度 | ✅ 可获得 |
| CN_DIGITAL_ECONOMY | 数字经济规模 | Digital Economy Scale | 工信部 | 年度 | ✅ 可获得 |
| CN_CARBON_EMISSIONS | 碳排放量 | Carbon Emissions | 生态环境部 | 季度 | ⚠️ 部分可获得 |

## 四、深入挖掘指标（50个指标）

### 4.1 就业深度指标（15个）
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_DELIVERY_WORKERS | 外卖配送员数量 | Food Delivery Workers | 美团/饿了么 | 月度 | ⚠️ 第三方数据 |
| CN_RIDE_HAILING_DRIVERS | 网约车司机数量 | Ride-hailing Drivers | 滴滴/高德 | 月度 | ⚠️ 第三方数据 |
| CN_LIVE_STREAMING_HOSTS | 直播主播数量 | Live Streaming Hosts | 抖音/快手 | 月度 | ⚠️ 第三方数据 |
| CN_ONLINE_TUTORS | 在线教师数量 | Online Tutors | 教育平台 | 月度 | ⚠️ 第三方数据 |
| CN_FREELANCERS | 自由职业者数量 | Freelancers | 人社部 | 季度 | ✅ 可获得 |
| CN_MIGRANT_WORKERS | 农民工数量 | Migrant Workers | 国家统计局 | 年度 | ✅ 可获得 |
| CN_COLLEGE_GRADUATES | 高校毕业生数量 | College Graduates | 教育部 | 年度 | ✅ 可获得 |
| CN_STARTUP_COMPANIES | 新注册企业数量 | New Registered Companies | 市场监管总局 | 月度 | ✅ 可获得 |
| CN_BANKRUPTCY_COMPANIES | 企业注销数量 | Company Bankruptcies | 市场监管总局 | 月度 | ✅ 可获得 |
| CN_SOCIAL_INSURANCE | 社保参保人数 | Social Insurance Participants | 人社部 | 月度 | ✅ 可获得 |
| CN_UNEMPLOYMENT_INSURANCE | 失业保险金申领人数 | Unemployment Insurance Claims | 人社部 | 月度 | ✅ 可获得 |
| CN_JOB_VACANCIES | 职位空缺数量 | Job Vacancies | 人社部 | 月度 | ✅ 可获得 |
| CN_RECRUITMENT_INDEX | 招聘景气指数 | Recruitment Prosperity Index | 智联招聘 | 季度 | ⚠️ 第三方数据 |
| CN_SALARY_INDEX | 平均薪资指数 | Average Salary Index | 智联招聘 | 季度 | ⚠️ 第三方数据 |
| CN_LABOR_SHORTAGE | 用工荒指数 | Labor Shortage Index | 人社部 | 季度 | ✅ 可获得 |

### 4.2 北向资金深度指标（10个）
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_NORTHBOUND_FLOW | 北向资金净流入 | Northbound Capital Flow | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_HOLDINGS | 北向资金持股市值 | Northbound Holdings Value | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_TOP10 | 北向资金前十大持股 | Northbound Top 10 Holdings | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_SECTOR | 北向资金行业配置 | Northbound Sector Allocation | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_TURNOVER | 北向资金换手率 | Northbound Turnover Rate | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_PREMIUM | 北向资金溢价率 | Northbound Premium Rate | AkShare | 日度 | ✅ 可获得 |
| CN_NORTHBOUND_VOLATILITY | 北向资金波动率 | Northbound Volatility | 计算指标 | 日度 | ✅ 可计算 |
| CN_NORTHBOUND_MOMENTUM | 北向资金动量指标 | Northbound Momentum | 计算指标 | 日度 | ✅ 可计算 |
| CN_NORTHBOUND_CONCENTRATION | 北向资金集中度 | Northbound Concentration | 计算指标 | 日度 | ✅ 可计算 |
| CN_NORTHBOUND_SENTIMENT | 北向资金情绪指数 | Northbound Sentiment Index | 计算指标 | 日度 | ✅ 可计算 |

### 4.3 南向资金深度指标（10个）
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| CN_SOUTHBOUND_FLOW | 南向资金净流入 | Southbound Capital Flow | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_HOLDINGS | 南向资金持股市值 | Southbound Holdings Value | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_TOP10 | 南向资金前十大持股 | Southbound Top 10 Holdings | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_SECTOR | 南向资金行业配置 | Southbound Sector Allocation | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_TURNOVER | 南向资金换手率 | Southbound Turnover Rate | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_PREMIUM | 南向资金溢价率 | Southbound Premium Rate | AkShare | 日度 | ✅ 可获得 |
| CN_SOUTHBOUND_VOLATILITY | 南向资金波动率 | Southbound Volatility | 计算指标 | 日度 | ✅ 可计算 |
| CN_SOUTHBOUND_MOMENTUM | 南向资金动量指标 | Southbound Momentum | 计算指标 | 日度 | ✅ 可计算 |
| CN_SOUTHBOUND_CONCENTRATION | 南向资金集中度 | Southbound Concentration | 计算指标 | 日度 | ✅ 可计算 |
| CN_SOUTHBOUND_SENTIMENT | 南向资金情绪指数 | Southbound Sentiment Index | 计算指标 | 日度 | ✅ 可计算 |

### 4.4 VLCC及航运深度指标（15个）
| 指标代码 | 中文名称 | 英文名称 | 数据源 | 频率 | 可获得性 |
|---------|---------|---------|--------|------|----------|
| GLOBAL_VLCC_RATE | VLCC运价指数 | VLCC Freight Rate | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BDI | 波罗的海干散货指数 | Baltic Dry Index | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BCI | 波罗的海海岬型指数 | Baltic Capesize Index | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BPI | 波罗的海巴拿马型指数 | Baltic Panamax Index | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BSI | 波罗的海超灵便型指数 | Baltic Supramax Index | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BHSI | 波罗的海灵便型指数 | Baltic Handysize Index | AkShare | 日度 | ✅ 可获得 |
| CN_PORT_THROUGHPUT | 中国港口吞吐量 | China Port Throughput | 交通部 | 月度 | ✅ 可获得 |
| CN_CONTAINER_THROUGHPUT | 中国集装箱吞吐量 | China Container Throughput | 交通部 | 月度 | ✅ 可获得 |
| CN_COASTAL_SHIPPING | 中国沿海货运量 | China Coastal Shipping | 交通部 | 月度 | ✅ 可获得 |
| CN_INLAND_SHIPPING | 中国内河货运量 | China Inland Shipping | 交通部 | 月度 | ✅ 可获得 |
| GLOBAL_SHIP_ORDERS | 全球新船订单 | Global Ship Orders | Clarksons | 月度 | ⚠️ 付费数据 |
| GLOBAL_SHIP_DELIVERIES | 全球新船交付 | Global Ship Deliveries | Clarksons | 月度 | ⚠️ 付费数据 |
| GLOBAL_SCRAP_STEEL | 全球废钢价格 | Global Scrap Steel Price | AkShare | 日度 | ✅ 可获得 |
| GLOBAL_BUNKER_FUEL | 全球船用燃油价格 | Global Bunker Fuel Price | AkShare | 日度 | ✅ 可获得 |
| CN_SHIPPING_CONFIDENCE | 中国航运信心指数 | China Shipping Confidence Index | 上海航运交易所 | 月度 | ✅ 可获得 |

## 五、数据获取可行性分析

### 5.1 高可获得性指标（✅）
- **申万行业指数**：AkShare提供完整的申万行业指数数据
- **克强指数传统指标**：国家统计局、央行等官方数据源
- **北向南向资金**：AkShare提供实时数据
- **航运指数**：AkShare提供主要航运指数

### 5.2 部分可获得性指标（⚠️）
- **新经济就业数据**：需要通过第三方平台API获取
- **碳排放数据**：官方数据更新频率较低
- **航运详细数据**：部分需要付费数据源

### 5.3 数据获取策略
1. **优先级1**：使用AkShare和官方数据源的高可获得性指标
2. **优先级2**：通过计算衍生的指标
3. **优先级3**：探索第三方数据源的可行性

## 六、实施计划

### 阶段1：核心指标实现（1-2周）
- 沪深300波动率指数
- 申万31个行业的指数、PE、PB
- 传统克强指数3个指标

### 阶段2：扩展指标实现（2-3周）
- 新克强指数和扩展克强指数
- 北向南向资金深度指标
- 主要航运指数

### 阶段3：深度挖掘指标（3-4周）
- 就业深度指标（官方数据部分）
- VLCC及航运深度指标
- 计算衍生指标

### 阶段4：第三方数据探索（4-5周）
- 新经济就业数据
- 付费航运数据
- 数据质量验证和清洗

## 七、技术实现要点

### 7.1 数据采集
- 扩展现有的AkShare数据采集器
- 新增官方统计数据采集器
- 实现第三方API数据采集器

### 7.2 数据处理
- 统一数据频率转换
- 缺失数据插值处理
- 异常数据检测和清洗

### 7.3 计算指标
- 实现波动率、动量等技术指标计算
- 实现集中度、情绪指数等复合指标计算
- 建立指标依赖关系管理

### 7.4 数据存储
- 扩展数据库表结构
- 优化数据查询性能
- 实现数据版本管理

## 总结

本扩充方案将新增约**159个指标**：
- 沪深300波动率指数：1个
- 申万行业指标：93个（31行业×3指标）
- 克强指数相关：15个
- 深入挖掘指标：50个

这将使系统总指标数量从现有的117个增加到**276个指标**，大幅提升系统的分析深度和广度，为经济周期分析提供更全面的数据支撑。 