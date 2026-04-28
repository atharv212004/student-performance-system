import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
import os

class DataPreprocessor:
    """
    Data preprocessing pipeline for student performance prediction
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = 'result'
        
    def load_data(self, file_path='data/clean_student_dataset.xlsx'):
        """Load dataset from Excel file"""
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            print(f"✅ Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            raise
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        print("🔧 Handling missing values...")
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            print(f"Found missing values:\n{missing_counts[missing_counts > 0]}")
            
            # Fill numeric columns with median
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
            
            # Fill categorical columns with mode
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].mode()[0], inplace=True)
        
        print("✅ Missing values handled")
        return df
    
    def create_engineered_features(self, df):
        """Create advanced engineered features"""
        print("🔧 Creating engineered features...")
        
        # Performance Index: Weighted combination of marks
        df['performance_index'] = (
            0.3 * df['internal_marks'] + 
            0.2 * df['assignment_score'] + 
            0.4 * df['final_exam_marks'] + 
            0.1 * df['previous_sem_marks']
        )
        
        # Study Efficiency: Marks per study hour
        df['study_efficiency'] = df['final_exam_marks'] / (df['study_hours'] + 1)  # +1 to avoid division by zero
        
        # Attendance Band: Categorize attendance
        df['attendance_band'] = pd.cut(
            df['attendance_percentage'], 
            bins=[0, 60, 80, 100], 
            labels=['Low', 'Medium', 'High']
        )
        # Convert to string to avoid NaN issues
        df['attendance_band'] = df['attendance_band'].astype(str)
        
        # Pressure Score: Combination of factors indicating academic pressure
        df['pressure_score'] = (
            (100 - df['attendance_percentage']) * 0.3 +
            (df['study_hours'] / 7) * 20 * 0.4 +  # Normalize study hours to daily and scale
            (100 - df['internal_marks']) * 0.3
        )
        
        # Age Group: Categorize age
        df['age_group'] = pd.cut(
            df['age'], 
            bins=[0, 20, 22, 25, 100], 
            labels=['Teen', 'Young', 'Adult', 'Mature']
        )
        # Convert to string to avoid NaN issues
        df['age_group'] = df['age_group'].astype(str)
        
        # Total Marks: Sum of all assessment marks
        df['total_marks'] = df['internal_marks'] + df['assignment_score'] + df['final_exam_marks']
        
        # Participation Score: Numeric representation
        df['participation_score'] = df['class_participation'].map({'Yes': 1, 'No': 0})
        df['activity_score'] = df['extracurricular_activity'].map({'Yes': 1, 'No': 0})
        
        # Fill any remaining NaN values
        df = df.fillna(0)
        
        print("✅ Engineered features created")
        return df
    
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical features"""
        print("🔧 Encoding categorical features...")
        
        categorical_columns = ['gender', 'class_participation', 'extracurricular_activity', 'attendance_band', 'age_group']
        
        for col in categorical_columns:
            if col in df.columns:
                if fit:
                    # Fit and transform during training
                    if col not in self.label_encoders:
                        self.label_encoders[col] = LabelEncoder()
                    df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    # Transform only during prediction
                    if col in self.label_encoders:
                        # Handle unseen categories
                        unique_values = set(self.label_encoders[col].classes_)
                        df[col] = df[col].astype(str).apply(
                            lambda x: x if x in unique_values else self.label_encoders[col].classes_[0]
                        )
                        df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
                    else:
                        # If encoder doesn't exist, create dummy encoding
                        df[f'{col}_encoded'] = 0
        
        print("✅ Categorical features encoded")
        return df
    
    def scale_features(self, df, fit=True):
        """Scale numerical features"""
        print("🔧 Scaling numerical features...")
        
        # Select features for scaling
        scale_columns = [
            'age', 'study_hours', 'attendance_percentage', 'internal_marks',
            'assignment_score', 'previous_sem_marks', 'final_exam_marks',
            'performance_index', 'study_efficiency', 'pressure_score', 'total_marks'
        ]
        
        # Only scale columns that exist in the dataframe
        scale_columns = [col for col in scale_columns if col in df.columns]
        
        if fit:
            # Fit and transform during training
            df[scale_columns] = self.scaler.fit_transform(df[scale_columns])
        else:
            # Transform only during prediction
            df[scale_columns] = self.scaler.transform(df[scale_columns])
        
        print("✅ Features scaled")
        return df
    
    def prepare_features(self, df, fit=True):
        """Prepare final feature set for ML models"""
        print("🔧 Preparing final feature set...")
        
        # Define feature columns
        self.feature_columns = [
            # Original features
            'age', 'study_hours', 'attendance_percentage', 'internal_marks',
            'assignment_score', 'previous_sem_marks', 'final_exam_marks',
            
            # Engineered features
            'performance_index', 'study_efficiency', 'pressure_score', 'total_marks',
            'participation_score', 'activity_score',
            
            # Encoded categorical features
            'gender_encoded', 'class_participation_encoded', 'extracurricular_activity_encoded',
            'attendance_band_encoded', 'age_group_encoded'
        ]
        
        # Select only available columns
        available_columns = [col for col in self.feature_columns if col in df.columns]
        
        if len(available_columns) != len(self.feature_columns):
            missing_cols = set(self.feature_columns) - set(available_columns)
            print(f"⚠️ Missing columns: {missing_cols}")
        
        X = df[available_columns].copy()
        
        # Final check for NaN values and fill them
        if X.isnull().sum().sum() > 0:
            print("⚠️ Found NaN values in features, filling with 0")
            X = X.fillna(0)
        
        # Handle target variable if present
        y = None
        if self.target_column in df.columns:
            # Encode target variable
            if fit and 'target_encoder' not in self.label_encoders:
                self.label_encoders['target_encoder'] = LabelEncoder()
                y = self.label_encoders['target_encoder'].fit_transform(df[self.target_column])
            elif 'target_encoder' in self.label_encoders:
                y = self.label_encoders['target_encoder'].transform(df[self.target_column])
        
        print(f"✅ Feature set prepared: {X.shape[1]} features")
        return X, y
    
    def preprocess_pipeline(self, df, fit=True):
        """Complete preprocessing pipeline"""
        print("🚀 Starting preprocessing pipeline...")
        
        # Step 1: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 2: Create engineered features
        df = self.create_engineered_features(df)
        
        # Step 3: Encode categorical features
        df = self.encode_categorical_features(df, fit=fit)
        
        # Step 4: Scale features
        df = self.scale_features(df, fit=fit)
        
        # Step 5: Prepare final feature set
        X, y = self.prepare_features(df, fit=fit)
        
        print("✅ Preprocessing pipeline completed")
        return X, y, df
    
    def save_preprocessor(self, filepath='ml/saved/preprocessor.pkl'):
        """Save the preprocessor for later use"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(preprocessor_data, f)
        
        print(f"✅ Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath='ml/saved/preprocessor.pkl'):
        """Load a saved preprocessor"""
        try:
            with open(filepath, 'rb') as f:
                preprocessor_data = pickle.load(f)
            
            self.scaler = preprocessor_data['scaler']
            self.label_encoders = preprocessor_data['label_encoders']
            self.feature_columns = preprocessor_data['feature_columns']
            
            print(f"✅ Preprocessor loaded from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error loading preprocessor: {e}")
            return False
    
    def preprocess_single_record(self, record_dict):
        """Preprocess a single student record for prediction"""
        # Convert to DataFrame
        df = pd.DataFrame([record_dict])
        
        # Apply preprocessing (without fitting)
        X, _, _ = self.preprocess_pipeline(df, fit=False)
        
        return X.iloc[0].values  # Return as numpy array

def create_train_test_split(X, y, test_size=0.2, random_state=42):
    """Create stratified train-test split"""
    print(f"🔧 Creating train-test split (test_size={test_size})...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=y
    )
    
    print(f"✅ Train set: {X_train.shape[0]} samples")
    print(f"✅ Test set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test the preprocessing pipeline
    preprocessor = DataPreprocessor()
    
    # Load and preprocess data
    df = preprocessor.load_data()
    X, y, processed_df = preprocessor.preprocess_pipeline(df)
    
    # Create train-test split
    X_train, X_test, y_train, y_test = create_train_test_split(X, y)
    
    # Save preprocessor
    preprocessor.save_preprocessor()
    
    print("\n📊 Preprocessing Summary:")
    print(f"Original dataset shape: {df.shape}")
    print(f"Processed features shape: {X.shape}")
    print(f"Feature columns: {len(preprocessor.feature_columns)}")
    print(f"Target classes: {preprocessor.label_encoders['target_encoder'].classes_}")