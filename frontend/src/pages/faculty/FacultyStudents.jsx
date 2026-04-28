import React, { useState, useEffect } from 'react';
import { Users, Search, Upload, Edit, Eye } from 'lucide-react';
import { facultyAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const FacultyStudents = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadStudents();
  }, [currentPage, searchTerm]);

  const loadStudents = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        per_page: 10,
        ...(searchTerm && { search: searchTerm })
      };
      
      const data = await facultyAPI.getStudents(params);
      setStudents(data.students);
      setPagination(data.pagination);
    } catch (error) {
      toast.error('Failed to load students');
      console.error('Students error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const result = await facultyAPI.uploadDataset(file);
      toast.success(`Dataset uploaded successfully! Added: ${result.added_count}, Updated: ${result.updated_count}`);
      loadStudents(); // Refresh the list
    } catch (error) {
      toast.error('Failed to upload dataset');
      console.error('Upload error:', error);
    }
  };

  if (loading && students.length === 0) {
    return <LoadingSpinner fullScreen text="Loading students..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Students Management</h1>
          <p className="text-gray-600 mt-1">
            Manage student records and performance data
          </p>
        </div>
        
        <div className="flex space-x-3">
          <label className="btn btn-secondary cursor-pointer">
            <Upload className="w-4 h-4 mr-2" />
            Upload Dataset
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Search and Filters */}
      <Card>
        <Card.Content>
          <div className="flex items-center space-x-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search students by name or ID..."
                value={searchTerm}
                onChange={handleSearch}
                className="input pl-10"
              />
            </div>
          </div>
        </Card.Content>
      </Card>

      {/* Students List */}
      <Card>
        <Card.Header>
          <Card.Title className="flex items-center">
            <Users className="w-5 h-5 mr-2 text-primary-600" />
            Students ({pagination?.total || 0})
          </Card.Title>
        </Card.Header>
        
        <Card.Content padding="none">
          {students.length === 0 ? (
            <div className="text-center py-12">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Students Found</h3>
              <p className="text-gray-600">
                {searchTerm ? 'No students match your search criteria.' : 'Upload a dataset to get started.'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Student
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Performance
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Attendance
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Result
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {students.map((student) => (
                    <tr key={student.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {student.student_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            ID: {student.student_id}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          Final: {student.final_exam_marks}%
                        </div>
                        <div className="text-sm text-gray-500">
                          Internal: {student.internal_marks}%
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {student.attendance_percentage}%
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {student.result ? (
                          <span className={`badge ${
                            student.result === 'Pass' ? 'badge-success' : 'badge-danger'
                          }`}>
                            {student.result}
                          </span>
                        ) : (
                          <span className="badge badge-secondary">Pending</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className="text-primary-600 hover:text-primary-900">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="text-gray-600 hover:text-gray-900">
                            <Edit className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card.Content>
      </Card>

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

export default FacultyStudents;