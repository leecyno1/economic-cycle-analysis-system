import React, { useState } from 'react';
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
} from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

import ApiService from '../services/api';

interface DataVisualizationProps {
  indicatorCode?: string;
  title?: string;
}

export default function DataVisualization({ 
  indicatorCode: initialIndicatorCode = 'ECONOMIC_GROWTH',
  title = '经济指标时间序列分析'
}: DataVisualizationProps) {
  const [selectedIndicator, setSelectedIndicator] = useState(initialIndicatorCode);
  const [timeRange, setTimeRange] = useState('365'); // 默认显示1年数据

  // 获取时间序列数据
  const { data: timeSeriesData, isLoading: timeSeriesLoading } = useQuery({
    queryKey: ['time-series', selectedIndicator, timeRange],
    queryFn: () => ApiService.getIndicatorTimeSeries(selectedIndicator, {
      recent_days: parseInt(timeRange)
    }),
    enabled: !!selectedIndicator,
  });

  // 获取指标列表用于选择
  const { data: indicatorsData } = useQuery({
    queryKey: ['indicators-for-chart'],
    queryFn: () => ApiService.getIndicators(),
  });

  // 处理图表数据
  const chartData = timeSeriesData?.data?.map(item => ({
    date: format(new Date(item.date), 'yyyy-MM-dd'),
    value: item.value,
    displayDate: format(new Date(item.date), 'MM/dd', { locale: zhCN }),
  })) || [];

  // 计算统计信息
  const stats = chartData.length > 0 ? {
    latest: chartData[chartData.length - 1]?.value || 0,
    max: Math.max(...chartData.map(d => d.value)),
    min: Math.min(...chartData.map(d => d.value)),
    avg: chartData.reduce((sum, d) => sum + d.value, 0) / chartData.length,
  } : null;

  const handleIndicatorChange = (event: any) => {
    setSelectedIndicator(event.target.value);
  };

  const handleTimeRangeChange = (event: any) => {
    setTimeRange(event.target.value);
  };

  // 自定义图表tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <Card>
          <CardContent sx={{ p: 2 }}>
            <Typography variant="body2">
              日期: {label}
            </Typography>
            <Typography variant="body2" color="primary">
              值: {payload[0].value.toFixed(4)}
            </Typography>
          </CardContent>
        </Card>
      );
    }
    return null;
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {title}
      </Typography>

      {/* 控制面板 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>选择指标</InputLabel>
                <Select
                  value={selectedIndicator}
                  label="选择指标"
                  onChange={handleIndicatorChange}
                >
                  {indicatorsData?.results?.slice(0, 20).map((indicator) => (
                    <MenuItem key={indicator.code} value={indicator.code}>
                      {indicator.name} ({indicator.code})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>时间范围</InputLabel>
                <Select
                  value={timeRange}
                  label="时间范围"
                  onChange={handleTimeRangeChange}
                >
                  <MenuItem value="30">近30天</MenuItem>
                  <MenuItem value="90">近3个月</MenuItem>
                  <MenuItem value="180">近6个月</MenuItem>
                  <MenuItem value="365">近1年</MenuItem>
                  <MenuItem value="1095">近3年</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={5}>
              {stats && (
                <Box display="flex" gap={1} flexWrap="wrap">
                  <Chip label={`最新: ${stats.latest.toFixed(2)}`} color="primary" size="small" />
                  <Chip label={`最大: ${stats.max.toFixed(2)}`} color="success" size="small" />
                  <Chip label={`最小: ${stats.min.toFixed(2)}`} color="error" size="small" />
                  <Chip label={`均值: ${stats.avg.toFixed(2)}`} color="default" size="small" />
                </Box>
              )}
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* 图表区域 */}
      <Grid container spacing={3}>
        {/* 主要时间序列图 */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {timeSeriesData?.indicator_name || '指标数据'} - 时间序列
              </Typography>
              {timeSeriesLoading ? (
                <Box display="flex" justifyContent="center" alignItems="center" height={400}>
                  <CircularProgress />
                </Box>
              ) : (
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="displayDate"
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis 
                      tick={{ fontSize: 12 }}
                      domain={['dataMin', 'dataMax']}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#1976d2"
                      strokeWidth={2}
                      dot={{ r: 3 }}
                      name="指标值"
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 面积图 */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                趋势分析
              </Typography>
              {timeSeriesLoading ? (
                <Box display="flex" justifyContent="center" alignItems="center" height={400}>
                  <CircularProgress />
                </Box>
              ) : (
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={chartData.slice(-30)}> {/* 只显示最近30天 */}
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="displayDate"
                      tick={{ fontSize: 10 }}
                    />
                    <YAxis 
                      tick={{ fontSize: 10 }}
                      domain={['dataMin', 'dataMax']}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Area
                      type="monotone"
                      dataKey="value"
                      stroke="#f57c00"
                      fill="#f57c00"
                      fillOpacity={0.3}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 数据表格 */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                最近数据 (最新10个数据点)
              </Typography>
              <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                      <th style={{ padding: '8px', textAlign: 'left' }}>日期</th>
                      <th style={{ padding: '8px', textAlign: 'right' }}>数值</th>
                      <th style={{ padding: '8px', textAlign: 'right' }}>变化</th>
                    </tr>
                  </thead>
                  <tbody>
                    {chartData.slice(-10).reverse().map((item, index, arr) => {
                      const prevValue = arr[index + 1]?.value;
                      const change = prevValue ? ((item.value - prevValue) / prevValue * 100) : 0;
                      return (
                        <tr key={item.date} style={{ borderBottom: '1px solid #f0f0f0' }}>
                          <td style={{ padding: '8px' }}>{item.date}</td>
                          <td style={{ padding: '8px', textAlign: 'right', fontFamily: 'monospace' }}>
                            {item.value.toFixed(4)}
                          </td>
                          <td 
                            style={{ 
                              padding: '8px', 
                              textAlign: 'right',
                              color: change > 0 ? 'green' : change < 0 ? 'red' : 'black'
                            }}
                          >
                            {change !== 0 ? `${change > 0 ? '+' : ''}${change.toFixed(2)}%` : '-'}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
} 