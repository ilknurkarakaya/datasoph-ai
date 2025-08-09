"""
DataSoph AI - Comprehensive Data Science Engine
World-class data science capabilities with full ML/AI stack
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
import warnings
from datetime import datetime
import json
import io
import base64

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class ComprehensiveDataScienceEngine:
    """
    Complete data science engine with advanced analytics capabilities
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        self.model_registry = {}
        
        # Initialize plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        self.logger.info("🚀 Comprehensive Data Science Engine initialized")

    def comprehensive_eda(self, df: pd.DataFrame, target_column: str = None) -> Dict[str, Any]:
        """
        Generate comprehensive Exploratory Data Analysis
        """
        try:
            eda_results = {
                'basic_info': self._get_basic_info(df),
                'data_quality': self._assess_data_quality(df),
                'statistical_summary': self._get_statistical_summary(df),
                'correlations': self._analyze_correlations(df),
                'missing_values': self._analyze_missing_values(df),
                'categorical_analysis': self._analyze_categorical_variables(df),
                'numerical_analysis': self._analyze_numerical_variables(df),
                'outlier_detection': self._detect_outliers(df),
                'data_distribution': self._analyze_distributions(df),
                'recommendations': self._generate_recommendations(df, target_column)
            }
            
            self.logger.info(f"✅ Comprehensive EDA completed for {df.shape[0]}x{df.shape[1]} dataset")
            return eda_results
            
        except Exception as e:
            self.logger.error(f"❌ EDA error: {e}")
            return {'error': str(e)}

    def _get_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic dataset information"""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': df.duplicated().sum(),
            'total_missing': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        }

    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        quality_score = 100
        issues = []
        
        # Check missing values
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        if missing_pct > 20:
            quality_score -= 25
            issues.append(f"High missing values: {missing_pct:.1f}%")
        elif missing_pct > 10:
            quality_score -= 15
            issues.append(f"Moderate missing values: {missing_pct:.1f}%")
        
        # Check duplicates
        duplicate_pct = (df.duplicated().sum() / len(df)) * 100
        if duplicate_pct > 10:
            quality_score -= 20
            issues.append(f"High duplicate rows: {duplicate_pct:.1f}%")
        
        # Check data consistency
        for col in df.select_dtypes(include=['object']):
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio > 0.95 and len(df) > 100:  # Might be ID column
                issues.append(f"Column '{col}' appears to be an identifier (95%+ unique values)")
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues,
            'recommendations': self._generate_quality_recommendations(issues)
        }

    def _get_statistical_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Enhanced statistical summary"""
        numeric_df = df.select_dtypes(include=[np.number])
        categorical_df = df.select_dtypes(include=['object', 'category'])
        
        summary = {
            'numeric_summary': numeric_df.describe().to_dict() if not numeric_df.empty else {},
            'categorical_summary': {},
            'advanced_stats': {}
        }
        
        # Categorical summary
        for col in categorical_df.columns:
            summary['categorical_summary'][col] = {
                'unique_count': df[col].nunique(),
                'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'frequency': df[col].value_counts().head().to_dict()
            }
        
        # Advanced statistics for numeric columns
        for col in numeric_df.columns:
            try:
                from scipy import stats
                data = numeric_df[col].dropna()
                
                summary['advanced_stats'][col] = {
                    'skewness': stats.skew(data),
                    'kurtosis': stats.kurtosis(data),
                    'normality_test': stats.normaltest(data).pvalue if len(data) > 8 else None,
                    'outlier_count': len(self._detect_outliers_zscore(data))
                }
            except ImportError:
                # Fallback if scipy not available
                data = numeric_df[col].dropna()
                mean = data.mean()
                std = data.std()
                summary['advanced_stats'][col] = {
                    'coefficient_variation': (std / mean) * 100 if mean != 0 else 0,
                    'outlier_count': len(data[(data < mean - 3*std) | (data > mean + 3*std)])
                }
        
        return summary

    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive correlation analysis"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {'message': 'Not enough numeric columns for correlation analysis'}
        
        # Pearson correlation
        pearson_corr = numeric_df.corr()
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(pearson_corr.columns)):
            for j in range(i+1, len(pearson_corr.columns)):
                corr_value = pearson_corr.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': pearson_corr.columns[i],
                        'var2': pearson_corr.columns[j],
                        'correlation': corr_value,
                        'strength': 'Very Strong' if abs(corr_value) > 0.9 else 'Strong'
                    })
        
        return {
            'correlation_matrix': pearson_corr.to_dict(),
            'strong_correlations': strong_correlations,
            'multicollinearity_warning': len([c for c in strong_correlations if abs(c['correlation']) > 0.9]) > 0
        }

    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detailed missing value analysis"""
        missing_info = {}
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                missing_info[col] = {
                    'count': int(missing_count),
                    'percentage': (missing_count / len(df)) * 100,
                    'pattern': self._analyze_missing_pattern(df, col)
                }
        
        # Missing value patterns
        missing_patterns = df.isnull().groupby(df.isnull().columns.tolist()).size().to_dict()
        
        return {
            'missing_by_column': missing_info,
            'missing_patterns': missing_patterns,
            'recommendation': self._recommend_missing_strategy(missing_info)
        }

    def _analyze_missing_pattern(self, df: pd.DataFrame, column: str) -> str:
        """Analyze missing value patterns"""
        missing_mask = df[column].isnull()
        
        if missing_mask.sum() == 0:
            return "No missing values"
        
        # Check if missing values are random
        if len(df) > 100:
            # Simple pattern detection
            consecutive_missing = 0
            max_consecutive = 0
            
            for i, is_missing in enumerate(missing_mask):
                if is_missing:
                    consecutive_missing += 1
                    max_consecutive = max(max_consecutive, consecutive_missing)
                else:
                    consecutive_missing = 0
            
            if max_consecutive > 10:
                return "Consecutive missing blocks detected"
            elif missing_mask.iloc[:len(missing_mask)//4].sum() > missing_mask.iloc[-len(missing_mask)//4:].sum() * 2:
                return "More missing values at beginning"
            elif missing_mask.iloc[-len(missing_mask)//4:].sum() > missing_mask.iloc[:len(missing_mask)//4].sum() * 2:
                return "More missing values at end"
            else:
                return "Randomly distributed"
        
        return "Pattern analysis needs more data"

    def _analyze_categorical_variables(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive categorical variable analysis"""
        categorical_df = df.select_dtypes(include=['object', 'category'])
        analysis = {}
        
        for col in categorical_df.columns:
            value_counts = df[col].value_counts()
            
            analysis[col] = {
                'unique_count': df[col].nunique(),
                'most_frequent': value_counts.index[0] if not value_counts.empty else None,
                'most_frequent_count': value_counts.iloc[0] if not value_counts.empty else 0,
                'frequency_distribution': value_counts.head(10).to_dict(),
                'cardinality_level': self._assess_cardinality(df[col]),
                'encoding_recommendation': self._recommend_encoding(df[col])
            }
        
        return analysis

    def _analyze_numerical_variables(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Advanced numerical variable analysis"""
        numeric_df = df.select_dtypes(include=[np.number])
        analysis = {}
        
        for col in numeric_df.columns:
            data = numeric_df[col].dropna()
            
            if len(data) == 0:
                continue
                
            analysis[col] = {
                'distribution_type': self._identify_distribution(data),
                'outlier_count': len(self._detect_outliers_zscore(data)),
                'transformation_suggestion': self._suggest_transformation(data),
                'business_interpretation': self._interpret_numeric_variable(col, data)
            }
        
        return analysis

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Multiple outlier detection methods"""
        numeric_df = df.select_dtypes(include=[np.number])
        outliers = {}
        
        for col in numeric_df.columns:
            data = numeric_df[col].dropna()
            if len(data) == 0:
                continue
                
            # Z-score method
            z_score_outliers = self._detect_outliers_zscore(data)
            
            # IQR method
            iqr_outliers = self._detect_outliers_iqr(data)
            
            outliers[col] = {
                'z_score_outliers': len(z_score_outliers),
                'iqr_outliers': len(iqr_outliers),
                'outlier_percentage': (len(set(z_score_outliers) | set(iqr_outliers)) / len(data)) * 100,
                'recommendation': self._recommend_outlier_treatment(col, len(z_score_outliers), len(iqr_outliers), len(data))
            }
        
        return outliers

    def _detect_outliers_zscore(self, data: pd.Series, threshold: float = 3) -> List[int]:
        """Detect outliers using Z-score method"""
        if len(data) == 0 or data.std() == 0:
            return []
        
        z_scores = np.abs((data - data.mean()) / data.std())
        return data[z_scores > threshold].index.tolist()

    def _detect_outliers_iqr(self, data: pd.Series) -> List[int]:
        """Detect outliers using IQR method"""
        if len(data) == 0:
            return []
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return data[(data < lower_bound) | (data > upper_bound)].index.tolist()

    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data distributions"""
        numeric_df = df.select_dtypes(include=[np.number])
        distributions = {}
        
        for col in numeric_df.columns:
            data = numeric_df[col].dropna()
            if len(data) == 0:
                continue
                
            distributions[col] = {
                'distribution_type': self._identify_distribution(data),
                'skewness': data.skew(),
                'kurtosis': data.kurtosis(),
                'normality_assessment': self._assess_normality(data)
            }
        
        return distributions

    def _identify_distribution(self, data: pd.Series) -> str:
        """Identify the likely distribution type"""
        skewness = data.skew()
        kurtosis = data.kurtosis()
        
        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return "Normal"
        elif skewness > 1:
            return "Right-skewed"
        elif skewness < -1:
            return "Left-skewed"
        elif kurtosis > 3:
            return "Heavy-tailed"
        elif kurtosis < -1:
            return "Light-tailed"
        else:
            return "Moderate skew"

    def _assess_normality(self, data: pd.Series) -> str:
        """Assess if data follows normal distribution"""
        try:
            from scipy import stats
            if len(data) > 5000:
                # Use smaller sample for large datasets
                sample_data = data.sample(5000, random_state=42)
            else:
                sample_data = data
            
            statistic, p_value = stats.normaltest(sample_data)
            
            if p_value > 0.05:
                return "Likely normal distribution"
            else:
                return "Not normally distributed"
        except ImportError:
            # Fallback without scipy
            skewness = abs(data.skew())
            kurtosis = abs(data.kurtosis())
            
            if skewness < 0.5 and kurtosis < 1:
                return "Approximately normal"
            else:
                return "Not normally distributed"

    def create_advanced_visualizations(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create advanced visualizations based on data analysis
        """
        visualizations = {}
        
        try:
            # 1. Correlation heatmap
            if 'correlations' in analysis_results and 'correlation_matrix' in analysis_results['correlations']:
                corr_matrix = pd.DataFrame(analysis_results['correlations']['correlation_matrix'])
                if not corr_matrix.empty:
                    visualizations['correlation_heatmap'] = self._create_correlation_heatmap(corr_matrix)
            
            # 2. Missing value heatmap
            if df.isnull().sum().sum() > 0:
                visualizations['missing_values_heatmap'] = self._create_missing_heatmap(df)
            
            # 3. Distribution plots
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                visualizations['distribution_plots'] = self._create_distribution_plots(df[numeric_cols])
            
            # 4. Outlier visualization
            if len(numeric_cols) > 0:
                visualizations['outlier_boxplots'] = self._create_outlier_plots(df[numeric_cols])
            
            # 5. Categorical analysis
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                visualizations['categorical_plots'] = self._create_categorical_plots(df[categorical_cols])
            
            self.logger.info(f"✅ Created {len(visualizations)} visualizations")
            return visualizations
            
        except Exception as e:
            self.logger.error(f"❌ Visualization error: {e}")
            return {'error': str(e)}

    def _create_correlation_heatmap(self, corr_matrix: pd.DataFrame) -> str:
        """Create correlation heatmap"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Convert to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    def _create_missing_heatmap(self, df: pd.DataFrame) -> str:
        """Create missing values heatmap"""
        plt.figure(figsize=(12, 6))
        missing_matrix = df.isnull()
        sns.heatmap(missing_matrix, yticklabels=False, cbar=True, cmap='viridis')
        plt.title('Missing Values Pattern', fontsize=16, fontweight='bold')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    def _create_distribution_plots(self, numeric_df: pd.DataFrame) -> str:
        """Create distribution plots for numeric variables"""
        n_cols = min(3, len(numeric_df.columns))
        n_rows = (len(numeric_df.columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(numeric_df.columns):
            if i < len(axes):
                numeric_df[col].hist(ax=axes[i], bins=30, alpha=0.7, edgecolor='black')
                axes[i].set_title(f'Distribution of {col}', fontweight='bold')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frequency')
        
        # Hide unused subplots
        for i in range(len(numeric_df.columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    def _create_outlier_plots(self, numeric_df: pd.DataFrame) -> str:
        """Create box plots for outlier detection"""
        n_cols = min(3, len(numeric_df.columns))
        n_rows = (len(numeric_df.columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(numeric_df.columns):
            if i < len(axes):
                numeric_df[col].plot(kind='box', ax=axes[i])
                axes[i].set_title(f'Outliers in {col}', fontweight='bold')
                axes[i].set_ylabel(col)
        
        # Hide unused subplots
        for i in range(len(numeric_df.columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    def _create_categorical_plots(self, categorical_df: pd.DataFrame) -> str:
        """Create plots for categorical variables"""
        n_cols = min(2, len(categorical_df.columns))
        n_rows = (len(categorical_df.columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 5*n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(categorical_df.columns):
            if i < len(axes):
                value_counts = categorical_df[col].value_counts().head(10)
                value_counts.plot(kind='bar', ax=axes[i])
                axes[i].set_title(f'Frequency of {col}', fontweight='bold')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Count')
                axes[i].tick_params(axis='x', rotation=45)
        
        # Hide unused subplots
        for i in range(len(categorical_df.columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    # Helper methods for recommendations
    def _generate_recommendations(self, df: pd.DataFrame, target_column: str = None) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Data quality recommendations
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        if missing_pct > 10:
            recommendations.append(f"Address missing values ({missing_pct:.1f}% of data)")
        
        # Duplicate handling
        if df.duplicated().sum() > 0:
            recommendations.append(f"Remove {df.duplicated().sum()} duplicate rows")
        
        # Feature engineering suggestions
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            recommendations.append("Extract time-based features from date columns")
        
        # ML preparation
        if target_column:
            if target_column in df.columns:
                if df[target_column].dtype in ['object', 'category']:
                    recommendations.append("Consider classification algorithms for categorical target")
                else:
                    recommendations.append("Consider regression algorithms for numerical target")
        
        return recommendations

    def _generate_quality_recommendations(self, issues: List[str]) -> List[str]:
        """Generate data quality improvement recommendations"""
        recommendations = []
        
        for issue in issues:
            if "missing values" in issue.lower():
                recommendations.append("Implement missing value imputation strategy")
            elif "duplicate" in issue.lower():
                recommendations.append("Remove duplicate records")
            elif "identifier" in issue.lower():
                recommendations.append("Consider removing ID columns for analysis")
        
        return recommendations

    def _recommend_missing_strategy(self, missing_info: Dict[str, Any]) -> List[str]:
        """Recommend missing value handling strategies"""
        strategies = []
        
        for col, info in missing_info.items():
            pct = info['percentage']
            if pct > 50:
                strategies.append(f"Consider dropping column '{col}' (>{pct:.1f}% missing)")
            elif pct > 20:
                strategies.append(f"Use advanced imputation for '{col}' ({pct:.1f}% missing)")
            else:
                strategies.append(f"Simple imputation suitable for '{col}' ({pct:.1f}% missing)")
        
        return strategies

    def _assess_cardinality(self, series: pd.Series) -> str:
        """Assess cardinality level of categorical variable"""
        unique_ratio = series.nunique() / len(series)
        
        if unique_ratio > 0.9:
            return "Very High (likely identifier)"
        elif unique_ratio > 0.5:
            return "High"
        elif unique_ratio > 0.1:
            return "Medium"
        else:
            return "Low"

    def _recommend_encoding(self, series: pd.Series) -> str:
        """Recommend encoding strategy for categorical variable"""
        unique_count = series.nunique()
        
        if unique_count == 2:
            return "Binary encoding (0/1)"
        elif unique_count <= 10:
            return "One-hot encoding"
        elif unique_count <= 50:
            return "Target encoding or label encoding"
        else:
            return "Consider feature hashing or dimensionality reduction"

    def _suggest_transformation(self, data: pd.Series) -> str:
        """Suggest transformation for numerical variable"""
        skewness = abs(data.skew())
        
        if skewness > 2:
            return "Log transformation recommended"
        elif skewness > 1:
            return "Square root transformation might help"
        elif data.min() >= 0 and data.std() / data.mean() > 1:
            return "Consider standardization or normalization"
        else:
            return "No transformation needed"

    def _interpret_numeric_variable(self, col_name: str, data: pd.Series) -> str:
        """Provide business interpretation of numeric variable"""
        col_lower = col_name.lower()
        
        if any(word in col_lower for word in ['price', 'cost', 'amount', 'revenue', 'salary']):
            return "Financial metric - consider inflation adjustment if historical"
        elif any(word in col_lower for word in ['age', 'year', 'time']):
            return "Temporal variable - may need age grouping or time-based features"
        elif any(word in col_lower for word in ['score', 'rating', 'percent']):
            return "Performance metric - useful for segmentation and targeting"
        elif any(word in col_lower for word in ['count', 'number', 'quantity']):
            return "Count variable - might follow Poisson distribution"
        else:
            return "Continuous variable - check distribution and outliers"

    def _recommend_outlier_treatment(self, col_name: str, z_outliers: int, 
                                   iqr_outliers: int, total_points: int) -> str:
        """Recommend outlier treatment strategy"""
        outlier_pct = max(z_outliers, iqr_outliers) / total_points * 100
        
        if outlier_pct > 10:
            return "High outlier percentage - investigate data collection process"
        elif outlier_pct > 5:
            return "Consider outlier transformation or robust scaling"
        elif outlier_pct > 1:
            return "Moderate outliers - consider capping or winsorization"
        else:
            return "Low outlier percentage - standard scaling appropriate" 