#!/usr/bin/env python3
"""
Test script to verify backend setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy imported successfully")
        
        from flask_jwt_extended import JWTManager
        print("✅ Flask-JWT-Extended imported successfully")
        
        from flask_cors import CORS
        print("✅ Flask-CORS imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import numpy as np
        print("✅ Numpy imported successfully")
        
        from sklearn.model_selection import train_test_split
        print("✅ Scikit-learn imported successfully")
        
        import xgboost as xgb
        print("✅ XGBoost imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    print("\n🏗️ Testing app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        
        with app.app_context():
            from models.db_models import db
            print("✅ Database models loaded successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_dataset():
    """Test if dataset can be loaded"""
    print("\n📊 Testing dataset...")
    
    try:
        import pandas as pd
        df = pd.read_excel('data/clean_student_dataset.xlsx')
        print(f"✅ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        
        required_columns = [
            'student_id', 'student_name', 'gender', 'age', 'study_hours',
            'attendance_percentage', 'internal_marks', 'assignment_score',
            'previous_sem_marks', 'class_participation', 'extracurricular_activity',
            'final_exam_marks', 'result'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        
        print("✅ All required columns present")
        return True
        
    except Exception as e:
        print(f"❌ Dataset error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Backend Setup Verification")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("App Creation Test", test_app_creation),
        ("Dataset Test", test_dataset)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Backend setup is ready.")
        print("\n📝 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python app.py")
        print("3. Test API: curl http://localhost:5000/api/health")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()