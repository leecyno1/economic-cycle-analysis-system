import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  Alert,
  CircularProgress,
  Badge,
  Tabs,
  Tab,
  SelectChangeEvent,
} from '@mui/material';
import {
  Search,
  TrendingUp,
  Assessment,
  Timeline,
  Refresh,
  Info,
  FilterList,
  Download,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

import ApiService, { Indicator, IndicatorCategory } from '../services/api';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`indicator-tabpanel-${index}`}
      aria-labelledby={`indicator-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function IndicatorDashboard() {
  const [selectedTab, setSelectedTab] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<number | ''>('');
  const [page, setPage] = useState(1);
  const [selectedIndicator, setSelectedIndicator] = useState<Indicator | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);

  // 获取指标分类
  const { data: categories = [], isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: ApiService.getCategories,
  });

  // 获取指标列表
  const {
    data: indicatorsData,
    isLoading: indicatorsLoading,
    refetch: refetchIndicators,
  } = useQuery({
    queryKey: ['indicators', selectedCategory, searchTerm, page],
    queryFn: () =>
      ApiService.getIndicators({
        category: selectedCategory || undefined,
        search: searchTerm || undefined,
        page,
      }),
  });

  // 获取所有最新数据
  const { data: latestData = [], isLoading: latestDataLoading } = useQuery({
    queryKey: ['latest-data'],
    queryFn: ApiService.getAllLatestData,
    refetchInterval: 5 * 60 * 1000, // 每5分钟更新
  });

  // 获取按分类分组的指标
  const { data: indicatorsByCategory = {}, isLoading: categoryGroupLoading } = useQuery({
    queryKey: ['indicators-by-category'],
    queryFn: ApiService.getIndicatorsByCategory,
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const handleIndicatorClick = (indicator: Indicator) => {
    setSelectedIndicator(indicator);
    setDetailDialogOpen(true);
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setPage(1);
  };

  const handleCategoryChange = (event: SelectChangeEvent<number | ''>) => {
    setSelectedCategory(event.target.value as number | '');
    setPage(1);
  };

  // 获取分类的颜色
  const getCategoryColor = (categoryName: string) => {
    const colors: Record<string, string> = {
      '核心宏观指标': '#1976d2',
      '行业景气指标': '#388e3c',
      '估值指标': '#f57c00',
      '拥挤度指标': '#d32f2f',
      '技术面指标': '#7b1fa2',
      '基本面指标': '#303f9f',
      '动量指标': '#c2185b',
      '情绪指标': '#0097a7',
      '流动性指标': '#5d4037',
      '风险指标': '#616161',
    };
    return colors[categoryName] || '#757575';
  };

  // 渲染概览标签页
  const renderOverviewTab = () => (
    <Grid container spacing={3}>
      {/* 统计卡片 */}
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={1}>
              <Assessment color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">总指标数</Typography>
            </Box>
            <Typography variant="h3" color="primary">
              {indicatorsData?.count || 0}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              覆盖16个维度
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={1}>
              <TrendingUp color="success" sx={{ mr: 1 }} />
              <Typography variant="h6">最新更新</Typography>
            </Box>
            <Typography variant="h3" color="success.main">
              {latestData.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              今日数据点
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={1}>
              <Timeline color="warning" sx={{ mr: 1 }} />
              <Typography variant="h6">数据质量</Typography>
            </Box>
            <Typography variant="h3" color="warning.main">
              92.5%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              平均质量评分
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={1}>
              <FilterList color="info" sx={{ mr: 1 }} />
              <Typography variant="h6">分类数量</Typography>
            </Box>
            <Typography variant="h3" color="info.main">
              {categories.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              个指标分类
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      {/* 分类概览 */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              指标分类分布
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(indicatorsByCategory).map(([categoryName, indicators]) => (
                <Grid item xs={12} sm={6} md={4} key={categoryName}>
                  <Card variant="outlined">
                    <CardContent>
                      <Box display="flex" alignItems="center" justifyContent="space-between">
                        <Typography variant="subtitle1">{categoryName}</Typography>
                        <Chip
                          label={indicators.length}
                          color="primary"
                          size="small"
                          style={{ backgroundColor: getCategoryColor(categoryName) }}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" mt={1}>
                        覆盖行业: {new Set(indicators.map(i => i.source)).size}个
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* 最新数据更新 */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="between" mb={2}>
              <Typography variant="h6">实时数据监控</Typography>
              <Button
                startIcon={<Refresh />}
                onClick={() => {/* 刷新数据 */}}
                size="small"
              >
                刷新
              </Button>
            </Box>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>指标代码</TableCell>
                    <TableCell>指标名称</TableCell>
                    <TableCell>分类</TableCell>
                    <TableCell>最新值</TableCell>
                    <TableCell>更新时间</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {latestData.slice(0, 10).map((item) => (
                    <TableRow key={item.indicator_code}>
                      <TableCell>
                        <Typography variant="body2" color="primary" sx={{ fontFamily: 'monospace' }}>
                          {item.indicator_code}
                        </Typography>
                      </TableCell>
                      <TableCell>{item.indicator_name}</TableCell>
                      <TableCell>
                        <Chip
                          label={item.category}
                          size="small"
                          color="default"
                          style={{ backgroundColor: getCategoryColor(item.category) }}
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {item.value.toFixed(2)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {format(new Date(item.date), 'MM-dd HH:mm', { locale: zhCN })}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  // 渲染指标列表标签页
  const renderIndicatorsTab = () => (
    <Box>
      {/* 搜索和筛选 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="搜索指标"
                value={searchTerm}
                onChange={handleSearch}
                InputProps={{
                  startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>选择分类</InputLabel>
                <Select
                  value={selectedCategory}
                  label="选择分类"
                  onChange={handleCategoryChange}
                >
                  <MenuItem value="">全部分类</MenuItem>
                  {categories.map((category) => (
                    <MenuItem key={category.id} value={category.id}>
                      {category.name} ({category.indicator_count})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<Download />}
              >
                导出数据
              </Button>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<Refresh />}
                onClick={() => refetchIndicators()}
              >
                刷新
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* 指标列表 */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            指标列表 ({indicatorsData?.count || 0} 个)
          </Typography>
          
          {indicatorsLoading ? (
            <Box display="flex" justifyContent="center" p={3}>
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>指标代码</TableCell>
                    <TableCell>指标名称</TableCell>
                    <TableCell>分类</TableCell>
                    <TableCell>数据源</TableCell>
                    <TableCell>频率</TableCell>
                    <TableCell>最新值</TableCell>
                    <TableCell>最新日期</TableCell>
                    <TableCell>操作</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {indicatorsData?.results.map((indicator) => (
                    <TableRow key={indicator.id} hover>
                      <TableCell>
                        <Typography variant="body2" color="primary" sx={{ fontFamily: 'monospace' }}>
                          {indicator.code}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {indicator.name}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={indicator.category_name}
                          size="small"
                          style={{ backgroundColor: getCategoryColor(indicator.category_name) }}
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {indicator.source}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip label={indicator.frequency} size="small" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {indicator.latest_value ? indicator.latest_value.toFixed(2) : '-'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {indicator.latest_date ? format(new Date(indicator.latest_date), 'yyyy-MM-dd') : '-'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Tooltip title="查看详情">
                          <IconButton size="small" onClick={() => handleIndicatorClick(indicator)}>
                            <Info />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>
    </Box>
  );

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Box mb={3}>
        <Typography variant="h4" gutterBottom>
          经济周期指标体系 (1,064个指标)
        </Typography>
        <Typography variant="body1" color="text.secondary">
          覆盖16个维度，115个二级行业的专业指标监控系统
        </Typography>
      </Box>

      {/* 标签页导航 */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={selectedTab} onChange={handleTabChange}>
          <Tab
            label={
              <Box display="flex" alignItems="center">
                <Assessment sx={{ mr: 1 }} />
                系统概览
              </Box>
            }
          />
          <Tab
            label={
              <Box display="flex" alignItems="center">
                <Timeline sx={{ mr: 1 }} />
                指标管理
                <Badge badgeContent={indicatorsData?.count} color="primary" sx={{ ml: 1 }} />
              </Box>
            }
          />
        </Tabs>
      </Box>

      {/* 标签页内容 */}
      <TabPanel value={selectedTab} index={0}>
        {renderOverviewTab()}
      </TabPanel>

      <TabPanel value={selectedTab} index={1}>
        {renderIndicatorsTab()}
      </TabPanel>

      {/* 指标详情对话框 */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          指标详情: {selectedIndicator?.name}
        </DialogTitle>
        <DialogContent>
          {selectedIndicator && (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">指标代码</Typography>
                <Typography variant="body1">{selectedIndicator.code}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">数据源</Typography>
                <Typography variant="body1">{selectedIndicator.source}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="text.secondary">描述</Typography>
                <Typography variant="body1">{selectedIndicator.description}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">频率</Typography>
                <Typography variant="body1">{selectedIndicator.frequency}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="text.secondary">领先/滞后性</Typography>
                <Typography variant="body1">{selectedIndicator.lead_lag_status}</Typography>
              </Grid>
            </Grid>
          )}
        </DialogContent>
      </Dialog>
    </Container>
  );
} 