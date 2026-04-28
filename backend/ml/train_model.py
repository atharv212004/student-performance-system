import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import xgboost as xgb
import pickle
import os
import json
from datetime import datetime
from ml.data_preprocessing import DataPreprocessor, create_train_test_split

class ModelTrainer:
    """
    Train and evaluate multiple ML models for student performance prediction
    """
    
    def __init__(self):
        self.models = {}
        self.model_scores = {}
        self.best_model = None
        self.best_model_name = None
        self.preprocessor = DataPreprocessor()
        
    def initialize_models(self):
        """Initialize ML models with optimized parameters"""
        print("🤖 Initializing ML models...")
        
        self.models = {
            'logistic_regression': LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced'
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=1
            )
        }
        
        print(f"✅ {len(self.models)} models initialized")
    
    def train_single_model(self, model_name, model, X_train, y_train, X_test, y_test):
        """Train and evaluate a single model"""
        print(f"\n🔧 Training {model_name}...")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        precision = precision_score(y_test, y_pred_test, average='weighted')
        recall = recall_score(y_test, y_pred_test, average='weighted')
        f1 = f1_score(y_test, y_pred_test, average='weighted')
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42), scoring='f1_weighted')
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred_test)
        
        # Store results
        results = {
            'model': model,
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred_test.tolist(),
            'probabilities': y_pred_proba.tolist() if y_pred_proba is not None else None
        }
        
        print(f"✅ {model_name} trained successfully")
        print(f"   Test Accuracy: {test_accuracy:.4f}")
        print(f"   F1 Score: {f1:.4f}")
        print(f"   CV Score: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        
        return results
    
    def train_all_models(self, X_train, y_train, X_test, y_test):
        """Train all models and compare performance"""
        print("🚀 Training all models...")
        
        self.initialize_models()
        
        for model_name, model in self.models.items():
            self.model_scores[model_name] = self.train_single_model(
                model_name, model, X_train, y_train, X_test, y_test
            )
        
        # Select best model based on F1 score
        best_f1 = 0
        for model_name, scores in self.model_scores.items():
            if scores['f1_score'] > best_f1:
                best_f1 = scores['f1_score']
                self.best_model_name = model_name
                self.best_model = scores['model']
        
        print(f"\n🏆 Best model: {self.best_model_name} (F1: {best_f1:.4f})")
    
    def print_detailed_results(self):
        """Print detailed evaluation results"""
        print("\n" + "="*80)
        print("📊 DETAILED MODEL EVALUATION RESULTS")
        print("="*80)
        
        for model_name, scores in self.model_scores.items():
            print(f"\n🤖 {model_name.upper().replace('_', ' ')}")
            print("-" * 50)
            print(f"Train Accuracy:     {scores['train_accuracy']:.4f}")
            print(f"Test Accuracy:      {scores['test_accuracy']:.4f}")
            print(f"Precision:          {scores['precision']:.4f}")
            print(f"Recall:             {scores['recall']:.4f}")
            print(f"F1 Score:           {scores['f1_score']:.4f}")
            print(f"CV Score:           {scores['cv_mean']:.4f} (±{scores['cv_std']:.4f})")
            
            # Confusion Matrix
            cm = np.array(scores['confusion_matrix'])
            print(f"\nConfusion Matrix:")
            print(f"                 Predicted")
            print(f"                Fail  Pass")
            print(f"Actual Fail    [{cm[0,0]:4d}  {cm[0,1]:4d}]")
            print(f"       Pass    [{cm[1,0]:4d}  {cm[1,1]:4d}]")
        
        print(f"\n🏆 BEST MODEL: {self.best_model_name.upper().replace('_', ' ')}")
        print(f"   F1 Score: {self.model_scores[self.best_model_name]['f1_score']:.4f}")
    
    def save_models(self, save_dir='ml/saved'):
        """Save all trained models and results"""
        os.makedirs(save_dir, exist_ok=True)
        
        # Save best model
        best_model_path = os.path.join(save_dir, 'best_model.pkl')
        with open(best_model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        
        # Save all models
        models_path = os.path.join(save_dir, 'all_models.pkl')
        models_to_save = {name: scores['model'] for name, scores in self.model_scores.items()}
        with open(models_path, 'wb') as f:
            pickle.dump(models_to_save, f)
        
        # Save model metadata
        metadata = {
            'best_model_name': self.best_model_name,
            'training_date': datetime.now().isoformat(),
            'model_scores': {
                name: {
                    'train_accuracy': scores['train_accuracy'],
                    'test_accuracy': scores['test_accuracy'],
                    'precision': scores['precision'],
                    'recall': scores['recall'],
                    'f1_score': scores['f1_score'],
                    'cv_mean': scores['cv_mean'],
                    'cv_std': scores['cv_std'],
                    'confusion_matrix': scores['confusion_matrix']
                }
                for name, scores in self.model_scores.items()
            }
        }
        
        metadata_path = os.path.join(save_dir, 'model_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n💾 Models saved to {save_dir}/")
        print(f"   - Best model: best_model.pkl")
        print(f"   - All models: all_models.pkl")
        print(f"   - Metadata: model_metadata.json")
    
    def load_models(self, save_dir='ml/saved'):
        """Load saved models"""
        try:
            # Load metadata
            metadata_path = os.path.join(save_dir, 'model_metadata.json')
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.best_model_name = metadata['best_model_name']
            self.model_scores = metadata['model_scores']
            
            # Load best model
            best_model_path = os.path.join(save_dir, 'best_model.pkl')
            with open(best_model_path, 'rb') as f:
                self.best_model = pickle.load(f)
            
            print(f"✅ Models loaded successfully")
            print(f"   Best model: {self.best_model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False

def train_models():
    """Main function to train all models"""
    print("🚀 STUDENT PERFORMANCE PREDICTION - MODEL TRAINING")
    print("="*60)
    
    try:
        # Initialize trainer and preprocessor
        trainer = ModelTrainer()
        
        # Load and preprocess data
        print("📊 Loading and preprocessing data...")
        df = trainer.preprocessor.load_data()
        X, y, processed_df = trainer.preprocessor.preprocess_pipeline(df)
        
        # Create train-test split
        X_train, X_test, y_train, y_test = create_train_test_split(X, y)
        
        # Train all models
        trainer.train_all_models(X_train, y_train, X_test, y_test)
        
        # Print results
        trainer.print_detailed_results()
        
        # Save models and preprocessor
        trainer.save_models()
        trainer.preprocessor.save_preprocessor()
        
        # Return training summary for API
        return {
            'success': True,
            'best_model': trainer.best_model_name,
            'best_f1_score': trainer.model_scores[trainer.best_model_name]['f1_score'],
            'models_trained': list(trainer.model_scores.keys()),
            'training_date': datetime.now().isoformat(),
            'dataset_size': len(df),
            'feature_count': X.shape[1]
        }
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Run training
    result = train_models()
    
    if result['success']:
        print("\n🎉 MODEL TRAINING COMPLETED SUCCESSFULLY!")
        print(f"   Best Model: {result['best_model']}")
        print(f"   F1 Score: {result['best_f1_score']:.4f}")
        print(f"   Dataset Size: {result['dataset_size']} records")
        print(f"   Features: {result['feature_count']}")
    else:
        print(f"\n❌ Training failed: {result['error']}")