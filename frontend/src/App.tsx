import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { 
  CssBaseline, 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Box, 
  Tabs,
  Tab,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { 
  TrendingUp,
  Assessment,
  Timeline,
  Menu as MenuIcon,
  Dashboard,
  BarChart,
} from '@mui/icons-material';

import SimpleIndicatorList from './components/SimpleIndicatorList';
import CycleAnalysis from './components/CycleAnalysis';

// 创建查询客户端
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5分钟
      refetchOnWindowFocus: false,
    },
  },
});

// 经济分析主题
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
  },
});

// 标签页组件
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
      id={`main-tabpanel-${index}`}
      aria-labelledby={`main-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [selectedTab, setSelectedTab] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const navigationItems = [
    { text: '系统概览', icon: <Dashboard />, tab: 0 },
    { text: '指标管理', icon: <Assessment />, tab: 0 },
    { text: '数据可视化', icon: <BarChart />, tab: 1 },
    { text: '周期分析', icon: <Timeline />, tab: 2 },
  ];

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        
        {/* 主导航栏 */}
        <AppBar position="static" elevation={1}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={toggleDrawer}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <TrendingUp sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              经济周期分析系统 (1,064指标体系)
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              兴证策略·16维度专业分析
            </Typography>
          </Toolbar>
        </AppBar>

        {/* 侧边导航抽屉 */}
        <Drawer
          anchor="left"
          open={drawerOpen}
          onClose={toggleDrawer}
        >
          <Box sx={{ width: 250, pt: 2 }}>
            <Typography variant="h6" sx={{ px: 2, mb: 2, color: 'primary.main' }}>
              导航菜单
            </Typography>
            <List>
              {navigationItems.map((item, index) => (
                <ListItem 
                  button 
                  key={item.text}
                  onClick={() => {
                    setSelectedTab(item.tab);
                    setDrawerOpen(false);
                  }}
                  selected={selectedTab === item.tab}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        {/* 主标签页导航 */}
        <Container maxWidth="xl">
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
            <Tabs value={selectedTab} onChange={handleTabChange}>
              <Tab
                label={
                  <Box display="flex" alignItems="center">
                    <Assessment sx={{ mr: 1 }} />
                    指标管理
                  </Box>
                }
              />
              <Tab
                label={
                  <Box display="flex" alignItems="center">
                    <BarChart sx={{ mr: 1 }} />
                    数据可视化
                  </Box>
                }
              />
              <Tab
                label={
                  <Box display="flex" alignItems="center">
                    <Timeline sx={{ mr: 1 }} />
                    周期分析
                  </Box>
                }
              />
            </Tabs>
          </Box>

          {/* 标签页内容 */}
          <TabPanel value={selectedTab} index={0}>
            <SimpleIndicatorList />
          </TabPanel>

          <TabPanel value={selectedTab} index={1}>
            <Box display="flex" flexDirection="column" alignItems="center" py={8}>
              <BarChart sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
              <Typography variant="h5" color="text.secondary" gutterBottom>
                数据可视化功能
              </Typography>
              <Typography variant="body1" color="text.secondary" textAlign="center">
                图表分析功能开发中...<br />
                将支持时间序列图、趋势分析、多维度对比等功能
              </Typography>
            </Box>
          </TabPanel>

          <TabPanel value={selectedTab} index={2}>
            <CycleAnalysis />
          </TabPanel>
        </Container>

        {/* 页脚 */}
        <Box 
          component="footer" 
          sx={{ 
            mt: 8, 
            py: 3, 
            backgroundColor: 'grey.100',
            borderTop: 1,
            borderColor: 'divider'
          }}
        >
          <Container maxWidth="xl">
            <Typography variant="body2" color="text.secondary" textAlign="center">
              © 2024 经济周期分析系统 · 基于兴证策略研究数据 · 
              覆盖115个二级行业 · 16个核心维度 · 1,064个专业指标
            </Typography>
          </Container>
        </Box>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
