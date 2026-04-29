import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_KEY = 'auth_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_KEY = 'user_data';

export const tokenManager = {
  getToken: () => localStorage.getItem(TOKEN_KEY),
  setToken: (token) => localStorage.setItem(TOKEN_KEY, token),
  removeToken: () => localStorage.removeItem(TOKEN_KEY),
  
  getRefreshToken: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  setRefreshToken: (token) => localStorage.setItem(REFRESH_TOKEN_KEY, token),
  removeRefreshToken: () => localStorage.removeItem(REFRESH_TOKEN_KEY),
  
  getUser: () => {
    const userData = localStorage.getItem(USER_KEY);
    return userData ? JSON.parse(userData) : null;
  },
  setUser: (user) => localStorage.setItem(USER_KEY, JSON.stringify(user)),
  removeUser: () => localStorage.removeItem(USER_KEY),
  
  clearAll: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }
};

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = tokenManager.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = tokenManager.getRefreshToken();
      if (refreshToken) {
        try {
          const response = await api.post('/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          });
          
          const { access_token } = response.data.data;
          tokenManager.setToken(access_token);
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          tokenManager.clearAll();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        // No refresh token, redirect to login
        tokenManager.clearAll();
        window.location.href = '/login';
      }
    }

    // Handle other errors
    if (error.response?.data?.message) {
      toast.error(error.response.data.message);
    } else if (error.message) {
      toast.error(error.message);
    } else {
      toast.error('An unexpected error occurred');
    }

    return Promise.reject(error);
  }
);

// API service functions
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    const { user, access_token, refresh_token } = response.data.data;
    
    tokenManager.setToken(access_token);
    tokenManager.setRefreshToken(refresh_token);
    tokenManager.setUser(user);
    
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    const { user, access_token, refresh_token } = response.data.data;
    
    tokenManager.setToken(access_token);
    tokenManager.setRefreshToken(refresh_token);
    tokenManager.setUser(user);
    
    return response.data;
  },

  logout: async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      // Ignore logout errors
    } finally {
      tokenManager.clearAll();
    }
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    const user = response.data.data.user;
    tokenManager.setUser(user);
    return user;
  }
};

export const studentAPI = {
  getDashboard: async () => {
    const response = await api.get('/student/dashboard');
    return response.data.data;
  },

  getPerformance: async () => {
    const response = await api.get('/student/performance');
    return response.data.data;
  },

  getPrediction: async () => {
    const response = await api.post('/student/predict');
    return response.data.data;
  },

  getPredictionHistory: async (page = 1, perPage = 10) => {
    const response = await api.get(`/student/predictions/history?page=${page}&per_page=${perPage}`);
    return response.data.data;
  },

  downloadReport: async () => {
    const response = await api.get('/student/report/download');
    return response.data.data;
  },

  trackProgress: async () => {
    const response = await api.get('/student/progress/track');
    return response.data.data;
  },

  getAcademicAnalytics: async () => {
    const response = await api.get('/student/analytics/academic');
    return response.data.data;
  }
};

export const facultyAPI = {
  getStudents: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/faculty/students?${queryString}`);
    return response.data.data;
  },

  updateStudent: async (studentId, data) => {
    const response = await api.put(`/faculty/student/${studentId}/update`, data);
    return response.data.data;
  },

  getStudentDetails: async (studentId) => {
    const response = await api.get(`/faculty/student/${studentId}`);
    return response.data.data;
  },

  uploadDataset: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/faculty/upload-dataset', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.data;
  },

  getAnalytics: async () => {
    const response = await api.get('/faculty/analytics');
    return response.data.data;
  }
};

export const adminAPI = {
  getUsers: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/admin/users?${queryString}`);
    return response.data.data;
  },

  updateUser: async (userId, data) => {
    const response = await api.put(`/admin/user/${userId}`, data);
    return response.data.data;
  },

  deleteUser: async (userId) => {
    const response = await api.delete(`/admin/user/${userId}`);
    return response.data;
  },

  trainModel: async () => {
    const response = await api.post('/admin/train-model');
    return response.data.data;
  },

  getSystemInsights: async () => {
    const response = await api.get('/admin/system-insights');
    return response.data.data;
  },

  getPredictionLogs: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/admin/predictions/logs?${queryString}`);
    return response.data.data;
  }
};

// Utility functions
export const apiUtils = {
  handleError: (error) => {
    console.error('API Error:', error);
    
    if (error.response?.data?.message) {
      return error.response.data.message;
    } else if (error.message) {
      return error.message;
    } else {
      return 'An unexpected error occurred';
    }
  },

  isAuthenticated: () => {
    return !!tokenManager.getToken();
  },

  getUserRole: () => {
    const user = tokenManager.getUser();
    return user?.role || null;
  },

  hasRole: (requiredRole) => {
    const userRole = apiUtils.getUserRole();
    
    if (requiredRole === 'student') {
      return userRole === 'student';
    } else if (requiredRole === 'faculty') {
      return ['faculty', 'admin'].includes(userRole);
    } else if (requiredRole === 'admin') {
      return userRole === 'admin';
    }
    
    return false;
  }
};

export default api;