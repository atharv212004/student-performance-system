"""
Ensemble ML Models for Student Performance Prediction
- Combines multiple models (Random Forest, Gradient Boosting, SVM, Neural Network)
- Provides better accuracy through voting ensemble
- Includes model evaluation and comparison
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

class EnsembleModelManager:
    """
    Ensemble model manager combining multiple ML models for better accuracy
    """
    
    def __init__(self, model_dir='ml/saved'):
        self.model_dir = model_dir
        self.models = {}
        self.scaler = StandardScaler()
        self.ensemble = None
        self.model_metadata = {
            'training_date': None,
            'ensemble_accuracy': 0,
            'individual_models': {},
            'best_model': None
        }
        os.makedirs(model_dir, exist_ok=True)
    
    def train_ensemble_models(self, X_train, y_train, X_test, y_test):
        """
        Train multiple models and create ensemble
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_test: Test features
            y_test: Test labels
            
        Returns:
            dict: Training results with metrics
        """
        results = {'models': {}, 'ensemble': {}}
        
        try:
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train individual models
            print("Training individual models...")
            
            # Model 1: Random Forest
            print("  - Training Random Forest...")
            rf_model = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            rf_model.fit(X_train_scaled, y_train)
            rf_pred = rf_model.predict(X_test_scaled)
            rf_metrics = self._calculate_metrics(y_test, rf_pred)
            self.models['random_forest'] = rf_model
            results['models']['random_forest'] = rf_metrics
            print(f"    Accuracy: {rf_metrics['accuracy']:.4f}")
            
            # Model 2: Gradient Boosting
            print("  - Training Gradient Boosting...")
            gb_model = GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=7,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            gb_model.fit(X_train_scaled, y_train)
            gb_pred = gb_model.predict(X_test_scaled)
            gb_metrics = self._calculate_metrics(y_test, gb_pred)
            self.models['gradient_boosting'] = gb_model
            results['models']['gradient_boosting'] = gb_metrics
            print(f"    Accuracy: {gb_metrics['accuracy']:.4f}")
            
            # Model 3: Support Vector Machine
            print("  - Training Support Vector Machine...")
            svm_model = SVC(
                kernel='rbf',
                C=100,
                gamma='scale',
                probability=True,
                random_state=42
            )
            svm_model.fit(X_train_scaled, y_train)
            svm_pred = svm_model.predict(X_test_scaled)
            svm_metrics = self._calculate_metrics(y_test, svm_pred)
            self.models['svm'] = svm_model
            results['models']['svm'] = svm_metrics
            print(f"    Accuracy: {svm_metrics['accuracy']:.4f}")
            
            # Create Voting Ensemble
            print("Creating voting ensemble...")
            self.ensemble = VotingClassifier(
                estimators=[
                    ('rf', rf_model),
                    ('gb', gb_model),
                    ('svm', svm_model)
                ],
                voting='soft'
            )
            self.ensemble.fit(X_train_scaled, y_train)
            
            ensemble_pred = self.ensemble.predict(X_test_scaled)
            ensemble_metrics = self._calculate_metrics(y_test, ensemble_pred)
            results['ensemble'] = ensemble_metrics
            print(f"  Ensemble Accuracy: {ensemble_metrics['accuracy']:.4f}")
            
            # Save models and metadata
            self._save_models()
            
            # Update metadata
            self.model_metadata = {
                'training_date': datetime.now().isoformat(),
                'ensemble_accuracy': ensemble_metrics['accuracy'],
                'individual_models': results['models'],
                'best_model': 'ensemble',
                'scaler_params': {
                    'mean': self.scaler.mean_.tolist(),
                    'scale': self.scaler.scale_.tolist()
                }
            }
            
            # Save metadata
            with open(os.path.join(self.model_dir, 'ensemble_metadata.json'), 'w') as f:
                json.dump(self.model_metadata, f, indent=2)
            
            return results
            
        except Exception as e:
            print(f"Error training ensemble: {e}")
            raise
    
    def _calculate_metrics(self, y_true, y_pred):
        """Calculate performance metrics"""
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0)
        }
    
    def _save_models(self):
        """Save trained models to disk"""
        for model_name, model in self.models.items():
            path = os.path.join(self.model_dir, f'{model_name}.pkl')
            with open(path, 'wb') as f:
                pickle.dump(model, f)
            print(f"Saved {model_name} model")
        
        # Save ensemble
        if self.ensemble:
            ensemble_path = os.path.join(self.model_dir, 'ensemble_model.pkl')
            with open(ensemble_path, 'wb') as f:
                pickle.dump(self.ensemble, f)
            print("Saved ensemble model")
        
        # Save scaler
        scaler_path = os.path.join(self.model_dir, 'ensemble_scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print("Saved scaler")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            # Load individual models
            for model_name in ['random_forest', 'gradient_boosting', 'svm']:
                path = os.path.join(self.model_dir, f'{model_name}.pkl')
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
            
            # Load ensemble
            ensemble_path = os.path.join(self.model_dir, 'ensemble_model.pkl')
            if os.path.exists(ensemble_path):
                with open(ensemble_path, 'rb') as f:
                    self.ensemble = pickle.load(f)
            
            # Load scaler
            scaler_path = os.path.join(self.model_dir, 'ensemble_scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            # Load metadata
            metadata_path = os.path.join(self.model_dir, 'ensemble_metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.model_metadata = json.load(f)
            
            return len(self.models) > 0 and self.ensemble is not None
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict(self, X):
        """
        Predict using ensemble
        
        Args:
            X: Feature array
            
        Returns:
            dict: Prediction with confidence
        """
        if self.ensemble is None:
            raise ValueError("Ensemble model not loaded")
        
        try:
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Get predictions from ensemble
            prediction = self.ensemble.predict(X_scaled)[0]
            probabilities = self.ensemble.predict_proba(X_scaled)[0]
            confidence = max(probabilities)
            
            # Get individual model predictions
            individual_predictions = {}
            for model_name, model in self.models.items():
                individual_predictions[model_name] = int(model.predict(X_scaled)[0])
            
            return {
                'prediction': int(prediction),
                'confidence': float(confidence),
                'probabilities': {
                    'pass': float(probabilities[1]) if len(probabilities) > 1 else 0,
                    'fail': float(probabilities[0])
                },
                'individual_predictions': individual_predictions
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            raise
    
    def get_model_info(self):
        """Get model information and performance"""
        return {
            'training_date': self.model_metadata.get('training_date'),
            'ensemble_accuracy': self.model_metadata.get('ensemble_accuracy'),
            'individual_models': self.model_metadata.get('individual_models'),
            'best_model': self.model_metadata.get('best_model'),
            'models_available': list(self.models.keys()),
            'ensemble_loaded': self.ensemble is not None
        }
