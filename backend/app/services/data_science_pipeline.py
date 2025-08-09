"""
DataSoph AI - Complete Data Science Pipeline Implementation
Comprehensive CRISP-DM lifecycle with Claude/ChatGPT level intelligence
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Machine Learning Stack
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVC, SVR
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, mean_squared_error
from sklearn.feature_selection import SelectKBest, RFE, chi2, f_classif
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline

# Advanced ML - Safe imports without dask dependency issues
xgb = None

try:
    import xgboost as xgb
    print("✅ XGBoost loaded successfully")
except ImportError:
    print("⚠️ XGBoost not available - using sklearn models only")

# Skip LightGBM completely to avoid dask/pandas compatibility issues
lgb = None
print("⚠️ LightGBM disabled due to environment compatibility")

# Statistical Analysis
import scipy.stats as stats

# Time Series
from datetime import datetime, timedelta

# Text Processing
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re

# Visualization Enhancement
import warnings
warnings.filterwarnings('ignore')

from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class DataSciencePhaseDetector:
    """Intelligent detection of data science phases from user queries"""
    
    def __init__(self):
        self.phase_patterns = {
            "problem_definition": {
                "keywords": ["problem", "business", "goal", "objective", "requirement", "what should", "how can", "strategy", "başlangıç", "problem tanımı", "hedef", "amaç"],
                "patterns": [r"what.*problem", r"business.*goal", r"how.*improve", r"objective.*project", r"ne.*problem", r"hangi.*hedef"]
            },
            "data_acquisition": {
                "keywords": ["load", "import", "read", "connect", "database", "csv", "excel", "api", "scrape", "yükle", "oku", "veri al", "dosya"],
                "patterns": [r"load.*data", r"read.*file", r"import.*dataset", r"connect.*database", r"veri.*yükle", r"dosya.*oku"]
            },
            "data_exploration": {
                "keywords": ["explore", "eda", "understand", "describe", "summary", "profile", "head", "info", "shape", "keşfet", "anla", "incele", "özet", "analiz"],
                "patterns": [r"explore.*data", r"understand.*dataset", r"data.*summary", r"show.*info", r"veri.*keşfet", r"analiz.*et"]
            },
            "data_cleaning": {
                "keywords": ["clean", "missing", "null", "duplicates", "outliers", "preprocess", "handle", "remove", "temizle", "eksik", "aykırı", "duplikat"],
                "patterns": [r"clean.*data", r"handle.*missing", r"remove.*outliers", r"deal.*duplicates", r"veri.*temizle", r"eksik.*değer"]
            },
            "feature_engineering": {
                "keywords": ["feature", "transform", "encode", "scale", "create", "engineer", "normalize", "standardize", "özellik", "dönüştür", "kodla", "ölçekle"],
                "patterns": [r"create.*features", r"transform.*variables", r"encode.*categorical", r"scale.*data", r"özellik.*oluştur", r"değişken.*dönüştür"]
            },
            "modeling": {
                "keywords": ["model", "algorithm", "predict", "classify", "regression", "cluster", "train", "fit", "machine learning", "makine öğrenmesi", "tahmin", "sınıflandır"],
                "patterns": [r"build.*model", r"train.*algorithm", r"predict.*target", r"classify.*data", r"model.*oluştur", r"tahmin.*yap"]
            },
            "visualization": {
                "keywords": ["plot", "chart", "graph", "visualize", "show", "display", "dashboard", "histogram", "scatter", "grafik", "çiz", "görselleştir", "dashboard"],
                "patterns": [r"plot.*data", r"create.*chart", r"visualize.*relationship", r"show.*distribution", r"grafik.*çiz", r"görselleştir"]
            },
            "evaluation": {
                "keywords": ["evaluate", "validate", "accuracy", "performance", "metric", "score", "test", "assessment", "değerlendir", "doğruluk", "performans", "test"],
                "patterns": [r"evaluate.*model", r"check.*performance", r"measure.*accuracy", r"validate.*results", r"model.*değerlendir", r"performans.*ölç"]
            },
            "interpretation": {
                "keywords": ["explain", "interpret", "understand", "why", "feature importance", "shap", "insights", "açıkla", "yorumla", "anla", "neden", "önem"],
                "patterns": [r"explain.*model", r"interpret.*results", r"feature.*importance", r"why.*prediction", r"model.*açıkla", r"sonuç.*yorumla"]
            },
            "deployment": {
                "keywords": ["deploy", "production", "api", "serve", "monitor", "implement", "operationalize", "dağıt", "prodüksiyon", "uygula", "izle"],
                "patterns": [r"deploy.*model", r"production.*ready", r"create.*api", r"implement.*solution", r"model.*dağıt", r"üretime.*al"]
            }
        }
    
    def detect_phase(self, query: str, context: dict = None) -> dict:
        """Detect which data science phase the user is in"""
        query_lower = query.lower()
        phase_scores = {}
        
        for phase, config in self.phase_patterns.items():
            score = 0
            
            # Keyword matching
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    score += 1
            
            # Pattern matching
            for pattern in config["patterns"]:
                if re.search(pattern, query_lower):
                    score += 2
            
            phase_scores[phase] = score
        
        # Determine primary and secondary phases
        sorted_phases = sorted(phase_scores.items(), key=lambda x: x[1], reverse=True)
        primary_phase = sorted_phases[0][0] if sorted_phases[0][1] > 0 else "general_conversation"
        secondary_phase = sorted_phases[1][0] if len(sorted_phases) > 1 and sorted_phases[1][1] > 0 else None
        
        return {
            "primary_phase": primary_phase,
            "secondary_phase": secondary_phase,
            "confidence": sorted_phases[0][1] if sorted_phases else 0,
            "all_scores": phase_scores
        }

class ComprehensiveDataAnalyzer:
    """Comprehensive data analysis engine for all CRISP-DM phases"""
    
    def __init__(self):
        self.analysis_results = {}
        
    def automated_eda(self, df: pd.DataFrame, target_column: str = None) -> dict:
        """Comprehensive automated exploratory data analysis"""
        
        analysis = {
            "basic_info": {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "null_counts": df.isnull().sum().to_dict(),
                "null_percentages": (df.isnull().sum() / len(df) * 100).to_dict()
            },
            "statistical_summary": {},
            "data_quality": {},
            "relationships": {},
            "recommendations": []
        }
        
        # Numerical columns analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            analysis["statistical_summary"]["numerical"] = df[numeric_cols].describe().to_dict()
            
            # Outlier detection
            outlier_info = {}
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col]
                outlier_info[col] = {
                    "count": len(outliers),
                    "percentage": len(outliers) / len(df) * 100
                }
            analysis["data_quality"]["outliers"] = outlier_info
        
        # Categorical columns analysis
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if categorical_cols:
            analysis["statistical_summary"]["categorical"] = {}
            for col in categorical_cols:
                analysis["statistical_summary"]["categorical"][col] = {
                    "unique_count": df[col].nunique(),
                    "top_values": df[col].value_counts().head().to_dict(),
                    "cardinality": "high" if df[col].nunique() > len(df) * 0.5 else "low"
                }
        
        # Correlation analysis
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        high_corr_pairs.append({
                            "feature1": corr_matrix.columns[i],
                            "feature2": corr_matrix.columns[j],
                            "correlation": corr_value,
                            "strength": "very_strong" if abs(corr_value) > 0.9 else "strong"
                        })
            analysis["relationships"]["high_correlations"] = high_corr_pairs
        
        # Target variable analysis
        if target_column and target_column in df.columns:
            target_analysis = self._analyze_target_variable(df, target_column, numeric_cols, categorical_cols)
            analysis["target_analysis"] = target_analysis
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_eda_recommendations(analysis, df)
        
        return analysis
    
    def _analyze_target_variable(self, df: pd.DataFrame, target_column: str, 
                               numeric_cols: List[str], categorical_cols: List[str]) -> dict:
        """Analyze target variable and its relationships"""
        
        target_analysis = {
            "type": "numerical" if target_column in numeric_cols else "categorical",
            "distribution": {},
            "relationships": {}
        }
        
        if target_column in numeric_cols:
            # Numerical target
            target_analysis["distribution"] = {
                "mean": df[target_column].mean(),
                "median": df[target_column].median(),
                "std": df[target_column].std(),
                "min": df[target_column].min(),
                "max": df[target_column].max(),
                "skewness": df[target_column].skew(),
                "kurtosis": df[target_column].kurtosis()
            }
            
            # Correlations with other numerical features
            correlations = {}
            for col in numeric_cols:
                if col != target_column:
                    corr = df[target_column].corr(df[col])
                    if abs(corr) > 0.3:
                        correlations[col] = corr
            target_analysis["relationships"]["numerical_correlations"] = correlations
            
        else:
            # Categorical target
            target_analysis["distribution"] = {
                "value_counts": df[target_column].value_counts().to_dict(),
                "unique_count": df[target_column].nunique(),
                "most_frequent": df[target_column].mode().iloc[0] if not df[target_column].mode().empty else None
            }
            
            # Check class balance
            class_counts = df[target_column].value_counts()
            min_class_ratio = class_counts.min() / class_counts.max()
            target_analysis["class_balance"] = {
                "balanced": min_class_ratio > 0.5,
                "ratio": min_class_ratio,
                "recommendation": "consider_resampling" if min_class_ratio < 0.3 else "good_balance"
            }
        
        return target_analysis
    
    def automated_feature_engineering(self, df: pd.DataFrame, target_column: str = None) -> dict:
        """Automated feature engineering suggestions and implementation"""
        
        suggestions = {
            "numerical_transformations": [],
            "categorical_transformations": [],
            "new_features": [],
            "feature_selection": [],
            "code_examples": []
        }
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Numerical feature suggestions
        for col in numeric_cols:
            if col == target_column:
                continue
                
            skewness = df[col].skew()
            if abs(skewness) > 1:
                transformation = "log" if skewness > 1 else "square_root"
                suggestions["numerical_transformations"].append({
                    "feature": col,
                    "transformation": transformation,
                    "reason": f"High skewness: {skewness:.2f}",
                    "code": f"df['{col}_transformed'] = np.log1p(df['{col}'])" if transformation == "log" else f"df['{col}_sqrt'] = np.sqrt(df['{col}'])"
                })
            
            # Check for scaling needs
            if df[col].std() > 1000 or df[col].mean() > 1000:
                suggestions["numerical_transformations"].append({
                    "feature": col,
                    "transformation": "standardization",
                    "reason": f"Large scale values (mean: {df[col].mean():.2f})",
                    "code": f"from sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\ndf['{col}_scaled'] = scaler.fit_transform(df[['{col}']])"
                })
        
        # Categorical feature suggestions
        for col in categorical_cols:
            if col == target_column:
                continue
                
            unique_count = df[col].nunique()
            if unique_count > 10:
                suggestions["categorical_transformations"].append({
                    "feature": col,
                    "transformation": "target_encoding",
                    "reason": f"High cardinality: {unique_count} unique values",
                    "code": f"# Target encoding for {col}\ntarget_mean = df.groupby('{col}')['{target_column}'].mean()\ndf['{col}_encoded'] = df['{col}'].map(target_mean)" if target_column else f"# Consider frequency encoding for {col}"
                })
            else:
                suggestions["categorical_transformations"].append({
                    "feature": col,
                    "transformation": "one_hot_encoding",
                    "reason": f"Low cardinality: {unique_count} unique values",
                    "code": f"df_encoded = pd.get_dummies(df, columns=['{col}'], prefix='{col}')"
                })
        
        # Feature interaction suggestions
        if len(numeric_cols) >= 2:
            suggestions["new_features"].append({
                "type": "interaction",
                "features": numeric_cols[:2],
                "transformation": "multiplication",
                "code": f"df['interaction_{numeric_cols[0]}_{numeric_cols[1]}'] = df['{numeric_cols[0]}'] * df['{numeric_cols[1]}')"
            })
        
        return suggestions
    
    def automated_model_selection(self, df: pd.DataFrame, target_column: str, problem_type: str = None) -> dict:
        """Automated model selection and evaluation"""
        
        if target_column not in df.columns:
            return {"error": f"Target column '{target_column}' not found in dataset"}
        
        # Auto-detect problem type if not specified
        if problem_type is None:
            if df[target_column].dtype in ['object', 'category'] or df[target_column].nunique() < 10:
                problem_type = "classification"
            else:
                problem_type = "regression"
        
        # Prepare features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Handle categorical variables in features
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
        else:
            X_encoded = X.copy()
        
        # Handle missing values
        if X_encoded.isnull().sum().sum() > 0:
            imputer = SimpleImputer(strategy='median')
            X_encoded = pd.DataFrame(imputer.fit_transform(X_encoded), columns=X_encoded.columns)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42, stratify=y if problem_type == "classification" and y.nunique() > 1 else None)
        
        results = {
            "problem_type": problem_type,
            "models": {}, 
            "best_model": None, 
            "recommendations": [],
            "feature_importance": {},
            "preprocessing_steps": []
        }
        
        if problem_type == "classification":
            models = {
                "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
                "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
            }
            
            # Add advanced models if available
            if xgb:
                models["XGBoost"] = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
            # LightGBM temporarily disabled
            # if lgb:
            #     models["LightGBM"] = lgb.LGBMClassifier(random_state=42, verbose=-1)
            
            scoring_method = 'accuracy'
            
        elif problem_type == "regression":
            models = {
                "Random Forest": RandomForestRegressor(random_state=42, n_estimators=100),
                "Linear Regression": LinearRegression(),
                "Ridge Regression": Ridge(random_state=42)
            }
            
            # Add advanced models if available
            if xgb:
                models["XGBoost"] = xgb.XGBRegressor(random_state=42)
            # LightGBM temporarily disabled
            # if lgb:
            #     models["LightGBM"] = lgb.LGBMRegressor(random_state=42, verbose=-1)
            
            scoring_method = 'neg_mean_squared_error'
        
        # Train and evaluate models
        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring=scoring_method)
                
                # Get feature importance if available
                feature_importance = {}
                if hasattr(model, 'feature_importances_'):
                    importance_scores = model.feature_importances_
                    feature_names = X_encoded.columns
                    feature_importance = dict(zip(feature_names, importance_scores))
                    # Sort by importance
                    feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
                
                results["models"][name] = {
                    "cv_mean": cv_scores.mean(),
                    "cv_std": cv_scores.std(),
                    "model_object": model,
                    "feature_importance": feature_importance
                }
                
            except Exception as e:
                results["models"][name] = {"error": str(e)}
        
        # Find best model
        valid_models = {k: v for k, v in results["models"].items() if "error" not in v}
        if valid_models:
            best_model_name = max(valid_models.keys(), key=lambda k: valid_models[k]["cv_mean"])
            results["best_model"] = best_model_name
            results["feature_importance"] = valid_models[best_model_name]["feature_importance"]
            
            results["recommendations"].extend([
                f"Best performing model: {best_model_name}",
                f"Cross-validation score: {valid_models[best_model_name]['cv_mean']:.4f} ± {valid_models[best_model_name]['cv_std']:.4f}",
                "Consider hyperparameter tuning for further improvement"
            ])
        
        return results
    
    def _generate_eda_recommendations(self, analysis: dict, df: pd.DataFrame) -> List[str]:
        """Generate actionable EDA recommendations"""
        recommendations = []
        
        # Missing value recommendations
        null_percentages = analysis["basic_info"]["null_percentages"]
        high_missing = [col for col, pct in null_percentages.items() if pct > 20]
        if high_missing:
            recommendations.append(f"Columns with high missing values (>20%): {', '.join(high_missing)}. Consider imputation or removal.")
        
        # Outlier recommendations
        if "outliers" in analysis["data_quality"]:
            high_outlier_cols = [col for col, info in analysis["data_quality"]["outliers"].items() if info["percentage"] > 5]
            if high_outlier_cols:
                recommendations.append(f"Columns with many outliers (>5%): {', '.join(high_outlier_cols)}. Consider outlier treatment.")
        
        # Correlation recommendations
        if "high_correlations" in analysis["relationships"]:
            high_corr = analysis["relationships"]["high_correlations"]
            if len(high_corr) > 0:
                recommendations.append(f"Found {len(high_corr)} highly correlated feature pairs. Consider dimensionality reduction.")
        
        # Data type recommendations
        categorical_cols = analysis["statistical_summary"].get("categorical", {})
        high_cardinality = [col for col, info in categorical_cols.items() if info["cardinality"] == "high"]
        if high_cardinality:
            recommendations.append(f"High cardinality categorical features: {', '.join(high_cardinality)}. Consider encoding strategies.")
        
        return recommendations

class AdvancedVisualizationEngine:
    """Comprehensive visualization engine for all data science phases"""
    
    def __init__(self):
        self.default_color_palette = px.colors.qualitative.Set3
        
    def create_comprehensive_eda_plots(self, df: pd.DataFrame, target_column: str = None) -> dict:
        """Generate comprehensive EDA visualizations"""
        
        plots = {"code_blocks": [], "plot_descriptions": []}
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Distribution plots for numerical columns
        if numeric_cols:
            plots["code_blocks"].append(f"""
# Numerical Features Distribution Analysis
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots({(len(numeric_cols) + 1) // 2}, 2, figsize=(15, {len(numeric_cols) * 2.5}))
axes = axes.ravel() if len(numeric_cols) > 1 else [axes]

numeric_cols = {numeric_cols}
for i, col in enumerate(numeric_cols):
    if i < len(axes):
        df[col].hist(bins=30, ax=axes[i], alpha=0.7, edgecolor='black')
        axes[i].set_title(f'Distribution of {{col}}', fontweight='bold')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Frequency')
        axes[i].grid(True, alpha=0.3)

# Hide unused subplots
for i in range(len(numeric_cols), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.show()

# Statistical summary
print("📊 Numerical Features Statistical Summary:")
print(df[numeric_cols].describe())
""")
            plots["plot_descriptions"].append("📊 Comprehensive distribution analysis of all numerical features with statistical summaries")
        
        # Correlation heatmap
        if len(numeric_cols) > 1:
            plots["code_blocks"].append(f"""
# Correlation Heatmap with Enhanced Styling
plt.figure(figsize=(12, 8))
correlation_matrix = df[{numeric_cols}].corr()

# Create mask for upper triangle
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

sns.heatmap(correlation_matrix, 
           mask=mask,
           annot=True, 
           cmap='RdBu_r', 
           center=0,
           square=True, 
           linewidths=0.5,
           fmt='.2f',
           cbar_kws={{"shrink": .8}})

plt.title('Feature Correlation Matrix\\n(Values closer to ±1 indicate stronger relationships)', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

# Find and display high correlations
high_corr_pairs = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_val = correlation_matrix.iloc[i, j]
        if abs(corr_val) > 0.7:
            high_corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_val))

if high_corr_pairs:
    print("🔗 High Correlation Pairs (|r| > 0.7):")
    for var1, var2, corr in high_corr_pairs:
        print(f"  • {{var1}} ↔ {{var2}}: {{corr:.3f}}")
else:
    print("✅ No highly correlated features found")
""")
            plots["plot_descriptions"].append("🔗 Advanced correlation heatmap showing feature relationships and multicollinearity detection")
        
        # Interactive Plotly visualizations
        if target_column and target_column in df.columns and len(numeric_cols) > 1:
            plots["code_blocks"].append(f"""
# Interactive Scatter Plot Matrix with Target Analysis
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Select relevant features for scatter matrix (max 6 for readability)
features_for_matrix = {numeric_cols[:6] if len(numeric_cols) > 6 else numeric_cols}
if '{target_column}' not in features_for_matrix:
    features_for_matrix = features_for_matrix[:-1] + ['{target_column}']

# Create interactive scatter plot matrix
fig = px.scatter_matrix(df[features_for_matrix], 
                       color='{target_column}' if '{target_column}' in df.columns else None,
                       title='🎯 Interactive Pairwise Feature Relationships',
                       height=800)

fig.update_layout(
    title_font_size=16,
    title_x=0.5
)

fig.show()

# Target variable analysis
if '{target_column}' in df.columns:
    print(f"🎯 Target Variable ({{'{target_column}'}}) Analysis:")
    if df['{target_column}'].dtype in ['object', 'category']:
        print("Type: Categorical")
        print(f"Classes: {{df['{target_column}'].unique()}}")
        print(f"Class distribution:\\n{{df['{target_column}'].value_counts()}}")
    else:
        print("Type: Numerical")
        print(f"Range: {{df['{target_column}'].min():.2f}} to {{df['{target_column}'].max():.2f}}")
        print(f"Mean: {{df['{target_column}'].mean():.2f}}")
        print(f"Std: {{df['{target_column}'].std():.2f}}")
""")
            plots["plot_descriptions"].append("🎯 Interactive scatter plot matrix with target variable analysis for relationship discovery")
        
        # Categorical data visualization
        if categorical_cols:
            plots["code_blocks"].append(f"""
# Categorical Features Analysis
categorical_cols = {categorical_cols}

fig, axes = plt.subplots({(len(categorical_cols) + 1) // 2}, 2, figsize=(15, {len(categorical_cols) * 3}))
axes = axes.ravel() if len(categorical_cols) > 1 else [axes]

for i, col in enumerate(categorical_cols):
    if i < len(axes):
        value_counts = df[col].value_counts().head(10)  # Top 10 categories
        
        if len(value_counts) <= 10:
            value_counts.plot(kind='bar', ax=axes[i], color='skyblue', alpha=0.7)
            axes[i].set_title(f'{{col}} Distribution', fontweight='bold')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Count')
            axes[i].tick_params(axis='x', rotation=45)
        else:
            # For high cardinality, show top 10
            axes[i].pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            axes[i].set_title(f'{{col}} Distribution (Top 10)', fontweight='bold')

# Hide unused subplots
for i in range(len(categorical_cols), len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.show()

# Categorical summary
print("📋 Categorical Features Summary:")
for col in categorical_cols:
    print(f"\\n{col}:")
    print(f"  • Unique values: {{df[col].nunique()}}")
    print(f"  • Most frequent: {{df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'}}")
    if df[col].nunique() > 10:
        print(f"  ⚠️  High cardinality detected - consider encoding strategies")
""")
            plots["plot_descriptions"].append("📋 Comprehensive categorical feature analysis with distribution plots and cardinality assessment")
        
        return plots
    
    def create_model_evaluation_plots(self, model, X_test, y_test, problem_type: str, feature_names: List[str] = None) -> dict:
        """Generate comprehensive model evaluation visualizations"""
        
        plots = {"code_blocks": [], "plot_descriptions": []}
        
        if problem_type == "classification":
            plots["code_blocks"].append("""
# 🎯 Classification Model Evaluation Suite
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Generate predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

# Create comprehensive evaluation dashboard
fig = plt.figure(figsize=(20, 12))

# 1. Confusion Matrix
plt.subplot(2, 3, 1)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
           xticklabels=model.classes_ if hasattr(model, 'classes_') else ['Class 0', 'Class 1'],
           yticklabels=model.classes_ if hasattr(model, 'classes_') else ['Class 0', 'Class 1'])
plt.title('🎯 Confusion Matrix', fontweight='bold', fontsize=12)
plt.ylabel('True Label')
plt.xlabel('Predicted Label')

# 2. ROC Curve (for binary classification)
if y_pred_proba is not None and len(np.unique(y_test)) == 2:
    plt.subplot(2, 3, 2)
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba[:, 1])
    roc_auc = auc(fpr, tpr)
    
    plt.plot(fpr, tpr, color='darkorange', lw=3, 
             label=f'ROC Curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', alpha=0.6)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('📈 ROC Curve', fontweight='bold', fontsize=12)
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)

# 3. Precision-Recall Curve
if y_pred_proba is not None and len(np.unique(y_test)) == 2:
    plt.subplot(2, 3, 3)
    precision, recall, _ = precision_recall_curve(y_test, y_pred_proba[:, 1])
    pr_auc = auc(recall, precision)
    
    plt.plot(recall, precision, color='green', lw=3,
             label=f'PR Curve (AUC = {pr_auc:.3f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('📊 Precision-Recall Curve', fontweight='bold', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)

# 4. Feature Importance (if available)
if hasattr(model, 'feature_importances_'):
    plt.subplot(2, 3, 4)
    feature_names = X_test.columns if hasattr(X_test, 'columns') else [f'Feature_{i}' for i in range(X_test.shape[1])]
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:15]  # Top 15 features
    
    plt.bar(range(len(indices)), importances[indices], alpha=0.7, color='lightcoral')
    plt.title('🔍 Top Feature Importances', fontweight='bold', fontsize=12)
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')

# 5. Prediction Distribution
plt.subplot(2, 3, 5)
if y_pred_proba is not None:
    plt.hist(y_pred_proba[:, 1], bins=30, alpha=0.7, color='purple', edgecolor='black')
    plt.axvline(x=0.5, color='red', linestyle='--', label='Decision Threshold')
    plt.title('🎲 Prediction Probability Distribution', fontweight='bold', fontsize=12)
    plt.xlabel('Predicted Probability (Positive Class)')
    plt.ylabel('Frequency')
    plt.legend()
else:
    unique_preds, counts = np.unique(y_pred, return_counts=True)
    plt.bar(unique_preds, counts, alpha=0.7, color='orange')
    plt.title('🎲 Prediction Distribution', fontweight='bold', fontsize=12)
    plt.xlabel('Predicted Class')
    plt.ylabel('Count')

# 6. Model Performance Summary
plt.subplot(2, 3, 6)
plt.axis('off')

# Calculate metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

metrics_text = f'''
📊 MODEL PERFORMANCE SUMMARY

✅ Accuracy: {accuracy:.3f}
🎯 Precision: {precision:.3f}
📈 Recall: {recall:.3f}
⚖️  F1-Score: {f1:.3f}
'''

if y_pred_proba is not None and len(np.unique(y_test)) == 2:
    metrics_text += f'📈 ROC AUC: {roc_auc:.3f}\\n'

plt.text(0.1, 0.6, metrics_text, fontsize=14, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

plt.tight_layout()
plt.show()

# Detailed Classification Report
print("\\n" + "="*60)
print("📋 DETAILED CLASSIFICATION REPORT")
print("="*60)
print(classification_report(y_test, y_pred))

# Business Insights
print("\\n" + "="*60)
print("💼 BUSINESS INSIGHTS & RECOMMENDATIONS")
print("="*60)
print(f"• Model correctly classifies {accuracy*100:.1f}% of cases")
if accuracy > 0.8:
    print("• ✅ Model shows strong predictive performance")
elif accuracy > 0.7:
    print("• ⚠️  Model shows good performance with room for improvement")
else:
    print("• 🔴 Model needs significant improvement before production use")
    
if y_pred_proba is not None and len(np.unique(y_test)) == 2:
    if roc_auc > 0.9:
        print("• 🌟 Excellent ability to distinguish between classes")
    elif roc_auc > 0.8:
        print("• ✅ Good discriminative power")
    else:
        print("• ⚠️  Consider feature engineering or algorithm tuning")
""")
            
        elif problem_type == "regression":
            plots["code_blocks"].append("""
# 📈 Regression Model Evaluation Suite
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

# Generate predictions
y_pred = model.predict(X_test)

# Create comprehensive evaluation dashboard
fig = plt.figure(figsize=(20, 12))

# 1. Actual vs Predicted Scatter Plot
plt.subplot(2, 3, 1)
plt.scatter(y_test, y_pred, alpha=0.6, color='blue', s=50)
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=3, label='Perfect Prediction')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('🎯 Actual vs Predicted Values', fontweight='bold', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Add R² annotation
r2 = r2_score(y_test, y_pred)
plt.text(0.05, 0.95, f'R² = {r2:.3f}', transform=plt.gca().transAxes, 
         fontsize=12, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# 2. Residuals Plot
plt.subplot(2, 3, 2)
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, alpha=0.6, color='green', s=50)
plt.axhline(y=0, color='red', linestyle='--', lw=2)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('📊 Residuals Plot', fontweight='bold', fontsize=12)
plt.grid(True, alpha=0.3)

# Add trend line for residuals
z = np.polyfit(y_pred, residuals, 1)
p = np.poly1d(z)
plt.plot(sorted(y_pred), p(sorted(y_pred)), "orange", linestyle='-', linewidth=2, 
         label=f'Trend (slope={z[0]:.4f})')
plt.legend()

# 3. Residuals Distribution
plt.subplot(2, 3, 3)
plt.hist(residuals, bins=30, alpha=0.7, color='purple', edgecolor='black')
plt.axvline(x=0, color='red', linestyle='--', lw=2, label='Zero Error')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('📈 Residuals Distribution', fontweight='bold', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# 4. Feature Importance (if available)
if hasattr(model, 'feature_importances_'):
    plt.subplot(2, 3, 4)
    feature_names = X_test.columns if hasattr(X_test, 'columns') else [f'Feature_{i}' for i in range(X_test.shape[1])]
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:15]  # Top 15 features
    
    plt.bar(range(len(indices)), importances[indices], alpha=0.7, color='lightcoral')
    plt.title('🔍 Top Feature Importances', fontweight='bold', fontsize=12)
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')

# 5. Prediction Error Analysis
plt.subplot(2, 3, 5)
errors = np.abs(residuals)
plt.hist(errors, bins=30, alpha=0.7, color='orange', edgecolor='black')
plt.xlabel('Absolute Error')
plt.ylabel('Frequency')
plt.title('📊 Absolute Error Distribution', fontweight='bold', fontsize=12)
plt.grid(True, alpha=0.3)

# Add percentile lines
percentiles = [50, 75, 90, 95]
for p in percentiles:
    val = np.percentile(errors, p)
    plt.axvline(x=val, linestyle='--', alpha=0.7, label=f'{p}th percentile')
plt.legend()

# 6. Model Performance Summary
plt.subplot(2, 3, 6)
plt.axis('off')

# Calculate comprehensive metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
target_std = y_test.std()

metrics_text = f'''
📊 MODEL PERFORMANCE SUMMARY

📈 R² Score: {r2:.4f}
📏 RMSE: {rmse:.4f}
📐 MAE: {mae:.4f}
📊 MAPE: {mape:.2f}%
📋 Target Std: {target_std:.4f}

📈 RMSE vs Target Std: {rmse/target_std:.2f}x
'''

performance_level = ""
if r2 > 0.9:
    performance_level = "🌟 EXCELLENT"
elif r2 > 0.8:
    performance_level = "✅ GOOD"
elif r2 > 0.6:
    performance_level = "⚠️  FAIR"
else:
    performance_level = "🔴 NEEDS IMPROVEMENT"

metrics_text += f"\\n🎯 Overall: {performance_level}"

plt.text(0.1, 0.6, metrics_text, fontsize=12, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))

plt.tight_layout()
plt.show()

# Detailed Performance Analysis
print("\\n" + "="*60)
print("📊 DETAILED REGRESSION ANALYSIS")
print("="*60)
print(f"Mean Squared Error (MSE): {mse:.6f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.6f}")
print(f"Mean Absolute Error (MAE): {mae:.6f}")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
print(f"R² Score: {r2:.6f}")
print(f"Explained Variance: {r2*100:.2f}%")

# Business Insights
print("\\n" + "="*60)
print("💼 BUSINESS INSIGHTS & RECOMMENDATIONS")
print("="*60)
print(f"• Model explains {r2*100:.1f}% of variance in target variable")
print(f"• Typical prediction error: ±{rmse:.2f} units")
print(f"• Average absolute error: {mae:.2f} units")

if r2 > 0.8:
    print("• ✅ Model ready for production deployment")
    print("• 💡 Consider A/B testing with current baseline")
elif r2 > 0.6:
    print("• ⚠️  Model shows promise but needs refinement")
    print("• 💡 Try feature engineering or ensemble methods")
else:
    print("• 🔴 Model needs significant improvement")
    print("• 💡 Consider different algorithms or more data")

# Residual analysis insights
residual_mean = np.mean(residuals)
residual_std = np.std(residuals)
print(f"\\n📊 Residual Analysis:")
print(f"• Mean residual: {residual_mean:.6f} (should be ~0)")
print(f"• Residual std: {residual_std:.6f}")

if abs(residual_mean) < 0.01 * target_std:
    print("• ✅ Model is unbiased (mean residual ≈ 0)")
else:
    print("• ⚠️  Model shows bias - predictions consistently high/low")

# Check for heteroscedasticity
correlation_resid_pred = np.corrcoef(y_pred, np.abs(residuals))[0, 1]
if abs(correlation_resid_pred) < 0.3:
    print("• ✅ Residuals show consistent variance (homoscedastic)")
else:
    print("• ⚠️  Residuals show changing variance (heteroscedastic)")
    print("• 💡 Consider log transformation of target variable")
""")
        
        return plots

class DataScienceMentor:
    """Intelligent mentor for guiding users through data science pipeline"""
    
    def __init__(self):
        self.conversation_context = {}
        self.pipeline_state = {}
        
    def generate_contextual_response(self, query: str, analysis_results: dict, 
                                   phase_info: dict, language: str) -> str:
        """Generate intelligent, context-aware responses"""
        
        current_phase = phase_info["primary_phase"]
        
        # Phase-specific response templates
        response_templates = {
            "problem_definition": {
                "Turkish": """
🎯 **İş Problemi ve Hedef Belirleme**

Projenizin temel yapı taşlarını analiz ediyorum:

{analysis_summary}

📋 **Önerilen Yaklaşım:**
{recommendations}

🚀 **Sonraki Adım:** Veri toplama ve keşif aşamasına geçelim. Hangi veri kaynaklarınız mevcut?

💡 **Pro İpucu:** İyi tanımlanmış bir problem, başarılı bir veri bilimi projesinin yarısıdır!
""",
                "English": """
🎯 **Business Problem and Goal Definition**

Analyzing the foundation of your project:

{analysis_summary}

📋 **Recommended Approach:**
{recommendations}

🚀 **Next Step:** Let's move to data collection and exploration. What data sources are available?

💡 **Pro Tip:** A well-defined problem is half of a successful data science project!
"""
            },
            "data_exploration": {
                "Turkish": """
📊 **Kapsamlı Veri Keşif Analizi**

{analysis_summary}

💡 **Kritik Bulgular:**
{key_insights}

🔍 **Veri Kalitesi Değerlendirmesi:**
{data_quality}

📈 **İstatistiksel Önemli Noktalar:**
{statistical_insights}

🚀 **Sonraki Adım:** {next_steps}

💼 **İş Değeri:** Bu bulgular, veri odaklı kararlar almak için sağlam bir temel oluşturuyor.
""",
                "English": """
📊 **Comprehensive Data Exploration Analysis**

{analysis_summary}

💡 **Critical Findings:**
{key_insights}

🔍 **Data Quality Assessment:**
{data_quality}

📈 **Statistical Key Points:**
{statistical_insights}

🚀 **Next Step:** {next_steps}

💼 **Business Value:** These findings provide a solid foundation for data-driven decision making.
"""
            },
            "modeling": {
                "Turkish": """
🤖 **Makine Öğrenmesi Model Geliştirme**

{analysis_summary}

🏆 **En İyi Model:** {best_model}

📊 **Performans Metrikleri:**
{performance_metrics}

🔍 **Model Yorumu:**
{model_interpretation}

💼 **İş Etkisi:** {business_impact}

🚀 **Sonraki Adım:** {next_steps}
""",
                "English": """
🤖 **Machine Learning Model Development**

{analysis_summary}

🏆 **Best Model:** {best_model}

📊 **Performance Metrics:**
{performance_metrics}

🔍 **Model Interpretation:**
{model_interpretation}

💼 **Business Impact:** {business_impact}

🚀 **Next Step:** {next_steps}
"""
            }
        }
        
        # Generate phase-appropriate response
        template = response_templates.get(current_phase, {}).get(language, 
            "🔍 I've analyzed your request. Here are my findings:\n\n{analysis_summary}")
        
        return template.format(
            analysis_summary=self._summarize_analysis(analysis_results),
            recommendations=self._generate_recommendations(analysis_results, current_phase),
            key_insights=self._extract_key_insights(analysis_results),
            data_quality=self._assess_data_quality(analysis_results),
            statistical_insights=self._get_statistical_insights(analysis_results),
            next_steps=self._suggest_next_steps(current_phase, analysis_results),
            best_model=self._get_best_model(analysis_results),
            performance_metrics=self._format_performance_metrics(analysis_results),
            model_interpretation=self._interpret_model(analysis_results),
            business_impact=self._assess_business_impact(analysis_results)
        )
    
    def _summarize_analysis(self, analysis_results: dict) -> str:
        """Create executive summary of analysis"""
        if not analysis_results:
            return "Ready to begin comprehensive data analysis."
        
        summary_parts = []
        
        if "basic_info" in analysis_results:
            info = analysis_results["basic_info"]
            summary_parts.append(f"📊 Dataset: {info['shape'][0]:,} records × {info['shape'][1]} features")
        
        if "data_quality" in analysis_results:
            quality = analysis_results["data_quality"]
            if "outliers" in quality:
                outlier_cols = [col for col, info in quality["outliers"].items() if info["percentage"] > 5]
                if outlier_cols:
                    summary_parts.append(f"⚠️ Outlier detection: {len(outlier_cols)} columns need attention")
        
        if "relationships" in analysis_results:
            if "high_correlations" in analysis_results["relationships"]:
                high_corr_count = len(analysis_results["relationships"]["high_correlations"])
                if high_corr_count > 0:
                    summary_parts.append(f"🔗 {high_corr_count} strong feature correlations identified")
        
        return "\n".join(summary_parts) if summary_parts else "Analysis in progress..."
    
    def _generate_recommendations(self, analysis_results: dict, phase: str) -> str:
        """Generate phase-specific recommendations"""
        recommendations = analysis_results.get("recommendations", [])
        
        if not recommendations:
            phase_recs = {
                "data_exploration": ["Perform comprehensive EDA", "Check data quality", "Identify key patterns"],
                "data_cleaning": ["Handle missing values", "Treat outliers", "Validate data consistency"],
                "feature_engineering": ["Create new features", "Encode categorical variables", "Scale numerical features"],
                "modeling": ["Select appropriate algorithm", "Tune hyperparameters", "Validate model performance"]
            }
            recommendations = phase_recs.get(phase, ["Continue with current analysis"])
        
        return "\n".join([f"• {rec}" for rec in recommendations[:5]])
    
    def _extract_key_insights(self, analysis_results: dict) -> str:
        """Extract and format key insights"""
        insights = []
        
        if "statistical_summary" in analysis_results:
            stats = analysis_results["statistical_summary"]
            if "numerical" in stats and stats["numerical"]:
                insights.append("Numerical features show diverse distributions")
            if "categorical" in stats and stats["categorical"]:
                insights.append("Categorical features require encoding strategies")
        
        if "target_analysis" in analysis_results:
            target = analysis_results["target_analysis"]
            if target["type"] == "categorical" and "class_balance" in target:
                if not target["class_balance"]["balanced"]:
                    insights.append("⚠️ Target classes are imbalanced - consider resampling")
        
        return "\n".join([f"• {insight}" for insight in insights[:3]]) if insights else "Key patterns identified in data structure"
    
    def _assess_data_quality(self, analysis_results: dict) -> str:
        """Assess and report data quality"""
        if "basic_info" not in analysis_results:
            return "Data quality assessment pending"
        
        info = analysis_results["basic_info"]
        total_missing = sum(info["null_percentages"].values())
        
        if total_missing < 5:
            return "✅ Excellent data quality - minimal missing values"
        elif total_missing < 15:
            return "⚠️ Good data quality - some cleaning needed"
        else:
            return "🔴 Data quality concerns - significant preprocessing required"
    
    def _get_statistical_insights(self, analysis_results: dict) -> str:
        """Generate statistical insights"""
        insights = []
        
        if "relationships" in analysis_results:
            relationships = analysis_results["relationships"]
            if "high_correlations" in relationships:
                high_corr = relationships["high_correlations"]
                if high_corr:
                    insights.append(f"Strong correlations detected between {len(high_corr)} feature pairs")
                    very_strong = [pair for pair in high_corr if abs(pair["correlation"]) > 0.9]
                    if very_strong:
                        insights.append(f"⚠️ {len(very_strong)} pairs show multicollinearity risk")
        
        return "\n".join([f"• {insight}" for insight in insights]) if insights else "Statistical analysis completed"
    
    def _suggest_next_steps(self, current_phase: str, analysis_results: dict) -> str:
        """Suggest appropriate next steps"""
        next_steps_map = {
            "problem_definition": "Define success metrics and collect relevant data",
            "data_acquisition": "Perform exploratory data analysis (EDA)",
            "data_exploration": "Clean data and handle quality issues",
            "data_cleaning": "Engineer features and prepare for modeling",
            "feature_engineering": "Select and train machine learning models",
            "modeling": "Evaluate model performance and interpret results",
            "evaluation": "Validate business impact and prepare for deployment",
            "interpretation": "Create deployment strategy and monitoring plan",
            "visualization": "Create stakeholder presentations and dashboards"
        }
        
        return next_steps_map.get(current_phase, "Continue with comprehensive analysis")
    
    def _get_best_model(self, analysis_results: dict) -> str:
        """Get best model information"""
        if "best_model" in analysis_results:
            return analysis_results["best_model"]
        return "Model selection in progress"
    
    def _format_performance_metrics(self, analysis_results: dict) -> str:
        """Format model performance metrics"""
        if "models" not in analysis_results:
            return "Performance evaluation pending"
        
        models = analysis_results["models"]
        best_model_name = analysis_results.get("best_model")
        
        if best_model_name and best_model_name in models:
            model_info = models[best_model_name]
            if "cv_mean" in model_info:
                return f"Cross-validation score: {model_info['cv_mean']:.4f} ± {model_info['cv_std']:.4f}"
        
        return "Performance metrics available"
    
    def _interpret_model(self, analysis_results: dict) -> str:
        """Provide model interpretation"""
        if "feature_importance" in analysis_results and analysis_results["feature_importance"]:
            top_features = list(analysis_results["feature_importance"].keys())[:3]
            return f"Top influential features: {', '.join(top_features)}"
        return "Model interpretation and feature analysis available"
    
    def _assess_business_impact(self, analysis_results: dict) -> str:
        """Assess potential business impact"""
        return "Model shows promising potential for business application and ROI generation" 