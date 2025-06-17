# 经济周期分析系统 (Economic Cycle Analysis System)

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-5.2-green.svg)
![React](https://img.shields.io/badge/react-18.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

基于兴证策略研究数据的专业经济周期分析和预测系统，覆盖**1,064个专业指标**，支持**16个维度**的深度经济分析。

## 🌟 项目特色

### 📊 专业指标体系
- **1,064个专业指标**：覆盖115个二级行业的全面数据
- **16个分析维度**：景气度、估值、拥挤度、技术面、基本面、动量、情绪、流动性等
- **多层次分类**：消费、周期、制造、TMT、医药、金融地产等行业分布
- **实时数据采集**：自动化数据获取和质量监控

### 🔄 智能周期分析
- **6种周期类型**：商业周期、基钦周期、朱格拉周期、库兹涅茨周期、康德拉季耶夫周期、综合周期
- **四阶段识别**：扩张期、峰值期、收缩期、谷底期的精准划分
- **置信度评估**：基于机器学习算法的周期判断置信度
- **趋势预测**：智能算法预测经济走势

### 📈 高级数据可视化
- **多指标对比**：支持最多5个指标的同步分析
- **实时监控**：30秒自动刷新的实时数据展示
- **多图表类型**：线图、面积图、柱状图、散点图等专业图表
- **自定义时间范围**：30天到5年的灵活时间选择

## 🏗️ 技术架构

### 后端 (Backend)
- **Django 5.2** + **Django REST Framework**
- **PostgreSQL** 数据库
- **Redis** 缓存层
- **Celery** 异步任务处理
- **机器学习算法**：高斯滤波、周期分解等

### 前端 (Frontend)
- **React 18** + **TypeScript**
- **Material-UI (MUI)** 设计系统
- **Recharts** 专业图表库
- **React Query** 状态管理
- **Vite** 构建工具

### 数据层
- **数据采集**：自动化指标数据获取
- **数据清洗**：智能数据质量检测
- **数据存储**：优化的数据库索引设计
- **数据API**：RESTful API接口

## 🚀 快速开始

### 环境要求
- Python 3.12+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+

### 后端部署

```bash
# 1. 克隆项目
git clone https://github.com/your-username/economic-cycle-analysis.git
cd economic-cycle-analysis

# 2. 创建虚拟环境
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库
cd economic_cycle_analysis
python manage.py migrate

# 5. 创建超级用户
python manage.py createsuperuser

# 6. 启动开发服务器
python manage.py runserver
```

### 前端部署

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 4. 访问应用
# 打开浏览器访问 http://localhost:5173
```

### 数据初始化

```bash
# 批量采集历史数据
python manage.py batch_collect_data

# 计算指标
python manage.py calculate_indicators

# 生成数据质量报告
python manage.py generate_quality_reports
```

## 📱 功能模块

### 1. 指标管理系统
- 1,064个指标的分类管理
- 实时数据状态监控
- 数据质量评估和报告
- 自动化数据采集

### 2. 数据可视化中心
- 多维度指标对比分析
- 时间序列图表展示
- 实时数据更新
- 自定义图表配置

### 3. 经济周期分析
- 智能周期识别算法
- 当前经济阶段判断
- 关键指标贡献度分析
- 专业投资建议

### 4. 实时监控仪表板
- 系统健康度监控
- 数据质量分布统计
- 告警和通知系统
- 性能指标追踪

## 📊 数据指标体系

### 核心维度 (8个)
1. **景气指数** - 宏观经济景气度评估
2. **估值** - 市场估值水平分析
3. **拥挤度** - 市场拥挤程度监控
4. **技术面** - 技术指标分析
5. **基本面** - 基础经济数据
6. **动量** - 市场动量指标
7. **情绪** - 市场情绪评估
8. **流动性** - 资金流动性分析

### 增强维度 (8个)
1. **波动率** - 市场波动性分析
2. **相关性** - 指标间相关关系
3. **季节性** - 季节性因素分析
4. **政策敏感度** - 政策影响评估
5. **供应链** - 供应链风险监控
6. **创新** - 创新能力评估
7. **ESG** - 环境社会治理指标
8. **风险** - 综合风险评估

## 🔧 配置说明

### 数据库配置
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'economic_cycle_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### API配置
```javascript
// frontend/src/services/api.ts
const API_BASE_URL = 'http://localhost:8000/data_hub/api';
```

## 📈 性能优化

- **数据库优化**：复合索引、查询优化
- **缓存策略**：Redis缓存热点数据
- **异步处理**：Celery后台任务
- **前端优化**：代码分割、懒加载
- **CDN加速**：静态资源CDN分发

## 🧪 测试

```bash
# 后端测试
python manage.py test

# 前端测试
npm test

# 端到端测试
npm run test:e2e
```

## 📝 API文档

访问 `http://localhost:8000/admin/` 查看Django管理后台
访问 `http://localhost:8000/data_hub/api/` 查看API接口

### 主要API端点
- `GET /api/indicators/` - 获取指标列表
- `GET /api/indicators/{id}/data/` - 获取指标数据
- `GET /api/quality-reports/` - 获取数据质量报告
- `POST /api/cycle-analysis/` - 周期分析

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- 项目维护者：[您的姓名]
- 邮箱：your.email@example.com
- 项目链接：[https://github.com/your-username/economic-cycle-analysis](https://github.com/your-username/economic-cycle-analysis)

## 🙏 致谢

- 兴证策略研究团队提供的专业数据支持
- 开源社区的技术支持
- 所有贡献者的努力

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！** 