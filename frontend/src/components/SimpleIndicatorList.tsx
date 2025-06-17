import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import ApiService from '../services/api';

export default function SimpleIndicatorList() {
  const [searchTerm, setSearchTerm] = useState('');

  // 获取指标列表
  const { data: indicatorsData, isLoading, error } = useQuery({
    queryKey: ['indicators-simple', searchTerm],
    queryFn: () => ApiService.getIndicators({ search: searchTerm || undefined }),
    retry: 1,
  });

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  if (error) {
    return (
      <Card>
        <CardContent>
          <Typography color="error">
            数据加载失败，请确保后端服务运行正常
          </Typography>
          <Typography variant="body2" color="text.secondary">
            错误信息: {error.message || '未知错误'}
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        经济指标列表
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <TextField
            fullWidth
            label="搜索指标"
            value={searchTerm}
            onChange={handleSearch}
            sx={{ mb: 2 }}
          />
          <Button variant="contained" color="primary">
            刷新数据
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            指标列表 ({indicatorsData?.count || 0} 个)
          </Typography>
          
          {isLoading ? (
            <Box display="flex" justifyContent="center" p={3}>
              <CircularProgress />
            </Box>
          ) : (
            <List>
              {indicatorsData?.results?.slice(0, 10).map((indicator) => (
                <ListItem key={indicator.id}>
                  <ListItemText
                    primary={indicator.name}
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          代码: {indicator.code}
                        </Typography>
                        <Box sx={{ mt: 1 }}>
                          <Chip 
                            label={indicator.category_name} 
                            size="small" 
                            color="primary" 
                            sx={{ mr: 1 }} 
                          />
                          <Chip 
                            label={indicator.frequency} 
                            size="small" 
                            variant="outlined" 
                          />
                        </Box>
                      </Box>
                    }
                  />
                </ListItem>
              )) || (
                <ListItem>
                  <ListItemText primary="暂无数据" />
                </ListItem>
              )}
            </List>
          )}
        </CardContent>
      </Card>
    </Box>
  );
} 