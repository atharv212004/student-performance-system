import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import LoadingSpinner from './components/LoadingSpinner';

// Import pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import StudentDashboard from './pages/student/StudentDashboard';
import StudentPerformance from './pages/student/StudentPerformance';
import StudentPredictions from './pages/student/StudentPredictions';
import FacultyDashboard from './pages/faculty/FacultyDashboard';
import FacultyStudents from './pages/faculty/FacultyStudents';
import FacultyAnalytics from './pages/faculty/FacultyAnalytics';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminUsers from './pages/admin/AdminUsers';
import AdminSystem from './pages/admin/AdminSystem';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* Protected routes with layout */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
            {/* Default redirect based on role */}
            <Route index element={<RoleBasedRedirect />} />
            
            {/* Student routes */}
            <Route path="student" element={
              <ProtectedRoute requiredRole="student">
                <StudentDashboard />
              </ProtectedRoute>
            } />
            <Route path="student/dashboard" element={
              <ProtectedRoute requiredRole="student">
                <StudentDashboard />
              </ProtectedRoute>
            } />
            <Route path="student/performance" element={
              <ProtectedRoute requiredRole="student">
                <StudentPerformance />
              </ProtectedRoute>
            } />
            <Route path="student/predictions" element={
              <ProtectedRoute requiredRole="student">
                <StudentPredictions />
              </ProtectedRoute>
            } />
            
            {/* Faculty routes */}
            <Route path="faculty" element={
              <ProtectedRoute requiredRole="faculty">
                <FacultyDashboard />
              </ProtectedRoute>
            } />
            <Route path="faculty/dashboard" element={
              <ProtectedRoute requiredRole="faculty">
                <FacultyDashboard />
              </ProtectedRoute>
            } />
            <Route path="faculty/students" element={
              <ProtectedRoute requiredRole="faculty">
                <FacultyStudents />
              </ProtectedRoute>
            } />
            <Route path="faculty/analytics" element={
              <ProtectedRoute requiredRole="faculty">
                <FacultyAnalytics />
              </ProtectedRoute>
            } />
            
            {/* Admin routes */}
            <Route path="admin" element={
              <ProtectedRoute requiredRole="admin">
                <AdminDashboard />
              </ProtectedRoute>
            } />
            <Route path="admin/dashboard" element={
              <ProtectedRoute requiredRole="admin">
                <AdminDashboard />
              </ProtectedRoute>
            } />
            <Route path="admin/users" element={
              <ProtectedRoute requiredRole="admin">
                <AdminUsers />
              </ProtectedRoute>
            } />
            <Route path="admin/system" element={
              <ProtectedRoute requiredRole="admin">
                <AdminSystem />
              </ProtectedRoute>
            } />
          </Route>
          
          {/* 404 page */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

// Component to redirect users to their role-specific dashboard
const RoleBasedRedirect = () => {
  const { user } = useAuth();
  
  if (!user) {
    return <LoadingSpinner />;
  }
  
  switch (user.role) {
    case 'student':
      return <Navigate to="/student/dashboard" replace />;
    case 'faculty':
      return <Navigate to="/faculty/dashboard" replace />;
    case 'admin':
      return <Navigate to="/admin/dashboard" replace />;
    default:
      return <Navigate to="/login" replace />;
  }
};

export default App;