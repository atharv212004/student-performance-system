"""
ML Utilities for Student Performance Prediction System
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from ml.data_preprocessing import DataPreprocessor
from ml.predict import StudentPerformancePredictor

class MLModelManager:
    """
    Centralized ML model management for the Flask application
    """
    
    def __init__(self, model_dir='ml/saved'):
        self.model_dir = model_dir
        self.predictor = StudentPerformancePredictor()
        self.is_initialized = False
        
    def initialize(self):
        """Initialize the ML system"""
        try:
            if self.predictor.load_model(self.model_dir):
                self.is_initialized = True
                print("✅ ML system initialized successfully")
                return True
            else:
                print("❌ Failed to initialize ML system")
                return False
        except Exception as e:
            print(f"❌ ML initialization error: {e}")
            return False
    
    def is_model_available(self):
        """Check if ML model is available"""
        model_path = os.path.join(self.model_dir, 'best_model.pkl')
        preprocessor_path = os.path.join(self.model_dir, 'preprocessor.pkl')
        metadata_path = os.path.join(self.model_dir, 'model_metadata.json')
        
        return all([
            os.path.exists(model_path),
            os.path.exists(preprocessor_path),
            os.path.exists(metadata_path)
        ])
    
    def get_model_status(self):
        """Get comprehensive model status"""
        status = {
            'available': self.is_model_available(),
            'initialized': self.is_initialized,
            'model_info': None,
            'last_training': None,
            'performance_metrics': None
        }
        
        if status['available']:
            try:
                # Load metadata
                metadata_path = os.path.join(self.model_dir, 'model_metadata.json')
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                status['model_info'] = {
                    'best_model': metadata['best_model_name'],
                    'training_date': metadata['training_date']
                }
                
                status['last_training'] = metadata['training_date']
                
                # Get performance metrics for best model
                best_model_name = metadata['best_model_name']
                if best_model_name in metadata['model_scores']:
                    status['performance_metrics'] = metadata['model_scores'][best_model_name]
                
            except Exception as e:
                print(f"⚠️ Error reading model metadata: {e}")
        
        return status
    
    def predict_student(self, student_data):
        """
        Predict student performance
        
        Args:
            student_data (dict): Student features
            
        Returns:
            dict: Prediction results or error
        """
        if not self.is_initialized:
            if not self.initialize():
                return {
                    'success': False,
                    'error': 'ML model not available. Please train the model first.'
                }
        
        try:
            result = self.predictor.predict_single_student(student_data)
            return {
                'success': True,
                'prediction': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def batch_predict(self, students_data):
        """
        Predict performance for multiple students
        
        Args:
            students_data (list): List of student feature dictionaries
            
        Returns:
            dict: Batch prediction results
        """
        if not self.is_initialized:
            if not self.initialize():
                return {
                    'success': False,
                    'error': 'ML model not available. Please train the model first.'
                }
        
        try:
            results = self.predictor.batch_predict(students_data)
            return {
                'success': True,
                'predictions': results
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global ML manager instance
_ml_manager = None

def get_ml_manager():
    """Get or create global ML manager instance"""
    global _ml_manager
    if _ml_manager is None:
        _ml_manager = MLModelManager()
    return _ml_manager

def convert_student_record_to_features(student_record):
    """
    Convert StudentRecord model to feature dictionary for ML prediction
    
    Args:
        student_record: StudentRecord model instance
        
    Returns:
        dict: Feature dictionary for ML prediction
    """
    return {
        'gender': student_record.gender,
        'age': student_record.age,
        'study_hours': student_record.study_hours,
        'attendance_percentage': student_record.attendance_percentage,
        'internal_marks': student_record.internal_marks,
        'assignment_score': student_record.assignment_score,
        'previous_sem_marks': student_record.previous_sem_marks,
        'class_participation': student_record.class_participation,
        'extracurricular_activity': student_record.extracurricular_activity,
        'final_exam_marks': student_record.final_exam_marks
    }

def validate_student_features(features):
    """
    Validate student features for ML prediction
    
    Args:
        features (dict): Student features dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_features = [
        'gender', 'age', 'study_hours', 'attendance_percentage',
        'internal_marks', 'assignment_score', 'previous_sem_marks',
        'class_participation', 'extracurricular_activity', 'final_exam_marks'
    ]
    
    # Check required features
    missing_features = [f for f in required_features if f not in features]
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features)}"
    
    # Validate data types and ranges
    try:
        # Numeric validations
        numeric_features = {
            'age': (15, 30),
            'study_hours': (0, 100),
            'attendance_percentage': (0, 100),
            'internal_marks': (0, 100),
            'assignment_score': (0, 100),
            'previous_sem_marks': (0, 100),
            'final_exam_marks': (0, 100)
        }
        
        for feature, (min_val, max_val) in numeric_features.items():
            value = features[feature]
            if not isinstance(value, (int, float)):
                return False, f"{feature} must be a number"
            if not (min_val <= value <= max_val):
                return False, f"{feature} must be between {min_val} and {max_val}"
        
        # Categorical validations
        if features['gender'] not in ['Male', 'Female']:
            return False, "gender must be 'Male' or 'Female'"
        
        if features['class_participation'] not in ['Yes', 'No']:
            return False, "class_participation must be 'Yes' or 'No'"
        
        if features['extracurricular_activity'] not in ['Yes', 'No']:
            return False, "extracurricular_activity must be 'Yes' or 'No'"
        
        return True, "Valid features"
        
    except Exception as e:
        return False, f"Feature validation error: {str(e)}"

def get_feature_importance_insights():
    """
    Get feature importance insights from the trained model
    
    Returns:
        dict: Feature importance analysis
    """
    ml_manager = get_ml_manager()
    
    if not ml_manager.is_model_available():
        return {
            'available': False,
            'message': 'Model not available'
        }
    
    try:
        # Load model and get feature importance
        model_path = os.path.join(ml_manager.model_dir, 'best_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load preprocessor to get feature names
        preprocessor = DataPreprocessor()
        preprocessor.load_preprocessor(os.path.join(ml_manager.model_dir, 'preprocessor.pkl'))
        
        insights = {
            'available': True,
            'feature_importance': None,
            'top_features': None,
            'insights': []
        }
        
        if hasattr(model, 'feature_importances_'):
            # Create feature importance dataframe
            importance_df = pd.DataFrame({
                'feature': preprocessor.feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            insights['feature_importance'] = importance_df.to_dict('records')
            insights['top_features'] = importance_df.head(5).to_dict('records')
            
            # Generate insights
            top_feature = importance_df.iloc[0]
            insights['insights'].append(f"Most important factor: {top_feature['feature']} ({top_feature['importance']:.3f})")
            
            # Categorize features
            academic_features = [f for f in importance_df['feature'].values if any(term in f.lower() for term in ['marks', 'score', 'performance'])]
            behavioral_features = [f for f in importance_df['feature'].values if any(term in f.lower() for term in ['attendance', 'participation', 'activity'])]
            
            if academic_features:
                insights['insights'].append(f"Key academic factors: {', '.join(academic_features[:3])}")
            
            if behavioral_features:
                insights['insights'].append(f"Key behavioral factors: {', '.join(behavioral_features[:3])}")
        
        return insights
        
    except Exception as e:
        return {
            'available': False,
            'message': f'Error analyzing feature importance: {str(e)}'
        }

def generate_model_performance_summary():
    """
    Generate a summary of model performance for dashboard display
    
    Returns:
        dict: Performance summary
    """
    ml_manager = get_ml_manager()
    status = ml_manager.get_model_status()
    
    if not status['available']:
        return {
            'available': False,
            'message': 'No trained model available'
        }
    
    try:
        summary = {
            'available': True,
            'model_name': status['model_info']['best_model'],
            'training_date': status['model_info']['training_date'],
            'performance': status['performance_metrics'],
            'status': 'Excellent' if status['performance_metrics']['f1_score'] > 0.9 else 'Good',
            'recommendations': []
        }
        
        # Add performance insights
        f1_score = status['performance_metrics']['f1_score']
        accuracy = status['performance_metrics']['test_accuracy']
        
        if f1_score > 0.95:
            summary['recommendations'].append("Model performance is excellent - ready for production use")
        elif f1_score > 0.85:
            summary['recommendations'].append("Model performance is good - suitable for most predictions")
        else:
            summary['recommendations'].append("Consider retraining with more data or feature engineering")
        
        if accuracy > 0.95:
            summary['recommendations'].append("High accuracy indicates reliable predictions")
        
        return summary
        
    except Exception as e:
        return {
            'available': False,
            'message': f'Error generating performance summary: {str(e)}'
        }

# Utility functions for data analysis
def analyze_dataset_statistics():
    """
    Analyze the dataset and provide statistics
    
    Returns:
        dict: Dataset statistics
    """
    try:
        preprocessor = DataPreprocessor()
        df = preprocessor.load_data()
        
        stats = {
            'total_records': len(df),
            'features': len(df.columns),
            'class_distribution': df['result'].value_counts().to_dict(),
            'missing_values': df.isnull().sum().sum(),
            'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
            'categorical_features': len(df.select_dtypes(include=['object']).columns)
        }
        
        # Calculate additional insights
        stats['pass_rate'] = (stats['class_distribution'].get('Pass', 0) / stats['total_records']) * 100
        stats['data_quality'] = 'Excellent' if stats['missing_values'] == 0 else 'Good'
        
        return {
            'success': True,
            'statistics': stats
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test ML utilities
    print("🧪 Testing ML Utilities")
    print("="*40)
    
    # Test ML manager
    ml_manager = get_ml_manager()
    print(f"Model available: {ml_manager.is_model_available()}")
    
    # Test model status
    status = ml_manager.get_model_status()
    print(f"Model status: {status}")
    
    # Test dataset statistics
    dataset_stats = analyze_dataset_statistics()
    print(f"Dataset statistics: {dataset_stats}")
    
    print("✅ ML utilities test completed")