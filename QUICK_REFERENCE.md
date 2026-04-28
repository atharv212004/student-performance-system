# 🚀 Quick Reference Guide

## Student Performance Analytics System - Common Tasks & Commands

---

## 📋 Table of Contents
1. [Starting the Application](#starting-the-application)
2. [Demo Accounts](#demo-accounts)
3. [Common Backend Tasks](#common-backend-tasks)
4. [Common Frontend Tasks](#common-frontend-tasks)
5. [API Endpoints](#api-endpoints)
6. [Troubleshooting](#troubleshooting)
7. [File Locations](#file-locations)

---

## 🚀 Starting the Application

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```
**URL**: http://localhost:5000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
**URL**: http://localhost:5173

---

## 👥 Demo Accounts

### Student
```
Email: student@example.com
Password: student123
```

### Faculty
```
Email: faculty@example.com
Password: faculty123
```

### Admin
```
Email: admin@example.com
Password: admin123
```

---

## 🔧 Common Backend Tasks

### Initialize Database
```bash
cd backend
python test_setup.py
```

### Train ML Model
```bash
cd backend/ml
python train_model.py
```

### Test API Endpoints
```bash
cd backend
python test_complete_system.py
```

### View Model Performance
```bash
cd backend/ml
python model_evaluation.py
```

### Generate API Documentation
```bash
cd backend
python -c "from utils.api_docs import generate_api_documentation; generate_api_documentation()"
```

### Reset Database
```bash
cd backend
rm instance/student_performance.db
python test_setup.py
```

---

## 🎨 Common Frontend Tasks

### Install Dependencies
```bash
cd frontend
npm install
```

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Lint Code
```bash
npm run lint
```

### Clear Cache
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 🌐 API Endpoints

### Authentication
```
POST   /api/auth/register      - Register new user
POST   /api/auth/login         - Login user
GET    /api/auth/me            - Get current user
POST   /api/auth/refresh       - Refresh token
```

### Student Endpoints
```
GET    /api/student/dashboard           - Get dashboard data
POST   /api/student/predict             - Generate prediction
GET    /api/student/performance         - Get performance data
GET    /api/student/report/download     - Download PDF report
GET    /api/student/predictions/history - Get prediction history
```

### Faculty Endpoints
```
GET    /api/faculty/students            - Get all students
GET    /api/faculty/student/:id         - Get student details
PUT    /api/faculty/student/:id/update  - Update student
POST   /api/faculty/upload-dataset      - Upload CSV/Excel
GET    /api/faculty/analytics           - Get analytics
```

### Admin Endpoints
```
GET    /api/admin/users                 - Get all users
PUT    /api/admin/user/:id              - Update user
DELETE /api/admin/user/:id              - Delete user
POST   /api/admin/train-model           - Train ML model
GET    /api/admin/system-insights       - Get system stats
GET    /api/admin/predictions/logs      - Get prediction logs
```

---

## 🔍 Troubleshooting

### Backend Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Frontend Port Already in Use
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5173 | xargs kill -9
```

### Module Not Found (Backend)
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Dependencies Error (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Locked Error
```bash
cd backend
rm instance/student_performance.db
python test_setup.py
```

### CORS Error
- Ensure backend is running on port 5000
- Check `vite.config.js` proxy settings
- Verify CORS is enabled in `backend/app.py`

### ML Model Not Found
```bash
cd backend/ml
python train_model.py
```

---

## 📁 File Locations

### Configuration Files
```
backend/config.py              - Backend configuration
frontend/vite.config.js        - Frontend configuration
frontend/tailwind.config.js    - Tailwind CSS config
```

### Database
```
backend/instance/student_performance.db  - SQLite database
```

### ML Models
```
backend/ml/saved/best_model.pkl         - Best trained model
backend/ml/saved/preprocessor.pkl       - Data preprocessor
backend/ml/saved/model_metadata.json    - Model metadata
```

### Dataset
```
clean_student_dataset.xlsx              - Sample dataset
backend/data/clean_student_dataset.xlsx - Backend copy
```

### API Documentation
```
backend/API_DOCUMENTATION.md            - Full API docs
backend/API_ROUTES_SUMMARY.md           - API summary
backend/api_documentation.json          - JSON format
```

### Reports
```
backend/reports/                        - Generated PDF reports
```

---

## 🎯 Common Workflows

### Add New Student (Faculty)
1. Login as faculty
2. Go to "Students" page
3. Click "Add Student" or upload CSV
4. Fill in student details
5. Save

### Generate Prediction (Student)
1. Login as student
2. Go to dashboard
3. Click "Get AI Prediction"
4. View results and feedback

### Train New Model (Admin)
1. Login as admin
2. Go to "System Management"
3. Click "Retrain ML Model"
4. Wait for training to complete
5. View results

### Upload Dataset (Faculty)
1. Login as faculty
2. Go to "Students" page
3. Click "Upload Dataset"
4. Select CSV/Excel file
5. Confirm upload

### Manage Users (Admin)
1. Login as admin
2. Go to "User Management"
3. Search/filter users
4. Edit or delete as needed

---

## 🔑 Environment Variables

### Backend (.env)
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///instance/student_performance.db
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5000/api
```

---

## 📊 Database Schema

### Users Table
```
id, email, password_hash, full_name, role, is_active, created_at
```

### StudentRecords Table
```
id, user_id, student_id, student_name, age, gender, 
attendance_percentage, study_hours_per_week, previous_exam_marks,
extracurricular_activity, parental_education_level, 
distance_from_home, internet_access, class_participation,
final_exam_marks, result, created_at, updated_at
```

### PredictionLogs Table
```
id, user_id, student_record_id, prediction_result, probability,
risk_level, feedback_message, model_used, created_at
```

---

## 🧪 Testing Commands

### Test Backend
```bash
cd backend
python test_simple.py           # Simple test
python test_setup.py            # Setup test
python test_complete_system.py  # Complete test
python tests/test_api_routes.py # API tests
```

### Test Frontend
```bash
cd frontend
npm run lint                    # Lint check
npm run build                   # Build test
```

---

## 📦 Deployment Commands

### Backend (Heroku)
```bash
heroku create your-app-name
git push heroku main
heroku run python test_setup.py
```

### Frontend (Vercel)
```bash
npm run build
vercel --prod
```

### Frontend (Netlify)
```bash
npm run build
netlify deploy --prod
```

---

## 🔄 Update Commands

### Update Backend Dependencies
```bash
cd backend
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Update Frontend Dependencies
```bash
cd frontend
npm update
npm audit fix
```

---

## 📝 Useful Scripts

### Create New Admin User
```python
# In Python shell
from backend.app import app, db
from backend.models.db_models import User

with app.app_context():
    user = User(
        email='newadmin@example.com',
        full_name='New Admin',
        role='admin'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

### Check Database Records
```python
# In Python shell
from backend.app import app, db
from backend.models.db_models import User, StudentRecord

with app.app_context():
    print(f"Users: {User.query.count()}")
    print(f"Students: {StudentRecord.query.count()}")
```

---

## 🎨 Customization

### Change Theme Colors (Frontend)
Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {...},  // Change primary color
      success: {...},  // Change success color
    }
  }
}
```

### Change Port (Backend)
Edit `backend/app.py`:
```python
app.run(debug=True, port=5001)  # Change port
```

### Change Port (Frontend)
Edit `frontend/vite.config.js`:
```javascript
server: {
  port: 3000  // Change port
}
```

---

## 📚 Documentation Links

- **Setup Guide**: [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- **Completion Report**: [PROJECT_COMPLETION_SUMMARY.md](PROJECT_COMPLETION_SUMMARY.md)
- **API Documentation**: [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)
- **ML Documentation**: [backend/ml/README.md](backend/ml/README.md)

---

## 🆘 Quick Help

### Backend Not Starting?
1. Check if virtual environment is activated
2. Verify all dependencies are installed
3. Check if port 5000 is available
4. Review error messages in terminal

### Frontend Not Starting?
1. Check if node_modules exists
2. Verify npm install completed
3. Check if port 5173 is available
4. Clear cache and reinstall

### Can't Login?
1. Verify backend is running
2. Check database exists
3. Run `python test_setup.py` to recreate demo accounts
4. Check browser console for errors

### Predictions Not Working?
1. Verify ML model is trained
2. Check `backend/ml/saved/` directory
3. Run `python ml/train_model.py`
4. Check student has complete data

---

## ✅ Quick Checklist

Before starting development:
- [ ] Backend virtual environment activated
- [ ] Backend dependencies installed
- [ ] Database initialized
- [ ] ML model trained
- [ ] Frontend dependencies installed
- [ ] Both servers running
- [ ] Can access http://localhost:5173
- [ ] Can login with demo accounts

---

**For detailed information, see [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)**

*Last Updated: 2026*
