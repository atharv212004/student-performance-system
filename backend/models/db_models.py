from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, faculty, admin
    full_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=True, index=True)  # For students
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)  # For faculty verification by admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_records = db.relationship('StudentRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    prediction_logs = db.relationship('PredictionLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'full_name': self.full_name,
            'student_id': self.student_id,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class StudentRecord(db.Model):
    __tablename__ = 'student_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    student_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    study_hours = db.Column(db.Integer, nullable=False)
    attendance_percentage = db.Column(db.Integer, nullable=False)
    internal_marks = db.Column(db.Integer, nullable=False)
    assignment_score = db.Column(db.Integer, nullable=False)
    previous_sem_marks = db.Column(db.Integer, nullable=False)
    class_participation = db.Column(db.String(10), nullable=False)  # Yes/No
    extracurricular_activity = db.Column(db.String(10), nullable=False)  # Yes/No
    final_exam_marks = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(10), nullable=True)  # Pass/Fail - can be null for predictions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert student record to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'student_name': self.student_name,
            'gender': self.gender,
            'age': self.age,
            'study_hours': self.study_hours,
            'attendance_percentage': self.attendance_percentage,
            'internal_marks': self.internal_marks,
            'assignment_score': self.assignment_score,
            'previous_sem_marks': self.previous_sem_marks,
            'class_participation': self.class_participation,
            'extracurricular_activity': self.extracurricular_activity,
            'final_exam_marks': self.final_exam_marks,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_features_dict(self):
        """Get features for ML prediction"""
        return {
            'gender': self.gender,
            'age': self.age,
            'study_hours': self.study_hours,
            'attendance_percentage': self.attendance_percentage,
            'internal_marks': self.internal_marks,
            'assignment_score': self.assignment_score,
            'previous_sem_marks': self.previous_sem_marks,
            'class_participation': self.class_participation,
            'extracurricular_activity': self.extracurricular_activity,
            'final_exam_marks': self.final_exam_marks
        }
    
    def __repr__(self):
        return f'<StudentRecord {self.student_id}>'

class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_record_id = db.Column(db.Integer, db.ForeignKey('student_records.id'), nullable=True)
    prediction_result = db.Column(db.String(10), nullable=False)  # Pass/Fail
    prediction_probability = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(10), nullable=False)  # Low/Medium/High
    model_used = db.Column(db.String(50), nullable=False)
    input_features = db.Column(db.Text, nullable=False)  # JSON string of input features
    feedback_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    student_record = db.relationship('StudentRecord', backref='predictions', lazy=True)
    
    def set_input_features(self, features_dict):
        """Store input features as JSON string"""
        self.input_features = json.dumps(features_dict)
    
    def get_input_features(self):
        """Get input features as dictionary"""
        return json.loads(self.input_features) if self.input_features else {}
    
    def to_dict(self):
        """Convert prediction log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_record_id': self.student_record_id,
            'prediction_result': self.prediction_result,
            'prediction_probability': self.prediction_probability,
            'risk_level': self.risk_level,
            'model_used': self.model_used,
            'input_features': self.get_input_features(),
            'feedback_message': self.feedback_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<PredictionLog {self.id} - {self.prediction_result}>'

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='password_resets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'is_used': self.is_used,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

class StudentReport(db.Model):
    __tablename__ = 'student_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_record_id = db.Column(db.Integer, db.ForeignKey('student_records.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # academic, performance, prediction, comprehensive
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    report_data = db.Column(db.Text, nullable=True)  # JSON string
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    downloaded_at = db.Column(db.DateTime, nullable=True)
    download_count = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref='reports')
    student_record = db.relationship('StudentRecord', backref='reports')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_record_id': self.student_record_id,
            'report_type': self.report_type,
            'file_name': self.file_name,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'downloaded_at': self.downloaded_at.isoformat() if self.downloaded_at else None,
            'download_count': self.download_count
        }

# Database initialization function
def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            # Create default users if they don't exist
            create_default_users()
        except Exception as e:
            print(f"⚠️ Error during initial DB creation: {e}")
            print("🔄 Attempting to drop and recreate all tables...")
            try:
                # Drop all tables and recreate
                db.drop_all()
                db.create_all()
                # Create default users
                create_default_users()
                print("✅ Database recreated successfully")
            except Exception as e2:
                print(f"❌ Failed to recreate database: {e2}")
                raise

def create_default_users():
    """Create default demo users"""
    default_users = [
        {
            'email': 'atharv@admin.io',
            'username': 'Atharv Pai',
            'password': '123456',
            'role': 'admin',
            'full_name': 'Atharv Pai'
        },
        {
            'email': 'faculty@demo.com',
            'password': 'faculty123',
            'role': 'faculty',
            'full_name': 'Faculty User',
            'is_verified': True
        },
        {
            'email': 'john@student.io',
            'username': 'John - STU001',
            'password': 'john@student.io',
            'role': 'student',
            'full_name': 'John',
            'student_id': 'STU001'
        },
        {
            'email': 'sarah@student.io',
            'username': 'Sarah - STU002',
            'password': 'sarah@student.io',
            'role': 'student',
            'full_name': 'Sarah',
            'student_id': 'STU002'
        }
    ]
    
    for user_data in default_users:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            user = User(
                email=user_data['email'],
                username=user_data.get('username'),
                role=user_data['role'],
                full_name=user_data['full_name'],
                student_id=user_data.get('student_id'),
                is_verified=user_data.get('is_verified', False)
            )
            user.set_password(user_data['password'])
            db.session.add(user)
    
    try:
        db.session.commit()
        print("Default users created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default users: {e}")