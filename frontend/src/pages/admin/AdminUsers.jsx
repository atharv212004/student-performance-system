import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  Plus,
  UserCheck,
  UserX,
  Shield,
  GraduationCap
} from 'lucide-react';
import { adminAPI } from '../../services/api';
import Card from '../../components/Card';
import LoadingSpinner from '../../components/LoadingSpinner';
import toast from 'react-hot-toast';

const AdminUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [pagination, setPagination] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  useEffect(() => {
    loadUsers();
  }, [currentPage, searchTerm, roleFilter]);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const params = {
        page: currentPage,
        per_page: 20,
        ...(searchTerm && { search: searchTerm }),
        ...(roleFilter && { role: roleFilter })
      };
      
      const data = await adminAPI.getUsers(params);
      setUsers(data.users);
      setPagination(data.pagination);
    } catch (error) {
      toast.error('Failed to load users');
      console.error('Users loading error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditUser = (user) => {
    setEditingUser({
      ...user,
      password: '' // Don't pre-fill password
    });
    setShowEditModal(true);
  };

  const handleSaveUser = async (e) => {
    e.preventDefault();
    
    try {
      const updateData = {
        full_name: editingUser.full_name,
        email: editingUser.email,
        role: editingUser.role,
        is_active: editingUser.is_active
      };
      
      // Only include password if it's provided
      if (editingUser.password && editingUser.password.trim()) {
        updateData.password = editingUser.password;
      }
      
      await adminAPI.updateUser(editingUser.id, updateData);
      
      toast.success('User updated successfully');
      setShowEditModal(false);
      setEditingUser(null);
      loadUsers();
    } catch (error) {
      toast.error('Failed to update user');
      console.error('User update error:', error);
    }
  };

  const handleDeleteUser = async (userId, userName) => {
    if (!window.confirm(`Are you sure you want to deactivate ${userName}?`)) {
      return;
    }
    
    try {
      await adminAPI.deleteUser(userId);
      toast.success('User deactivated successfully');
      loadUsers();
    } catch (error) {
      toast.error('Failed to deactivate user');
      console.error('User deletion error:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handleRoleFilter = (e) => {
    setRoleFilter(e.target.value);
    setCurrentPage(1);
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'admin': return Shield;
      case 'faculty': return GraduationCap;
      case 'student': return Users;
      default: return Users;
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'admin': return 'badge-danger';
      case 'faculty': return 'badge-warning';
      case 'student': return 'badge-primary';
      default: return 'badge-gray';
    }
  };

  if (loading && users.length === 0) {
    return <LoadingSpinner fullScreen text="Loading users..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600 mt-1">
            Manage system users and their permissions
          </p>
        </div>
        
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add User
        </button>
      </div>

      {/* Filters */}
      <Card>
        <Card.Content className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search users by name or email..."
                  value={searchTerm}
                  onChange={handleSearch}
                  className="input pl-10 w-full"
                />
              </div>
            </div>
            
            <div className="sm:w-48">
              <div className="relative">
                <Filter className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <select
                  value={roleFilter}
                  onChange={handleRoleFilter}
                  className="input pl-10 w-full"
                >
                  <option value="">All Roles</option>
                  <option value="student">Students</option>
                  <option value="faculty">Faculty</option>
                  <option value="admin">Admins</option>
                </select>
              </div>
            </div>
          </div>
        </Card.Content>
      </Card>

      {/* Users Table */}
      <Card>
        <Card.Header>
          <Card.Title className="flex items-center">
            <Users className="w-5 h-5 mr-2" />
            Users ({pagination?.total || 0})
          </Card.Title>
        </Card.Header>
        
        <Card.Content className="p-0">
          {loading ? (
            <div className="p-8 text-center">
              <LoadingSpinner />
            </div>
          ) : users.length === 0 ? (
            <div className="p-8 text-center">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Users Found</h3>
              <p className="text-gray-600">
                {searchTerm || roleFilter 
                  ? 'Try adjusting your search or filter criteria'
                  : 'No users have been added to the system yet'
                }
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      User
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Role
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {users.map((user) => {
                    const RoleIcon = getRoleIcon(user.role);
                    
                    return (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
                              <RoleIcon className="w-5 h-5 text-primary-600" />
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900">
                                {user.full_name}
                              </div>
                              <div className="text-sm text-gray-500">
                                {user.email}
                              </div>
                            </div>
                          </div>
                        </td>
                        
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`badge ${getRoleBadgeColor(user.role)}`}>
                            {user.role}
                          </span>
                        </td>
                        
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            {user.is_active ? (
                              <>
                                <UserCheck className="w-4 h-4 text-success-500 mr-1" />
                                <span className="text-sm text-success-700">Active</span>
                              </>
                            ) : (
                              <>
                                <UserX className="w-4 h-4 text-danger-500 mr-1" />
                                <span className="text-sm text-danger-700">Inactive</span>
                              </>
                            )}
                          </div>
                        </td>
                        
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(user.created_at).toLocaleDateString()}
                        </td>
                        
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex items-center justify-end space-x-2">
                            <button
                              onClick={() => handleEditUser(user)}
                              className="text-primary-600 hover:text-primary-900"
                              title="Edit user"
                            >
                              <Edit className="w-4 h-4" />
                            </button>
                            
                            <button
                              onClick={() => handleDeleteUser(user.id, user.full_name)}
                              className="text-danger-600 hover:text-danger-900"
                              title="Deactivate user"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </Card.Content>
      </Card>

      {/* Pagination */}
      {pagination && pagination.pages > 1 && (
        <div className="flex justify-center">
          <nav className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={!pagination.has_prev}
              className="btn btn-outline btn-sm disabled:opacity-50"
            >
              Previous
            </button>
            
            <span className="text-sm text-gray-700">
              Page {pagination.page} of {pagination.pages}
            </span>
            
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={!pagination.has_next}
              className="btn btn-outline btn-sm disabled:opacity-50"
            >
              Next
            </button>
          </nav>
        </div>
      )}

      {/* Edit User Modal */}
      {showEditModal && editingUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Edit User
            </h3>
            
            <form onSubmit={handleSaveUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  value={editingUser.full_name}
                  onChange={(e) => setEditingUser({
                    ...editingUser,
                    full_name: e.target.value
                  })}
                  className="input w-full"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={editingUser.email}
                  onChange={(e) => setEditingUser({
                    ...editingUser,
                    email: e.target.value
                  })}
                  className="input w-full"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Role
                </label>
                <select
                  value={editingUser.role}
                  onChange={(e) => setEditingUser({
                    ...editingUser,
                    role: e.target.value
                  })}
                  className="input w-full"
                  required
                >
                  <option value="student">Student</option>
                  <option value="faculty">Faculty</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  New Password (leave blank to keep current)
                </label>
                <input
                  type="password"
                  value={editingUser.password}
                  onChange={(e) => setEditingUser({
                    ...editingUser,
                    password: e.target.value
                  })}
                  className="input w-full"
                  placeholder="Enter new password..."
                />
              </div>
              
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_active"
                  checked={editingUser.is_active}
                  onChange={(e) => setEditingUser({
                    ...editingUser,
                    is_active: e.target.checked
                  })}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <label htmlFor="is_active" className="ml-2 text-sm text-gray-700">
                  Active user
                </label>
              </div>
              
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowEditModal(false);
                    setEditingUser(null);
                  }}
                  className="btn btn-outline"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;