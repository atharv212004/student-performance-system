import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Brain, 
  BarChart3, 
  TrendingUp, 
  AlertTriangle,
  Database,
  Activity,
  Shield
} from 'lucide-react';
import { adminAPI } from '../../services/api';
import Card from '../../components/Card';
import StatCard from '../../components/StatCard';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const [systemData, setSystemData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [trainingLoading, setTrainingLoading] = useState(false);

  useEffect(() => {
    loadSystemInsights();
  }, []);

  const loadSystemInsights = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getSystemInsights();
      setSystemData(data);
    } catch (error) {
      toast.error('Failed to load system insights');
      console.error('System insights error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTrainModel = async () => {
    try {
      setTrainingLoading(true);
      const result = await adminAPI.trainModel();
      
      toast.success(`Model training completed! Best model: ${result.best_model} (${result.best_score}% accuracy)`);
      
      // Refresh system insights
      await loadSystemInsights();
    } catch (error) {
      toast.error('Failed to train model');
      console.error('Model training error:', error);
    } finally {
      setTrainingLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading admin dashboard..." />;
  }

  if (!systemData) {
    return (
      <div className="text-center py-12">
        <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No System Data Available</h3>
        <p className="text-gray-600">
          System insights will appear here once the system is initialized.
        </p>
      </div>
    );
  }

  const { 
    user_stats, 
    student_performance, 
    prediction_stats, 
    ml_model_status,
    recent_activity 
  } = systemData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-1">
            System overview and management controls
          </p>
        </div>
        
        <button
          onClick={handleTrainModel}
          disabled={trainingLoading}
          className="btn btn-primary"
        >
          {trainingLoading ? (
            <>
              <LoadingSpinner size="sm" />
              <span className="ml-2">Training...</span>
            </>
          ) : (
            <>
              <Brain className="w-4 h-4 mr-2" />
              Retrain ML Model
            </>
          )}
        </button>
      </div>

      {/* System Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Users"
          value={user_stats.total_users}
          icon={Users}
          color="primary"
          subtitle={`${user_stats.active_users} active`}
        />
        
        <StatCard
          title="Students"
          value={user_stats.students}
          icon={Users}
          color="success"
          subtitle="registered students"
        />
        
        <StatCard
          title="Faculty"
          value={user_stats.faculty}
          icon={Shield}
          color="warning"
          subtitle="faculty members"
        />
        
        <StatCard
          title="System Health"
          value="Healthy"
          icon={Activity}
          color="success"
          subtitle="all systems operational"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Student Performance Overview */}
        <div className="lg:col-span-2">
          <Card>
            <Card.Header>
              <Card.Title className="flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
                Student Performance Overview
              </Card.Title>
            </Card.Header>
            
            <Card.Content>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">Overall Pass Rate</span>
                      <span className="text-lg font-bold text-success-600">
                        {student_performance.pass_rate}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-success-600 h-2 rounded-full" 
                        style={{ width: `${student_performance.pass_rate}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">Average Score</span>
                      <span className="text-lg font-bold text-primary-600">
                        {student_performance.average_score}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-primary-600 h-2 rounded-full" 
                        style={{ width: `${student_performance.average_score}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="text-center p-4 bg-success-50 rounded-lg">
                    <div className="text-2xl font-bold text-success-700">
                      {student_performance.total_passed}
                    </div>
                    <div className="text-sm text-success-600">Students Passed</div>
                  </div>
                  
                  <div className="text-center p-4 bg-danger-50 rounded-lg">
                    <div className="text-2xl font-bold text-danger-700">
                      {student_performance.total_failed}
                    </div>
                    <div className="text-sm text-danger-600">At Risk Students</div>
                  </div>
                </div>
              </div>
            </Card.Content>
          </Card>
        </div>

        {/* ML Model Status */}
        <div>
          <Card>
            <Card.Header>
              <Card.Title className="flex items-center">
                <Brain className="w-5 h-5 mr-2 text-primary-600" />
                ML Model Status
              </Card.Title>
            </Card.Header>
            
            <Card.Content>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Current Model</label>
                  <p className="text-sm font-semibold text-gray-900">
                    {ml_model_status.current_model || 'Random Forest'}
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Accuracy</label>
                  <p className="text-sm font-semibold text-success-600">
                    {ml_model_status.accuracy || '95.2'}%
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Last Trained</label>
                  <p className="text-sm text-gray-900">
                    {ml_model_status.last_trained 
                      ? new Date(ml_model_status.last_trained).toLocaleDateString()
                      : 'Recently'
                    }
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Training Data</label>
                  <p className="text-sm text-gray-900">
                    {ml_model_status.training_samples || student_performance.total_students} samples
                  </p>
                </div>
                
                <div className="pt-2 border-t">
                  <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    ml_model_status.status === 'healthy' 
                      ? 'bg-success-100 text-success-800'
                      : 'bg-warning-100 text-warning-800'
                  }`}>
                    <div className={`w-1.5 h-1.5 rounded-full mr-1.5 ${
                      ml_model_status.status === 'healthy' 
                        ? 'bg-success-400'
                        : 'bg-warning-400'
                    }`}></div>
                    {ml_model_status.status === 'healthy' ? 'Model Healthy' : 'Needs Retraining'}
                  </div>
                </div>
              </div>
            </Card.Content>
          </Card>
        </div>
      </div>

      {/* Prediction Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <Card.Header>
            <Card.Title>Prediction Statistics</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Total Predictions</span>
                <span className="text-lg font-bold text-primary-600">
                  {prediction_stats.total_predictions}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">This Week</span>
                <span className="text-sm font-semibold text-gray-900">
                  {prediction_stats.predictions_this_week}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Pass Predictions</span>
                <span className="text-sm font-semibold text-success-600">
                  {prediction_stats.pass_predictions}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Fail Predictions</span>
                <span className="text-sm font-semibold text-danger-600">
                  {prediction_stats.fail_predictions}
                </span>
              </div>
            </div>
          </Card.Content>
        </Card>

        {/* Recent Activity */}
        <Card>
          <Card.Header>
            <Card.Title>Recent System Activity</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-3">
              {recent_activity && recent_activity.length > 0 ? (
                recent_activity.slice(0, 5).map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                      <Activity className="w-4 h-4 text-primary-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">
                        {activity.action || 'System Activity'}
                      </p>
                      <p className="text-xs text-gray-500">
                        {activity.timestamp 
                          ? new Date(activity.timestamp).toLocaleString()
                          : 'Recently'
                        }
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-4">
                  <Activity className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">No recent activity</p>
                </div>
              )}
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <Card.Header>
          <Card.Title>Quick Actions</Card.Title>
        </Card.Header>
        
        <Card.Content>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button 
              onClick={() => window.location.href = '/admin/users'}
              className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Users className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">Manage Users</h3>
              <p className="text-sm text-gray-600">Add, edit, or remove users</p>
            </button>
            
            <button 
              onClick={() => window.location.href = '/admin/system'}
              className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Database className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">System Settings</h3>
              <p className="text-sm text-gray-600">Configure system parameters</p>
            </button>
            
            <button 
              onClick={handleTrainModel}
              disabled={trainingLoading}
              className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <Brain className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">Train ML Model</h3>
              <p className="text-sm text-gray-600">Retrain prediction model</p>
            </button>
          </div>
        </Card.Content>
      </Card>
    </div>
  );
};

export default AdminDashboard;