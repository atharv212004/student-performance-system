import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authAPI, tokenManager, apiUtils } from '../services/api';
import toast from 'react-hot-toast';

// Auth context
const AuthContext = createContext();

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'SET_USER':
      return { 
        ...state, 
        user: action.payload, 
        isAuthenticated: !!action.payload,
        loading: false 
      };
    
    case 'CLEAR_USER':
      return { 
        ...state, 
        user: null, 
        isAuthenticated: false,
        loading: false 
      };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    
    default:
      return state;
  }
};

// Initial state
const initialState = {
  user: null,
  isAuthenticated: false,
  loading: true,
  error: null,
};

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Initialize auth state on app load
  useEffect(() => {
    const initializeAuth = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      try {
        const token = tokenManager.getToken();
        const storedUser = tokenManager.getUser();
        
        if (token && storedUser) {
          // Verify token is still valid
          try {
            const user = await authAPI.getCurrentUser();
            dispatch({ type: 'SET_USER', payload: user });
          } catch (error) {
            // Token is invalid, clear storage
            tokenManager.clearAll();
            dispatch({ type: 'CLEAR_USER' });
          }
        } else {
          dispatch({ type: 'CLEAR_USER' });
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        dispatch({ type: 'CLEAR_USER' });
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async (credentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'CLEAR_ERROR' });
    
    try {
      const response = await authAPI.login(credentials);
      const user = response.data.user;
      
      dispatch({ type: 'SET_USER', payload: user });
      toast.success(`Welcome back, ${user.full_name}!`);
      
      return { success: true, user };
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      return { success: false, error: errorMessage };
    }
  };

  // Register function
  const register = async (userData) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'CLEAR_ERROR' });
    
    try {
      const response = await authAPI.register(userData);
      const user = response.data.user;
      
      dispatch({ type: 'SET_USER', payload: user });
      toast.success(`Welcome, ${user.full_name}! Your account has been created.`);
      
      return { success: true, user };
    } catch (error) {
      const errorMessage = apiUtils.handleError(error);
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      return { success: false, error: errorMessage };
    }
  };

  // Logout function
  const logout = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      await authAPI.logout();
      dispatch({ type: 'CLEAR_USER' });
      toast.success('Logged out successfully');
    } catch (error) {
      // Even if logout fails on server, clear local state
      dispatch({ type: 'CLEAR_USER' });
      console.error('Logout error:', error);
    }
  };

  // Clear error function
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  // Check if user has required role
  const hasRole = (requiredRole) => {
    if (!state.user) return false;
    return apiUtils.hasRole(requiredRole);
  };

  // Context value
  const value = {
    ...state,
    login,
    register,
    logout,
    clearError,
    hasRole,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;