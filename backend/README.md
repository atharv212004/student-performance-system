# Student Performance Analytics - Backend

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Setup
```bash
python test_setup.py
```

### 3. Run Application
```bash
python app.py
```

The backend will be available at: `http://localhost:5000`

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh token

### Student Routes
- `GET /api/student/dashboard` - Student dashboard
- `POST /api/student/predict` - Get AI prediction
- `GET /api/student/performance` - Performance data
- `GET /api/student/report/download` - Download PDF report

### Faculty Routes
- `GET /api/faculty/students` - All students
- `PUT /api/faculty/student/:id/update` - Update student
- `POST /api/faculty/upload-dataset` - Upload CSV/Excel
- `GET /api/faculty/analytics` - Analytics data

### Admin Routes
- `GET /api/admin/users` - All users
- `PUT /api/admin/user/:id` - Update user
- `DELETE /api/admin/user/:id` - Delete user
- `POST /api/admin/train-model` - Train ML model
- `GET /api/admin/system-insights` - System insights

## 🔑 Demo Accounts

| Role    | Email            | Password   |
|---------|------------------|------------|
| Student | student@demo.com | student123 |
| Faculty | faculty@demo.com | faculty123 |
| Admin   | admin@demo.com   | admin123   |

## 🏗️ Project Structure

```
backend/
├── app.py                 # Flask application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── models/
│   └── db_models.py      # Database models
├── routes/               # API routes
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── faculty_routes.py
│   └── admin_routes.py
├── ml/                   # ML pipeline (Phase 2)
├── utils/                # Utilities (Phase 6)
└── data/                 # Dataset
    └── clean_student_dataset.xlsx
```

## 🔧 Configuration

The application uses SQLite by default. To use a different database, set the `DATABASE_URL` environment variable.

## 🧪 Testing

Run the setup test to verify everything is working:
```bash
python test_setup.py
```

## 📊 Database Schema

### Users Table
- id, email, password_hash, role, full_name, is_active, created_at, updated_at

### Student Records Table
- id, user_id, student_id, student_name, gender, age, study_hours, attendance_percentage, internal_marks, assignment_score, previous_sem_marks, class_participation, extracurricular_activity, final_exam_marks, result, created_at, updated_at

### Prediction Logs Table
- id, user_id, student_record_id, prediction_result, prediction_probability, risk_level, model_used, input_features, feedback_message, created_at

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- Role-based access control
- CORS protection
- Input validation
- SQL injection prevention (ORM)

---

**Phase 1 Complete!** ✅

Next: Phase 2 - ML Pipeline Development