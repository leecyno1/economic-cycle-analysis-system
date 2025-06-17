import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Tooltip,
  Badge,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Error,
  Schedule,
  Refresh,
  Notifications,
  NotificationsActive,
  Info,
  Assessment,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

import ApiService from '../services/api';

// 数据质量状态类型
interface DataQualityStatus {
  excellent: number;
  good: number;
  fair: number;
  poor: number;
  total: number;
}

// 指标状态类型
interface IndicatorStatus {
  id: number;
  code: string;
  name: string;
  lastUpdate: string;
  status: 'normal' | 'warning' | 'error';
  dataQuality: string;
  changePercent?: number;
}

export default function RealTimeMonitor() {
  const [alertsOpen, setAlertsOpen] = useState(false);
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // 获取系统状态概览
  const { 
    data: systemStatus, 
    isLoading: statusLoading,
    refetch: refetchStatus
  } = useQuery({
    queryKey: ['system-status'],
    queryFn: async () => {
      // 模拟系统状态数据
      const [indicators, dataQualityReports] = await Promise.all([
        ApiService.getIndicators(),
        ApiService.getDataQualityReports().catch(() => ({ results: [] }))
      ]);

      // 计算数据质量分布
      const qualityStatus: DataQualityStatus = {
        excellent: 0,
        good: 0,
        fair: 0,
        poor: 0,
        total: indicators.results?.length || 0
      };

      // 模拟数据质量分布
      qualityStatus.excellent = Math.floor(qualityStatus.total * 0.7);
      qualityStatus.good = Math.floor(qualityStatus.total * 0.2);
      qualityStatus.fair = Math.floor(qualityStatus.total * 0.08);
      qualityStatus.poor = qualityStatus.total - qualityStatus.excellent - qualityStatus.good - qualityStatus.fair;

      // 模拟指标状态
      const indicatorStatuses: IndicatorStatus[] = (indicators.results || []).slice(0, 10).map(indicator => ({
        id: indicator.id,
        code: indicator.code,
        name: indicator.name,
        lastUpdate: indicator.last_update_date || format(new Date(), 'yyyy-MM-dd'),
        status: Math.random() > 0.1 ? 'normal' : (Math.random() > 0.5 ? 'warning' : 'error'),
        dataQuality: ['excellent', 'good', 'fair', 'poor'][Math.floor(Math.random() * 4)],
        changePercent: (Math.random() - 0.5) * 10
      }));

      return {
        qualityStatus,
        indicatorStatuses,
        totalIndicators: qualityStatus.total,
        activeIndicators: Math.floor(qualityStatus.total * 0.95),
        lastDataUpdate: format(new Date(), 'yyyy-MM-dd HH:mm:ss'),
        systemHealth: 'normal' as 'normal' | 'warning' | 'error'
      };
    },
    refetchInterval: 30000, // 30秒自动刷新
  });

  // 处理手动刷新
  const handleRefresh = () => {
    refetchStatus();
    setLastRefresh(new Date());
  };

  // 获取状态颜色
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  // 获取数据质量颜色
  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent': return '#4caf50';
      case 'good': return '#8bc34a';
      case 'fair': return '#ff9800';
      case 'poor': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  // 计算系统健康度
  const calculateHealthScore = () => {
    if (!systemStatus) return 0;
    const { qualityStatus } = systemStatus;
    return Math.round(
      (qualityStatus.excellent * 100 + qualityStatus.good * 80 + qualityStatus.fair * 60 + qualityStatus.poor * 40) 
      / qualityStatus.total
    );
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            📱 实时监控中心
          </Typography>
          <Typography variant="body1" color="text.secondary">
            1,064个指标实时状态监控 · 数据质量评估 · 系统健康度追踪
          </Typography>
        </Box>
        
        <Box display="flex" gap={1} alignItems="center">
          <Typography variant="caption" color="text.secondary">
            最后更新: {format(lastRefresh, 'HH:mm:ss')}
          </Typography>
          <IconButton onClick={handleRefresh} size="small">
            <Refresh />
          </IconButton>
          <IconButton 
            onClick={() => setNotificationsEnabled(!notificationsEnabled)}
            color={notificationsEnabled ? 'primary' : 'default'}
          >
            {notificationsEnabled ? <NotificationsActive /> : <Notifications />}
          </IconButton>
        </Box>
      </Box>

      {statusLoading ? (
        <Box display="flex" justifyContent="center" py={8}>
          <CircularProgress size={60} />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {/* 系统概览卡片 */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  系统概览
                </Typography>
                
                <Grid container spacing={3}>
                  {/* 总体指标 */}
                  <Grid item xs={6} md={3}>
                    <Box textAlign="center">
                      <Typography variant="h3" color="primary">
                        {systemStatus?.totalIndicators || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        总指标数
                      </Typography>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={6} md={3}>
                    <Box textAlign="center">
                      <Typography variant="h3" color="success.main">
                        {systemStatus?.activeIndicators || 0}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        活跃指标
                      </Typography>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={6} md={3}>
                    <Box textAlign="center">
                      <Typography variant="h3" color="info.main">
                        {calculateHealthScore()}%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        系统健康度
                      </Typography>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={6} md={3}>
                    <Box textAlign="center">
                      <Chip 
                        label={systemStatus?.systemHealth === 'normal' ? '正常' : '异常'}
                        color={getStatusColor(systemStatus?.systemHealth || 'normal')}
                        icon={systemStatus?.systemHealth === 'normal' ? <CheckCircle /> : <Warning />}
                      />
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        系统状态
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* 快速操作 */}
          <Grid item xs={12} lg={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  快速操作
                </Typography>
                
                <Box display="flex" flexDirection="column" gap={2}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<Badge badgeContent={3} color="error"><Warning /></Badge>}
                    onClick={() => setAlertsOpen(true)}
                  >
                    查看告警 (3)
                  </Button>
                  
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<Assessment />}
                    href="/analysis"
                  >
                    深度分析
                  </Button>
                  
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={handleRefresh}
                  >
                    刷新数据
                  </Button>
                </Box>
                
                <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                  最后数据更新: {systemStatus?.lastDataUpdate}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* 数据质量分布 */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  数据质量分布
                </Typography>
                
                {systemStatus?.qualityStatus && (
                  <Box>
                    {/* 质量分布条形图 */}
                    <Box mb={2}>
                      <Box display="flex" height={20} borderRadius={1} overflow="hidden">
                        <Box 
                          flex={systemStatus.qualityStatus.excellent}
                          bgcolor={getQualityColor('excellent')}
                        />
                        <Box 
                          flex={systemStatus.qualityStatus.good}
                          bgcolor={getQualityColor('good')}
                        />
                        <Box 
                          flex={systemStatus.qualityStatus.fair}
                          bgcolor={getQualityColor('fair')}
                        />
                        <Box 
                          flex={systemStatus.qualityStatus.poor}
                          bgcolor={getQualityColor('poor')}
                        />
                      </Box>
                    </Box>
                    
                    {/* 质量统计 */}
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Box width={12} height={12} bgcolor={getQualityColor('excellent')} borderRadius="50%" />
                          <Typography variant="body2">优秀: {systemStatus.qualityStatus.excellent}</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Box width={12} height={12} bgcolor={getQualityColor('good')} borderRadius="50%" />
                          <Typography variant="body2">良好: {systemStatus.qualityStatus.good}</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Box width={12} height={12} bgcolor={getQualityColor('fair')} borderRadius="50%" />
                          <Typography variant="body2">一般: {systemStatus.qualityStatus.fair}</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Box width={12} height={12} bgcolor={getQualityColor('poor')} borderRadius="50%" />
                          <Typography variant="body2">较差: {systemStatus.qualityStatus.poor}</Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* 关键指标状态 */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  关键指标状态
                </Typography>
                
                <List dense>
                  {systemStatus?.indicatorStatuses.slice(0, 5).map((indicator) => (
                    <ListItem key={indicator.id}>
                      <ListItemIcon>
                        {indicator.status === 'normal' ? (
                          <CheckCircle color="success" />
                        ) : indicator.status === 'warning' ? (
                          <Warning color="warning" />
                        ) : (
                          <Error color="error" />
                        )}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="body2" fontWeight="bold">
                              {indicator.code}
                            </Typography>
                            {indicator.changePercent !== undefined && (
                              <Box display="flex" alignItems="center" gap={0.5}>
                                {indicator.changePercent > 0 ? (
                                  <TrendingUp fontSize="small" color="success" />
                                ) : (
                                  <TrendingDown fontSize="small" color="error" />
                                )}
                                <Typography 
                                  variant="caption" 
                                  color={indicator.changePercent > 0 ? 'success.main' : 'error.main'}
                                >
                                  {indicator.changePercent > 0 ? '+' : ''}{indicator.changePercent.toFixed(2)}%
                                </Typography>
                              </Box>
                            )}
                          </Box>
                        }
                        secondary={
                          <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="caption" color="text.secondary">
                              {indicator.lastUpdate}
                            </Typography>
                            <Chip 
                              label={indicator.dataQuality} 
                              size="small"
                              sx={{ 
                                bgcolor: getQualityColor(indicator.dataQuality),
                                color: 'white',
                                fontSize: '0.7rem'
                              }}
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* 系统性能指标 */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  系统性能指标
                </Typography>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={3}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        数据采集成功率
                      </Typography>
                      <Box display="flex" alignItems="center" gap={2} mt={1}>
                        <LinearProgress 
                          variant="determinate" 
                          value={96} 
                          sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                        />
                        <Typography variant="body2" fontWeight="bold">96%</Typography>
                      </Box>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={3}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        API响应时间
                      </Typography>
                      <Box display="flex" alignItems="center" gap={2} mt={1}>
                        <LinearProgress 
                          variant="determinate" 
                          value={75} 
                          sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                          color="warning"
                        />
                        <Typography variant="body2" fontWeight="bold">240ms</Typography>
                      </Box>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={3}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        数据库连接池
                      </Typography>
                      <Box display="flex" alignItems="center" gap={2} mt={1}>
                        <LinearProgress 
                          variant="determinate" 
                          value={60} 
                          sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                          color="success"
                        />
                        <Typography variant="body2" fontWeight="bold">12/20</Typography>
                      </Box>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={3}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        缓存命中率
                      </Typography>
                      <Box display="flex" alignItems="center" gap={2} mt={1}>
                        <LinearProgress 
                          variant="determinate" 
                          value={88} 
                          sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                          color="success"
                        />
                        <Typography variant="body2" fontWeight="bold">88%</Typography>
                      </Box>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* 告警对话框 */}
      <Dialog open={alertsOpen} onClose={() => setAlertsOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>系统告警</DialogTitle>
        <DialogContent>
          <List>
            <ListItem>
              <ListItemIcon>
                <Warning color="warning" />
              </ListItemIcon>
              <ListItemText
                primary="GDP增长率数据延迟"
                secondary="最新数据时间：2天前，建议检查数据源"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Error color="error" />
              </ListItemIcon>
              <ListItemText
                primary="CPI数据采集失败"
                secondary="连续3次采集失败，请检查API连接"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Info color="info" />
              </ListItemIcon>
              <ListItemText
                primary="系统维护通知"
                secondary="今晚23:00-01:00进行系统维护，可能影响数据更新"
              />
            </ListItem>
          </List>
        </DialogContent>
      </Dialog>
    </Box>
  );
} 