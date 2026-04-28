from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_models import db, User, StudentRecord, PredictionLog
from functools import wraps
from datetime import datetime
import os

student_bp = Blueprint('student', __name__)

def student_required(f):
    """Decorator to ensure user has student role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'student':
            return jsonify({
                'success': False,
                'message': 'Student access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard', methods=['GET'])
@student_required
def get_dashboard():
    """Get student dashboard data with prediction"""
    try:
        user_id = get_jwt_identity()
        
        # Get student record
        student_record = StudentRecord.query.filter_by(user_id=user_id).first()
        
        if not student_record:
            return jsonify({
                'success': False,
                'message': 'Student record not found. Please contact faculty to add your record.'
            }), 404
        
        # Get recent predictions
        recent_predictions = PredictionLog.query.filter_by(
            user_id=user_id
        ).order_by(PredictionLog.created_at.desc()).limit(5).all()
        
        # Calculate performance metrics
        performance_metrics = {
            'overall_score': round((
                student_record.internal_marks + 
                student_record.assignment_score + 
                student_record.final_exam_marks
            ) / 3, 2),
            'attendance_rate': student_record.attendance_percentage,
            'study_hours_per_week': student_record.study_hours,
            'participation_level': student_record.class_participation,
            'extracurricular_involvement': student_record.extracurricular_activity
        }
        
        # Get latest prediction if available
        latest_prediction = recent_predictions[0] if recent_predictions else None
        
        return jsonify({
            'success': True,
            'data': {
                'student_info': student_record.to_dict(),
                'performance_metrics': performance_metrics,
                'latest_prediction': latest_prediction.to_dict() if latest_prediction else None,
                'prediction_history': [pred.to_dict() for pred in recent_predictions]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get dashboard data',
            'error': str(e)
        }), 500

@student_bp.route('/predict', methods=['POST'])
@student_required
def predict_performance():
    """Get AI prediction for student performance"""
    try:
        user_id = get_jwt_identity()
        
        # Get student record
        student_record = StudentRecord.query.filter_by(user_id=user_id).first()
        
        if not student_record:
            return jsonify({
                'success': False,
                'message': 'Student record not found'
            }), 404
        
        # Import prediction module (will be created in Phase 2)
        try:
            from ml.ml_utils import get_ml_manager, convert_student_record_to_features
            
            # Get ML manager and make prediction
            ml_manager = get_ml_manager()
            features = convert_student_record_to_features(student_record)
            prediction_result = ml_manager.predict_student(features)
            
            if not prediction_result['success']:
                return jsonify({
                    'success': False,
                    'message': prediction_result['error']
                }), 503
            
            prediction_data = prediction_result['prediction']
            
            # Save prediction log
            prediction_log = PredictionLog(
                user_id=user_id,
                student_record_id=student_record.id,
                prediction_result=prediction_data['prediction'],
                prediction_probability=prediction_data['probability'],
                risk_level=prediction_data['risk_level'],
                model_used=prediction_data['model_used'],
                feedback_message=prediction_data['feedback']
            )
            prediction_log.set_input_features(features)
            
            db.session.add(prediction_log)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': {
                    'prediction': prediction_data,
                    'log_id': prediction_log.id
                }
            }), 200
            
        except ImportError:
            return jsonify({
                'success': False,
                'message': 'ML model not available. Please train the model first.'
            }), 503
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Prediction failed',
            'error': str(e)
        }), 500

@student_bp.route('/performance', methods=['GET'])
@student_required
def get_performance_data():
    """Get detailed performance analytics"""
    try:
        user_id = get_jwt_identity()
        
        # Get student record
        student_record = StudentRecord.query.filter_by(user_id=user_id).first()
        
        if not student_record:
            return jsonify({
                'success': False,
                'message': 'Student record not found'
            }), 404
        
        # Calculate detailed metrics
        marks_breakdown = {
            'internal_marks': student_record.internal_marks,
            'assignment_score': student_record.assignment_score,
            'final_exam_marks': student_record.final_exam_marks,
            'previous_sem_marks': student_record.previous_sem_marks
        }
        
        # Performance trends (mock data for now - can be enhanced with historical data)
        performance_trends = {
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'scores': [
                student_record.previous_sem_marks,
                student_record.previous_sem_marks + 5,
                student_record.internal_marks,
                student_record.assignment_score,
                student_record.final_exam_marks,
                round((student_record.internal_marks + student_record.assignment_score + student_record.final_exam_marks) / 3)
            ]
        }
        
        # Study patterns
        study_patterns = {
            'daily_hours': student_record.study_hours / 7,  # Convert weekly to daily
            'attendance_pattern': student_record.attendance_percentage,
            'participation_score': 85 if student_record.class_participation == 'Yes' else 45,
            'activity_involvement': 90 if student_record.extracurricular_activity == 'Yes' else 30
        }
        
        return jsonify({
            'success': True,
            'data': {
                'marks_breakdown': marks_breakdown,
                'performance_trends': performance_trends,
                'study_patterns': study_patterns,
                'overall_gpa': round(sum(marks_breakdown.values()) / len(marks_breakdown) / 10, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get performance data',
            'error': str(e)
        }), 500

@student_bp.route('/report/download', methods=['GET'])
@student_required
def download_report():
    """Generate and download PDF report"""
    try:
        user_id = get_jwt_identity()
        
        # Get student record
        student_record = StudentRecord.query.filter_by(user_id=user_id).first()
        
        if not student_record:
            return jsonify({
                'success': False,
                'message': 'Student record not found'
            }), 404
        
        # Import PDF generation utility (will be created in Phase 6)
        try:
            from utils.pdf_generator import generate_student_report
            from ml.ml_utils import get_ml_manager, convert_student_record_to_features
            
            # Get latest prediction for the report
            latest_prediction = PredictionLog.query.filter_by(
                user_id=user_id
            ).order_by(PredictionLog.created_at.desc()).first()
            
            prediction_data = None
            if latest_prediction:
                prediction_data = latest_prediction.to_dict()
            else:
                # Generate a fresh prediction for the report
                try:
                    ml_manager = get_ml_manager()
                    features = convert_student_record_to_features(student_record)
                    prediction_result = ml_manager.predict_student(features)
                    
                    if prediction_result['success']:
                        prediction_data = prediction_result['prediction']
                except Exception as e:
                    print(f"Could not generate prediction for report: {e}")
            
            # Generate PDF report
            pdf_path = generate_student_report(student_record, prediction_data)
            
            # Get just the filename for the response
            filename = os.path.basename(pdf_path)
            
            return jsonify({
                'success': True,
                'message': 'Report generated successfully',
                'data': {
                    'download_url': f'/api/student/report/file/{filename}',
                    'filename': filename,
                    'generated_at': datetime.now().isoformat()
                }
            }), 200
            
        except ImportError:
            return jsonify({
                'success': False,
                'message': 'PDF generation not available'
            }), 503
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Report generation failed',
            'error': str(e)
        }), 500

@student_bp.route('/predictions/history', methods=['GET'])
@student_required
def get_prediction_history():
    """Get student's prediction history"""
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get predictions with pagination
        predictions = PredictionLog.query.filter_by(
            user_id=user_id
        ).order_by(PredictionLog.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'predictions': [pred.to_dict() for pred in predictions.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': predictions.total,
                    'pages': predictions.pages,
                    'has_next': predictions.has_next,
                    'has_prev': predictions.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get prediction history',
            'error': str(e)
        }), 500

@student_bp.route('/report/file/<filename>', methods=['GET'])
@student_required
def download_report_file(filename):
    """Serve PDF report file for download"""
    try:
        user_id = get_jwt_identity()
        
        # Security check - ensure user can only access their own reports
        # Extract student ID from filename if possible
        reports_dir = 'reports'
        file_path = os.path.join(reports_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': 'Report file not found'
            }), 404
        
        # Additional security: check if filename contains user's student record ID
        student_record = StudentRecord.query.filter_by(user_id=user_id).first()
        if student_record and student_record.student_id not in filename:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to download report',
            'error': str(e)
        }), 500