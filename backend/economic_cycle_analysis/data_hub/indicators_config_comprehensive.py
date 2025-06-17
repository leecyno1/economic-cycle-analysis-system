# 经济周期分析系统 - 综合指标配置
# 包含：IVIX、申万行业、克强指数、深度挖掘指标

# 1. 沪深300波动率指数
IVIX_INDICATORS = {
    'CN_IVIX': {
        'name_cn': '沪深300波动率指数',
        'name_en': 'CSI 300 Volatility Index',
        'category': '市场情绪面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'index_vix_hs300',
        'unit': '点',
        'description': '反映沪深300指数期权隐含波动率的指标'
    }
}

# 2. 申万一级行业指标（31个行业 × 3个指标 = 93个）
SW_INDUSTRY_INDICATORS = {
    # 农林牧渔
    'SW_AGRICULTURE_INDEX': {'name_cn': '申万农林牧渔指数', 'name_en': 'SW Agriculture Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_AGRICULTURE_PE': {'name_cn': '申万农林牧渔PE', 'name_en': 'SW Agriculture PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_AGRICULTURE_PB': {'name_cn': '申万农林牧渔PB', 'name_en': 'SW Agriculture PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 基础化工
    'SW_CHEMICAL_INDEX': {'name_cn': '申万基础化工指数', 'name_en': 'SW Chemical Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_CHEMICAL_PE': {'name_cn': '申万基础化工PE', 'name_en': 'SW Chemical PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_CHEMICAL_PB': {'name_cn': '申万基础化工PB', 'name_en': 'SW Chemical PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 钢铁
    'SW_STEEL_INDEX': {'name_cn': '申万钢铁指数', 'name_en': 'SW Steel Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_STEEL_PE': {'name_cn': '申万钢铁PE', 'name_en': 'SW Steel PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_STEEL_PB': {'name_cn': '申万钢铁PB', 'name_en': 'SW Steel PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 有色金属
    'SW_NONFERROUS_INDEX': {'name_cn': '申万有色金属指数', 'name_en': 'SW Non-ferrous Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_NONFERROUS_PE': {'name_cn': '申万有色金属PE', 'name_en': 'SW Non-ferrous PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_NONFERROUS_PB': {'name_cn': '申万有色金属PB', 'name_en': 'SW Non-ferrous PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 电子
    'SW_ELECTRONICS_INDEX': {'name_cn': '申万电子指数', 'name_en': 'SW Electronics Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_ELECTRONICS_PE': {'name_cn': '申万电子PE', 'name_en': 'SW Electronics PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_ELECTRONICS_PB': {'name_cn': '申万电子PB', 'name_en': 'SW Electronics PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 家用电器
    'SW_APPLIANCES_INDEX': {'name_cn': '申万家用电器指数', 'name_en': 'SW Appliances Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_APPLIANCES_PE': {'name_cn': '申万家用电器PE', 'name_en': 'SW Appliances PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_APPLIANCES_PB': {'name_cn': '申万家用电器PB', 'name_en': 'SW Appliances PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 食品饮料
    'SW_FOOD_BEVERAGE_INDEX': {'name_cn': '申万食品饮料指数', 'name_en': 'SW Food Beverage Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_FOOD_BEVERAGE_PE': {'name_cn': '申万食品饮料PE', 'name_en': 'SW Food Beverage PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_FOOD_BEVERAGE_PB': {'name_cn': '申万食品饮料PB', 'name_en': 'SW Food Beverage PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 纺织服饰
    'SW_TEXTILE_INDEX': {'name_cn': '申万纺织服饰指数', 'name_en': 'SW Textile Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_TEXTILE_PE': {'name_cn': '申万纺织服饰PE', 'name_en': 'SW Textile PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_TEXTILE_PB': {'name_cn': '申万纺织服饰PB', 'name_en': 'SW Textile PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 轻工制造
    'SW_LIGHT_INDUSTRY_INDEX': {'name_cn': '申万轻工制造指数', 'name_en': 'SW Light Industry Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_LIGHT_INDUSTRY_PE': {'name_cn': '申万轻工制造PE', 'name_en': 'SW Light Industry PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_LIGHT_INDUSTRY_PB': {'name_cn': '申万轻工制造PB', 'name_en': 'SW Light Industry PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 医药生物
    'SW_PHARMACEUTICAL_INDEX': {'name_cn': '申万医药生物指数', 'name_en': 'SW Pharmaceutical Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_PHARMACEUTICAL_PE': {'name_cn': '申万医药生物PE', 'name_en': 'SW Pharmaceutical PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_PHARMACEUTICAL_PB': {'name_cn': '申万医药生物PB', 'name_en': 'SW Pharmaceutical PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 公用事业
    'SW_UTILITIES_INDEX': {'name_cn': '申万公用事业指数', 'name_en': 'SW Utilities Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_UTILITIES_PE': {'name_cn': '申万公用事业PE', 'name_en': 'SW Utilities PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_UTILITIES_PB': {'name_cn': '申万公用事业PB', 'name_en': 'SW Utilities PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 交通运输
    'SW_TRANSPORTATION_INDEX': {'name_cn': '申万交通运输指数', 'name_en': 'SW Transportation Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_TRANSPORTATION_PE': {'name_cn': '申万交通运输PE', 'name_en': 'SW Transportation PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_TRANSPORTATION_PB': {'name_cn': '申万交通运输PB', 'name_en': 'SW Transportation PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 房地产
    'SW_REAL_ESTATE_INDEX': {'name_cn': '申万房地产指数', 'name_en': 'SW Real Estate Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_REAL_ESTATE_PE': {'name_cn': '申万房地产PE', 'name_en': 'SW Real Estate PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_REAL_ESTATE_PB': {'name_cn': '申万房地产PB', 'name_en': 'SW Real Estate PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 商贸零售
    'SW_RETAIL_INDEX': {'name_cn': '申万商贸零售指数', 'name_en': 'SW Retail Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_RETAIL_PE': {'name_cn': '申万商贸零售PE', 'name_en': 'SW Retail PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_RETAIL_PB': {'name_cn': '申万商贸零售PB', 'name_en': 'SW Retail PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 社会服务
    'SW_SOCIAL_SERVICE_INDEX': {'name_cn': '申万社会服务指数', 'name_en': 'SW Social Service Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_SOCIAL_SERVICE_PE': {'name_cn': '申万社会服务PE', 'name_en': 'SW Social Service PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_SOCIAL_SERVICE_PB': {'name_cn': '申万社会服务PB', 'name_en': 'SW Social Service PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 综合
    'SW_COMPREHENSIVE_INDEX': {'name_cn': '申万综合指数', 'name_en': 'SW Comprehensive Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_COMPREHENSIVE_PE': {'name_cn': '申万综合PE', 'name_en': 'SW Comprehensive PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_COMPREHENSIVE_PB': {'name_cn': '申万综合PB', 'name_en': 'SW Comprehensive PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 建筑材料
    'SW_BUILDING_MATERIALS_INDEX': {'name_cn': '申万建筑材料指数', 'name_en': 'SW Building Materials Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_BUILDING_MATERIALS_PE': {'name_cn': '申万建筑材料PE', 'name_en': 'SW Building Materials PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_BUILDING_MATERIALS_PB': {'name_cn': '申万建筑材料PB', 'name_en': 'SW Building Materials PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 建筑装饰
    'SW_CONSTRUCTION_INDEX': {'name_cn': '申万建筑装饰指数', 'name_en': 'SW Construction Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_CONSTRUCTION_PE': {'name_cn': '申万建筑装饰PE', 'name_en': 'SW Construction PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_CONSTRUCTION_PB': {'name_cn': '申万建筑装饰PB', 'name_en': 'SW Construction PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 电力设备
    'SW_POWER_EQUIPMENT_INDEX': {'name_cn': '申万电力设备指数', 'name_en': 'SW Power Equipment Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_POWER_EQUIPMENT_PE': {'name_cn': '申万电力设备PE', 'name_en': 'SW Power Equipment PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_POWER_EQUIPMENT_PB': {'name_cn': '申万电力设备PB', 'name_en': 'SW Power Equipment PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 机械设备
    'SW_MACHINERY_INDEX': {'name_cn': '申万机械设备指数', 'name_en': 'SW Machinery Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_MACHINERY_PE': {'name_cn': '申万机械设备PE', 'name_en': 'SW Machinery PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_MACHINERY_PB': {'name_cn': '申万机械设备PB', 'name_en': 'SW Machinery PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 国防军工
    'SW_DEFENSE_INDEX': {'name_cn': '申万国防军工指数', 'name_en': 'SW Defense Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_DEFENSE_PE': {'name_cn': '申万国防军工PE', 'name_en': 'SW Defense PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_DEFENSE_PB': {'name_cn': '申万国防军工PB', 'name_en': 'SW Defense PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 汽车
    'SW_AUTOMOTIVE_INDEX': {'name_cn': '申万汽车指数', 'name_en': 'SW Automotive Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_AUTOMOTIVE_PE': {'name_cn': '申万汽车PE', 'name_en': 'SW Automotive PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_AUTOMOTIVE_PB': {'name_cn': '申万汽车PB', 'name_en': 'SW Automotive PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 计算机
    'SW_COMPUTER_INDEX': {'name_cn': '申万计算机指数', 'name_en': 'SW Computer Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_COMPUTER_PE': {'name_cn': '申万计算机PE', 'name_en': 'SW Computer PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_COMPUTER_PB': {'name_cn': '申万计算机PB', 'name_en': 'SW Computer PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 传媒
    'SW_MEDIA_INDEX': {'name_cn': '申万传媒指数', 'name_en': 'SW Media Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_MEDIA_PE': {'name_cn': '申万传媒PE', 'name_en': 'SW Media PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_MEDIA_PB': {'name_cn': '申万传媒PB', 'name_en': 'SW Media PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 通信
    'SW_TELECOM_INDEX': {'name_cn': '申万通信指数', 'name_en': 'SW Telecom Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_TELECOM_PE': {'name_cn': '申万通信PE', 'name_en': 'SW Telecom PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_TELECOM_PB': {'name_cn': '申万通信PB', 'name_en': 'SW Telecom PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 银行
    'SW_BANKING_INDEX': {'name_cn': '申万银行指数', 'name_en': 'SW Banking Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_BANKING_PE': {'name_cn': '申万银行PE', 'name_en': 'SW Banking PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_BANKING_PB': {'name_cn': '申万银行PB', 'name_en': 'SW Banking PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 非银金融
    'SW_NONBANK_FINANCE_INDEX': {'name_cn': '申万非银金融指数', 'name_en': 'SW Non-bank Finance Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_NONBANK_FINANCE_PE': {'name_cn': '申万非银金融PE', 'name_en': 'SW Non-bank Finance PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_NONBANK_FINANCE_PB': {'name_cn': '申万非银金融PB', 'name_en': 'SW Non-bank Finance PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 煤炭
    'SW_COAL_INDEX': {'name_cn': '申万煤炭指数', 'name_en': 'SW Coal Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_COAL_PE': {'name_cn': '申万煤炭PE', 'name_en': 'SW Coal PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_COAL_PB': {'name_cn': '申万煤炭PB', 'name_en': 'SW Coal PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 石油石化
    'SW_PETROCHEMICAL_INDEX': {'name_cn': '申万石油石化指数', 'name_en': 'SW Petrochemical Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_PETROCHEMICAL_PE': {'name_cn': '申万石油石化PE', 'name_en': 'SW Petrochemical PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_PETROCHEMICAL_PB': {'name_cn': '申万石油石化PB', 'name_en': 'SW Petrochemical PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 环保
    'SW_ENVIRONMENTAL_INDEX': {'name_cn': '申万环保指数', 'name_en': 'SW Environmental Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_ENVIRONMENTAL_PE': {'name_cn': '申万环保PE', 'name_en': 'SW Environmental PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_ENVIRONMENTAL_PB': {'name_cn': '申万环保PB', 'name_en': 'SW Environmental PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
    
    # 美容护理
    'SW_BEAUTY_INDEX': {'name_cn': '申万美容护理指数', 'name_en': 'SW Beauty Index', 'category': '行业面', 'api_function': 'sw_index_spot'},
    'SW_BEAUTY_PE': {'name_cn': '申万美容护理PE', 'name_en': 'SW Beauty PE', 'category': '行业面', 'api_function': 'sw_index_pe'},
    'SW_BEAUTY_PB': {'name_cn': '申万美容护理PB', 'name_en': 'SW Beauty PB', 'category': '行业面', 'api_function': 'sw_index_pb'},
}

# 3. 克强指数相关指标
KEQIANG_INDICATORS = {
    # 传统克强指数
    'CN_ELECTRICITY_CONSUMPTION': {
        'name_cn': '全社会用电量',
        'name_en': 'Total Electricity Consumption',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'energy_consumption',
        'unit': '亿千瓦时'
    },
    'CN_RAILWAY_FREIGHT': {
        'name_cn': '铁路货运量',
        'name_en': 'Railway Freight Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'railway_freight',
        'unit': '万吨'
    },
    'CN_BANK_LOANS': {
        'name_cn': '银行贷款发放量',
        'name_en': 'Bank Loan Disbursement',
        'category': '流动性面',
        'frequency': 'monthly',
        'source': 'pboc',
        'api_function': 'bank_loans',
        'unit': '亿元'
    },
    
    # 新克强指数
    'CN_URBAN_EMPLOYMENT': {
        'name_cn': '城镇新增就业人数',
        'name_en': 'Urban New Employment',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'urban_employment',
        'unit': '万人'
    },
    'CN_DISPOSABLE_INCOME': {
        'name_cn': '居民人均可支配收入',
        'name_en': 'Per Capita Disposable Income',
        'category': '宏观经济面',
        'frequency': 'quarterly',
        'source': 'official',
        'api_function': 'disposable_income',
        'unit': '元'
    },
    'CN_ENERGY_INTENSITY': {
        'name_cn': '单位GDP能耗',
        'name_en': 'Energy Intensity per GDP',
        'category': '宏观经济面',
        'frequency': 'quarterly',
        'source': 'official',
        'api_function': 'energy_intensity',
        'unit': '吨标准煤/万元'
    },
    
    # 扩展克强指数
    'CN_INDUSTRIAL_ELECTRICITY': {
        'name_cn': '工业用电量',
        'name_en': 'Industrial Electricity Consumption',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'industrial_electricity',
        'unit': '亿千瓦时'
    },
    'CN_HIGHWAY_FREIGHT': {
        'name_cn': '公路货运量',
        'name_en': 'Highway Freight Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'highway_freight',
        'unit': '万吨'
    },
    'CN_WATERWAY_FREIGHT': {
        'name_cn': '水路货运量',
        'name_en': 'Waterway Freight Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'waterway_freight',
        'unit': '万吨'
    },
    'CN_AVIATION_FREIGHT': {
        'name_cn': '民航货运量',
        'name_en': 'Aviation Freight Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'aviation_freight',
        'unit': '万吨'
    },
    'CN_EXPRESS_DELIVERY': {
        'name_cn': '快递业务量',
        'name_en': 'Express Delivery Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'express_delivery',
        'unit': '亿件'
    },
    'CN_MOBILE_PAYMENT': {
        'name_cn': '移动支付交易额',
        'name_en': 'Mobile Payment Volume',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'pboc',
        'api_function': 'mobile_payment',
        'unit': '万亿元'
    },
    'CN_INTERNET_USERS': {
        'name_cn': '互联网用户数',
        'name_en': 'Internet Users',
        'category': '宏观经济面',
        'frequency': 'quarterly',
        'source': 'official',
        'api_function': 'internet_users',
        'unit': '万人'
    },
    'CN_DIGITAL_ECONOMY': {
        'name_cn': '数字经济规模',
        'name_en': 'Digital Economy Scale',
        'category': '宏观经济面',
        'frequency': 'annual',
        'source': 'official',
        'api_function': 'digital_economy',
        'unit': '万亿元'
    },
    'CN_CARBON_EMISSIONS': {
        'name_cn': '碳排放量',
        'name_en': 'Carbon Emissions',
        'category': '宏观经济面',
        'frequency': 'quarterly',
        'source': 'official',
        'api_function': 'carbon_emissions',
        'unit': '万吨'
    }
}

# 4. 深入挖掘指标
DEEP_DIVE_INDICATORS = {
    # 就业深度指标
    'CN_FREELANCERS': {
        'name_cn': '自由职业者数量',
        'name_en': 'Freelancers',
        'category': '宏观经济面',
        'frequency': 'quarterly',
        'source': 'official',
        'api_function': 'freelancers',
        'unit': '万人'
    },
    'CN_MIGRANT_WORKERS': {
        'name_cn': '农民工数量',
        'name_en': 'Migrant Workers',
        'category': '宏观经济面',
        'frequency': 'annual',
        'source': 'official',
        'api_function': 'migrant_workers',
        'unit': '万人'
    },
    'CN_STARTUP_COMPANIES': {
        'name_cn': '新注册企业数量',
        'name_en': 'New Registered Companies',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'startup_companies',
        'unit': '万家'
    },
    'CN_BANKRUPTCY_COMPANIES': {
        'name_cn': '企业注销数量',
        'name_en': 'Company Bankruptcies',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'bankruptcy_companies',
        'unit': '万家'
    },
    'CN_SOCIAL_INSURANCE': {
        'name_cn': '社保参保人数',
        'name_en': 'Social Insurance Participants',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'social_insurance',
        'unit': '万人'
    },
    
    # 北向资金深度指标
    'CN_NORTHBOUND_FLOW': {
        'name_cn': '北向资金净流入',
        'name_en': 'Northbound Capital Flow',
        'category': '资金面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'stock_connect_north_net_flow_in',
        'unit': '亿元'
    },
    'CN_NORTHBOUND_HOLDINGS': {
        'name_cn': '北向资金持股市值',
        'name_en': 'Northbound Holdings Value',
        'category': '资金面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'stock_connect_north_holdings',
        'unit': '亿元'
    },
    'CN_NORTHBOUND_TOP10': {
        'name_cn': '北向资金前十大持股',
        'name_en': 'Northbound Top 10 Holdings',
        'category': '资金面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'stock_connect_north_top10',
        'unit': '亿元'
    },
    
    # 南向资金深度指标
    'CN_SOUTHBOUND_FLOW': {
        'name_cn': '南向资金净流入',
        'name_en': 'Southbound Capital Flow',
        'category': '资金面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'stock_connect_south_net_flow_in',
        'unit': '亿元'
    },
    'CN_SOUTHBOUND_HOLDINGS': {
        'name_cn': '南向资金持股市值',
        'name_en': 'Southbound Holdings Value',
        'category': '资金面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'stock_connect_south_holdings',
        'unit': '亿元'
    },
    
    # VLCC及航运深度指标
    'GLOBAL_VLCC_RATE': {
        'name_cn': 'VLCC运价指数',
        'name_en': 'VLCC Freight Rate',
        'category': '大宗商品面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'energy_oil_vlcc',
        'unit': '点'
    },
    'GLOBAL_BDI': {
        'name_cn': '波罗的海干散货指数',
        'name_en': 'Baltic Dry Index',
        'category': '大宗商品面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'drybulk_index_bdi',
        'unit': '点'
    },
    'GLOBAL_BCI': {
        'name_cn': '波罗的海海岬型指数',
        'name_en': 'Baltic Capesize Index',
        'category': '大宗商品面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'drybulk_index_bci',
        'unit': '点'
    },
    'GLOBAL_BPI': {
        'name_cn': '波罗的海巴拿马型指数',
        'name_en': 'Baltic Panamax Index',
        'category': '大宗商品面',
        'frequency': 'daily',
        'source': 'akshare',
        'api_function': 'drybulk_index_bpi',
        'unit': '点'
    },
    'CN_PORT_THROUGHPUT': {
        'name_cn': '中国港口吞吐量',
        'name_en': 'China Port Throughput',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'port_throughput',
        'unit': '万吨'
    },
    'CN_CONTAINER_THROUGHPUT': {
        'name_cn': '中国集装箱吞吐量',
        'name_en': 'China Container Throughput',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'container_throughput',
        'unit': '万TEU'
    },
    'CN_SHIPPING_CONFIDENCE': {
        'name_cn': '中国航运信心指数',
        'name_en': 'China Shipping Confidence Index',
        'category': '市场情绪面',
        'frequency': 'monthly',
        'source': 'official',
        'api_function': 'shipping_confidence',
        'unit': '点'
    }
}

# 5. 计算指标
CALCULATED_INDICATORS = {
    # 北向资金计算指标
    'CN_NORTHBOUND_VOLATILITY': {
        'name_cn': '北向资金波动率',
        'name_en': 'Northbound Volatility',
        'category': '资金面',
        'frequency': 'daily',
        'calculation': 'rolling_std(CN_NORTHBOUND_FLOW, 20)',
        'unit': '%'
    },
    'CN_NORTHBOUND_MOMENTUM': {
        'name_cn': '北向资金动量指标',
        'name_en': 'Northbound Momentum',
        'category': '资金面',
        'frequency': 'daily',
        'calculation': 'CN_NORTHBOUND_FLOW.rolling(5).mean() / CN_NORTHBOUND_FLOW.rolling(20).mean()',
        'unit': '倍'
    },
    
    # 南向资金计算指标
    'CN_SOUTHBOUND_VOLATILITY': {
        'name_cn': '南向资金波动率',
        'name_en': 'Southbound Volatility',
        'category': '资金面',
        'frequency': 'daily',
        'calculation': 'rolling_std(CN_SOUTHBOUND_FLOW, 20)',
        'unit': '%'
    },
    'CN_SOUTHBOUND_MOMENTUM': {
        'name_cn': '南向资金动量指标',
        'name_en': 'Southbound Momentum',
        'category': '资金面',
        'frequency': 'daily',
        'calculation': 'CN_SOUTHBOUND_FLOW.rolling(5).mean() / CN_SOUTHBOUND_FLOW.rolling(20).mean()',
        'unit': '倍'
    },
    
    # 克强指数计算
    'CN_KEQIANG_INDEX': {
        'name_cn': '克强指数',
        'name_en': 'Keqiang Index',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'calculation': '(CN_ELECTRICITY_CONSUMPTION * 0.4 + CN_RAILWAY_FREIGHT * 0.25 + CN_BANK_LOANS * 0.35)',
        'unit': '指数'
    },
    
    # 新克强指数计算
    'CN_NEW_KEQIANG_INDEX': {
        'name_cn': '新克强指数',
        'name_en': 'New Keqiang Index',
        'category': '宏观经济面',
        'frequency': 'monthly',
        'calculation': '(CN_URBAN_EMPLOYMENT * 0.3 + CN_DISPOSABLE_INCOME * 0.4 + CN_ENERGY_INTENSITY * 0.3)',
        'unit': '指数'
    }
}

# 合并所有指标
ALL_COMPREHENSIVE_INDICATORS = {
    **IVIX_INDICATORS,
    **SW_INDUSTRY_INDICATORS,
    **KEQIANG_INDICATORS,
    **DEEP_DIVE_INDICATORS,
    **CALCULATED_INDICATORS
}

# 指标统计
INDICATOR_STATS = {
    'total_indicators': len(ALL_COMPREHENSIVE_INDICATORS),
    'ivix_indicators': len(IVIX_INDICATORS),
    'sw_industry_indicators': len(SW_INDUSTRY_INDICATORS),
    'keqiang_indicators': len(KEQIANG_INDICATORS),
    'deep_dive_indicators': len(DEEP_DIVE_INDICATORS),
    'calculated_indicators': len(CALCULATED_INDICATORS)
}

print(f"综合指标配置完成！")
print(f"总指标数量: {INDICATOR_STATS['total_indicators']}")
print(f"- IVIX指标: {INDICATOR_STATS['ivix_indicators']}")
print(f"- 申万行业指标: {INDICATOR_STATS['sw_industry_indicators']}")
print(f"- 克强指数指标: {INDICATOR_STATS['keqiang_indicators']}")
print(f"- 深度挖掘指标: {INDICATOR_STATS['deep_dive_indicators']}")
print(f"- 计算指标: {INDICATOR_STATS['calculated_indicators']}") 