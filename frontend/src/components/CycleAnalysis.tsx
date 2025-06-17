import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Chip,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  ShowChart,
  Assessment,
  Psychology,
  Timeline,
  Speed,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  AreaChart,
} from 'recharts';
import { useQuery } from '@tanstack/react-query';

// 周期类型定义
const CYCLE_TYPES = [
  { value: 'business', label: '商业周期', description: '传统经济波动周期', duration: '6-8年' },
  { value: 'kitchin', label: '基钦周期', description: '库存调整周期', duration: '3-4年' },
  { value: 'juglar', label: '朱格拉周期', description: '设备投资周期', duration: '9-10年' },
  { value: 'kuznets', label: '库兹涅茨周期', description: '建筑周期', duration: '15-25年' },
  { value: 'kondratieff', label: '康德拉季耶夫周期', description: '长波周期', duration: '50-60年' },
  { value: 'custom', label: '综合周期', description: '多周期叠加分析', duration: '动态' },
];

// 周期阶段定义
const CYCLE_PHASES = [
  { phase: 'expansion', label: '扩张期', color: '#4caf50', description: '经济增长，指标上升' },
  { phase: 'peak', label: '峰值期', color: '#ff9800', description: '经济过热，即将转折' },
  { phase: 'contraction', label: '收缩期', color: '#f44336', description: '经济衰退，指标下降' },
  { phase: 'trough', label: '谷底期', color: '#2196f3', description: '经济触底，准备复苏' },
];

// 模拟周期分析数据
const mockCycleData = [
  { date: '2020-01', value: 45.2, phase: 'contraction', confidence: 0.85 },
  { date: '2020-04', value: 42.1, phase: 'trough', confidence: 0.92 },
  { date: '2020-07', value: 48.3, phase: 'expansion', confidence: 0.78 },
  { date: '2020-10', value: 52.4, phase: 'expansion', confidence: 0.88 },
  { date: '2021-01', value: 55.1, phase: 'expansion', confidence: 0.91 },
  { date: '2021-04', value: 58.7, phase: 'expansion', confidence: 0.89 },
  { date: '2021-07', value: 61.2, phase: 'peak', confidence: 0.76 },
  { date: '2021-10', value: 59.8, phase: 'peak', confidence: 0.82 },
  { date: '2022-01', value: 56.3, phase: 'contraction', confidence: 0.87 },
  { date: '2022-04', value: 52.1, phase: 'contraction', confidence: 0.93 },
  { date: '2022-07', value: 49.6, phase: 'contraction', confidence: 0.85 },
  { date: '2022-10', value: 47.8, phase: 'trough', confidence: 0.79 },
  { date: '2023-01', value: 50.2, phase: 'expansion', confidence: 0.84 },
  { date: '2023-04', value: 53.7, phase: 'expansion', confidence: 0.88 },
  { date: '2023-07', value: 56.4, phase: 'expansion', confidence: 0.92 },
  { date: '2023-10', value: 58.9, phase: 'expansion', confidence: 0.86 },
];

export default function CycleAnalysis() {
  const [selectedCycle, setSelectedCycle] = useState('business');
  const [analysisMode, setAnalysisMode] = useState('historical');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // 模拟周期分析API调用
  const { data: cycleAnalysis, isLoading } = useQuery({
    queryKey: ['cycle-analysis', selectedCycle, analysisMode],
    queryFn: async () => {
      // 模拟API延迟
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      return {
        currentPhase: 'expansion',
        phaseConfidence: 0.86,
        phaseDuration: 8, // 月
        expectedDuration: 12, // 月
        cycleStrength: 0.73,
        historicalData: mockCycleData,
        keyIndicators: [
          { name: 'GDP增长率', weight: 0.25, contribution: 0.18 },
          { name: 'PMI制造业', weight: 0.20, contribution: 0.15 },
          { name: 'CPI同比', weight: 0.15, contribution: -0.08 },
          { name: '失业率', weight: 0.15, contribution: -0.12 },
          { name: '利率水平', weight: 0.25, contribution: 0.09 },
        ]
      };
    },
  });

  // 开始深度分析
  const handleDeepAnalysis = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 3000);
  };

  // 获取阶段颜色
  const getPhaseColor = (phase: string) => {
    const phaseInfo = CYCLE_PHASES.find(p => p.phase === phase);
    return phaseInfo?.color || '#9e9e9e';
  };

  // 获取阶段标签
  const getPhaseLabel = (phase: string) => {
    const phaseInfo = CYCLE_PHASES.find(p => p.phase === phase);
    return phaseInfo?.label || phase;
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🔄 经济周期分析
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        基于多维度指标的经济周期识别 · 智能算法预测 · 专业投资建议
      </Typography>

      {/* 控制面板 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            {/* 周期类型选择 */}
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>周期类型</InputLabel>
                <Select
                  value={selectedCycle}
                  label="周期类型"
                  onChange={(e) => setSelectedCycle(e.target.value)}
                >
                  {CYCLE_TYPES.map((cycle) => (
                    <MenuItem key={cycle.value} value={cycle.value}>
                      <Box>
                        <Typography variant="body2">{cycle.label}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {cycle.description} ({cycle.duration})
                        </Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* 分析模式 */}
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>分析模式</InputLabel>
                <Select
                  value={analysisMode}
                  label="分析模式"
                  onChange={(e) => setAnalysisMode(e.target.value)}
                >
                  <MenuItem value="historical">历史回顾</MenuItem>
                  <MenuItem value="current">当前状态</MenuItem>
                  <MenuItem value="forecast">预测分析</MenuItem>
                  <MenuItem value="comprehensive">综合分析</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* 操作按钮 */}
            <Grid item xs={12} md={4}>
              <Box display="flex" gap={1}>
                <Button
                  variant="contained"
                  startIcon={<Psychology />}
                  onClick={handleDeepAnalysis}
                  disabled={isAnalyzing}
                  fullWidth
                >
                  {isAnalyzing ? '分析中...' : '深度分析'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {isLoading ? (
        <Box display="flex" justifyContent="center" py={8}>
          <CircularProgress size={60} />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {/* 当前周期状态 */}
          <Grid item xs={12} lg={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  当前周期状态
                </Typography>
                
                {cycleAnalysis && (
                  <Box>
                    {/* 当前阶段 */}
                    <Box textAlign="center" mb={3}>
                      <Chip
                        label={getPhaseLabel(cycleAnalysis.currentPhase)}
                        sx={{
                          bgcolor: getPhaseColor(cycleAnalysis.currentPhase),
                          color: 'white',
                          fontSize: '1rem',
                          px: 2,
                          py: 1,
                        }}
                        icon={<TrendingUp />}
                      />
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        置信度: {(cycleAnalysis.phaseConfidence * 100).toFixed(1)}%
                      </Typography>
                    </Box>

                    {/* 阶段进度 */}
                    <Box mb={3}>
                      <Box display="flex" justifyContent="space-between" mb={1}>
                        <Typography variant="body2">阶段进度</Typography>
                        <Typography variant="body2">
                          {cycleAnalysis.phaseDuration}/{cycleAnalysis.expectedDuration} 月
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={(cycleAnalysis.phaseDuration / cycleAnalysis.expectedDuration) * 100}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>

                    {/* 周期强度 */}
                    <Box mb={3}>
                      <Box display="flex" justifyContent="space-between" mb={1}>
                        <Typography variant="body2">周期强度</Typography>
                        <Typography variant="body2">
                          {(cycleAnalysis.cycleStrength * 100).toFixed(1)}%
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={cycleAnalysis.cycleStrength * 100}
                        color="warning"
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>

                    {/* 关键提示 */}
                    <Alert severity="info" sx={{ mt: 2 }}>
                      基于当前分析，经济处于
                      <strong>{getPhaseLabel(cycleAnalysis.currentPhase)}</strong>，
                      建议关注趋势变化信号。
                    </Alert>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* 周期图表 */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  周期波动图
                </Typography>
                
                {cycleAnalysis && (
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={cycleAnalysis.historicalData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      
                      {/* 历史数据线 */}
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#1976d2"
                        strokeWidth={2}
                        dot={(props: any) => {
                          const { payload } = props;
                          return (
                            <circle
                              cx={props.cx}
                              cy={props.cy}
                              r={4}
                              fill={getPhaseColor(payload.phase)}
                              stroke="#fff"
                              strokeWidth={2}
                            />
                          );
                        }}
                        name="周期指数"
                      />
                      
                      {/* 阶段参考线 */}
                      <ReferenceLine y={50} stroke="#999" strokeDasharray="5 5" label="中性线" />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* 关键指标贡献 */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  关键指标贡献度
                </Typography>
                
                {cycleAnalysis && (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>指标名称</TableCell>
                          <TableCell align="right">权重</TableCell>
                          <TableCell align="right">贡献度</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {cycleAnalysis.keyIndicators.map((indicator, index) => (
                          <TableRow key={index}>
                            <TableCell>{indicator.name}</TableCell>
                            <TableCell align="right">
                              {(indicator.weight * 100).toFixed(1)}%
                            </TableCell>
                            <TableCell align="right">
                              <Box display="flex" alignItems="center" justifyContent="flex-end" gap={1}>
                                {indicator.contribution > 0 ? (
                                  <TrendingUp fontSize="small" color="success" />
                                ) : (
                                  <TrendingUp 
                                    fontSize="small" 
                                    color="error" 
                                    sx={{ transform: 'rotate(180deg)' }}
                                  />
                                )}
                                <Typography
                                  variant="body2"
                                  color={indicator.contribution > 0 ? 'success.main' : 'error.main'}
                                >
                                  {indicator.contribution > 0 ? '+' : ''}
                                  {(indicator.contribution * 100).toFixed(1)}%
                                </Typography>
                              </Box>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* 周期阶段说明 */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  周期阶段解读
                </Typography>
                
                <Grid container spacing={2}>
                  {CYCLE_PHASES.map((phase) => (
                    <Grid item xs={6} key={phase.phase}>
                      <Box
                        p={2}
                        borderRadius={2}
                        border={1}
                        borderColor="grey.200"
                        textAlign="center"
                      >
                        <Box
                          width={40}
                          height={40}
                          borderRadius="50%"
                          bgcolor={phase.color}
                          mx="auto"
                          mb={1}
                          display="flex"
                          alignItems="center"
                          justifyContent="center"
                        >
                          <Typography variant="h6" color="white">
                            {phase.label.charAt(0)}
                          </Typography>
                        </Box>
                        <Typography variant="subtitle2" gutterBottom>
                          {phase.label}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {phase.description}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
}