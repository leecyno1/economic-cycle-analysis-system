import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Switch,
  FormControlLabel,
  Autocomplete,
  TextField,
  Paper,
  Divider,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  ComposedChart,
  ReferenceLine,
} from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { format, subDays } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  Timeline,
  TrendingUp,
  TrendingDown,
  ShowChart,
  BarChart as BarChartIcon,
  ScatterPlot,
  Refresh,
  Save,
  Settings,
} from '@mui/icons-material';

import ApiService from '../services/api';

// 图表类型枚举
const CHART_TYPES = {
  LINE: 'line',
  AREA: 'area',
  BAR: 'bar',
  SCATTER: 'scatter',
  COMPOSED: 'composed',
} as const;

// 时间范围选项
const TIME_RANGES = [
  { value: '30', label: '近30天' },
  { value: '90', label: '近3个月' },
  { value: '180', label: '近6个月' },
  { value: '365', label: '近1年' },
  { value: '1095', label: '近3年' },
  { value: '1825', label: '近5年' },
];

// 预定义指标组合
const PREDEFINED_GROUPS = [
  {
    name: '核心宏观指标',
    indicators: ['GDP_GROWTH', 'CPI_YOY', 'PMI_MANUFACTURING'],
    colors: ['#1976d2', '#388e3c', '#f57c00'],
  },
  {
    name: '股市情绪指标',
    indicators: ['VIX_INDEX', 'MARGIN_BALANCE', 'TURNOVER_RATE'],
    colors: ['#d32f2f', '#7b1fa2', '#0097a7'],
  },
  {
    name: '流动性指标',
    indicators: ['M2_GROWTH', 'SHIBOR_3M', 'REPO_RATE'],
    colors: ['#5d4037', '#455a64', '#6d4c41'],
  },
];

interface ChartDataPoint {
  date: string;
  displayDate: string;
  [key: string]: number | string;
}

export default function AdvancedDataVisualization() {
  // 状态管理
  const [selectedIndicators, setSelectedIndicators] = useState<string[]>(['GDP_GROWTH']);
  const [chartType, setChartType] = useState(CHART_TYPES.LINE);
  const [timeRange, setTimeRange] = useState('365');
  const [realTimeEnabled, setRealTimeEnabled] = useState(false);
  const [showTrendLines, setShowTrendLines] = useState(true);
  const [selectedGroup, setSelectedGroup] = useState('');

  // 获取指标列表
  const { data: indicatorsData } = useQuery({
    queryKey: ['indicators-for-charts'],
    queryFn: () => ApiService.getIndicators(),
  });

  // 获取多指标时间序列数据
  const { 
    data: chartData, 
    isLoading: chartLoading,
    refetch: refetchData,
    error: chartError
  } = useQuery({
    queryKey: ['multi-indicator-charts', selectedIndicators, timeRange],
    queryFn: async () => {
      if (selectedIndicators.length === 0) return [];
      
      const promises = selectedIndicators.map(code => 
        ApiService.getIndicatorTimeSeries(code, {
          recent_days: parseInt(timeRange)
        }).catch(err => {
          console.warn(`Failed to fetch data for ${code}:`, err);
          return null;
        })
      );
      
      const results = await Promise.all(promises);
      
      // 合并数据
      const mergedData: ChartDataPoint[] = [];
      const dateMap = new Map<string, ChartDataPoint>();
      
      results.forEach((result, index) => {
        if (!result?.data) return;
        
        const indicatorCode = selectedIndicators[index];
        result.data.forEach(point => {
          const dateKey = point.date;
          if (!dateMap.has(dateKey)) {
            dateMap.set(dateKey, {
              date: dateKey,
              displayDate: format(new Date(dateKey), 'MM/dd', { locale: zhCN }),
            });
          }
          const existingPoint = dateMap.get(dateKey)!;
          existingPoint[indicatorCode] = point.value;
        });
      });
      
      return Array.from(dateMap.values()).sort((a, b) => 
        new Date(a.date).getTime() - new Date(b.date).getTime()
      );
    },
    enabled: selectedIndicators.length > 0,
    refetchInterval: realTimeEnabled ? 30000 : false, // 30秒刷新
  });

  // 自动刷新逻辑
  useEffect(() => {
    if (realTimeEnabled) {
      const interval = setInterval(() => {
        refetchData();
      }, 30000);
      return () => clearInterval(interval);
    }
  }, [realTimeEnabled, refetchData]);

  // 处理指标选择
  const handleIndicatorChange = (event: any, newValue: string[]) => {
    setSelectedIndicators(newValue.slice(0, 5)); // 最多5个指标
  };

  // 处理预定义组合选择
  const handleGroupChange = (event: any) => {
    const groupName = event.target.value;
    setSelectedGroup(groupName);
    
    if (groupName) {
      const group = PREDEFINED_GROUPS.find(g => g.name === groupName);
      if (group) {
        setSelectedIndicators(group.indicators);
      }
    }
  };

  // 计算指标统计
  const getIndicatorStats = (indicatorCode: string) => {
    if (!chartData || chartData.length === 0) return null;
    
    const values = chartData
      .map(d => d[indicatorCode] as number)
      .filter(v => v !== undefined && !isNaN(v));
    
    if (values.length === 0) return null;
    
    const latest = values[values.length - 1];
    const previous = values[values.length - 2];
    const change = previous ? ((latest - previous) / previous * 100) : 0;
    
    return {
      latest,
      change,
      max: Math.max(...values),
      min: Math.min(...values),
      avg: values.reduce((sum, v) => sum + v, 0) / values.length,
    };
  };

  // 获取指标颜色
  const getIndicatorColor = (index: number) => {
    const colors = ['#1976d2', '#388e3c', '#f57c00', '#d32f2f', '#7b1fa2'];
    return colors[index % colors.length];
  };

  // 自定义Tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <Paper sx={{ p: 2, maxWidth: 300 }}>
          <Typography variant="subtitle2" gutterBottom>
            {label}
          </Typography>
          {payload.map((entry: any, index: number) => (
            <Box key={index} display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="body2" color={entry.color}>
                {entry.dataKey}:
              </Typography>
              <Typography variant="body2" fontWeight="bold">
                {typeof entry.value === 'number' ? entry.value.toFixed(4) : entry.value}
              </Typography>
            </Box>
          ))}
        </Paper>
      );
    }
    return null;
  };

  // 渲染图表
  const renderChart = () => {
    if (!chartData || chartData.length === 0) {
      return (
        <Box display="flex" justifyContent="center" alignItems="center" height={400}>
          <Typography variant="body1" color="text.secondary">
            暂无数据
          </Typography>
        </Box>
      );
    }

    const commonProps = {
      data: chartData,
      margin: { top: 20, right: 30, left: 20, bottom: 5 },
    };

    switch (chartType) {
      case CHART_TYPES.AREA:
        return (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="displayDate" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {selectedIndicators.map((indicator, index) => (
                <Area
                  key={indicator}
                  type="monotone"
                  dataKey={indicator}
                  stroke={getIndicatorColor(index)}
                  fill={getIndicatorColor(index)}
                  fillOpacity={0.3}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        );

      case CHART_TYPES.BAR:
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="displayDate" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {selectedIndicators.map((indicator, index) => (
                <Bar
                  key={indicator}
                  dataKey={indicator}
                  fill={getIndicatorColor(index)}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        );

      case CHART_TYPES.SCATTER:
        return (
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="displayDate" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {selectedIndicators.map((indicator, index) => (
                <Scatter
                  key={indicator}
                  dataKey={indicator}
                  fill={getIndicatorColor(index)}
                />
              ))}
            </ScatterChart>
          </ResponsiveContainer>
        );

      default: // LINE
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="displayDate" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {selectedIndicators.map((indicator, index) => {
                const stats = getIndicatorStats(indicator);
                return (
                  <Line
                    key={indicator}
                    type="monotone"
                    dataKey={indicator}
                    stroke={getIndicatorColor(index)}
                    strokeWidth={2}
                    dot={{ r: 3 }}
                    name={`${indicator} (${stats?.latest.toFixed(2) || 'N/A'})`}
                  />
                );
              })}
              {showTrendLines && selectedIndicators.map((indicator, index) => {
                const stats = getIndicatorStats(indicator);
                return stats ? (
                  <ReferenceLine 
                    key={`avg-${indicator}`}
                    y={stats.avg} 
                    stroke={getIndicatorColor(index)} 
                    strokeDasharray="8 8" 
                    strokeOpacity={0.5}
                  />
                ) : null;
              })}
            </LineChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        📊 高级数据可视化分析
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        多维度指标对比分析 · 实时数据监控 · 专业图表展示
      </Typography>

      {/* 控制面板 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            {/* 指标选择 */}
            <Grid item xs={12} md={6}>
              <Autocomplete
                multiple
                options={indicatorsData?.results?.map(i => i.code) || []}
                value={selectedIndicators}
                onChange={handleIndicatorChange}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="选择指标 (最多5个)"
                    placeholder="搜索指标代码..."
                  />
                )}
                renderTags={(tagValue, getTagProps) =>
                  tagValue.map((option, index) => (
                    <Chip
                      label={option}
                      {...getTagProps({ index })}
                      color="primary"
                      size="small"
                    />
                  ))
                }
                limitTags={3}
                sx={{ maxWidth: '100%' }}
              />
            </Grid>

            {/* 预定义组合 */}
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>预定义组合</InputLabel>
                <Select
                  value={selectedGroup}
                  label="预定义组合"
                  onChange={handleGroupChange}
                >
                  <MenuItem value="">自定义选择</MenuItem>
                  {PREDEFINED_GROUPS.map((group) => (
                    <MenuItem key={group.name} value={group.name}>
                      {group.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* 时间范围 */}
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>时间范围</InputLabel>
                <Select
                  value={timeRange}
                  label="时间范围"
                  onChange={(e) => setTimeRange(e.target.value)}
                >
                  {TIME_RANGES.map((range) => (
                    <MenuItem key={range.value} value={range.value}>
                      {range.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* 图表类型和选项 */}
            <Grid item xs={12}>
              <Box display="flex" gap={2} alignItems="center" flexWrap="wrap">
                <Box display="flex" gap={1}>
                  <Button
                    variant={chartType === CHART_TYPES.LINE ? 'contained' : 'outlined'}
                    startIcon={<ShowChart />}
                    onClick={() => setChartType(CHART_TYPES.LINE)}
                    size="small"
                  >
                    线图
                  </Button>
                  <Button
                    variant={chartType === CHART_TYPES.AREA ? 'contained' : 'outlined'}
                    startIcon={<Timeline />}
                    onClick={() => setChartType(CHART_TYPES.AREA)}
                    size="small"
                  >
                    面积图
                  </Button>
                  <Button
                    variant={chartType === CHART_TYPES.BAR ? 'contained' : 'outlined'}
                    startIcon={<BarChartIcon />}
                    onClick={() => setChartType(CHART_TYPES.BAR)}
                    size="small"
                  >
                    柱状图
                  </Button>
                  <Button
                    variant={chartType === CHART_TYPES.SCATTER ? 'contained' : 'outlined'}
                    startIcon={<ScatterPlot />}
                    onClick={() => setChartType(CHART_TYPES.SCATTER)}
                    size="small"
                  >
                    散点图
                  </Button>
                </Box>

                <Divider orientation="vertical" flexItem />

                <FormControlLabel
                  control={
                    <Switch
                      checked={realTimeEnabled}
                      onChange={(e) => setRealTimeEnabled(e.target.checked)}
                      size="small"
                    />
                  }
                  label="实时更新"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={showTrendLines}
                      onChange={(e) => setShowTrendLines(e.target.checked)}
                      size="small"
                    />
                  }
                  label="显示趋势线"
                />

                <Button
                  startIcon={<Refresh />}
                  onClick={() => refetchData()}
                  size="small"
                  disabled={chartLoading}
                >
                  刷新
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* 错误提示 */}
      {chartError && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          数据加载出现问题，请检查后端服务状态或选择其他指标
        </Alert>
      )}

      {/* 指标统计卡片 */}
      {selectedIndicators.length > 0 && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {selectedIndicators.map((indicator, index) => {
            const stats = getIndicatorStats(indicator);
            return (
              <Grid item xs={12} sm={6} md={4} key={indicator}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="space-between">
                      <Typography variant="h6" noWrap>
                        {indicator}
                      </Typography>
                      <Box
                        width={12}
                        height={12}
                        borderRadius="50%"
                        bgcolor={getIndicatorColor(index)}
                      />
                    </Box>
                    {stats ? (
                      <Box>
                        <Typography variant="h4" color="primary">
                          {stats.latest.toFixed(2)}
                        </Typography>
                        <Box display="flex" alignItems="center" gap={1}>
                          {stats.change > 0 ? (
                            <TrendingUp color="success" fontSize="small" />
                          ) : (
                            <TrendingDown color="error" fontSize="small" />
                          )}
                          <Typography 
                            variant="body2" 
                            color={stats.change > 0 ? 'success.main' : 'error.main'}
                          >
                            {stats.change > 0 ? '+' : ''}{stats.change.toFixed(2)}%
                          </Typography>
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          最大: {stats.max.toFixed(2)} | 最小: {stats.min.toFixed(2)}
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        暂无数据
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      )}

      {/* 主图表区域 */}
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">
              多指标对比分析
              {realTimeEnabled && (
                <Chip label="实时" color="success" size="small" sx={{ ml: 1 }} />
              )}
            </Typography>
            <Box display="flex" gap={1}>
              <Button startIcon={<Save />} size="small">
                保存图表
              </Button>
              <Button startIcon={<Settings />} size="small">
                图表设置
              </Button>
            </Box>
          </Box>
          
          {chartLoading ? (
            <Box display="flex" justifyContent="center" alignItems="center" height={400}>
              <CircularProgress size={40} />
            </Box>
          ) : (
            renderChart()
          )}
        </CardContent>
      </Card>
    </Box>
  );
} 