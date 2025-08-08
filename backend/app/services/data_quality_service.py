"""
DataSoph AI - Advanced Data Quality Assessment Service
Automatic data quality detection, analysis, and cleaning recommendations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path
import json

# Statistical analysis
import scipy.stats as stats
from scipy import stats as scipy_stats

logger = logging.getLogger(__name__)

class DataQualityService:
    """Advanced data quality assessment and cleaning recommendations"""
    
    def __init__(self):
        self.quality_thresholds = {
            'missing_data_critical': 0.5,  # 50% missing is critical
            'missing_data_warning': 0.2,   # 20% missing is warning
            'outlier_threshold': 3.0,      # Z-score threshold for outliers
            'unique_ratio_threshold': 0.95, # High cardinality threshold
            'constant_threshold': 0.99,    # Nearly constant values
            'duplicate_threshold': 0.1     # 10% duplicates is concerning
        }
    
    def assess_data_quality(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        try:
            # Load data
            df = self._load_data(file_path)
            if df is None:
                return {"error": "Could not load data"}
            
            assessment = {
                "overall_score": 0,
                "issues": [],
                "recommendations": [],
                "detailed_analysis": {}
            }
            
            # 1. Missing Data Analysis
            missing_analysis = self._analyze_missing_data(df)
            assessment["detailed_analysis"]["missing_data"] = missing_analysis
            
            # 2. Duplicate Records Analysis
            duplicate_analysis = self._analyze_duplicates(df)
            assessment["detailed_analysis"]["duplicates"] = duplicate_analysis
            
            # 3. Data Type Issues
            dtype_analysis = self._analyze_data_types(df)
            assessment["detailed_analysis"]["data_types"] = dtype_analysis
            
            # 4. Outlier Detection
            outlier_analysis = self._analyze_outliers(df)
            assessment["detailed_analysis"]["outliers"] = outlier_analysis
            
            # 5. Data Consistency
            consistency_analysis = self._analyze_consistency(df)
            assessment["detailed_analysis"]["consistency"] = consistency_analysis
            
            # 6. Data Distribution Analysis
            distribution_analysis = self._analyze_distributions(df)
            assessment["detailed_analysis"]["distributions"] = distribution_analysis
            
            # 7. Calculate overall quality score
            assessment["overall_score"] = self._calculate_quality_score(assessment["detailed_analysis"])
            
            # 8. Generate issues and recommendations
            assessment["issues"] = self._generate_issues(assessment["detailed_analysis"])
            assessment["recommendations"] = self._generate_recommendations(assessment["detailed_analysis"])
            
            return assessment
            
        except Exception as e:
            logger.error(f"Data quality assessment error: {e}")
            return {"error": f"Assessment failed: {str(e)}"}
    
    def generate_cleaning_code(self, file_path: str) -> Dict[str, Any]:
        """Generate Python code for data cleaning based on quality assessment"""
        try:
            assessment = self.assess_data_quality(file_path)
            
            if "error" in assessment:
                return assessment
            
            cleaning_code = []
            cleaning_code.append("# DataSoph AI - Automated Data Cleaning Script")
            cleaning_code.append("import pandas as pd")
            cleaning_code.append("import numpy as np")
            cleaning_code.append("from scipy import stats")
            cleaning_code.append("")
            cleaning_code.append("# Load data")
            cleaning_code.append(f"df = pd.read_csv('{file_path}')  # Adjust file loading as needed")
            cleaning_code.append("original_shape = df.shape")
            cleaning_code.append("print(f'Original data shape: {original_shape}')")
            cleaning_code.append("")
            
            # Generate cleaning code based on issues
            detailed_analysis = assessment["detailed_analysis"]
            
            # Handle missing data
            if detailed_analysis.get("missing_data", {}).get("has_missing", False):
                cleaning_code.extend(self._generate_missing_data_code(detailed_analysis["missing_data"]))
            
            # Handle duplicates
            if detailed_analysis.get("duplicates", {}).get("has_duplicates", False):
                cleaning_code.extend(self._generate_duplicate_removal_code(detailed_analysis["duplicates"]))
            
            # Handle outliers
            if detailed_analysis.get("outliers", {}).get("has_outliers", False):
                cleaning_code.extend(self._generate_outlier_handling_code(detailed_analysis["outliers"]))
            
            # Handle data type issues
            if detailed_analysis.get("data_types", {}).get("has_issues", False):
                cleaning_code.extend(self._generate_dtype_correction_code(detailed_analysis["data_types"]))
            
            cleaning_code.append("")
            cleaning_code.append("# Final summary")
            cleaning_code.append("cleaned_shape = df.shape")
            cleaning_code.append("print(f'Cleaned data shape: {cleaned_shape}')")
            cleaning_code.append("print(f'Rows removed: {original_shape[0] - cleaned_shape[0]}')")
            cleaning_code.append("")
            cleaning_code.append("# Save cleaned data")
            cleaning_code.append("df.to_csv('cleaned_data.csv', index=False)")
            cleaning_code.append("print('Cleaned data saved as cleaned_data.csv')")
            
            return {
                "status": "success",
                "cleaning_code": "\n".join(cleaning_code),
                "summary": f"Generated {len(cleaning_code)} lines of cleaning code",
                "issues_addressed": len(assessment["issues"])
            }
            
        except Exception as e:
            logger.error(f"Cleaning code generation error: {e}")
            return {"error": f"Code generation failed: {str(e)}"}
    
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
    
    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns"""
        missing_count = df.isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        analysis = {
            "has_missing": missing_count.sum() > 0,
            "total_missing": int(missing_count.sum()),
            "missing_percentage": float(missing_pct.sum() / len(df.columns)),
            "columns_with_missing": []
        }
        
        for col in df.columns:
            if missing_count[col] > 0:
                severity = "critical" if missing_pct[col] > self.quality_thresholds['missing_data_critical'] * 100 else \
                          "warning" if missing_pct[col] > self.quality_thresholds['missing_data_warning'] * 100 else "minor"
                
                analysis["columns_with_missing"].append({
                    "column": col,
                    "missing_count": int(missing_count[col]),
                    "missing_percentage": float(missing_pct[col]),
                    "severity": severity,
                    "data_type": str(df[col].dtype)
                })
        
        return analysis
    
    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze duplicate records"""
        duplicate_count = df.duplicated().sum()
        duplicate_pct = (duplicate_count / len(df)) * 100
        
        analysis = {
            "has_duplicates": duplicate_count > 0,
            "duplicate_count": int(duplicate_count),
            "duplicate_percentage": float(duplicate_pct),
            "severity": "critical" if duplicate_pct > self.quality_thresholds['duplicate_threshold'] * 100 else "minor"
        }
        
        return analysis
    
    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data type issues"""
        issues = []
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) == 0:
                continue
                
            # Check if numeric column stored as object
            if df[col].dtype == 'object':
                # Try to convert to numeric
                try:
                    pd.to_numeric(col_data.astype(str), errors='raise')
                    issues.append({
                        "column": col,
                        "issue": "numeric_stored_as_text",
                        "description": f"Column '{col}' contains numeric data but stored as text",
                        "severity": "warning"
                    })
                except:
                    pass
                
                # Check for date-like strings
                if col_data.astype(str).str.match(r'\d{4}-\d{2}-\d{2}').any():
                    issues.append({
                        "column": col,
                        "issue": "date_stored_as_text",
                        "description": f"Column '{col}' contains date data but stored as text",
                        "severity": "warning"
                    })
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues
        }
    
    def _analyze_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze outliers in numeric columns"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_analysis = []
        
        for col in numeric_cols:
            col_data = df[col].dropna()
            
            if len(col_data) < 10:  # Skip if too few data points
                continue
            
            # Z-score method
            z_scores = np.abs(stats.zscore(col_data))
            outliers_zscore = np.sum(z_scores > self.quality_thresholds['outlier_threshold'])
            
            # IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers_iqr = np.sum((col_data < lower_bound) | (col_data > upper_bound))
            
            if outliers_zscore > 0 or outliers_iqr > 0:
                outlier_pct = max(outliers_zscore, outliers_iqr) / len(col_data) * 100
                severity = "critical" if outlier_pct > 10 else "warning" if outlier_pct > 5 else "minor"
                
                outlier_analysis.append({
                    "column": col,
                    "outliers_zscore": int(outliers_zscore),
                    "outliers_iqr": int(outliers_iqr),
                    "outlier_percentage": float(outlier_pct),
                    "severity": severity,
                    "bounds": {
                        "lower_iqr": float(lower_bound),
                        "upper_iqr": float(upper_bound),
                        "q1": float(Q1),
                        "q3": float(Q3)
                    }
                })
        
        return {
            "has_outliers": len(outlier_analysis) > 0,
            "outlier_columns": outlier_analysis
        }
    
    def _analyze_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data consistency issues"""
        issues = []
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            # Check for constant/nearly constant columns
            unique_ratio = len(col_data.unique()) / len(col_data)
            if unique_ratio < (1 - self.quality_thresholds['constant_threshold']):
                issues.append({
                    "column": col,
                    "issue": "nearly_constant",
                    "description": f"Column '{col}' has very low variance",
                    "unique_ratio": float(unique_ratio),
                    "severity": "warning"
                })
            
            # Check for high cardinality in categorical columns
            if df[col].dtype == 'object' and unique_ratio > self.quality_thresholds['unique_ratio_threshold']:
                issues.append({
                    "column": col,
                    "issue": "high_cardinality",
                    "description": f"Column '{col}' has very high cardinality",
                    "unique_ratio": float(unique_ratio),
                    "severity": "warning"
                })
        
        return {
            "has_issues": len(issues) > 0,
            "issues": issues
        }
    
    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data distributions"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        distribution_analysis = []
        
        for col in numeric_cols:
            col_data = df[col].dropna()
            
            if len(col_data) < 10:
                continue
            
            # Basic statistics
            skewness = float(col_data.skew())
            kurtosis = float(col_data.kurtosis())
            
            # Normality test (if sample size is appropriate)
            if 3 <= len(col_data) <= 5000:
                try:
                    _, p_value = stats.shapiro(col_data.sample(min(5000, len(col_data))))
                    is_normal = p_value > 0.05
                except:
                    is_normal = None
                    p_value = None
            else:
                is_normal = None
                p_value = None
            
            distribution_analysis.append({
                "column": col,
                "skewness": skewness,
                "kurtosis": kurtosis,
                "is_normal": is_normal,
                "normality_p_value": float(p_value) if p_value else None,
                "mean": float(col_data.mean()),
                "median": float(col_data.median()),
                "std": float(col_data.std())
            })
        
        return {
            "numeric_distributions": distribution_analysis
        }
    
    def _calculate_quality_score(self, detailed_analysis: Dict[str, Any]) -> float:
        """Calculate overall data quality score (0-100)"""
        score = 100.0
        
        # Missing data penalty
        missing_analysis = detailed_analysis.get("missing_data", {})
        if missing_analysis.get("has_missing", False):
            missing_pct = missing_analysis.get("missing_percentage", 0)
            score -= min(50, missing_pct * 2)  # Max 50 point penalty
        
        # Duplicate penalty
        duplicate_analysis = detailed_analysis.get("duplicates", {})
        if duplicate_analysis.get("has_duplicates", False):
            duplicate_pct = duplicate_analysis.get("duplicate_percentage", 0)
            score -= min(30, duplicate_pct * 3)  # Max 30 point penalty
        
        # Data type issues penalty
        dtype_analysis = detailed_analysis.get("data_types", {})
        if dtype_analysis.get("has_issues", False):
            score -= len(dtype_analysis.get("issues", [])) * 5  # 5 points per issue
        
        # Outlier penalty
        outlier_analysis = detailed_analysis.get("outliers", {})
        if outlier_analysis.get("has_outliers", False):
            outlier_columns = outlier_analysis.get("outlier_columns", [])
            for col_info in outlier_columns:
                if col_info["severity"] == "critical":
                    score -= 15
                elif col_info["severity"] == "warning":
                    score -= 10
                else:
                    score -= 5
        
        # Consistency issues penalty
        consistency_analysis = detailed_analysis.get("consistency", {})
        if consistency_analysis.get("has_issues", False):
            score -= len(consistency_analysis.get("issues", [])) * 5
        
        return max(0.0, min(100.0, score))
    
    def _generate_issues(self, detailed_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate list of data quality issues"""
        issues = []
        
        # Missing data issues
        missing_analysis = detailed_analysis.get("missing_data", {})
        for col_info in missing_analysis.get("columns_with_missing", []):
            issues.append({
                "type": "missing_data",
                "severity": col_info["severity"],
                "description": f"Column '{col_info['column']}' has {col_info['missing_percentage']:.1f}% missing values",
                "column": col_info["column"]
            })
        
        # Duplicate issues
        duplicate_analysis = detailed_analysis.get("duplicates", {})
        if duplicate_analysis.get("has_duplicates", False):
            issues.append({
                "type": "duplicates",
                "severity": duplicate_analysis["severity"],
                "description": f"Dataset contains {duplicate_analysis['duplicate_count']} duplicate rows ({duplicate_analysis['duplicate_percentage']:.1f}%)",
                "column": None
            })
        
        # Data type issues
        dtype_analysis = detailed_analysis.get("data_types", {})
        for issue in dtype_analysis.get("issues", []):
            issues.append({
                "type": "data_type",
                "severity": issue["severity"],
                "description": issue["description"],
                "column": issue["column"]
            })
        
        # Outlier issues
        outlier_analysis = detailed_analysis.get("outliers", {})
        for col_info in outlier_analysis.get("outlier_columns", []):
            issues.append({
                "type": "outliers",
                "severity": col_info["severity"],
                "description": f"Column '{col_info['column']}' has {col_info['outlier_percentage']:.1f}% outlier values",
                "column": col_info["column"]
            })
        
        return issues
    
    def _generate_recommendations(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Missing data recommendations
        missing_analysis = detailed_analysis.get("missing_data", {})
        if missing_analysis.get("has_missing", False):
            recommendations.append("🔧 Handle missing data: Consider imputation methods or removal of rows/columns with excessive missing values")
            
            for col_info in missing_analysis.get("columns_with_missing", []):
                if col_info["severity"] == "critical":
                    recommendations.append(f"❌ Consider removing column '{col_info['column']}' due to {col_info['missing_percentage']:.1f}% missing data")
                elif col_info["data_type"] in ["int64", "float64"]:
                    recommendations.append(f"📊 For numeric column '{col_info['column']}': Use mean/median imputation or interpolation")
                else:
                    recommendations.append(f"🏷️ For categorical column '{col_info['column']}': Use mode imputation or create 'Unknown' category")
        
        # Duplicate recommendations
        duplicate_analysis = detailed_analysis.get("duplicates", {})
        if duplicate_analysis.get("has_duplicates", False):
            recommendations.append(f"🔄 Remove {duplicate_analysis['duplicate_count']} duplicate rows to improve data quality")
        
        # Data type recommendations
        dtype_analysis = detailed_analysis.get("data_types", {})
        for issue in dtype_analysis.get("issues", []):
            if issue["issue"] == "numeric_stored_as_text":
                recommendations.append(f"🔢 Convert column '{issue['column']}' to numeric type for better analysis")
            elif issue["issue"] == "date_stored_as_text":
                recommendations.append(f"📅 Convert column '{issue['column']}' to datetime type for time-based analysis")
        
        # Outlier recommendations
        outlier_analysis = detailed_analysis.get("outliers", {})
        for col_info in outlier_analysis.get("outlier_columns", []):
            if col_info["severity"] == "critical":
                recommendations.append(f"⚠️ Investigate outliers in '{col_info['column']}' - consider capping, transformation, or removal")
            else:
                recommendations.append(f"📈 Monitor outliers in '{col_info['column']}' - may indicate important data patterns")
        
        # General recommendations
        if not recommendations:
            recommendations.append("✅ Data quality looks good! Ready for analysis and modeling")
        else:
            recommendations.append("🚀 After cleaning, your data will be ready for advanced ML models and analysis")
        
        return recommendations
    
    def _generate_missing_data_code(self, missing_analysis: Dict[str, Any]) -> List[str]:
        """Generate code for handling missing data"""
        code = []
        code.append("# Handle missing data")
        
        for col_info in missing_analysis.get("columns_with_missing", []):
            col = col_info["column"]
            severity = col_info["severity"]
            data_type = col_info["data_type"]
            
            if severity == "critical":
                code.append(f"# Remove column '{col}' due to excessive missing data")
                code.append(f"df = df.drop(columns=['{col}'])")
            elif data_type in ["int64", "float64"]:
                code.append(f"# Impute missing values in numeric column '{col}' with median")
                code.append(f"df['{col}'].fillna(df['{col}'].median(), inplace=True)")
            else:
                code.append(f"# Impute missing values in categorical column '{col}' with mode")
                code.append(f"df['{col}'].fillna(df['{col}'].mode()[0], inplace=True)")
        
        code.append("")
        return code
    
    def _generate_duplicate_removal_code(self, duplicate_analysis: Dict[str, Any]) -> List[str]:
        """Generate code for removing duplicates"""
        code = []
        code.append("# Remove duplicate rows")
        code.append("df = df.drop_duplicates()")
        code.append(f"print(f'Removed {duplicate_analysis['duplicate_count']} duplicate rows')")
        code.append("")
        return code
    
    def _generate_outlier_handling_code(self, outlier_analysis: Dict[str, Any]) -> List[str]:
        """Generate code for handling outliers"""
        code = []
        code.append("# Handle outliers using IQR method")
        
        for col_info in outlier_analysis.get("outlier_columns", []):
            col = col_info["column"]
            bounds = col_info["bounds"]
            
            code.append(f"# Cap outliers in '{col}'")
            code.append(f"df['{col}'] = np.clip(df['{col}'], {bounds['lower_iqr']:.2f}, {bounds['upper_iqr']:.2f})")
        
        code.append("")
        return code
    
    def _generate_dtype_correction_code(self, dtype_analysis: Dict[str, Any]) -> List[str]:
        """Generate code for correcting data types"""
        code = []
        code.append("# Correct data types")
        
        for issue in dtype_analysis.get("issues", []):
            col = issue["column"]
            issue_type = issue["issue"]
            
            if issue_type == "numeric_stored_as_text":
                code.append(f"# Convert '{col}' to numeric")
                code.append(f"df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce')")
            elif issue_type == "date_stored_as_text":
                code.append(f"# Convert '{col}' to datetime")
                code.append(f"df['{col}'] = pd.to_datetime(df['{col}'], errors='coerce')")
        
        code.append("")
        return code

# Global data quality service instance
data_quality_service = DataQualityService() 