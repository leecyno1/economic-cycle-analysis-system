import axios from 'axios';

// API基础配置
const API_BASE_URL = 'http://localhost:8000/data_hub/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// 数据类型定义
export interface IndicatorCategory {
  id: number;
  name: string;
  description: string;
  indicator_count: number;
}

export interface Indicator {
  id: number;
  code: string;
  name: string;
  category: number;
  category_name: string;
  description: string;
  source: string;
  frequency: string;
  lead_lag_status: string;
  latest_value: number | null;
  latest_date: string | null;
  data_count: number;
}

export interface IndicatorData {
  id: number;
  indicator: number;
  indicator_code: string;
  indicator_name: string;
  date: string;
  value: number;
}

export interface IndicatorStats {
  indicator_code: string;
  indicator_name: string;
  total_count: number;
  latest_date: string;
  earliest_date: string;
  latest_value: number;
  avg_value: number;
  max_value: number;
  min_value: number;
}

// API服务类
export class ApiService {
  // 获取指标分类
  static async getCategories(): Promise<IndicatorCategory[]> {
    const response = await apiClient.get('/categories/');
    return response.data.results || response.data;
  }

  // 获取指标列表
  static async getIndicators(params?: {
    category?: number;
    search?: string;
    page?: number;
  }): Promise<{results: Indicator[], count: number}> {
    const response = await apiClient.get('/indicators/', { params });
    return response.data;
  }

  // 获取指标详情
  static async getIndicator(id: number): Promise<Indicator> {
    const response = await apiClient.get(`/indicators/${id}/`);
    return response.data;
  }

  // 获取指标统计信息
  static async getIndicatorStats(id: number): Promise<IndicatorStats> {
    const response = await apiClient.get(`/indicators/${id}/statistics/`);
    return response.data;
  }

  // 获取指标的最新数据
  static async getIndicatorLatestData(id: number): Promise<IndicatorData> {
    const response = await apiClient.get(`/indicators/${id}/latest_data/`);
    return response.data;
  }

  // 获取指标时间序列数据
  static async getIndicatorTimeSeries(
    indicatorCode: string,
    params?: {
      start_date?: string;
      end_date?: string;
      recent_days?: number;
    }
  ): Promise<{
    indicator_code: string;
    indicator_name: string;
    data: Array<{date: string; value: number}>;
  }> {
    const response = await apiClient.get('/data/time_series/', {
      params: { indicator_code: indicatorCode, ...params }
    });
    return response.data;
  }

  // 批量查询指标数据
  static async getBulkIndicatorData(
    indicatorCodes: string[],
    params?: {
      start_date?: string;
      end_date?: string;
    }
  ): Promise<Record<string, IndicatorData[]>> {
    const response = await apiClient.post('/data/bulk_query/', {
      indicator_codes: indicatorCodes,
      ...params
    });
    return response.data;
  }

  // 获取所有指标的最新数据
  static async getAllLatestData(): Promise<Array<{
    indicator_code: string;
    indicator_name: string;
    category: string;
    date: string;
    value: number;
  }>> {
    const response = await apiClient.get('/data/latest_all/');
    return response.data;
  }

  // 按分类获取指标
  static async getIndicatorsByCategory(): Promise<Record<string, Indicator[]>> {
    const response = await apiClient.get('/indicators/by_category/');
    return response.data;
  }
}

export default ApiService; 