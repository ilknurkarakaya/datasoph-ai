"""
DataSoph AI - Advanced Machine Learning Service
Automated ML model training, evaluation, and prediction
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from pathlib import Path
import json
import pickle
import uuid
from datetime import datetime

# Core ML libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Classification models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

# Regression models
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

# Clustering
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

# Evaluation metrics
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    mean_squared_error, r2_score, mean_absolute_error,
    silhouette_score, adjusted_rand_score
)

# Advanced ML (if available)
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

logger = logging.getLogger(__name__)

class MLService:
    """Advanced machine learning service with automated model training"""
    
    def __init__(self):
        self.models_storage = {}  # In-memory model storage
        self.default_models = {
            'classification': {
                'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
                'svm': SVC(random_state=42, probability=True),
                'decision_tree': DecisionTreeClassifier(random_state=42),
                'naive_bayes': GaussianNB()
            },
            'regression': {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'linear_regression': LinearRegression(),
                'ridge': Ridge(random_state=42),
                'lasso': Lasso(random_state=42),
                'svr': SVR(),
                'decision_tree': DecisionTreeRegressor(random_state=42)
            },
            'clustering': {
                'kmeans': KMeans(n_clusters=3, random_state=42),
                'dbscan': DBSCAN(eps=0.5, min_samples=5)
            }
        }
        
        # Add advanced models if available
        if HAS_XGBOOST:
            self.default_models['classification']['xgboost'] = xgb.XGBClassifier(random_state=42)
            self.default_models['regression']['xgboost'] = xgb.XGBRegressor(random_state=42)
        
        if HAS_LIGHTGBM:
            self.default_models['classification']['lightgbm'] = lgb.LGBMClassifier(random_state=42, verbose=-1)
            self.default_models['regression']['lightgbm'] = lgb.LGBMRegressor(random_state=42, verbose=-1)
    
    def auto_analyze_and_recommend(self, file_path: str) -> Dict[str, Any]:
        """Automatically analyze data and recommend ML approaches"""
        try:
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            analysis = {
                "data_summary": self._get_data_summary(df),
                "ml_recommendations": [],
                "suggested_targets": [],
                "preprocessing_needed": [],
                "model_suggestions": {}
            }
            
            # Analyze data characteristics
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Suggest potential target variables
            analysis["suggested_targets"] = self._suggest_target_variables(df, numeric_cols, categorical_cols)
            
            # Preprocessing recommendations
            analysis["preprocessing_needed"] = self._analyze_preprocessing_needs(df)
            
            # ML task recommendations
            for target_info in analysis["suggested_targets"]:
                target_col = target_info["column"]
                task_type = target_info["task_type"]
                
                if task_type in ["classification", "regression"]:
                    models = self._recommend_supervised_models(df, target_col, task_type)
                    analysis["model_suggestions"][target_col] = {
                        "task_type": task_type,
                        "recommended_models": models,
                        "expected_performance": self._estimate_performance(df, target_col, task_type)
                    }
            
            # Unsupervised learning recommendations
            if len(numeric_cols) >= 2:
                analysis["ml_recommendations"].append({
                    "type": "clustering",
                    "description": "Discover hidden patterns and group similar data points",
                    "methods": ["K-Means", "DBSCAN"],
                    "use_cases": ["Customer segmentation", "Anomaly detection", "Market analysis"]
                })
                
                analysis["ml_recommendations"].append({
                    "type": "dimensionality_reduction",
                    "description": "Reduce data complexity while preserving important information",
                    "methods": ["PCA", "t-SNE"],
                    "use_cases": ["Visualization", "Feature reduction", "Noise removal"]
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"ML analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def train_model(self, file_path: str, target_column: str, 
                   model_type: str = "auto", task_type: str = "auto",
                   test_size: float = 0.2, cross_validation: bool = True) -> Dict[str, Any]:
        """Train machine learning model with comprehensive evaluation"""
        try:
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            if target_column not in df.columns:
                return {"error": f"Target column '{target_column}' not found"}
            
            # Auto-detect task type if not specified
            if task_type == "auto":
                task_type = self._detect_task_type(df, target_column)
            
            # Prepare data
            X, y, preprocessing_pipeline = self._prepare_data(df, target_column, task_type)
            
            if X is None:
                return {"error": "Failed to prepare data"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, 
                stratify=y if task_type == "classification" and len(np.unique(y)) > 1 else None
            )
            
            # Select and train model
            if model_type == "auto":
                model_results = self._auto_select_model(X_train, y_train, task_type, cross_validation)
                best_model = model_results["best_model"]
                model_name = model_results["best_model_name"]
                all_scores = model_results["all_scores"]
            else:
                if model_type not in self.default_models.get(task_type, {}):
                    return {"error": f"Model type '{model_type}' not available for {task_type}"}
                
                model = self.default_models[task_type][model_type]
                best_model = self._create_full_pipeline(preprocessing_pipeline, model)
                best_model.fit(X_train, y_train)
                model_name = model_type
                all_scores = {}
            
            # Evaluate model
            evaluation = self._evaluate_model(best_model, X_train, X_test, y_train, y_test, task_type)
            
            # Store model
            model_id = str(uuid.uuid4())
            self.models_storage[model_id] = {
                "model": best_model,
                "preprocessing_pipeline": preprocessing_pipeline,
                "task_type": task_type,
                "target_column": target_column,
                "model_name": model_name,
                "feature_names": X.columns.tolist() if hasattr(X, 'columns') else None,
                "created_at": datetime.now().isoformat(),
                "evaluation": evaluation
            }
            
            # Generate insights
            insights = self._generate_model_insights(best_model, X, y, task_type, target_column)
            
            return {
                "status": "success",
                "model_id": model_id,
                "model_name": model_name,
                "task_type": task_type,
                "evaluation": evaluation,
                "insights": insights,
                "all_model_scores": all_scores,
                "message": f"🤖 {model_name.title()} model trained successfully!"
            }
            
        except Exception as e:
            logger.error(f"Model training error: {e}")
            return {"error": f"Training failed: {str(e)}"}
    
    def make_predictions(self, model_id: str, file_path: str) -> Dict[str, Any]:
        """Make predictions using trained model"""
        try:
            if model_id not in self.models_storage:
                return {"error": "Model not found"}
            
            model_info = self.models_storage[model_id]
            model = model_info["model"]
            task_type = model_info["task_type"]
            target_column = model_info["target_column"]
            
            # Load data
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            # Remove target column if present
            if target_column in df.columns:
                X = df.drop(columns=[target_column])
            else:
                X = df.copy()
            
            # Make predictions
            if task_type == "classification":
                predictions = model.predict(X)
                probabilities = model.predict_proba(X) if hasattr(model, 'predict_proba') else None
            else:  # regression
                predictions = model.predict(X)
                probabilities = None
            
            # Create results DataFrame
            results_df = df.copy()
            results_df['predicted'] = predictions
            
            if probabilities is not None:
                classes = model.classes_ if hasattr(model, 'classes_') else np.unique(predictions)
                for i, class_name in enumerate(classes):
                    results_df[f'probability_{class_name}'] = probabilities[:, i]
            
            # Generate prediction summary
            summary = self._generate_prediction_summary(predictions, probabilities, task_type)
            
            return {
                "status": "success",
                "predictions": predictions.tolist(),
                "probabilities": probabilities.tolist() if probabilities is not None else None,
                "summary": summary,
                "results_preview": results_df.head(10).to_dict('records'),
                "message": f"✅ Predictions generated for {len(predictions)} samples"
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"error": f"Prediction failed: {str(e)}"}
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get detailed information about a trained model"""
        try:
            if model_id not in self.models_storage:
                return {"error": "Model not found"}
            
            model_info = self.models_storage[model_id].copy()
            # Remove the actual model object for JSON serialization
            model_info.pop("model", None)
            model_info.pop("preprocessing_pipeline", None)
            
            return {
                "status": "success",
                "model_info": model_info
            }
            
        except Exception as e:
            logger.error(f"Model info error: {e}")
            return {"error": f"Failed to get model info: {str(e)}"}
    
    def list_models(self) -> Dict[str, Any]:
        """List all trained models"""
        try:
            models_list = []
            
            for model_id, model_info in self.models_storage.items():
                models_list.append({
                    "model_id": model_id,
                    "model_name": model_info["model_name"],
                    "task_type": model_info["task_type"],
                    "target_column": model_info["target_column"],
                    "created_at": model_info["created_at"],
                    "accuracy": model_info["evaluation"].get("accuracy", model_info["evaluation"].get("r2_score", 0))
                })
            
            return {
                "status": "success",
                "models": models_list,
                "count": len(models_list)
            }
            
        except Exception as e:
            logger.error(f"List models error: {e}")
            return {"error": f"Failed to list models: {str(e)}"}
    
    def _load_data(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load data from file"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                return pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif file_ext == '.json':
                return pd.read_json(file_path)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Data loading error: {e}")
            return None
    
    def _get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get data summary for ML analysis"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        return {
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(categorical_cols),
            "missing_values": df.isnull().sum().sum(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024**2)
        }
    
    def _suggest_target_variables(self, df: pd.DataFrame, numeric_cols: List[str], 
                                 categorical_cols: List[str]) -> List[Dict[str, Any]]:
        """Suggest potential target variables"""
        suggestions = []
        
        # Suggest categorical columns for classification
        for col in categorical_cols:
            unique_count = df[col].nunique()
            if 2 <= unique_count <= 20:  # Good for classification
                suggestions.append({
                    "column": col,
                    "task_type": "classification",
                    "reason": f"Categorical with {unique_count} classes - ideal for classification",
                    "confidence": "high" if unique_count <= 10 else "medium"
                })
        
        # Suggest numeric columns for regression
        for col in numeric_cols:
            # Check if it's not an ID-like column
            if not any(keyword in col.lower() for keyword in ['id', 'index', 'key']):
                suggestions.append({
                    "column": col,
                    "task_type": "regression",
                    "reason": f"Continuous numeric variable - suitable for regression",
                    "confidence": "medium"
                })
        
        # Binary classification from numeric columns
        for col in numeric_cols:
            unique_values = df[col].dropna().unique()
            if len(unique_values) == 2 and set(unique_values).issubset({0, 1}):
                suggestions.append({
                    "column": col,
                    "task_type": "classification",
                    "reason": f"Binary variable (0/1) - perfect for binary classification",
                    "confidence": "high"
                })
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _analyze_preprocessing_needs(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze what preprocessing is needed"""
        needs = []
        
        # Missing values
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            needs.append({
                "type": "missing_values",
                "description": f"Handle {missing_count} missing values with imputation",
                "priority": "high"
            })
        
        # Categorical encoding
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            needs.append({
                "type": "categorical_encoding",
                "description": f"Encode {len(categorical_cols)} categorical columns",
                "priority": "high"
            })
        
        # Feature scaling
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            # Check if scaling is needed
            ranges = []
            for col in numeric_cols:
                col_range = df[col].max() - df[col].min()
                ranges.append(col_range)
            
            if max(ranges) / min(ranges) > 100:  # Large difference in scales
                needs.append({
                    "type": "feature_scaling",
                    "description": "Scale features due to different value ranges",
                    "priority": "medium"
                })
        
        return needs
    
    def _recommend_supervised_models(self, df: pd.DataFrame, target_col: str, task_type: str) -> List[Dict[str, Any]]:
        """Recommend models based on data characteristics"""
        recommendations = []
        data_size = len(df)
        feature_count = len(df.columns) - 1
        
        if task_type == "classification":
            unique_classes = df[target_col].nunique()
            
            # Random Forest - always good
            recommendations.append({
                "model": "random_forest",
                "reason": "Excellent performance, handles mixed data types, provides feature importance",
                "pros": ["Robust", "No scaling needed", "Feature importance"],
                "cons": ["Can overfit", "Less interpretable"],
                "suitability_score": 0.9
            })
            
            # Logistic Regression - good for linear relationships
            recommendations.append({
                "model": "logistic_regression",
                "reason": "Fast, interpretable, good baseline model",
                "pros": ["Interpretable", "Fast", "Probabilistic output"],
                "cons": ["Assumes linearity", "Needs scaling"],
                "suitability_score": 0.7
            })
            
            # XGBoost if available and data is sufficient
            if HAS_XGBOOST and data_size > 1000:
                recommendations.append({
                    "model": "xgboost",
                    "reason": "State-of-the-art performance, handles complex patterns",
                    "pros": ["High accuracy", "Built-in regularization", "Feature importance"],
                    "cons": ["Requires tuning", "Can overfit"],
                    "suitability_score": 0.95
                })
        
        elif task_type == "regression":
            # Random Forest - always good
            recommendations.append({
                "model": "random_forest",
                "reason": "Handles non-linear relationships, robust to outliers",
                "pros": ["Non-linear", "Robust", "Feature importance"],
                "cons": ["Can overfit", "Memory intensive"],
                "suitability_score": 0.9
            })
            
            # Linear Regression - good baseline
            recommendations.append({
                "model": "linear_regression",
                "reason": "Simple, fast, interpretable baseline",
                "pros": ["Interpretable", "Fast", "No hyperparameters"],
                "cons": ["Assumes linearity", "Sensitive to outliers"],
                "suitability_score": 0.6
            })
            
            # XGBoost if available
            if HAS_XGBOOST and data_size > 1000:
                recommendations.append({
                    "model": "xgboost",
                    "reason": "Excellent performance for structured data",
                    "pros": ["High accuracy", "Handles missing values", "Feature importance"],
                    "cons": ["Requires tuning", "Slower training"],
                    "suitability_score": 0.95
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations[:3]  # Top 3 recommendations
    
    def _estimate_performance(self, df: pd.DataFrame, target_col: str, task_type: str) -> Dict[str, Any]:
        """Estimate expected model performance"""
        data_size = len(df)
        feature_count = len(df.columns) - 1
        
        # Base performance estimates
        if task_type == "classification":
            unique_classes = df[target_col].nunique()
            class_balance = df[target_col].value_counts(normalize=True).std()
            
            if data_size < 100:
                expected_accuracy = 0.6
            elif data_size < 1000:
                expected_accuracy = 0.75
            else:
                expected_accuracy = 0.85
            
            # Adjust for class imbalance
            if class_balance > 0.3:  # Imbalanced
                expected_accuracy -= 0.1
            
            # Adjust for complexity
            if unique_classes > 10:
                expected_accuracy -= 0.1
            
            return {
                "expected_accuracy": max(0.5, min(0.95, expected_accuracy)),
                "difficulty": "high" if unique_classes > 10 or class_balance > 0.3 else "medium",
                "data_sufficiency": "good" if data_size > 1000 else "limited"
            }
        
        else:  # regression
            if data_size < 100:
                expected_r2 = 0.5
            elif data_size < 1000:
                expected_r2 = 0.7
            else:
                expected_r2 = 0.8
            
            return {
                "expected_r2": max(0.3, min(0.9, expected_r2)),
                "difficulty": "medium",
                "data_sufficiency": "good" if data_size > 1000 else "limited"
            }
    
    def _detect_task_type(self, df: pd.DataFrame, target_column: str) -> str:
        """Auto-detect whether it's classification or regression"""
        target_data = df[target_column].dropna()
        unique_count = target_data.nunique()
        
        # If numeric and few unique values, likely classification
        if pd.api.types.is_numeric_dtype(target_data):
            if unique_count <= 20 and unique_count < len(target_data) * 0.1:
                return "classification"
            else:
                return "regression"
        else:
            return "classification"
    
    def _prepare_data(self, df: pd.DataFrame, target_column: str, task_type: str) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray], Optional[ColumnTransformer]]:
        """Prepare data for ML training"""
        try:
            # Separate features and target
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            # Handle missing values in target
            valid_indices = ~y.isnull()
            X = X[valid_indices]
            y = y[valid_indices]
            
            if len(X) == 0:
                return None, None, None
            
            # Encode target for classification
            if task_type == "classification" and not pd.api.types.is_numeric_dtype(y):
                label_encoder = LabelEncoder()
                y = label_encoder.fit_transform(y)
            
            # Create preprocessing pipeline
            numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
            
            preprocessors = []
            
            if numeric_cols:
                numeric_pipeline = Pipeline([
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ])
                preprocessors.append(('num', numeric_pipeline, numeric_cols))
            
            if categorical_cols:
                categorical_pipeline = Pipeline([
                    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                    ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
                ])
                preprocessors.append(('cat', categorical_pipeline, categorical_cols))
            
            if preprocessors:
                preprocessing_pipeline = ColumnTransformer(preprocessors)
                X_processed = preprocessing_pipeline.fit_transform(X)
                
                # Convert back to DataFrame for easier handling
                if hasattr(preprocessing_pipeline, 'get_feature_names_out'):
                    feature_names = preprocessing_pipeline.get_feature_names_out()
                else:
                    feature_names = [f'feature_{i}' for i in range(X_processed.shape[1])]
                
                X_processed = pd.DataFrame(X_processed, columns=feature_names)
            else:
                X_processed = X
                preprocessing_pipeline = None
            
            return X_processed, y.values, preprocessing_pipeline
            
        except Exception as e:
            logger.error(f"Data preparation error: {e}")
            return None, None, None
    
    def _auto_select_model(self, X_train: pd.DataFrame, y_train: np.ndarray, 
                          task_type: str, cross_validation: bool = True) -> Dict[str, Any]:
        """Automatically select the best model"""
        models_to_try = self.default_models[task_type].copy()
        
        # Add advanced models if available
        if HAS_XGBOOST and len(X_train) > 500:
            if task_type == "classification":
                models_to_try['xgboost'] = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
            else:
                models_to_try['xgboost'] = xgb.XGBRegressor(random_state=42)
        
        if HAS_LIGHTGBM and len(X_train) > 500:
            if task_type == "classification":
                models_to_try['lightgbm'] = lgb.LGBMClassifier(random_state=42, verbose=-1)
            else:
                models_to_try['lightgbm'] = lgb.LGBMRegressor(random_state=42, verbose=-1)
        
        best_score = -np.inf
        best_model = None
        best_model_name = None
        all_scores = {}
        
        scoring = 'accuracy' if task_type == "classification" else 'r2'
        
        for name, model in models_to_try.items():
            try:
                if cross_validation and len(X_train) > 50:
                    # Use cross-validation
                    scores = cross_val_score(model, X_train, y_train, cv=5, scoring=scoring)
                    mean_score = scores.mean()
                    all_scores[name] = {
                        'mean_score': float(mean_score),
                        'std_score': float(scores.std()),
                        'all_scores': scores.tolist()
                    }
                else:
                    # Simple train-validation split
                    X_temp_train, X_temp_val, y_temp_train, y_temp_val = train_test_split(
                        X_train, y_train, test_size=0.2, random_state=42
                    )
                    model.fit(X_temp_train, y_temp_train)
                    
                    if task_type == "classification":
                        mean_score = accuracy_score(y_temp_val, model.predict(X_temp_val))
                    else:
                        mean_score = r2_score(y_temp_val, model.predict(X_temp_val))
                    
                    all_scores[name] = {'mean_score': float(mean_score)}
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
                    best_model_name = name
                    
            except Exception as e:
                logger.warning(f"Failed to evaluate {name}: {e}")
                continue
        
        if best_model is None:
            # Fallback to Random Forest
            best_model = models_to_try['random_forest']
            best_model_name = 'random_forest'
        
        # Train the best model on full training data
        best_model.fit(X_train, y_train)
        
        return {
            "best_model": best_model,
            "best_model_name": best_model_name,
            "best_score": float(best_score),
            "all_scores": all_scores
        }
    
    def _create_full_pipeline(self, preprocessing_pipeline: Optional[ColumnTransformer], 
                             model) -> Pipeline:
        """Create full ML pipeline with preprocessing and model"""
        if preprocessing_pipeline is not None:
            return Pipeline([
                ('preprocessor', preprocessing_pipeline),
                ('model', model)
            ])
        else:
            return Pipeline([('model', model)])
    
    def _evaluate_model(self, model, X_train, X_test, y_train, y_test, task_type: str) -> Dict[str, Any]:
        """Comprehensive model evaluation"""
        evaluation = {}
        
        # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        if task_type == "classification":
            # Classification metrics
            evaluation.update({
                "train_accuracy": float(accuracy_score(y_train, y_train_pred)),
                "test_accuracy": float(accuracy_score(y_test, y_test_pred)),
                "classification_report": classification_report(y_test, y_test_pred, output_dict=True)
            })
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_test_pred)
            evaluation["confusion_matrix"] = cm.tolist()
            
        else:  # regression
            # Regression metrics
            evaluation.update({
                "train_r2": float(r2_score(y_train, y_train_pred)),
                "test_r2": float(r2_score(y_test, y_test_pred)),
                "train_mse": float(mean_squared_error(y_train, y_train_pred)),
                "test_mse": float(mean_squared_error(y_test, y_test_pred)),
                "train_mae": float(mean_absolute_error(y_train, y_train_pred)),
                "test_mae": float(mean_absolute_error(y_test, y_test_pred))
            })
        
        # Calculate overfitting indicator
        if task_type == "classification":
            train_score = evaluation["train_accuracy"]
            test_score = evaluation["test_accuracy"]
        else:
            train_score = evaluation["train_r2"]
            test_score = evaluation["test_r2"]
        
        overfitting = train_score - test_score
        evaluation["overfitting_indicator"] = float(overfitting)
        evaluation["overfitting_status"] = "high" if overfitting > 0.1 else "moderate" if overfitting > 0.05 else "low"
        
        return evaluation
    
    def _generate_model_insights(self, model, X, y, task_type: str, target_column: str) -> List[str]:
        """Generate insights about the trained model"""
        insights = []
        
        # Feature importance (if available)
        if hasattr(model, 'feature_importances_') or (hasattr(model, 'named_steps') and hasattr(model.named_steps.get('model'), 'feature_importances_')):
            try:
                if hasattr(model, 'feature_importances_'):
                    importances = model.feature_importances_
                else:
                    importances = model.named_steps['model'].feature_importances_
                
                if hasattr(X, 'columns'):
                    feature_names = X.columns
                else:
                    feature_names = [f'feature_{i}' for i in range(len(importances))]
                
                # Get top 3 most important features
                top_indices = np.argsort(importances)[-3:][::-1]
                top_features = [feature_names[i] for i in top_indices]
                
                insights.append(f"🎯 Most important features for predicting {target_column}: {', '.join(top_features)}")
                
            except Exception as e:
                logger.warning(f"Could not extract feature importance: {e}")
        
        # Model-specific insights
        model_name = type(model).__name__.lower()
        if 'randomforest' in model_name:
            insights.append("🌳 Random Forest provides good balance between accuracy and interpretability")
        elif 'xgb' in model_name or 'xgboost' in model_name:
            insights.append("🚀 XGBoost is excellent for structured data and handles missing values automatically")
        elif 'logistic' in model_name:
            insights.append("📊 Logistic Regression provides interpretable coefficients and probability estimates")
        elif 'linear' in model_name:
            insights.append("📈 Linear model assumes linear relationship between features and target")
        
        # Data insights
        if len(X) < 1000:
            insights.append("⚠️ Limited data size - consider collecting more data for better performance")
        elif len(X) > 10000:
            insights.append("✅ Good data size - model should generalize well")
        
        # Task-specific insights
        if task_type == "classification":
            unique_classes = len(np.unique(y))
            if unique_classes == 2:
                insights.append("🎯 Binary classification - perfect for yes/no decisions")
            else:
                insights.append(f"🎯 Multi-class classification with {unique_classes} classes")
        else:
            insights.append("📈 Regression model - predicts continuous values")
        
        return insights
    
    def _generate_prediction_summary(self, predictions: np.ndarray, 
                                   probabilities: Optional[np.ndarray], 
                                   task_type: str) -> Dict[str, Any]:
        """Generate summary of predictions"""
        summary = {"total_predictions": len(predictions)}
        
        if task_type == "classification":
            unique, counts = np.unique(predictions, return_counts=True)
            summary["class_distribution"] = {str(cls): int(count) for cls, count in zip(unique, counts)}
            
            if probabilities is not None:
                # Calculate confidence statistics
                max_probs = np.max(probabilities, axis=1)
                summary["confidence_stats"] = {
                    "mean_confidence": float(np.mean(max_probs)),
                    "min_confidence": float(np.min(max_probs)),
                    "max_confidence": float(np.max(max_probs)),
                    "low_confidence_count": int(np.sum(max_probs < 0.7))
                }
        else:  # regression
            summary["prediction_stats"] = {
                "mean": float(np.mean(predictions)),
                "median": float(np.median(predictions)),
                "std": float(np.std(predictions)),
                "min": float(np.min(predictions)),
                "max": float(np.max(predictions))
            }
        
        return summary

# Global ML service instance
ml_service = MLService() 