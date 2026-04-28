import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  BarChart3, 
  Calendar, 
  Award, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';
import { studentAPI } from '../../services/api';
import Card from '../../components/Card';
import StatCard from '../../components/StatCard';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const StudentDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predictionLoading, setPredictionLoading] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await studentAPI.getDashboard();
      setDashboardData(data);
    } catch (error) {
      toast.error('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetPrediction = async () => {
    try {
      setPredictionLoading(true);
      const result = await studentAPI.getPrediction();
      
      // Refresh dashboard to show new prediction
      await loadDashboardData();
      
      toast.success('New prediction generated!');
    } catch (error) {
      toast.error('Failed to generate prediction');
      console.error('Prediction error:', error);
    } finally {
      setPredictionLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading your dashboard..." />;
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="w-12 h-12 text-warning-500 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Data Available</h3>
        <p className="text-gray-600">
          Your student record hasn't been created yet. Please contact your faculty.
        </p>
      </div>
    );
  }

  const { student_info, performance_metrics, latest_prediction, prediction_history } = dashboardData;

  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'danger';
      default: return 'primary';
    }
  };

  const getPredictionIcon = (prediction) => {
    return prediction === 'Pass' ? CheckCircle : AlertTriangle;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Welcome back!</h1>
          <p className="text-gray-600 mt-1">
            Here's your academic performance overview
          </p>
        </div>
        
        <button
          onClick={handleGetPrediction}
          disabled={predictionLoading}
          className="btn btn-primary"
        >
          {predictionLoading ? (
            <>
              <LoadingSpinner size="sm" />
              <span className="ml-2">Generating...</span>
            </>
          ) : (
            <>
              <Brain className="w-4 h-4 mr-2" />
              Get AI Prediction
            </>
          )}
        </button>
      </div>

      {/* Performance Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Overall Score"
          value={`${performance_metrics.overall_score}%`}
          icon={Award}
          color="primary"
          trend={performance_metrics.overall_score >= 75 ? 'up' : 'down'}
          trendValue={`${performance_metrics.overall_score >= 75 ? 'Good' : 'Needs Improvement'}`}
        />
        
        <StatCard
          title="Attendance Rate"
          value={`${performance_metrics.attendance_rate}%`}
          icon={Calendar}
          color={performance_metrics.attendance_rate >= 80 ? 'success' : 'warning'}
          trend={performance_metrics.attendance_rate >= 80 ? 'up' : 'down'}
          trendValue={`${performance_metrics.attendance_rate >= 80 ? 'Excellent' : 'Improve'}`}
        />
        
        <StatCard
          title="Study Hours/Week"
          value={performance_metrics.study_hours_per_week}
          icon={Clock}
          color="primary"
          subtitle="hours per week"
        />
        
        <StatCard
          title="Participation"
          value={performance_metrics.participation_level}
          icon={TrendingUp}
          color={performance_metrics.participation_level === 'Yes' ? 'success' : 'warning'}
          subtitle="Class engagement"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Latest Prediction */}
        <div className="lg:col-span-2">
          <Card>
            <Card.Header>
              <Card.Title className="flex items-center">
                <Brain className="w-5 h-5 mr-2 text-primary-600" />
                Latest AI Prediction
              </Card.Title>
            </Card.Header>
            
            {latest_prediction ? (
              <Card.Content>
                <div className="flex items-start space-x-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    latest_prediction.prediction === 'Pass' 
                      ? 'bg-success-100' 
                      : 'bg-danger-100'
                  }`}>
                    {React.createElement(getPredictionIcon(latest_prediction.prediction), {
                      className: `w-6 h-6 ${
                        latest_prediction.prediction === 'Pass' 
                          ? 'text-success-600' 
                          : 'text-danger-600'
                      }`
                    })}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className={`text-xl font-bold ${
                        latest_prediction.prediction === 'Pass' 
                          ? 'text-success-700' 
                          : 'text-danger-700'
                      }`}>
                        {latest_prediction.prediction}
                      </h3>
                      
                      <span className={`badge ${
                        getRiskColor(latest_prediction.risk_level) === 'success' 
                          ? 'badge-success' 
                          : getRiskColor(latest_prediction.risk_level) === 'warning'
                          ? 'badge-warning'
                          : 'badge-danger'
                      }`}>
                        {latest_prediction.risk_level} Risk
                      </span>
                      
                      <span className="text-sm text-gray-500">
                        {(latest_prediction.probability * 100).toFixed(1)}% confidence
                      </span>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">AI Feedback:</h4>
                      <p className="text-sm text-gray-700 whitespace-pre-line">
                        {latest_prediction.feedback_message}
                      </p>
                    </div>
                    
                    <div className="mt-3 text-xs text-gray-500">
                      Generated on {new Date(latest_prediction.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </Card.Content>
            ) : (
              <Card.Content>
                <div className="text-center py-8">
                  <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No Predictions Yet</h3>
                  <p className="text-gray-600 mb-4">
                    Get your first AI-powered performance prediction
                  </p>
                  <button
                    onClick={handleGetPrediction}
                    disabled={predictionLoading}
                    className="btn btn-primary"
                  >
                    {predictionLoading ? (
                      <>
                        <LoadingSpinner size="sm" />
                        <span className="ml-2">Generating...</span>
                      </>
                    ) : (
                      'Generate Prediction'
                    )}
                  </button>
                </div>
              </Card.Content>
            )}
          </Card>
        </div>

        {/* Student Info */}
        <div>
          <Card>
            <Card.Header>
              <Card.Title>Student Information</Card.Title>
            </Card.Header>
            
            <Card.Content>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-500">Student ID</label>
                  <p className="text-sm text-gray-900">{student_info.student_id}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Name</label>
                  <p className="text-sm text-gray-900">{student_info.student_name}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Age</label>
                  <p className="text-sm text-gray-900">{student_info.age} years</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Gender</label>
                  <p className="text-sm text-gray-900">{student_info.gender}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-500">Extracurricular</label>
                  <p className="text-sm text-gray-900">{student_info.extracurricular_activity}</p>
                </div>
              </div>
            </Card.Content>
          </Card>
        </div>
      </div>

      {/* Recent Predictions */}
      {prediction_history && prediction_history.length > 0 && (
        <Card>
          <Card.Header>
            <Card.Title>Recent Predictions</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-3">
              {prediction_history.slice(0, 3).map((prediction, index) => (
                <div key={prediction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      prediction.prediction_result === 'Pass' 
                        ? 'bg-success-100' 
                        : 'bg-danger-100'
                    }`}>
                      {React.createElement(getPredictionIcon(prediction.prediction_result), {
                        className: `w-4 h-4 ${
                          prediction.prediction_result === 'Pass' 
                            ? 'text-success-600' 
                            : 'text-danger-600'
                        }`
                      })}
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {prediction.prediction_result}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(prediction.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <span className={`badge ${
                      getRiskColor(prediction.risk_level) === 'success' 
                        ? 'badge-success' 
                        : getRiskColor(prediction.risk_level) === 'warning'
                        ? 'badge-warning'
                        : 'badge-danger'
                    }`}>
                      {prediction.risk_level}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card.Content>
        </Card>
      )}
    </div>
  );
};

export default StudentDashboard;