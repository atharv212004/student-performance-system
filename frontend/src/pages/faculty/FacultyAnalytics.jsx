import React, { useState, useEffect } from 'react';
import { BarChart3, PieChart, TrendingUp, Users } from 'lucide-react';
import { facultyAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import { BarChart, PieChart as PieChartComponent, LineChart } from '../../components/charts';
import toast from 'react-hot-toast';

const FacultyAnalytics = () => {
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
    return <LoadingSpinner fullScreen text="Loading analytics..." />;
  }

  if (!analyticsData) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Analytics Data</h3>
        <p className="text-gray-600">
          Analytics will be available once student data is added to the system.
        </p>
      </div>
    );
  }

  const { overview, averages, distributions } = analyticsData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Comprehensive analytics and insights on student performance
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <Card.Content>
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Users className="w-8 h-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Students</p>
                <p className="text-2xl font-bold text-gray-900">{overview.total_students}</p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content>
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="w-8 h-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pass Rate</p>
                <p className="text-2xl font-bold text-gray-900">{overview.pass_rate}%</p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content>
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="w-8 h-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg. Score</p>
                <p className="text-2xl font-bold text-gray-900">{averages.final_exam_marks}</p>
              </div>
            </div>
          </Card.Content>
        </Card>

        <Card>
          <Card.Content>
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <PieChart className="w-8 h-8 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Attendance</p>
                <p className="text-2xl font-bold text-gray-900">{averages.attendance_percentage}%</p>
              </div>
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Distribution */}
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
              Performance Distribution
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <BarChart
              data={{
                labels: Object.keys(distributions.marks_ranges || {}),
                values: Object.values(distributions.marks_ranges || {}),
                label: 'Students'
              }}
              title=""
              height={250}
              showLegend={false}
              colors={['#3B82F6', '#10B981', '#F59E0B', '#EF4444']}
            />
          </Card.Content>
        </Card>

        {/* Gender Distribution */}
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <PieChart className="w-5 h-5 mr-2 text-success-600" />
              Gender Distribution
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <PieChartComponent
              data={{
                labels: Object.keys(distributions.gender || {}),
                values: Object.values(distributions.gender || {}),
                label: 'Students'
              }}
              title=""
              height={250}
              colors={['#3B82F6', '#EC4899', '#10B981']}
            />
          </Card.Content>
        </Card>

        {/* Participation Analysis */}
        <Card>
          <Card.Header>
            <Card.Title>Class Participation</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <PieChartComponent
              data={{
                labels: Object.keys(distributions.participation || {}),
                values: Object.values(distributions.participation || {}),
                label: 'Students'
              }}
              title=""
              height={250}
              colors={['#10B981', '#F59E0B']}
            />
          </Card.Content>
        </Card>

        {/* Activities Analysis */}
        <Card>
          <Card.Header>
            <Card.Title>Extracurricular Activities</Card.Title>
          </Card.Header>
          
          <Card.Content>
            <BarChart
              data={{
                labels: Object.keys(distributions.activities || {}),
                values: Object.values(distributions.activities || {}),
                label: 'Students'
              }}
              title=""
              height={250}
              showLegend={false}
              colors={['#10B981', '#6B7280']}
            />
          </Card.Content>
        </Card>
      </div>

      {/* Performance Averages */}
      <Card>
        <Card.Header>
          <Card.Title>Performance Averages</Card.Title>
        </Card.Header>
        
        <Card.Content>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(averages).map(([key, value]) => (
              <div key={key} className="text-center">
                <p className="text-sm font-medium text-gray-600 capitalize">
                  {key.replace('_', ' ')}
                </p>
                <p className="text-2xl font-bold text-gray-900">{value}</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full" 
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </Card.Content>
      </Card>
    </div>
  );
};

export default FacultyAnalytics;