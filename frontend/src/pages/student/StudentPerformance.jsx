import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Download } from 'lucide-react';
import { studentAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import { BarChart, LineChart } from '../../components/charts';
import toast from 'react-hot-toast';

const StudentPerformance = () => {
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPerformanceData();
  }, []);

  const loadPerformanceData = async () => {
    try {
      setLoading(true);
      const data = await studentAPI.getPerformance();
      setPerformanceData(data);
    } catch (error) {
      toast.error('Failed to load performance data');
      console.error('Performance error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    try {
      const result = await studentAPI.downloadReport();
      toast.success('Report generated successfully!');
      
      // Open download URL in new tab
      if (result.download_url) {
        window.open(result.download_url, '_blank');
      }
    } catch (error) {
      toast.error('Failed to generate report');
      console.error('Report error:', error);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading performance data..." />;
  }

  if (!performanceData) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Performance Data</h3>
        <p className="text-gray-600">
          Performance data will appear here once available.
        </p>
      </div>
    );
  }

  const { marks_breakdown, performance_trends, study_patterns, overall_gpa } = performanceData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Performance Analytics</h1>
          <p className="text-gray-600 mt-1">
            Detailed analysis of your academic performance
          </p>
        </div>
        
        <button
          onClick={handleDownloadReport}
          className="btn btn-primary"
        >
          <Download className="w-4 h-4 mr-2" />
          Download Report
        </button>
      </div>

      {/* Overall GPA */}
      <Card>
        <Card.Content>
          <div className="text-center">
            <h2 className="text-4xl font-bold text-primary-600">{overall_gpa}</h2>
            <p className="text-lg text-gray-600">Overall GPA</p>
          </div>
        </Card.Content>
      </Card>

      {/* Performance Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Marks Breakdown */}
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
              Marks Breakdown
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <BarChart
              data={{
                labels: Object.keys(marks_breakdown).map(key => 
                  key.replace('_', ' ').split(' ').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')
                ),
                values: Object.values(marks_breakdown),
                label: 'Marks'
              }}
              title=""
              height={250}
              showLegend={false}
              colors={['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']}
            />
          </Card.Content>
        </Card>

        {/* Study Patterns */}
        <Card>
          <Card.Header>
            <Card.Title className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-success-600" />
              Study Patterns
            </Card.Title>
          </Card.Header>
          
          <Card.Content>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Daily Study Hours</span>
                <span className="text-sm font-semibold text-gray-900">
                  {study_patterns.daily_hours.toFixed(1)}h
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Attendance Pattern</span>
                <span className="text-sm font-semibold text-gray-900">
                  {study_patterns.attendance_pattern}%
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Participation Score</span>
                <span className="text-sm font-semibold text-gray-900">
                  {study_patterns.participation_score}%
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Activity Involvement</span>
                <span className="text-sm font-semibold text-gray-900">
                  {study_patterns.activity_involvement}%
                </span>
              </div>
            </div>
          </Card.Content>
        </Card>
      </div>

      {/* Performance Trends */}
      <Card>
        <Card.Header>
          <Card.Title>Performance Trends</Card.Title>
        </Card.Header>
        
        <Card.Content>
          <LineChart
            data={{
              labels: performance_trends.months,
              values: performance_trends.scores,
              label: 'Performance Score'
            }}
            title=""
            height={300}
            fill={true}
            color="#3B82F6"
          />
        </Card.Content>
      </Card>
    </div>
  );
};

export default StudentPerformance;