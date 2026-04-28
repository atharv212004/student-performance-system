from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_models import db, User, StudentRecord, PredictionLog
from functools import wraps
import pandas as pd
import os
from werkzeug.utils import secure_filename

faculty_bp = Blueprint('faculty', __name__)

def faculty_required(f):
    """Decorator to ensure user has faculty role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ['faculty', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Faculty access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@faculty_bp.route('/students', methods=['GET'])
@faculty_required
def get_all_students():
    """Get all student records with optional filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        result_filter = request.args.get('result', '', type=str)
        
        # Build query
        query = StudentRecord.query
        
        # Apply search filter
        if search:
            query = query.filter(
                db.or_(
                    StudentRecord.student_name.ilike(f'%{search}%'),
                    StudentRecord.student_id.ilike(f'%{search}%')
                )
            )
        
        # Apply result filter
        if result_filter and result_filter in ['Pass', 'Fail']:
            query = query.filter(StudentRecord.result == result_filter)
        
        # Get paginated results
        students = query.order_by(StudentRecord.student_name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get statistics
        total_students = StudentRecord.query.count()
        pass_count = StudentRecord.query.filter_by(result='Pass').count()
        fail_count = StudentRecord.query.filter_by(result='Fail').count()
        
        return jsonify({
            'success': True,
            'data': {
                'students': [student.to_dict() for student in students.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': students.total,
                    'pages': students.pages,
                    'has_next': students.has_next,
                    'has_prev': students.has_prev
                },
                'statistics': {
                    'total_students': total_students,
                    'pass_count': pass_count,
                    'fail_count': fail_count,
                    'pass_rate': round((pass_count / total_students * 100), 2) if total_students > 0 else 0
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get students',
            'error': str(e)
        }), 500

@faculty_bp.route('/student/<int:student_id>/update', methods=['PUT'])
@faculty_required
def update_student_marks(student_id):
    """Update student marks and information"""
    try:
        data = request.get_json()
        
        # Get student record
        student = StudentRecord.query.get(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        # Update allowed fields
        updatable_fields = [
            'study_hours', 'attendance_percentage', 'internal_marks',
            'assignment_score', 'final_exam_marks', 'class_participation',
            'extracurricular_activity', 'result'
        ]
        
        updated_fields = []
        for field in updatable_fields:
            if field in data:
                old_value = getattr(student, field)
                new_value = data[field]
                
                # Validate numeric fields
                if field in ['study_hours', 'attendance_percentage', 'internal_marks', 
                           'assignment_score', 'final_exam_marks']:
                    if not isinstance(new_value, (int, float)) or new_value < 0:
                        return jsonify({
                            'success': False,
                            'message': f'{field} must be a positive number'
                        }), 400
                    
                    # Validate percentage fields
                    if field == 'attendance_percentage' and new_value > 100:
                        return jsonify({
                            'success': False,
                            'message': 'Attendance percentage cannot exceed 100'
                        }), 400
                    
                    # Validate marks fields (assuming max 100)
                    if field in ['internal_marks', 'assignment_score', 'final_exam_marks'] and new_value > 100:
                        return jsonify({
                            'success': False,
                            'message': f'{field} cannot exceed 100'
                        }), 400
                
                # Validate categorical fields
                if field in ['class_participation', 'extracurricular_activity']:
                    if new_value not in ['Yes', 'No']:
                        return jsonify({
                            'success': False,
                            'message': f'{field} must be "Yes" or "No"'
                        }), 400
                
                if field == 'result' and new_value not in ['Pass', 'Fail', None]:
                    return jsonify({
                        'success': False,
                        'message': 'Result must be "Pass" or "Fail"'
                    }), 400
                
                setattr(student, field, new_value)
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
            'message': f'Student updated successfully. Fields updated: {", ".join(updated_fields)}',
            'data': {
                'student': student.to_dict(),
                'updated_fields': updated_fields
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update student',
            'error': str(e)
        }), 500

@faculty_bp.route('/upload-dataset', methods=['POST'])
@faculty_required
def upload_dataset():
    """Upload and process student dataset (CSV/Excel)"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename, {'csv', 'xlsx', 'xls'}):
            return jsonify({
                'success': False,
                'message': 'Invalid file type. Only CSV and Excel files are allowed'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Read and process file
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            # Validate required columns
            required_columns = [
                'student_id', 'student_name', 'gender', 'age', 'study_hours',
                'attendance_percentage', 'internal_marks', 'assignment_score',
                'previous_sem_marks', 'class_participation', 'extracurricular_activity',
                'final_exam_marks'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return jsonify({
                    'success': False,
                    'message': f'Missing required columns: {", ".join(missing_columns)}'
                }), 400
            
            # Process and save records
            added_count = 0
            updated_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Check if student already exists
                    existing_student = StudentRecord.query.filter_by(
                        student_id=row['student_id']
                    ).first()
                    
                    if existing_student:
                        # Update existing record
                        for col in required_columns:
                            if col in df.columns and pd.notna(row[col]):
                                setattr(existing_student, col, row[col])
                        
                        # Set result if available
                        if 'result' in df.columns and pd.notna(row['result']):
                            existing_student.result = row['result']
                        
                        updated_count += 1
                    else:
                        # Create new record
                        student_data = {col: row[col] for col in required_columns if pd.notna(row[col])}
                        
                        # Set result if available
                        if 'result' in df.columns and pd.notna(row['result']):
                            student_data['result'] = row['result']
                        
                        # Create user account for student if not exists
                        user_email = f"{row['student_id'].lower()}@student.edu"
                        existing_user = User.query.filter_by(email=user_email).first()
                        
                        if not existing_user:
                            user = User(
                                email=user_email,
                                full_name=row['student_name'],
                                role='student'
                            )
                            user.set_password('student123')  # Default password
                            db.session.add(user)
                            db.session.flush()  # Get user ID
                            student_data['user_id'] = user.id
                        else:
                            student_data['user_id'] = existing_user.id
                        
                        student = StudentRecord(**student_data)
                        db.session.add(student)
                        added_count += 1
                        
                except Exception as row_error:
                    errors.append(f"Row {index + 1}: {str(row_error)}")
            
            db.session.commit()
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'message': 'Dataset uploaded successfully',
                'data': {
                    'total_rows': len(df),
                    'added_count': added_count,
                    'updated_count': updated_count,
                    'errors': errors[:10]  # Limit errors shown
                }
            }), 200
            
        except Exception as process_error:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            raise process_error
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Dataset upload failed',
            'error': str(e)
        }), 500

@faculty_bp.route('/analytics', methods=['GET'])
@faculty_required
def get_analytics_data():
    """Get analytics data for faculty dashboard"""
    try:
        # Get basic statistics
        total_students = StudentRecord.query.count()
        pass_count = StudentRecord.query.filter_by(result='Pass').count()
        fail_count = StudentRecord.query.filter_by(result='Fail').count()
        
        # Get average scores
        avg_internal = db.session.query(db.func.avg(StudentRecord.internal_marks)).scalar() or 0
        avg_assignment = db.session.query(db.func.avg(StudentRecord.assignment_score)).scalar() or 0
        avg_final = db.session.query(db.func.avg(StudentRecord.final_exam_marks)).scalar() or 0
        avg_attendance = db.session.query(db.func.avg(StudentRecord.attendance_percentage)).scalar() or 0
        
        # Get gender distribution
        gender_stats = db.session.query(
            StudentRecord.gender,
            db.func.count(StudentRecord.id)
        ).group_by(StudentRecord.gender).all()
        
        # Get participation statistics
        participation_stats = db.session.query(
            StudentRecord.class_participation,
            db.func.count(StudentRecord.id)
        ).group_by(StudentRecord.class_participation).all()
        
        # Get extracurricular statistics
        activity_stats = db.session.query(
            StudentRecord.extracurricular_activity,
            db.func.count(StudentRecord.id)
        ).group_by(StudentRecord.extracurricular_activity).all()
        
        # Get marks distribution (for charts)
        marks_ranges = [
            ('0-40', StudentRecord.query.filter(StudentRecord.final_exam_marks < 40).count()),
            ('40-60', StudentRecord.query.filter(
                db.and_(StudentRecord.final_exam_marks >= 40, StudentRecord.final_exam_marks < 60)
            ).count()),
            ('60-80', StudentRecord.query.filter(
                db.and_(StudentRecord.final_exam_marks >= 60, StudentRecord.final_exam_marks < 80)
            ).count()),
            ('80-100', StudentRecord.query.filter(StudentRecord.final_exam_marks >= 80).count())
        ]
        
        # Get recent predictions count
        recent_predictions = PredictionLog.query.filter(
            PredictionLog.created_at >= db.func.date('now', '-7 days')
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_students': total_students,
                    'pass_count': pass_count,
                    'fail_count': fail_count,
                    'pass_rate': round((pass_count / total_students * 100), 2) if total_students > 0 else 0,
                    'recent_predictions': recent_predictions
                },
                'averages': {
                    'internal_marks': round(avg_internal, 2),
                    'assignment_score': round(avg_assignment, 2),
                    'final_exam_marks': round(avg_final, 2),
                    'attendance_percentage': round(avg_attendance, 2)
                },
                'distributions': {
                    'gender': dict(gender_stats),
                    'participation': dict(participation_stats),
                    'activities': dict(activity_stats),
                    'marks_ranges': dict(marks_ranges)
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get analytics data',
            'error': str(e)
        }), 500

@faculty_bp.route('/student/<int:student_id>', methods=['GET'])
@faculty_required
def get_student_details(student_id):
    """Get detailed information about a specific student"""
    try:
        student = StudentRecord.query.get(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        # Get student's prediction history
        predictions = PredictionLog.query.filter_by(
            student_record_id=student_id
        ).order_by(PredictionLog.created_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'student': student.to_dict(),
                'predictions': [pred.to_dict() for pred in predictions]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to get student details',
            'error': str(e)
        }), 500