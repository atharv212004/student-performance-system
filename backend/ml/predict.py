import pickle
import numpy as np
import os
import json
from datetime import datetime
from ml.data_preprocessing import DataPreprocessor

class StudentPerformancePredictor:
    """
    Prediction engine for student performance
    """
    
    def __init__(self):
        self.model = None
        self.preprocessor = DataPreprocessor()
        self.model_metadata = None
        self.is_loaded = False
        
    def load_model(self, model_dir='ml/saved'):
        """Load the trained model and preprocessor"""
        try:
            # Load preprocessor
            preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
            if not self.preprocessor.load_preprocessor(preprocessor_path):
                return False
            
            # Load best model
            model_path = os.path.join(model_dir, 'best_model.pkl')
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load metadata
            metadata_path = os.path.join(model_dir, 'model_metadata.json')
            with open(metadata_path, 'r') as f:
                self.model_metadata = json.load(f)
            
            self.is_loaded = True
            print(f"✅ Model loaded successfully: {self.model_metadata['best_model_name']}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def predict_single_student(self, student_data):
        """
        Predict performance for a single student
        
        Args:
            student_data (dict): Dictionary containing student features
            
        Returns:
            dict: Prediction results with probability, risk level, and feedback
        """
        if not self.is_loaded:
            if not self.load_model():
                raise Exception("Model not available. Please train the model first.")
        
        try:
            # Preprocess the input data
            X = self.preprocessor.preprocess_single_record(student_data)
            
            # Make prediction
            prediction = self.model.predict([X])[0]
            prediction_proba = self.model.predict_proba([X])[0]
            
            # Get class labels
            target_encoder = self.preprocessor.label_encoders['target_encoder']
            prediction_label = target_encoder.inverse_transform([prediction])[0]
            
            # Calculate probabilities for each class
            class_probabilities = {
                target_encoder.classes_[i]: prob 
                for i, prob in enumerate(prediction_proba)
            }
            
            # Determine risk level and feedback
            pass_probability = class_probabilities.get('Pass', 0)
            fail_probability = class_probabilities.get('Fail', 0)
            
            risk_level, feedback = self._generate_risk_assessment(
                student_data, pass_probability, prediction_label
            )
            
            return {
                'prediction': prediction_label,
                'probability': float(max(prediction_proba)),
                'class_probabilities': {k: float(v) for k, v in class_probabilities.items()},
                'risk_level': risk_level,
                'feedback': feedback,
                'model_used': self.model_metadata['best_model_name'],
                'prediction_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def _generate_risk_assessment(self, student_data, pass_probability, prediction):
        """Generate risk level and personalized feedback"""
        
        # Determine risk level
        if pass_probability >= 0.8:
            risk_level = "Low"
        elif pass_probability >= 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Generate personalized feedback
        feedback_parts = []
        
        # Overall prediction feedback
        if prediction == "Pass":
            if pass_probability >= 0.9:
                feedback_parts.append("🎉 Excellent! You're on track for outstanding performance.")
            elif pass_probability >= 0.8:
                feedback_parts.append("✅ Great job! You're likely to pass with good performance.")
            else:
                feedback_parts.append("👍 You're on the right track, but there's room for improvement.")
        else:
            feedback_parts.append("⚠️ Warning: Current performance indicates risk of failure.")
        
        # Specific recommendations based on student data
        recommendations = []
        
        # Attendance recommendations
        attendance = student_data.get('attendance_percentage', 0)
        if attendance < 75:
            recommendations.append(f"📚 Improve attendance (currently {attendance}%). Aim for 85%+ for better outcomes.")
        elif attendance < 85:
            recommendations.append(f"📈 Good attendance ({attendance}%), try to maintain 90%+ for optimal results.")
        
        # Study hours recommendations
        study_hours = student_data.get('study_hours', 0)
        if study_hours < 20:
            recommendations.append(f"⏰ Increase study time (currently {study_hours}h/week). Aim for 25-30 hours weekly.")
        elif study_hours > 40:
            recommendations.append(f"⚖️ Consider balancing study time ({study_hours}h/week) to avoid burnout.")
        
        # Performance recommendations
        internal_marks = student_data.get('internal_marks', 0)
        assignment_score = student_data.get('assignment_score', 0)
        
        if internal_marks < 60:
            recommendations.append("📖 Focus on understanding core concepts. Consider additional tutoring.")
        
        if assignment_score < 70:
            recommendations.append("📝 Improve assignment quality. Seek feedback from instructors.")
        
        # Participation recommendations
        if student_data.get('class_participation') == 'No':
            recommendations.append("🗣️ Increase class participation to enhance understanding and engagement.")
        
        if student_data.get('extracurricular_activity') == 'No':
            recommendations.append("🎯 Consider joining extracurricular activities for holistic development.")
        
        # Combine feedback
        if recommendations:
            feedback_parts.append("\n📋 Recommendations:")
            feedback_parts.extend([f"• {rec}" for rec in recommendations[:4]])  # Limit to top 4
        
        # Add motivational message
        if risk_level == "High":
            feedback_parts.append("\n💪 Don't give up! With focused effort and the right strategies, you can improve significantly.")
        elif risk_level == "Medium":
            feedback_parts.append("\n🚀 You're close to excellent performance! Small improvements can make a big difference.")
        else:
            feedback_parts.append("\n🌟 Keep up the excellent work! You're setting a great example.")
        
        return risk_level, "\n".join(feedback_parts)
    
    def batch_predict(self, students_data):
        """Predict performance for multiple students"""
        if not self.is_loaded:
            if not self.load_model():
                raise Exception("Model not available. Please train the model first.")
        
        results = []
        for i, student_data in enumerate(students_data):
            try:
                result = self.predict_single_student(student_data)
                result['student_index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'student_index': i,
                    'error': str(e),
                    'prediction': None
                })
        
        return results
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.is_loaded:
            return None
        
        return {
            'model_name': self.model_metadata['best_model_name'],
            'training_date': self.model_metadata['training_date'],
            'model_scores': self.model_metadata['model_scores'][self.model_metadata['best_model_name']],
            'feature_count': len(self.preprocessor.feature_columns)
        }

# Global predictor instance
_predictor = None

def get_predictor():
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = StudentPerformancePredictor()
    return _predictor

def predict_student_performance(student_data):
    """
    Main function to predict student performance
    
    Args:
        student_data (dict): Student features dictionary
        
    Returns:
        dict: Prediction results
    """
    predictor = get_predictor()
    return predictor.predict_single_student(student_data)

def batch_predict_performance(students_data):
    """
    Predict performance for multiple students
    
    Args:
        students_data (list): List of student feature dictionaries
        
    Returns:
        list: List of prediction results
    """
    predictor = get_predictor()
    return predictor.batch_predict(students_data)

def get_model_information():
    """Get information about the current model"""
    predictor = get_predictor()
    return predictor.get_model_info()

# Example usage and testing
if __name__ == "__main__":
    # Test the prediction system
    print("🧪 Testing Student Performance Predictor")
    print("="*50)
    
    # Sample student data
    sample_student = {
        'gender': 'Male',
        'age': 20,
        'study_hours': 25,
        'attendance_percentage': 85,
        'internal_marks': 75,
        'assignment_score': 80,
        'previous_sem_marks': 70,
        'class_participation': 'Yes',
        'extracurricular_activity': 'Yes',
        'final_exam_marks': 78
    }
    
    try:
        # Make prediction
        result = predict_student_performance(sample_student)
        
        print("📊 Prediction Results:")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['probability']:.2%}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Model Used: {result['model_used']}")
        print(f"\n💬 Feedback:")
        print(result['feedback'])
        
        # Get model info
        model_info = get_model_information()
        if model_info:
            print(f"\n🤖 Model Information:")
            print(f"   Name: {model_info['model_name']}")
            print(f"   Training Date: {model_info['training_date']}")
            print(f"   F1 Score: {model_info['model_scores']['f1_score']:.4f}")
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        print("💡 Make sure to train the model first by running: python ml/train_model.py")