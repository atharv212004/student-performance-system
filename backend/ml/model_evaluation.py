import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import json
import os
from datetime import datetime

class ModelEvaluator:
    """
    Comprehensive model evaluation and visualization
    """
    
    def __init__(self):
        self.evaluation_results = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name, class_names=None):
        """
        Comprehensive evaluation of a single model
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            model_name: Name of the model
            class_names: List of class names
            
        Returns:
            dict: Evaluation metrics
        """
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Basic metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Per-class metrics
        precision_per_class = precision_score(y_test, y_pred, average=None)
        recall_per_class = recall_score(y_test, y_pred, average=None)
        f1_per_class = f1_score(y_test, y_pred, average=None)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # ROC AUC (for binary classification)
        roc_auc = None
        if y_pred_proba is not None and len(np.unique(y_test)) == 2:
            roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        
        # Classification report
        class_report = classification_report(y_test, y_pred, output_dict=True)
        
        results = {
            'model_name': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'precision_per_class': precision_per_class.tolist(),
            'recall_per_class': recall_per_class.tolist(),
            'f1_per_class': f1_per_class.tolist(),
            'confusion_matrix': cm.tolist(),
            'roc_auc': roc_auc,
            'classification_report': class_report,
            'predictions': y_pred.tolist(),
            'probabilities': y_pred_proba.tolist() if y_pred_proba is not None else None
        }
        
        self.evaluation_results[model_name] = results
        return results
    
    def compare_models(self, models_results):
        """
        Compare multiple models and generate comparison metrics
        
        Args:
            models_results: Dictionary of model evaluation results
            
        Returns:
            dict: Comparison summary
        """
        comparison = {
            'model_names': list(models_results.keys()),
            'metrics_comparison': {}
        }
        
        # Extract metrics for comparison
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        for metric in metrics:
            comparison['metrics_comparison'][metric] = {}
            values = []
            
            for model_name, results in models_results.items():
                value = results.get(metric)
                comparison['metrics_comparison'][metric][model_name] = value
                if value is not None:
                    values.append(value)
            
            # Add summary statistics
            if values:
                comparison['metrics_comparison'][metric]['best'] = max(values)
                comparison['metrics_comparison'][metric]['worst'] = min(values)
                comparison['metrics_comparison'][metric]['mean'] = np.mean(values)
                comparison['metrics_comparison'][metric]['std'] = np.std(values)
        
        # Find best model for each metric
        best_models = {}
        for metric in metrics:
            best_score = -1
            best_model = None
            
            for model_name, results in models_results.items():
                score = results.get(metric)
                if score is not None and score > best_score:
                    best_score = score
                    best_model = model_name
            
            if best_model:
                best_models[metric] = {'model': best_model, 'score': best_score}
        
        comparison['best_models'] = best_models
        
        return comparison
    
    def generate_confusion_matrix_analysis(self, cm, class_names=None):
        """
        Generate detailed confusion matrix analysis
        
        Args:
            cm: Confusion matrix
            class_names: List of class names
            
        Returns:
            dict: Confusion matrix analysis
        """
        if class_names is None:
            class_names = [f'Class_{i}' for i in range(len(cm))]
        
        # Calculate per-class metrics from confusion matrix
        analysis = {
            'total_samples': np.sum(cm),
            'per_class_analysis': {}
        }
        
        for i, class_name in enumerate(class_names):
            tp = cm[i, i]  # True positives
            fp = np.sum(cm[:, i]) - tp  # False positives
            fn = np.sum(cm[i, :]) - tp  # False negatives
            tn = np.sum(cm) - tp - fp - fn  # True negatives
            
            # Calculate metrics
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            analysis['per_class_analysis'][class_name] = {
                'true_positives': int(tp),
                'false_positives': int(fp),
                'false_negatives': int(fn),
                'true_negatives': int(tn),
                'precision': precision,
                'recall': recall,
                'specificity': specificity,
                'f1_score': f1,
                'support': int(np.sum(cm[i, :]))
            }
        
        return analysis
    
    def calculate_feature_importance_analysis(self, model, feature_names):
        """
        Extract and analyze feature importance (for tree-based models)
        
        Args:
            model: Trained model
            feature_names: List of feature names
            
        Returns:
            dict: Feature importance analysis
        """
        importance_analysis = {
            'has_feature_importance': False,
            'feature_importance': None,
            'top_features': None
        }
        
        # Check if model has feature importance
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Create feature importance dataframe
            feature_importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            importance_analysis.update({
                'has_feature_importance': True,
                'feature_importance': feature_importance_df.to_dict('records'),
                'top_features': feature_importance_df.head(10).to_dict('records'),
                'total_features': len(feature_names)
            })
        
        elif hasattr(model, 'coef_'):
            # For linear models, use coefficient magnitudes
            coef = np.abs(model.coef_[0]) if len(model.coef_.shape) > 1 else np.abs(model.coef_)
            
            feature_importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': coef
            }).sort_values('importance', ascending=False)
            
            importance_analysis.update({
                'has_feature_importance': True,
                'feature_importance': feature_importance_df.to_dict('records'),
                'top_features': feature_importance_df.head(10).to_dict('records'),
                'total_features': len(feature_names)
            })
        
        return importance_analysis
    
    def generate_performance_summary(self, model_results):
        """
        Generate a comprehensive performance summary
        
        Args:
            model_results: Dictionary of model evaluation results
            
        Returns:
            dict: Performance summary
        """
        summary = {
            'evaluation_date': datetime.now().isoformat(),
            'total_models_evaluated': len(model_results),
            'models_summary': {},
            'overall_insights': {}
        }
        
        # Summarize each model
        for model_name, results in model_results.items():
            cm = np.array(results['confusion_matrix'])
            cm_analysis = self.generate_confusion_matrix_analysis(cm, ['Fail', 'Pass'])
            
            summary['models_summary'][model_name] = {
                'accuracy': results['accuracy'],
                'precision': results['precision'],
                'recall': results['recall'],
                'f1_score': results['f1_score'],
                'roc_auc': results['roc_auc'],
                'confusion_matrix_analysis': cm_analysis,
                'strengths': self._identify_model_strengths(results),
                'weaknesses': self._identify_model_weaknesses(results)
            }
        
        # Overall insights
        if model_results:
            best_accuracy = max(r['accuracy'] for r in model_results.values())
            best_f1 = max(r['f1_score'] for r in model_results.values())
            
            summary['overall_insights'] = {
                'best_accuracy_achieved': best_accuracy,
                'best_f1_score_achieved': best_f1,
                'performance_tier': self._classify_performance_tier(best_f1),
                'recommendations': self._generate_recommendations(model_results)
            }
        
        return summary
    
    def _identify_model_strengths(self, results):
        """Identify model strengths based on metrics"""
        strengths = []
        
        if results['accuracy'] > 0.85:
            strengths.append("High overall accuracy")
        
        if results['precision'] > 0.85:
            strengths.append("High precision (low false positives)")
        
        if results['recall'] > 0.85:
            strengths.append("High recall (low false negatives)")
        
        if results['f1_score'] > 0.85:
            strengths.append("Excellent balanced performance")
        
        if results['roc_auc'] and results['roc_auc'] > 0.9:
            strengths.append("Excellent class separation ability")
        
        return strengths if strengths else ["Baseline performance achieved"]
    
    def _identify_model_weaknesses(self, results):
        """Identify model weaknesses based on metrics"""
        weaknesses = []
        
        if results['accuracy'] < 0.7:
            weaknesses.append("Low overall accuracy")
        
        if results['precision'] < 0.7:
            weaknesses.append("High false positive rate")
        
        if results['recall'] < 0.7:
            weaknesses.append("High false negative rate")
        
        if results['f1_score'] < 0.7:
            weaknesses.append("Poor balanced performance")
        
        if results['roc_auc'] and results['roc_auc'] < 0.7:
            weaknesses.append("Poor class separation")
        
        # Check for class imbalance issues
        cm = np.array(results['confusion_matrix'])
        if len(cm) == 2:
            class_0_recall = cm[0,0] / (cm[0,0] + cm[0,1]) if (cm[0,0] + cm[0,1]) > 0 else 0
            class_1_recall = cm[1,1] / (cm[1,0] + cm[1,1]) if (cm[1,0] + cm[1,1]) > 0 else 0
            
            if abs(class_0_recall - class_1_recall) > 0.2:
                weaknesses.append("Imbalanced class performance")
        
        return weaknesses if weaknesses else ["No significant weaknesses identified"]
    
    def _classify_performance_tier(self, f1_score):
        """Classify model performance into tiers"""
        if f1_score >= 0.9:
            return "Excellent"
        elif f1_score >= 0.8:
            return "Good"
        elif f1_score >= 0.7:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _generate_recommendations(self, model_results):
        """Generate recommendations based on evaluation results"""
        recommendations = []
        
        # Find best performing model
        best_model = max(model_results.items(), key=lambda x: x[1]['f1_score'])
        best_name, best_results = best_model
        
        recommendations.append(f"Use {best_name} as primary model (F1: {best_results['f1_score']:.3f})")
        
        # Performance-based recommendations
        if best_results['f1_score'] < 0.8:
            recommendations.extend([
                "Consider feature engineering to improve performance",
                "Collect more training data if possible",
                "Try hyperparameter tuning for better results"
            ])
        
        # Class imbalance recommendations
        cm = np.array(best_results['confusion_matrix'])
        if len(cm) == 2:
            class_support = [np.sum(cm[i, :]) for i in range(2)]
            imbalance_ratio = max(class_support) / min(class_support)
            
            if imbalance_ratio > 2:
                recommendations.append("Address class imbalance with sampling techniques")
        
        return recommendations
    
    def save_evaluation_report(self, filepath='ml/saved/evaluation_report.json'):
        """Save comprehensive evaluation report"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Generate comprehensive report
        comparison = self.compare_models(self.evaluation_results)
        summary = self.generate_performance_summary(self.evaluation_results)
        
        report = {
            'evaluation_metadata': {
                'report_date': datetime.now().isoformat(),
                'total_models': len(self.evaluation_results)
            },
            'individual_results': self.evaluation_results,
            'model_comparison': comparison,
            'performance_summary': summary
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Evaluation report saved to {filepath}")
        return report

# Utility functions for easy access
def evaluate_trained_models(models_dict, X_test, y_test, feature_names=None):
    """
    Evaluate multiple trained models
    
    Args:
        models_dict: Dictionary of {model_name: model}
        X_test: Test features
        y_test: Test labels
        feature_names: List of feature names
        
    Returns:
        dict: Comprehensive evaluation report
    """
    evaluator = ModelEvaluator()
    
    # Evaluate each model
    for model_name, model in models_dict.items():
        print(f"📊 Evaluating {model_name}...")
        evaluator.evaluate_model(model, X_test, y_test, model_name)
    
    # Generate and save report
    report = evaluator.save_evaluation_report()
    
    return report

if __name__ == "__main__":
    print("🧪 Model Evaluation Module")
    print("This module provides comprehensive model evaluation capabilities.")
    print("Use it after training models to get detailed performance analysis.")