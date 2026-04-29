from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_models import db, User, StudentRecord, PredictionLog
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to ensure user has admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(int(user_id))
        
        if not user or user.role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with pagination and filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role_filter = request.args.get('role', '', type=str)
        search = request.args.get('search', '', type=str)
        
        # Build query
        query = User.query
        
        # Apply role filter
        if role_filter and role_filter in ['student', 'faculty', 'admin']:
            query = query.filter(User.role == role_filter)
        
        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    User.full_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%')
                )
            )
        
        # Get paginated results
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get role statistics
        role_stats = db.session.query(
            User.role,
            db.func.count(User.id)
        ).group_by(User.role).all()
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in users.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': users.total,
                    'pages': users.pages,
                    'has_next': users.has_next,
                    'has_prev': users.has_prev
                },
                'statistics': {
                    'role_distribution': dict(role_stats),
                    'total_users': User.query.count(),
                    'active_users': User.query.filter_by(is_active=True).count()
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get users',
            'error': str(e)
        }), 500

@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        
        # Get user
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Prevent admin from deactivating themselves
        current_user_id = int(get_jwt_identity())
        if user_id == current_user_id and 'is_active' in data and not data['is_active']:
            return jsonify({
                'success': False,
                'message': 'Cannot deactivate your own account'
            }), 400
        
        # Update allowed fields
        updatable_fields = ['full_name', 'role', 'is_active']
        updated_fields = []
        
        for field in updatable_fields:
            if field in data:
                old_value = getattr(user, field)
                new_value = data[field]
                
                # Validate role
                if field == 'role' and new_value not in ['student', 'faculty', 'admin']:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid role. Must be student, faculty, or admin'
                    }), 400
                
                # Validate is_active
                if field == 'is_active' and not isinstance(new_value, bool):
                    return jsonify({
                        'success': False,
                        'message': 'is_active must be a boolean value'
                    }), 400
                
                setattr(user, field, new_value)
                if old_value != new_value:
                    updated_fields.append(field)
        
        if not updated_fields:
            return jsonify({
                'success': False,
                'message': 'No valid fields to update'
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User updated successfully. Fields updated: {", ".join(updated_fields)}',
            'data': {
                'user': user.to_dict(),
                'updated_fields': updated_fields
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update user',
            'error': str(e)
        }), 500

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user (soft delete by deactivating)"""
    try:
        # Get user
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Prevent admin from deleting themselves
        current_user_id = int(get_jwt_identity())
        if user_id == current_user_id:
            return jsonify({
                'success': False,
                'message': 'Cannot delete your own account'
            }), 400
        
        # Soft delete by deactivating
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deactivated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to delete user',
            'error': str(e)
        }), 500

@admin_bp.route('/train-model', methods=['POST'])
@admin_required
def train_model():
    """Trigger ML model training"""
    try:
        # Check if we have enough data
        student_count = StudentRecord.query.filter(StudentRecord.result.isnot(None)).count()
        
        if student_count < 10:
            return jsonify({
                'success': False,
                'message': f'Insufficient data for training. Need at least 10 records with results, found {student_count}'
            }), 400
        
        # Import and run training (will be created in Phase 2)
        try:
            from ml.train_model import train_models
            
            # Run training
            training_result = train_models()
            
            if training_result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Model training completed successfully',
                    'data': training_result
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Model training failed',
                    'error': training_result.get('error', 'Unknown error')
                }), 500
            
        except ImportError:
            return jsonify({
                'success': False,
                'message': 'ML training module not available'
            }), 503
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Model training failed',
            'error': str(e)
        }), 500

@admin_bp.route('/system-insights', methods=['GET'])
@admin_required
def get_system_insights():
    """Get comprehensive system insights and statistics"""
    try:
        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        user_roles = db.session.query(
            User.role,
            db.func.count(User.id)
        ).group_by(User.role).all()
        
        # Student statistics
        total_students = StudentRecord.query.count()
        students_with_results = StudentRecord.query.filter(StudentRecord.result.isnot(None)).count()
        pass_count = StudentRecord.query.filter_by(result='Pass').count()
        fail_count = StudentRecord.query.filter_by(result='Fail').count()
        
        # Prediction statistics
        total_predictions = PredictionLog.query.count()
        recent_predictions = PredictionLog.query.filter(
            PredictionLog.created_at >= db.func.date('now', '-7 days')
        ).count()
        
        # Model usage statistics
        model_usage = db.session.query(
            PredictionLog.model_used,
            db.func.count(PredictionLog.id)
        ).group_by(PredictionLog.model_used).all()
        
        # Risk level distribution
        risk_distribution = db.session.query(
            PredictionLog.risk_level,
            db.func.count(PredictionLog.id)
        ).group_by(PredictionLog.risk_level).all()
        
        # Performance metrics
        avg_scores = {
            'internal_marks': db.session.query(db.func.avg(StudentRecord.internal_marks)).scalar() or 0,
            'assignment_score': db.session.query(db.func.avg(StudentRecord.assignment_score)).scalar() or 0,
            'final_exam_marks': db.session.query(db.func.avg(StudentRecord.final_exam_marks)).scalar() or 0,
            'attendance_percentage': db.session.query(db.func.avg(StudentRecord.attendance_percentage)).scalar() or 0
        }
        
        # Check model availability
        model_available = os.path.exists('ml/saved/best_model.pkl')
        
        # Get ML model status if available
        ml_status = None
        if model_available:
            try:
                from ml.ml_utils import get_ml_manager
                ml_manager = get_ml_manager()
                ml_status = ml_manager.get_model_status()
            except Exception as e:
                print(f"Error getting ML status: {e}")
        
        return jsonify({
            'success': True,
            'data': {
                'users': {
                    'total': total_users,
                    'active': active_users,
                    'inactive': total_users - active_users,
                    'role_distribution': dict(user_roles)
                },
                'students': {
                    'total': total_students,
                    'with_results': students_with_results,
                    'without_results': total_students - students_with_results,
                    'pass_count': pass_count,
                    'fail_count': fail_count,
                    'pass_rate': round((pass_count / students_with_results * 100), 2) if students_with_results > 0 else 0
                },
                'predictions': {
                    'total': total_predictions,
                    'recent_week': recent_predictions,
                    'model_usage': dict(model_usage),
                    'risk_distribution': dict(risk_distribution)
                },
                'performance': {
                    'averages': {k: round(v, 2) for k, v in avg_scores.items()}
                },
                'system': {
                    'model_available': model_available,
                    'ml_status': ml_status,
                    'database_size': total_users + total_students + total_predictions
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get system insights',
            'error': str(e)
        }), 500

@admin_bp.route('/predictions/logs', methods=['GET'])
@admin_required
def get_prediction_logs():
    """Get all prediction logs with filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        model_filter = request.args.get('model', '', type=str)
        risk_filter = request.args.get('risk', '', type=str)
        
        # Build query
        query = PredictionLog.query
        
        # Apply filters
        if model_filter:
            query = query.filter(PredictionLog.model_used == model_filter)
        
        if risk_filter and risk_filter in ['Low', 'Medium', 'High']:
            query = query.filter(PredictionLog.risk_level == risk_filter)
        
        # Get paginated results
        logs = query.order_by(PredictionLog.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'logs': [log.to_dict() for log in logs.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': logs.total,
                    'pages': logs.pages,
                    'has_next': logs.has_next,
                    'has_prev': logs.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get prediction logs',
            'error': str(e)
        }), 500