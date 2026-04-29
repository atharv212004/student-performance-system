import React, { useState, useEffect } from 'react';
import { 
  Download, 
  FileText, 
  Calendar, 
  Eye, 
  Trash2, 
  Loader2,
  AlertCircle,
  CheckCircle,
  BarChart3,
  TrendingUp
} from 'lucide-react';
import { studentAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const StudentReports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [reportTypes] = useState([
    {
      id: 'academic',
      name: 'Academic Performance',
      description: 'Comprehensive academic metrics and scores',
      icon: BarChart3
    },
    {
      id: 'prediction',
      name: 'Performance Prediction',
      description: 'AI-powered performance predictions',
      icon: TrendingUp
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Report',
      description: 'Complete analysis with recommendations',
      icon: FileText
    }
  ]);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      // Mock data - replace with actual API call when available
      setReports([
        {
          id: 1,
          name: 'Academic Performance - March 2024',
          type: 'academic',
          generated_at: new Date(2024, 2, 15),
          size: '2.4 MB',
          download_count: 3
        },
        {
          id: 2,
          name: 'Semester Prediction Report',
          type: 'prediction',
          generated_at: new Date(2024, 2, 10),
          size: '1.8 MB',
          download_count: 1
        }
      ]);
    } catch (error) {
      toast.error('Failed to load reports');
      console.error('Reports error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async (reportType) => {
    try {
      setGenerating(true);
      
      // Call API to generate report based on type
      const response = await studentAPI.downloadReport();
      
      if (response.download_url) {
        // Add to reports list
        const newReport = {
          id: reports.length + 1,
          name: `${reportType.name} - ${new Date().toLocaleDateString()}`,
          type: reportType.id,
          generated_at: new Date(),
          size: '2.0 MB',
          download_count: 0
        };
        
        setReports([newReport, ...reports]);
        toast.success(`${reportType.name} generated successfully!`);
        
        // Auto-download the report
        downloadReport(newReport, response.download_url);
      }
    } catch (error) {
      toast.error('Failed to generate report');
      console.error('Generation error:', error);
    } finally {
      setGenerating(false);
    }
  };

  const downloadReport = (report, url) => {
    try {
      const link = document.createElement('a');
      link.href = url || `/api/student/report/file/${report.id}`;
      link.download = `${report.name}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      toast.success('Report downloaded successfully');
    } catch (error) {
      toast.error('Failed to download report');
      console.error('Download error:', error);
    }
  };

  const deleteReport = async (reportId) => {
    try {
      setReports(reports.filter(r => r.id !== reportId));
      toast.success('Report deleted');
    } catch (error) {
      toast.error('Failed to delete report');
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen text="Loading your reports..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Student Reports</h1>
        <p className="text-gray-600 mt-1">
          Generate and download comprehensive academic reports
        </p>
      </div>

      {/* Generate Report Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {reportTypes.map((reportType) => {
          const IconComponent = reportType.icon;
          return (
            <Card key={reportType.id} className="hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <IconComponent className="w-8 h-8 text-blue-600" />
                  {generating && (
                    <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                  )}
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {reportType.name}
                </h3>
                
                <p className="text-sm text-gray-600 mb-4">
                  {reportType.description}
                </p>
                
                <button
                  onClick={() => handleGenerateReport(reportType)}
                  disabled={generating}
                  className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2 font-medium"
                >
                  <Download className="w-4 h-4" />
                  {generating ? 'Generating...' : 'Generate & Download'}
                </button>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Recent Reports</h2>
          <span className="text-sm text-gray-600">
            {reports.length} report{reports.length !== 1 ? 's' : ''}
          </span>
        </div>

        {reports.length === 0 ? (
          <Card>
            <div className="p-8 text-center">
              <AlertCircle className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600">
                No reports generated yet. Create your first report above!
              </p>
            </div>
          </Card>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Report Name</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Type</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Generated</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Size</th>
                  <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Downloads</th>
                  <th className="px-6 py-3 text-right text-sm font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {reports.map((report) => (
                  <tr key={report.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <FileText className="w-5 h-5 text-blue-600" />
                        <span className="text-sm font-medium text-gray-900">{report.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-600 capitalize">{report.type}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Calendar className="w-4 h-4" />
                        {report.generated_at.toLocaleDateString()}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-600">{report.size}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        {report.download_count}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex gap-3 justify-end">
                        <button
                          onClick={() => {
                            setSelectedReport(report);
                            setShowPreview(true);
                          }}
                          className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                          title="Preview"
                        >
                          <Eye className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => downloadReport(report)}
                          className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Download"
                        >
                          <Download className="w-5 h-5" />
                        </button>
                        <button
                          onClick={() => deleteReport(report.id)}
                          className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Preview Modal */}
      {showPreview && selectedReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-auto">
            <div className="sticky top-0 bg-gray-50 border-b p-4 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                {selectedReport.name}
              </h3>
              <button
                onClick={() => setShowPreview(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            <div className="p-6">
              <div className="bg-gray-100 h-96 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">PDF Preview</p>
                  <button
                    onClick={() => {
                      downloadReport(selectedReport);
                      setShowPreview(false);
                    }}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Download to View
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentReports;
