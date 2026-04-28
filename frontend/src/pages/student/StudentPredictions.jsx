import React, { useState, useEffect } from 'react';
import { Brain, Calendar, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import { studentAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const StudentPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadPredictions(currentPage);
  }, [currentPage]);

  const loadPredictions = async (page = 1) => {
    try {
      setLoading(true);
      const data = await studentAPI.getPredictionHistory(page, 10);
      setPredictions(data.predictions);
      setPagination(data.pagination);
    } catch (error) {
      toast.error('Failed to load prediction history');
      console.error('Predictions error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateNewPrediction = async () => {
    try {
      await studentAPI.getPrediction();
      toast.success('New prediction generated!');
      // Reload predictions
      loadPredictions(1);
      setCurrentPage(1);
    } catch (error) {
      toast.error('Failed to generate prediction');
      console.error('Prediction error:', error);
    }
  };

  const getPredictionIcon = (prediction) => {
    return prediction === 'Pass' ? CheckCircle : AlertTriangle;
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'low': return 'badge-success';
      case 'medium': return 'badge-warning';
      case 'high': return 'badge-danger';
      default: return 'badge-secondary';
    }
  };

  if (loading && predictions.length === 0) {
    return <LoadingSpinner fullScreen text="Loading prediction history..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Predictions</h1>
          <p className="text-gray-600 mt-1">
            Your performance prediction history and insights
          </p>
        </div>
        
        <button
          onClick={handleGenerateNewPrediction}
          className="btn btn-primary"
        >
          <Brain className="w-4 h-4 mr-2" />
          Generate New Prediction
        </button>
      </div>

      {/* Predictions List */}
      {predictions.length === 0 ? (
        <Card>
          <Card.Content>
            <div className="text-center py-12">
              <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Predictions Yet</h3>
              <p className="text-gray-600 mb-4">
                Generate your first AI-powered performance prediction
              </p>
              <button
                onClick={handleGenerateNewPrediction}
                className="btn btn-primary"
              >
                <Brain className="w-4 h-4 mr-2" />
                Generate Prediction
              </button>
            </div>
          </Card.Content>
        </Card>
      ) : (
        <div className="space-y-4">
          {predictions.map((prediction) => (
            <Card key={prediction.id}>
              <Card.Content>
                <div className="flex items-start space-x-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    prediction.prediction_result === 'Pass' 
                      ? 'bg-success-100' 
                      : 'bg-danger-100'
                  }`}>
                    {React.createElement(getPredictionIcon(prediction.prediction_result), {
                      className: `w-6 h-6 ${
                        prediction.prediction_result === 'Pass' 
                          ? 'text-success-600' 
                          : 'text-danger-600'
                      }`
                    })}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <h3 className={`text-xl font-bold ${
                          prediction.prediction_result === 'Pass' 
                            ? 'text-success-700' 
                            : 'text-danger-700'
                        }`}>
                          {prediction.prediction_result}
                        </h3>
                        
                        <span className={`badge ${getRiskColor(prediction.risk_level)}`}>
                          {prediction.risk_level} Risk
                        </span>
                        
                        <span className="text-sm text-gray-500">
                          {(prediction.prediction_probability * 100).toFixed(1)}% confidence
                        </span>
                      </div>
                      
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar className="w-4 h-4 mr-1" />
                        {new Date(prediction.created_at).toLocaleDateString()}
                      </div>
                    </div>
                    
                    {prediction.feedback_message && (
                      <div className="bg-gray-50 rounded-lg p-4">
                        <h4 className="font-medium text-gray-900 mb-2">AI Feedback:</h4>
                        <p className="text-sm text-gray-700 whitespace-pre-line">
                          {prediction.feedback_message}
                        </p>
                      </div>
                    )}
                    
                    <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                      <span>Model: {prediction.model_used}</span>
                      <span>ID: {prediction.id}</span>
                    </div>
                  </div>
                </div>
              </Card.Content>
            </Card>
          ))}
        </div>
      )}

      {/* Pagination */}
      {pagination && pagination.pages > 1 && (
        <div className="flex justify-center items-center space-x-2">
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={!pagination.has_prev}
            className="btn btn-secondary btn-sm"
          >
            Previous
          </button>
          
          <span className="text-sm text-gray-600">
            Page {pagination.page} of {pagination.pages}
          </span>
          
          <button
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={!pagination.has_next}
            className="btn btn-secondary btn-sm"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default StudentPredictions;