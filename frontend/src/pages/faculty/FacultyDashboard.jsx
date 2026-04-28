import React, { useState, useEffect } from 'react';
import { Users, BarChart3, TrendingUp, AlertTriangle } from 'lucide-react';
import { facultyAPI } from '../../services/api';
import Card from '../../components/Card';
import StatCard from '../../components/StatCard';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const FacultyDashboard = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      const data = await facultyAPI.getAnalytics();
      setAnalyticsData(data);
    } catch (error) {
      toast.error('Failed to load analytics data');
      console.error('Analytics error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading faculty dashboard..." />;
  }

  if (!analyticsData) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Data Available</h3>
        <p className="text-gray-600">
          Analytics data will appear here once students are added to the system.
        </p>
      </div>
    );
  }

  const { overview, averages, distributions } = analyticsData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Faculty Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Overview of student performance and analytics
        </p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Students"
          value={overview.total_students}
          icon={Users}
          color="primary"
        />
        
        <StatCard
          title="Pass Rate"
          value={`${overview.pass_rate}%`}
          icon={TrendingUp}
          color={overview.pass_rate >= 75 ? 'success' : 'warning'}
          trend={overview.pass_rate >= 75 ? 'up' : 'down'}
        />
        
        <StatCard
          title="Students Passed"
          value={overview.pass_count}
          icon={BarChart3}
          color="success"
        />
        
        <StatCard
          title="At Risk Students"
          value={overview.fail_count}
          icon={AlertTriangle}
          color="danger"
        />
      </div>

      {/* Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Averages */}
        <Card>
          <Card.Header>
            <Card.Title>Performance Averages</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-4">
              {Object.entries(averages).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700 capitalize">
                    {key.replace('_', ' ')}
                  </span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-primary-600 h-2 rounded-full" 
                        style={{ width: `${value}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-900 w-12">
                      {value}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card.Content>
        </Card>

        {/* Student Distributions */}
        <Card>
          <Card.Header>
            <Card.Title>Student Distributions</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-6">
              {/* Gender Distribution */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Gender Distribution</h4>
                <div className="space-y-2">
                  {Object.entries(distributions.gender || {}).map(([gender, count]) => (
                    <div key={gender} className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">{gender}</span>
                      <span className="text-sm font-semibold text-gray-900">{count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Participation Distribution */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Class Participation</h4>
                <div className="space-y-2">
                  {Object.entries(distributions.participation || {}).map(([participation, count]) => (
                    <div key={participation} className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">{participation}</span>
                      <span className="text-sm font-semibold text-gray-900">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <Card.Header>
          <Card.Title>Recent Predictions</Card.Title>
        </Card.Header>
        
        <Card.Content>
          <div className="text-center py-8">
            <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">
              Recent prediction activity will be displayed here
            </p>
            <p className="text-sm text-gray-500 mt-1">
              {overview.recent_predictions} predictions in the last 7 days
            </p>
          </div>
        </Card.Content>
      </Card>
    </div>
  );
};

export default FacultyDashboard;