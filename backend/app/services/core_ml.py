"""
Core ML Service - Minimal machine learning
Replaces: expert_data_scientist.py + automl_pipeline.py + model_explainer.py
"""
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CoreML:
    def __init__(self):
        self.model = None
        self.task_type = None
    
    def auto_ml(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """Simple AutoML - no complexity"""
        try:
            # Prepare data
            X = df.drop(columns=[target_col])
            y = df[target_col]
            
            # Handle categorical variables simply
            for col in X.select_dtypes(include=['object']).columns:
                X[col] = LabelEncoder().fit_transform(X[col].astype(str))
            
            # Detect task type
            if y.dtype == 'object' or y.nunique() < 20:
                self.task_type = 'classification'
                if y.dtype == 'object':
                    y = LabelEncoder().fit_transform(y)
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                self.task_type = 'regression'
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            if self.task_type == 'classification':
                score = accuracy_score(y_test, y_pred)
                metric = 'accuracy'
            else:
                score = r2_score(y_test, y_pred)
                metric = 'r2_score'
            
            # Feature importance
            importance = dict(zip(X.columns, self.model.feature_importances_))
            top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'task_type': self.task_type,
                'score': score,
                'metric': metric,
                'top_features': top_features,
                'model_trained': True
            }
            
        except Exception as e:
            logger.error(f"AutoML error: {e}")
            return {'error': str(e)}

# Global instance
ml = CoreML()
