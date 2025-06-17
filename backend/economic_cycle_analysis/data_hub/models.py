from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json

# Create your models here.

class IndicatorCategory(models.Model):
    """指标分类模型 - 支持层级分类结构"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称")
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name="英文名称") 
    code = models.CharField(max_length=50, unique=True, verbose_name="分类代码")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    
    # 层级结构支持
    level = models.IntegerField(default=1, verbose_name="分类层级")  # 1=一级 2=二级 3=三级
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="父分类")
    
    # 排序和显示
    sort_order = models.IntegerField(default=0, verbose_name="排序顺序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    
    # 审计字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "指标分类"
        verbose_name_plural = "指标分类"
        ordering = ['level', 'sort_order', 'name']

    def get_full_path(self):
        """获取完整分类路径"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Indicator(models.Model):
    """指标模型 - 支持1,064个专业指标体系"""
    
    class Frequency(models.TextChoices):
        DAILY = 'D', '日度'
        WEEKLY = 'W', '周度'
        MONTHLY = 'M', '月度'
        QUARTERLY = 'Q', '季度'
        YEARLY = 'Y', '年度'

    class LeadLag(models.TextChoices):
        LEADING = 'LEAD', '领先指标'
        SYNCHRONOUS = 'SYNC', '同步指标'
        LAGGING = 'LAG', '滞后指标'

    class DataAvailability(models.TextChoices):
        HIGH = 'high', '高 - 数据充足'
        MEDIUM = 'medium', '中 - 数据一般'
        LOW = 'low', '低 - 数据稀缺'
        CALCULATED = 'calculated', '计算 - 基于其他指标计算'

    class ImplementationPhase(models.IntegerChoices):
        PHASE_1 = 1, '第一阶段 - 核心指标'
        PHASE_2 = 2, '第二阶段 - 扩展指标'
        PHASE_3 = 3, '第三阶段 - 增强指标'

    # 基础信息
    name = models.CharField(max_length=255, verbose_name="指标名称")
    name_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="英文名称") 
    code = models.CharField(max_length=100, unique=True, verbose_name="指标代码")
    description = models.TextField(blank=True, null=True, verbose_name="指标描述")
    
    # 分类信息
    category = models.ForeignKey(IndicatorCategory, related_name='indicators', on_delete=models.CASCADE, verbose_name="主分类")
    sub_category = models.CharField(max_length=100, blank=True, null=True, verbose_name="子分类")
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name="行业板块")
    industry = models.CharField(max_length=100, blank=True, null=True, verbose_name="细分行业")
    
    # 技术属性
    frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTHLY, verbose_name="数据频率")
    lead_lag_status = models.CharField(max_length=10, choices=LeadLag.choices, verbose_name="领先滞后属性")
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="数据单位")
    
    # 数据源信息
    source = models.CharField(max_length=100, verbose_name="数据源")
    api_function = models.CharField(max_length=100, blank=True, null=True, verbose_name="API函数名")
    data_availability = models.CharField(max_length=20, choices=DataAvailability.choices, default=DataAvailability.MEDIUM, verbose_name="数据可用性")
    
    # 计算相关
    calculation_method = models.TextField(blank=True, null=True, verbose_name="计算方法")
    calculation_formula = models.TextField(blank=True, null=True, verbose_name="计算公式")
    dependent_indicators = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name="依赖指标")
    
    # 业务属性
    importance_level = models.IntegerField(
        default=3, 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="重要程度",
        help_text="1-5星，5星最重要"
    )
    implementation_phase = models.IntegerField(
        choices=ImplementationPhase.choices, 
        default=ImplementationPhase.PHASE_1, 
        verbose_name="实施阶段"
    )
    investment_significance = models.TextField(blank=True, null=True, verbose_name="投资意义")
    
    # 维度标签 - 支持8个核心维度和8个增强维度
    dimension_prosperity = models.BooleanField(default=False, verbose_name="景气度维度")
    dimension_valuation = models.BooleanField(default=False, verbose_name="估值维度")  
    dimension_crowdedness = models.BooleanField(default=False, verbose_name="拥挤度维度")
    dimension_technical = models.BooleanField(default=False, verbose_name="技术面维度")
    dimension_fundamental = models.BooleanField(default=False, verbose_name="基本面维度")
    dimension_momentum = models.BooleanField(default=False, verbose_name="动量维度")
    dimension_sentiment = models.BooleanField(default=False, verbose_name="情绪维度")
    dimension_liquidity = models.BooleanField(default=False, verbose_name="流动性维度")
    
    # 增强维度
    dimension_volatility = models.BooleanField(default=False, verbose_name="波动率维度")
    dimension_correlation = models.BooleanField(default=False, verbose_name="相关性维度")
    dimension_seasonality = models.BooleanField(default=False, verbose_name="季节性维度")
    dimension_policy = models.BooleanField(default=False, verbose_name="政策敏感度维度")
    dimension_supply_chain = models.BooleanField(default=False, verbose_name="供应链维度")
    dimension_innovation = models.BooleanField(default=False, verbose_name="创新维度")
    dimension_esg = models.BooleanField(default=False, verbose_name="ESG维度")
    dimension_risk = models.BooleanField(default=False, verbose_name="风险维度")
    
    # 数据质量控制
    data_quality_score = models.FloatField(
        null=True, blank=True, 
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name="数据质量评分",
        help_text="0-1之间，1表示最高质量"
    )
    last_update_date = models.DateField(null=True, blank=True, verbose_name="最后更新日期")
    update_frequency_days = models.IntegerField(null=True, blank=True, verbose_name="更新频率(天)")
    
    # 状态管理
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    is_deprecated = models.BooleanField(default=False, verbose_name="是否废弃")
    
    # 审计字段
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="创建人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    # 元数据存储
    metadata = models.JSONField(default=dict, blank=True, verbose_name="元数据")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "指标"
        verbose_name_plural = "指标"
        ordering = ['implementation_phase', '-importance_level', 'name']
        
    def get_dimensions(self):
        """获取指标所属的所有维度"""
        dimensions = []
        dimension_fields = [
            ('dimension_prosperity', '景气度'),
            ('dimension_valuation', '估值'), 
            ('dimension_crowdedness', '拥挤度'),
            ('dimension_technical', '技术面'),
            ('dimension_fundamental', '基本面'),
            ('dimension_momentum', '动量'),
            ('dimension_sentiment', '情绪'),
            ('dimension_liquidity', '流动性'),
            ('dimension_volatility', '波动率'),
            ('dimension_correlation', '相关性'),
            ('dimension_seasonality', '季节性'),
            ('dimension_policy', '政策敏感度'),
            ('dimension_supply_chain', '供应链'),
            ('dimension_innovation', '创新'),
            ('dimension_esg', 'ESG'),
            ('dimension_risk', '风险'),
        ]
        
        for field_name, display_name in dimension_fields:
            if getattr(self, field_name):
                dimensions.append(display_name)
        return dimensions

    def get_importance_stars(self):
        """获取重要程度的星级显示"""
        return '★' * self.importance_level + '☆' * (5 - self.importance_level)


class IndicatorData(models.Model):
    """指标数据模型 - 存储时间序列数据"""
    
    indicator = models.ForeignKey(Indicator, related_name='data_points', on_delete=models.CASCADE, verbose_name="指标")
    date = models.DateField(verbose_name="日期")
    value = models.FloatField(verbose_name="数值")
    
    # 数据质量信息
    is_estimated = models.BooleanField(default=False, verbose_name="是否为估算值")
    is_anomaly = models.BooleanField(default=False, verbose_name="是否异常值")
    confidence_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name="置信度",
        help_text="0-1之间，1表示最高置信度"
    )
    
    # 数据来源
    source_system = models.CharField(max_length=100, blank=True, null=True, verbose_name="来源系统")
    collection_time = models.DateTimeField(auto_now_add=True, verbose_name="采集时间")
    
    # 计算相关
    raw_value = models.FloatField(null=True, blank=True, verbose_name="原始值")
    calculated_value = models.FloatField(null=True, blank=True, verbose_name="计算值")
    calculation_notes = models.TextField(blank=True, null=True, verbose_name="计算说明")

    def __str__(self):
        return f"{self.indicator.name} - {self.date}: {self.value}"

    class Meta:
        unique_together = ('indicator', 'date')
        ordering = ['-date']
        verbose_name = "指标数据"
        verbose_name_plural = "指标数据"
        indexes = [
            models.Index(fields=['indicator', '-date']),
            models.Index(fields=['date']),
            models.Index(fields=['indicator', 'is_anomaly']),
        ]


# class CompositeIndicator(models.Model):
#     """复合指标模型 - 支持计算型指标如景气度指数"""
    
#     class CalculationMethod(models.TextChoices):
#         WEIGHTED_AVERAGE = 'weighted_avg', '加权平均'
#         SIMPLE_AVERAGE = 'simple_avg', '简单平均'
#         FACTOR_MODEL = 'factor_model', '因子模型'
#         CUSTOM_FORMULA = 'custom_formula', '自定义公式'
    
#     # 基础信息
#     indicator = models.OneToOneField(Indicator, on_delete=models.CASCADE, verbose_name="关联指标")
#     calculation_method = models.CharField(
#         max_length=20, 
#         choices=CalculationMethod.choices,
#         default=CalculationMethod.WEIGHTED_AVERAGE,
#         verbose_name="计算方法"
#     )
    
#     # 指标组成
#     component_indicators = models.ManyToManyField(
#         Indicator, 
#         through='CompositeIndicatorComponent',
#         related_name='composite_indicators',
#         verbose_name="组成指标"
#     )
#     calculation_formula = models.TextField(blank=True, null=True, verbose_name="计算公式")
#     rebalance_frequency = models.CharField(max_length=10, default='M', verbose_name="再平衡频率")
    
#     # 状态管理
#     is_auto_update = models.BooleanField(default=True, verbose_name="是否自动更新")
#     last_calculation = models.DateTimeField(null=True, blank=True, verbose_name="最后计算时间")
    
#     def __str__(self):
#         return f"复合指标: {self.indicator.name}"

#     class Meta:
#         verbose_name = "复合指标"
#         verbose_name_plural = "复合指标"

# class CompositeIndicatorComponent(models.Model):
#     """复合指标组成部分 - 定义权重和计算规则"""
    
#     composite_indicator = models.ForeignKey(CompositeIndicator, on_delete=models.CASCADE, verbose_name="复合指标")
#     component_indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, verbose_name="组成指标")
    
#     # 权重配置
#     weight = models.FloatField(default=1.0, verbose_name="权重")
#     is_dynamic_weight = models.BooleanField(default=False, verbose_name="是否动态权重")
    
#     # 计算配置
#     transformation = models.CharField(
#         max_length=50, 
#         blank=True, 
#         null=True, 
#         verbose_name="数据变换",
#         help_text="如: log, diff, pct_change, zscore等"
#     )
#     lag_periods = models.IntegerField(default=0, verbose_name="滞后期数")

#     def __str__(self):
#         return f"{self.composite_indicator.indicator.name} -> {self.component_indicator.name} (权重: {self.weight})"

#     class Meta:
#         unique_together = ('composite_indicator', 'component_indicator')
#         verbose_name = "复合指标组成"
#         verbose_name_plural = "复合指标组成"


class DataQualityReport(models.Model):
    """数据质量报告模型"""
    
    class QualityLevel(models.TextChoices):
        EXCELLENT = 'excellent', '优秀'
        GOOD = 'good', '良好' 
        FAIR = 'fair', '一般'
        POOR = 'poor', '较差'
        
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, verbose_name="指标")
    report_date = models.DateField(verbose_name="报告日期")
    
    # 质量指标
    completeness_score = models.FloatField(verbose_name="完整性评分")  # 数据缺失率
    timeliness_score = models.FloatField(verbose_name="及时性评分")    # 更新及时性
    accuracy_score = models.FloatField(verbose_name="准确性评分")     # 数据准确性
    consistency_score = models.FloatField(verbose_name="一致性评分") # 数据一致性
    
    overall_quality = models.CharField(
        max_length=20,
        choices=QualityLevel.choices,
        verbose_name="总体质量"
    )
    
    # 问题记录
    issues_found = models.JSONField(default=list, verbose_name="发现的问题")
    recommendations = models.TextField(blank=True, null=True, verbose_name="改进建议")
    
    class Meta:
        unique_together = ('indicator', 'report_date')
        ordering = ['-report_date']
        verbose_name = "数据质量报告"
        verbose_name_plural = "数据质量报告"
