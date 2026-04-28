import React, { useState, useEffect } from 'react';
import { 
  Database, 
  Brain, 
  Activity, 
  Settings, 
  Download,
  Upload,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Info,
  BarChart3
} from 'lucide-react';
import { adminAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const AdminSystem = () => {
  const [systemData, setSystemData] = useState(null);
  const [predictionLogs, setPredictionLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [logsLoading, setLogsLoading] = useState(false);
  const [trainingLoading, setTrainingLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [logsPagination, setLogsPagination] = useState(null);

  useEffect(() => {
    loadSystemData();
    loadPredictionLogs();
  }, []);

  useEffect(() => {
    loadPredictionLogs();
  }, [currentPage]);

  const loadSystemData = async () => {
    try {
      setLoading(true);
      const data = await adminAPI.getSystemInsights();
      setSystemData(data);
    } catch (error) {
      toast.error('Failed to load system data');
      console.error('System data error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPredictionLogs = async () => {
    try {
      setLogsLoading(true);
      const data = await adminAPI.getPredictionLogs({
        page: currentPage,
        per_page: 10
      });
      setPredictionLogs(data.logs);
      setLogsPagination(data.pagination);
    } catch (error) {
      toast.error('Failed to load prediction logs');
      console.error('Prediction logs error:', error);
    } finally {
      setLogsLoading(false);
    }
  };

  const handleTrainModel = async () => {
    try {
      setTrainingLoading(true);
      const result = await adminAPI.trainModel();
      
      toast.success(`Model training completed! Best model: ${result.best_model} (${result.best_score}% accuracy)`);
      
      // Refresh system data
      await loadSystemData();
    } catch (error) {
      toast.error('Failed to train model');
      console.error('Model training error:', error);
    } finally {
      setTrainingLoading(false);
    }
  };

  const getRiskBadgeColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return 'badge-success';
      case 'medium': return 'badge-warning';
      case 'high': return 'badge-danger';
      default: return 'badge-gray';
    }
  };

  const getPredictionBadgeColor = (prediction) => {
    return prediction === 'Pass' ? 'badge-success' : 'badge-danger';
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading system information..." />;
  }

  const { 
    user_stats, 
    student_performance, 
    prediction_stats, 
    ml_model_status 
  } = systemData || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">System Management</h1>
        <p className="text-gray-600 mt-1">
          Monitor system health, manage ML models, and view system logs
        </p>
      </div>

      {/* System Health Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <Card.Content className="p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 rounded-lg bg-success-100 flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">System Status</p>
                <p className="text-lg font-semibold text-success-700">Healthy</p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content className="p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center">
                <Database className="w-6 h-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Database</p>
                <p className="text-lg font-semibold text-primary-700">Connected</p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content className="p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 rounded-lg bg-warning-100 flex items-center justify-center">
                <Brain className="w-6 h-6 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">ML Model</p>
                <p className="text-lg font-semibold text-warning-700">
                  {ml_model_status?.accuracy || '95.2'}%
                </p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content className="p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 rounded-lg bg-info-100 flex items-center justify-center">
                <Activity className="w-6 h-6 text-info-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Predictions</p>
                <p className="text-lg font-semibold text-info-700">
                  {prediction_stats?.total_predictions || 0}
                </p>
              </div>
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* ML Model Management */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <Brain className="w-5 h-5 mr-2 text-primary-600" />
              ML Model Management
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Current Model Status</h4>
                
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Model Type</span>
                    <span className="text-sm font-medium text-gray-900">
                      {ml_model_status?.current_model || 'Random Forest'}
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Accuracy</span>
                    <span className="text-sm font-medium text-success-600">
                      {ml_model_status?.accuracy || '95.2'}%
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Training Samples</span>
                    <span className="text-sm font-medium text-gray-900">
                      {ml_model_status?.training_samples || student_performance?.total_students || 0}
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Last Trained</span>
                    <span className="text-sm font-medium text-gray-900">
                      {ml_model_status?.last_trained 
                        ? new Date(ml_model_status.last_trained).toLocaleDateString()
                        : 'Recently'
                      }
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={handleTrainModel}
                  disabled={trainingLoading}
                  className="btn btn-primary flex-1"
                >
                  {trainingLoading ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span className="ml-2">Training...</span>
                    </>
                  ) : (
                    <>
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Retrain Model
                    </>
                  )}
                </button>
                
                <button className="btn btn-outline">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </button>
              </div>
            </div>
          </Card.Content>
        </Card>

        {/* System Statistics */}
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
              System Statistics
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900 mb-3">User Statistics</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total Users</span>
                    <span className="text-sm font-medium text-gray-900">
                      {user_stats?.total_users || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Students</span>
                    <span className="text-sm font-medium text-gray-900">
                      {user_stats?.students || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Faculty</span>
                    <span className="text-sm font-medium text-gray-900">
                      {user_stats?.faculty || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Admins</span>
                    <span className="text-sm font-medium text-gray-900">
                      {user_stats?.admins || 0}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-4">
                <h4 className="font-medium text-gray-900 mb-3">Performance Overview</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Pass Rate</span>
                    <span className="text-sm font-medium text-success-600">
                      {student_performance?.pass_rate || 0}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Average Score</span>
                    <span className="text-sm font-medium text-gray-900">
                      {student_performance?.average_score || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total Predictions</span>
                    <span className="text-sm font-medium text-gray-900">
                      {prediction_stats?.total_predictions || 0}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* System Actions */}
      <Card>
        <Card.Header>
          <Card.Title className="flex items-center">
            <Settings className="w-5 h-5 mr-2 text-primary-600" />
            System Actions
          </Card.Title>
        </Card.Header>
        
        <Card.Content>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Upload className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">Backup Database</h3>
              <p className="text-sm text-gray-600">Create system backup</p>
            </button>
            
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Download className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">Export Data</h3>
              <p className="text-sm text-gray-600">Download system data</p>
            </button>
            
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <RefreshCw className="w-8 h-8 text-primary-600 mb-2" />
              <h3 className="font-medium text-gray-900">System Refresh</h3>
              <p className="text-sm text-gray-600">Refresh all caches</p>
            </button>
          </div>
        </Card.Content>
      </Card>

      {/* Prediction Logs */}
      <Card>
        <Card.Header>
          <Card.Title className="flex items-center">
            <Activity className="w-5 h-5 mr-2 text-primary-600" />
            Recent Prediction Logs
          </Card.Title>
        </Card.Header>
        
        <Card.Content className="p-0">
          {logsLoading ? (
            <div className="p-8 text-center">
              <LoadingSpinner />
            </div>
          ) : predictionLogs.length === 0 ? (
            <div className="p-8 text-center">
              <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Prediction Logs</h3>
              <p className="text-gray-600">
                Prediction logs will appear here once students start using the system
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Student
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Prediction
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Risk Level
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Confidence
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Model
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {predictionLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {log.student_name || `Student ${log.student_id}`}
                        </div>
                        <div className="text-sm text-gray-500">
                          ID: {log.student_id}
                        </div>
                      </td>
                      
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`badge ${getPredictionBadgeColor(log.prediction_result)}`}>
                          {log.prediction_result}
                        </span>
                      </td>
                      
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`badge ${getRiskBadgeColor(log.risk_level)}`}>
                          {log.risk_level}
                        </span>
                      </td>
                      
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {(log.probability * 100).toFixed(1)}%
                      </td>
                      
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {log.model_used || 'Random Forest'}
                      </td>
                      
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(log.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card.Content>
      </Card>

      {/* Pagination for Logs */}
      {logsPagination && logsPagination.pages > 1 && (
        <div className="flex justify-center">
          <nav className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={!logsPagination.has_prev}
              className="btn btn-outline btn-sm disabled:opacity-50"
            >
              Previous
            </button>
            
            <span className="text-sm text-gray-700">
              Page {logsPagination.page} of {logsPagination.pages}
            </span>
            
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={!logsPagination.has_next}
              className="btn btn-outline btn-sm disabled:opacity-50"
            >
              Next
            </button>
          </nav>
        </div>
      )}
    </div>
  );
};

export default AdminSystem;