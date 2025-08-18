export interface CodeTemplate {
  name: string;
  description: string;
  code: string;
  language: string;
  category: 'data-analysis' | 'machine-learning' | 'visualization' | 'statistics' | 'preprocessing';
  complexity: 'beginner' | 'intermediate' | 'advanced';
  estimatedRuntime?: string;
  memoryUsage?: string;
}

export const codeTemplates: Record<string, Record<string, CodeTemplate>> = {
  python: {
    dataAnalysis: {
      name: 'Data Analysis Template',
      description: 'Comprehensive data exploration and analysis workflow',
      category: 'data-analysis',
      complexity: 'beginner',
      language: 'python',
      estimatedRuntime: '2-5 minutes',
      memoryUsage: '< 500MB',
      code: `# Data Analysis Template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load and inspect data
df = pd.read_csv('your_data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Basic information
print("\\n=== DATASET OVERVIEW ===")
print(df.info())
print("\\n=== MISSING VALUES ===")
print(df.isnull().sum())
print("\\n=== BASIC STATISTICS ===")
print(df.describe())

# Data types analysis
print("\\n=== DATA TYPES ===")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols}")
print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols}")
print(f"Datetime columns ({len(datetime_cols)}): {datetime_cols}")

# Visualization setup
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Distribution of numeric variables
if len(numeric_cols) > 0:
    df[numeric_cols].hist(bins=30, ax=axes[0,0] if len(numeric_cols) == 1 else None, figsize=(15, 10))
    axes[0,0].set_title('Distribution of Numeric Variables')

# Correlation heatmap
if len(numeric_cols) > 1:
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[0,1])
    axes[0,1].set_title('Correlation Matrix')

# Missing values heatmap
sns.heatmap(df.isnull(), yticklabels=False, cbar=True, cmap='viridis', ax=axes[1,0])
axes[1,0].set_title('Missing Values Pattern')

# Categorical variables count
if len(categorical_cols) > 0:
    top_categorical = categorical_cols[0] if categorical_cols else None
    if top_categorical:
        df[top_categorical].value_counts().head(10).plot(kind='bar', ax=axes[1,1])
        axes[1,1].set_title(f'Top 10 Values in {top_categorical}')
        axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

print("\\n=== ANALYSIS COMPLETE ===")
print("Next steps: Clean data, feature engineering, modeling")`
    },
    
    machineLearning: {
      name: 'Machine Learning Pipeline',
      description: 'Complete ML workflow with preprocessing, training, and evaluation',
      category: 'machine-learning',
      complexity: 'intermediate',
      language: 'python',
      estimatedRuntime: '5-15 minutes',
      memoryUsage: '500MB - 2GB',
      code: `# Machine Learning Pipeline Template
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('your_data.csv')
print(f"Dataset shape: {df.shape}")

# Define target variable (modify as needed)
target_column = 'target'  # Replace with your target column name
X = df.drop(target_column, axis=1)
y = df[target_column]

# Determine if it's classification or regression
is_classification = y.dtype == 'object' or y.nunique() < 20

print(f"Problem type: {'Classification' if is_classification else 'Regression'}")
print(f"Target variable: {target_column}")
print(f"Number of features: {X.shape[1]}")
print(f"Number of samples: {X.shape[0]}")

# Handle categorical variables
categorical_columns = X.select_dtypes(include=['object']).columns
if len(categorical_columns) > 0:
    print(f"\\nEncoding categorical variables: {list(categorical_columns)}")
    le = LabelEncoder()
    for col in categorical_columns:
        X[col] = le.fit_transform(X[col].astype(str))

# Handle missing values
if X.isnull().sum().sum() > 0:
    print("\\nHandling missing values...")
    X = X.fillna(X.mean())  # Simple imputation

# Encode target if classification
if is_classification and y.dtype == 'object':
    le_target = LabelEncoder()
    y = le_target.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, 
    stratify=y if is_classification else None
)

print(f"\\nTraining set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

# Create preprocessing and model pipeline
if is_classification:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    scoring = 'accuracy'
else:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    scoring = 'r2'

# Create pipeline with scaling
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', model)
])

# Cross-validation
print("\\n=== CROSS-VALIDATION ===")
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring=scoring)
print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# Fit the model
pipeline.fit(X_train, y_train)

# Make predictions
train_pred = pipeline.predict(X_train)
test_pred = pipeline.predict(X_test)

# Evaluate model
print("\\n=== MODEL EVALUATION ===")
if is_classification:
    print("Training Accuracy:", pipeline.score(X_train, y_train))
    print("Testing Accuracy:", pipeline.score(X_test, y_test))
    print("\\nClassification Report:")
    print(classification_report(y_test, test_pred))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, test_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()
else:
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    
    print(f"Training R²: {train_r2:.4f}")
    print(f"Testing R²: {test_r2:.4f}")
    print(f"Training RMSE: {train_rmse:.4f}")
    print(f"Testing RMSE: {test_rmse:.4f}")
    
    # Residual plot
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, test_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted')
    
    plt.subplot(1, 2, 2)
    residuals = y_test - test_pred
    plt.scatter(test_pred, residuals, alpha=0.6)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.tight_layout()
    plt.show()

# Feature importance
feature_importance = pipeline.named_steps['model'].feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("\\n=== TOP 10 FEATURE IMPORTANCE ===")
print(importance_df.head(10))

# Plot feature importance
plt.figure(figsize=(10, 8))
importance_df.head(15).plot(x='feature', y='importance', kind='barh')
plt.title('Top 15 Feature Importance')
plt.xlabel('Importance')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print("\\n=== MODELING COMPLETE ===")
print("Consider: hyperparameter tuning, feature selection, ensemble methods")`
    },
    
    visualization: {
      name: 'Data Visualization Suite',
      description: 'Comprehensive visualization toolkit for data exploration',
      category: 'visualization',
      complexity: 'beginner',
      language: 'python',
      estimatedRuntime: '3-8 minutes',
      memoryUsage: '< 1GB',
      code: `# Data Visualization Suite
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load data
df = pd.read_csv('your_data.csv')
print(f"Dataset shape: {df.shape}")

# Identify column types
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

print(f"Numeric columns: {len(numeric_cols)}")
print(f"Categorical columns: {len(categorical_cols)}")

# 1. UNIVARIATE ANALYSIS
print("\\n=== UNIVARIATE ANALYSIS ===")

# Histograms for numeric variables
if len(numeric_cols) > 0:
    n_numeric = len(numeric_cols)
    cols = min(3, n_numeric)
    rows = (n_numeric + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
    if rows == 1 and cols == 1:
        axes = [axes]
    elif rows == 1:
        axes = axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols[:9]):  # Limit to 9 plots
        if i < len(axes):
            df[col].hist(bins=30, ax=axes[i], alpha=0.7)
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
    
    # Hide empty subplots
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# Box plots for outlier detection
if len(numeric_cols) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    df[numeric_cols].boxplot(ax=ax)
    plt.xticks(rotation=45)
    plt.title('Box Plots for Outlier Detection')
    plt.tight_layout()
    plt.show()

# Count plots for categorical variables
if len(categorical_cols) > 0:
    n_categorical = min(4, len(categorical_cols))
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(categorical_cols[:4]):
        top_categories = df[col].value_counts().head(10)
        top_categories.plot(kind='bar', ax=axes[i])
        axes[i].set_title(f'Top 10 Categories in {col}')
        axes[i].tick_params(axis='x', rotation=45)
    
    # Hide empty subplots
    for i in range(len(categorical_cols[:4]), 4):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 2. BIVARIATE ANALYSIS
print("\\n=== BIVARIATE ANALYSIS ===")

# Correlation heatmap
if len(numeric_cols) > 1:
    plt.figure(figsize=(12, 8))
    correlation_matrix = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdBu_r', 
                center=0, square=True, linewidths=0.5)
    plt.title('Correlation Matrix (Lower Triangle)')
    plt.tight_layout()
    plt.show()

# Scatter plots for top correlated pairs
if len(numeric_cols) > 1:
    corr_matrix = df[numeric_cols].corr()
    # Get top correlated pairs (excluding diagonal)
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append((
                corr_matrix.columns[i], 
                corr_matrix.columns[j], 
                abs(corr_matrix.iloc[i, j])
            ))
    
    top_pairs = sorted(corr_pairs, key=lambda x: x[2], reverse=True)[:4]
    
    if top_pairs:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        for i, (col1, col2, corr) in enumerate(top_pairs):
            axes[i].scatter(df[col1], df[col2], alpha=0.6)
            axes[i].set_xlabel(col1)
            axes[i].set_ylabel(col2)
            axes[i].set_title(f'{col1} vs {col2} (r={corr:.3f})')
        
        plt.tight_layout()
        plt.show()

# 3. INTERACTIVE PLOTLY VISUALIZATIONS
print("\\n=== INTERACTIVE VISUALIZATIONS ===")

# Interactive correlation heatmap
if len(numeric_cols) > 1:
    fig = px.imshow(df[numeric_cols].corr(), 
                    title="Interactive Correlation Heatmap",
                    color_continuous_scale='RdBu_r',
                    aspect="auto")
    fig.show()

# Interactive scatter plot with categorical coloring
if len(numeric_cols) >= 2 and len(categorical_cols) > 0:
    fig = px.scatter(df, 
                     x=numeric_cols[0], 
                     y=numeric_cols[1],
                     color=categorical_cols[0] if categorical_cols else None,
                     title=f"Interactive Scatter: {numeric_cols[0]} vs {numeric_cols[1]}",
                     hover_data=numeric_cols[:3])
    fig.show()

# Interactive histogram
if len(numeric_cols) > 0:
    fig = px.histogram(df, 
                       x=numeric_cols[0],
                       title=f"Interactive Histogram: {numeric_cols[0]}",
                       nbins=30)
    fig.show()

# 4. ADVANCED VISUALIZATIONS
print("\\n=== ADVANCED VISUALIZATIONS ===")

# Pair plot for numeric variables (limited to first 5)
if len(numeric_cols) > 1:
    subset_cols = numeric_cols[:5]
    if len(categorical_cols) > 0:
        hue_col = categorical_cols[0]
        # Limit categories to avoid overcrowding
        top_categories = df[hue_col].value_counts().head(5).index
        subset_df = df[df[hue_col].isin(top_categories)]
        sns.pairplot(subset_df[subset_cols + [hue_col]], hue=hue_col, diag_kind='hist')
    else:
        sns.pairplot(df[subset_cols], diag_kind='hist')
    plt.suptitle('Pair Plot of Numeric Variables', y=1.02)
    plt.show()

# Distribution comparison
if len(categorical_cols) > 0 and len(numeric_cols) > 0:
    cat_col = categorical_cols[0]
    num_col = numeric_cols[0]
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    for category in df[cat_col].value_counts().head(5).index:
        subset = df[df[cat_col] == category][num_col]
        plt.hist(subset, alpha=0.6, label=category, bins=20)
    plt.xlabel(num_col)
    plt.ylabel('Frequency')
    plt.title(f'{num_col} Distribution by {cat_col}')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    df.boxplot(column=num_col, by=cat_col, ax=plt.gca())
    plt.title(f'{num_col} by {cat_col}')
    plt.suptitle('')  # Remove automatic title
    
    plt.tight_layout()
    plt.show()

print("\\n=== VISUALIZATION COMPLETE ===")
print("All major visualization types have been generated!")
print("Consider: time series plots, geographic maps, 3D visualizations")`
    }
  },
  
  sql: {
    exploration: {
      name: 'Data Exploration Query',
      description: 'Comprehensive SQL queries for data exploration and profiling',
      category: 'data-analysis',
      complexity: 'beginner',
      language: 'sql',
      estimatedRuntime: '1-3 minutes',
      code: `-- Data Exploration and Profiling Queries
-- Replace 'your_table' with your actual table name

-- 1. BASIC TABLE INFORMATION
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT customer_id) as unique_customers,
    MIN(order_date) as earliest_date,
    MAX(order_date) as latest_date,
    AVG(order_value) as avg_order_value,
    STDDEV(order_value) as std_order_value
FROM your_table;

-- 2. DATA QUALITY CHECK
SELECT 
    'customer_id' as column_name,
    COUNT(*) as total_count,
    COUNT(customer_id) as non_null_count,
    COUNT(*) - COUNT(customer_id) as null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(customer_id)) / COUNT(*), 2) as null_percentage
FROM your_table

UNION ALL

SELECT 
    'order_date' as column_name,
    COUNT(*) as total_count,
    COUNT(order_date) as non_null_count,
    COUNT(*) - COUNT(order_date) as null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(order_date)) / COUNT(*), 2) as null_percentage
FROM your_table

UNION ALL

SELECT 
    'order_value' as column_name,
    COUNT(*) as total_count,
    COUNT(order_value) as non_null_count,
    COUNT(*) - COUNT(order_value) as null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(order_value)) / COUNT(*), 2) as null_percentage
FROM your_table;

-- 3. DESCRIPTIVE STATISTICS
SELECT 
    MIN(order_value) as min_value,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_value) as q1,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_value) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_value) as q3,
    MAX(order_value) as max_value,
    AVG(order_value) as mean_value,
    STDDEV(order_value) as std_deviation,
    VARIANCE(order_value) as variance
FROM your_table
WHERE order_value IS NOT NULL;

-- 4. CATEGORICAL ANALYSIS
SELECT 
    category,
    COUNT(*) as frequency,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM your_table
WHERE category IS NOT NULL
GROUP BY category
ORDER BY frequency DESC
LIMIT 10;

-- 5. TIME SERIES ANALYSIS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(order_value) as total_revenue,
    AVG(order_value) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM your_table
WHERE order_date IS NOT NULL
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- 6. OUTLIER DETECTION
WITH stats AS (
    SELECT 
        AVG(order_value) as mean_val,
        STDDEV(order_value) as std_val
    FROM your_table
    WHERE order_value IS NOT NULL
),
outliers AS (
    SELECT 
        *,
        ABS(order_value - stats.mean_val) / stats.std_val as z_score
    FROM your_table, stats
    WHERE order_value IS NOT NULL
)
SELECT 
    COUNT(*) as total_outliers,
    MIN(order_value) as min_outlier_value,
    MAX(order_value) as max_outlier_value,
    AVG(order_value) as avg_outlier_value
FROM outliers
WHERE z_score > 3;`
    },
    
    analytics: {
      name: 'Customer Analytics Query',
      description: 'Advanced customer behavior and revenue analytics',
      category: 'data-analysis',
      complexity: 'intermediate',
      language: 'sql',
      estimatedRuntime: '2-5 minutes',
      code: `-- Customer Analytics and Business Intelligence Queries

-- 1. CUSTOMER LIFETIME VALUE (CLV) ANALYSIS
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(order_value) as total_spent,
        AVG(order_value) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        MAX(order_date) - MIN(order_date) as customer_lifespan_days
    FROM your_table
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
),
clv_segments AS (
    SELECT 
        customer_id,
        total_spent,
        order_count,
        avg_order_value,
        customer_lifespan_days,
        CASE 
            WHEN total_spent >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY total_spent) FROM customer_metrics) THEN 'High Value'
            WHEN total_spent >= (SELECT PERCENTILE_CONT(0.7) WITHIN GROUP (ORDER BY total_spent) FROM customer_metrics) THEN 'Medium Value'
            ELSE 'Low Value'
        END as value_segment,
        CASE 
            WHEN order_count >= 10 THEN 'Frequent'
            WHEN order_count >= 5 THEN 'Regular'
            ELSE 'Occasional'
        END as frequency_segment
    FROM customer_metrics
)
SELECT 
    value_segment,
    frequency_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_clv,
    AVG(order_count) as avg_orders,
    AVG(avg_order_value) as avg_aov,
    SUM(total_spent) as total_revenue
FROM clv_segments
GROUP BY value_segment, frequency_segment
ORDER BY avg_clv DESC;

-- 2. RFM ANALYSIS (Recency, Frequency, Monetary)
WITH rfm_base AS (
    SELECT 
        customer_id,
        CURRENT_DATE - MAX(order_date) as recency_days,
        COUNT(*) as frequency,
        SUM(order_value) as monetary
    FROM your_table
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) as recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) as monetary_score
    FROM rfm_base
),
rfm_segments AS (
    SELECT 
        customer_id,
        recency_score,
        frequency_score,
        monetary_score,
        CASE 
            WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
            WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
            WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'New Customers'
            WHEN recency_score <= 2 AND frequency_score >= 3 THEN 'At Risk'
            WHEN recency_score <= 2 AND frequency_score <= 2 THEN 'Lost Customers'
            ELSE 'Developing'
        END as rfm_segment
    FROM rfm_scores
)
SELECT 
    rfm_segment,
    COUNT(*) as customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage,
    AVG(recency_score) as avg_recency,
    AVG(frequency_score) as avg_frequency,
    AVG(monetary_score) as avg_monetary
FROM rfm_segments
GROUP BY rfm_segment
ORDER BY customer_count DESC;

-- 3. COHORT ANALYSIS
WITH cohort_data AS (
    SELECT 
        customer_id,
        order_date,
        order_value,
        DATE_TRUNC('month', MIN(order_date) OVER (PARTITION BY customer_id)) as cohort_month
    FROM your_table
    WHERE customer_id IS NOT NULL
),
cohort_table AS (
    SELECT 
        cohort_month,
        DATE_TRUNC('month', order_date) as order_month,
        COUNT(DISTINCT customer_id) as customers,
        SUM(order_value) as revenue
    FROM cohort_data
    GROUP BY cohort_month, DATE_TRUNC('month', order_date)
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) as cohort_size
    FROM cohort_data
    GROUP BY cohort_month
)
SELECT 
    ct.cohort_month,
    ct.order_month,
    ct.customers,
    cs.cohort_size,
    ROUND(100.0 * ct.customers / cs.cohort_size, 2) as retention_rate,
    ct.revenue,
    ROUND(ct.revenue / ct.customers, 2) as revenue_per_customer
FROM cohort_table ct
JOIN cohort_sizes cs ON ct.cohort_month = cs.cohort_month
ORDER BY ct.cohort_month, ct.order_month;

-- 4. PURCHASE PATTERN ANALYSIS
WITH order_intervals AS (
    SELECT 
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order_date,
        order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as days_between_orders
    FROM your_table
    WHERE customer_id IS NOT NULL
)
SELECT 
    CASE 
        WHEN days_between_orders IS NULL THEN 'First Order'
        WHEN days_between_orders <= 7 THEN '1 Week or Less'
        WHEN days_between_orders <= 30 THEN '1 Month or Less'
        WHEN days_between_orders <= 90 THEN '3 Months or Less'
        WHEN days_between_orders <= 180 THEN '6 Months or Less'
        ELSE 'More than 6 Months'
    END as purchase_interval,
    COUNT(*) as order_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage
FROM order_intervals
GROUP BY 
    CASE 
        WHEN days_between_orders IS NULL THEN 'First Order'
        WHEN days_between_orders <= 7 THEN '1 Week or Less'
        WHEN days_between_orders <= 30 THEN '1 Month or Less'
        WHEN days_between_orders <= 90 THEN '3 Months or Less'
        WHEN days_between_orders <= 180 THEN '6 Months or Less'
        ELSE 'More than 6 Months'
    END
ORDER BY 
    CASE 
        WHEN purchase_interval = 'First Order' THEN 1
        WHEN purchase_interval = '1 Week or Less' THEN 2
        WHEN purchase_interval = '1 Month or Less' THEN 3
        WHEN purchase_interval = '3 Months or Less' THEN 4
        WHEN purchase_interval = '6 Months or Less' THEN 5
        ELSE 6
    END;

-- 5. REVENUE TREND ANALYSIS
SELECT 
    DATE_TRUNC('week', order_date) as week,
    COUNT(*) as order_count,
    SUM(order_value) as weekly_revenue,
    AVG(order_value) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(order_value) / COUNT(DISTINCT customer_id) as revenue_per_customer,
    LAG(SUM(order_value)) OVER (ORDER BY DATE_TRUNC('week', order_date)) as prev_week_revenue,
    ROUND(100.0 * (SUM(order_value) - LAG(SUM(order_value)) OVER (ORDER BY DATE_TRUNC('week', order_date))) / 
          LAG(SUM(order_value)) OVER (ORDER BY DATE_TRUNC('week', order_date)), 2) as revenue_growth_rate
FROM your_table
WHERE order_date >= CURRENT_DATE - INTERVAL '12 weeks'
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week DESC;`
    }
  },
  
  r: {
    statistics: {
      name: 'Statistical Analysis in R',
      description: 'Comprehensive statistical analysis and hypothesis testing',
      category: 'statistics',
      complexity: 'intermediate',
      language: 'r',
      estimatedRuntime: '3-10 minutes',
      memoryUsage: '< 1GB',
      code: `# Statistical Analysis in R - Comprehensive Template
# Load required libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(car)
library(nortest)
library(MASS)
library(broom)
library(knitr)

# Load data
data <- read.csv("your_data.csv")
cat("Dataset dimensions:", dim(data), "\\n")
cat("Dataset structure:\\n")
str(data)

# =================================
# 1. DESCRIPTIVE STATISTICS
# =================================
cat("\\n=== DESCRIPTIVE STATISTICS ===\\n")

# Summary statistics for all variables
summary(data)

# Separate numeric and categorical variables
numeric_vars <- sapply(data, is.numeric)
numeric_data <- data[, numeric_vars]
categorical_data <- data[, !numeric_vars]

if(ncol(numeric_data) > 0) {
  cat("\\nDetailed statistics for numeric variables:\\n")
  
  # Custom summary function
  detailed_summary <- function(x) {
    c(
      Mean = mean(x, na.rm = TRUE),
      Median = median(x, na.rm = TRUE),
      SD = sd(x, na.rm = TRUE),
      IQR = IQR(x, na.rm = TRUE),
      Min = min(x, na.rm = TRUE),
      Max = max(x, na.rm = TRUE),
      Skewness = moments::skewness(x, na.rm = TRUE),
      Kurtosis = moments::kurtosis(x, na.rm = TRUE)
    )
  }
  
  # Apply to all numeric columns
  if(require(moments, quietly = TRUE)) {
    detailed_stats <- sapply(numeric_data, detailed_summary)
    print(round(detailed_stats, 3))
  }
}

# =================================
# 2. DATA VISUALIZATION
# =================================
cat("\\n=== DATA VISUALIZATION ===\\n")

# Histograms for numeric variables
if(ncol(numeric_data) > 0) {
  # Create histograms
  p1 <- numeric_data %>%
    gather() %>%
    ggplot(aes(value)) +
    facet_wrap(~ key, scales = "free") +
    geom_histogram(bins = 30, alpha = 0.7, fill = "steelblue") +
    theme_minimal() +
    labs(title = "Distribution of Numeric Variables")
  
  print(p1)
  
  # Box plots for outlier detection
  p2 <- numeric_data %>%
    gather() %>%
    ggplot(aes(x = key, y = value)) +
    geom_boxplot(fill = "lightblue", alpha = 0.7) +
    facet_wrap(~ key, scales = "free") +
    theme_minimal() +
    theme(axis.text.x = element_blank()) +
    labs(title = "Box Plots for Outlier Detection", x = "Variables", y = "Values")
  
  print(p2)
}

# =================================
# 3. CORRELATION ANALYSIS
# =================================
if(ncol(numeric_data) > 1) {
  cat("\\n=== CORRELATION ANALYSIS ===\\n")
  
  # Correlation matrix
  correlation_matrix <- cor(numeric_data, use = "complete.obs")
  print(round(correlation_matrix, 3))
  
  # Correlation plot
  corrplot(correlation_matrix, method = "color", type = "upper", 
           order = "hclust", tl.cex = 0.8, tl.col = "black")
  
  # Significance test for correlations
  cor_test_results <- corr.test(numeric_data)
  cat("\\nCorrelation p-values:\\n")
  print(round(cor_test_results$p, 3))
}

# =================================
# 4. NORMALITY TESTING
# =================================
cat("\\n=== NORMALITY TESTING ===\\n")

if(ncol(numeric_data) > 0) {
  normality_results <- data.frame(
    Variable = names(numeric_data),
    Shapiro_W = NA,
    Shapiro_p = NA,
    Anderson_A = NA,
    Anderson_p = NA,
    Lilliefors_D = NA,
    Lilliefors_p = NA
  )
  
  for(i in 1:ncol(numeric_data)) {
    var_name <- names(numeric_data)[i]
    var_data <- numeric_data[, i]
    var_data <- var_data[!is.na(var_data)]
    
    if(length(var_data) > 3 && length(var_data) <= 5000) {
      # Shapiro-Wilk test
      shapiro_result <- shapiro.test(var_data)
      normality_results[i, "Shapiro_W"] <- shapiro_result$statistic
      normality_results[i, "Shapiro_p"] <- shapiro_result$p.value
      
      # Anderson-Darling test
      ad_result <- ad.test(var_data)
      normality_results[i, "Anderson_A"] <- ad_result$statistic
      normality_results[i, "Anderson_p"] <- ad_result$p.value
      
      # Lilliefors test
      lillie_result <- lillie.test(var_data)
      normality_results[i, "Lilliefors_D"] <- lillie_result$statistic
      normality_results[i, "Lilliefors_p"] <- lillie_result$p.value
    }
  }
  
  print(normality_results)
  
  # Q-Q plots
  if(ncol(numeric_data) <= 6) {
    par(mfrow = c(2, 3))
    for(i in 1:ncol(numeric_data)) {
      var_data <- numeric_data[, i]
      var_data <- var_data[!is.na(var_data)]
      qqnorm(var_data, main = paste("Q-Q Plot:", names(numeric_data)[i]))
      qqline(var_data, col = "red")
    }
    par(mfrow = c(1, 1))
  }
}

# =================================
# 5. HYPOTHESIS TESTING
# =================================
cat("\\n=== HYPOTHESIS TESTING ===\\n")

# Example: t-tests between groups (modify as needed)
if(ncol(categorical_data) > 0 && ncol(numeric_data) > 0) {
  cat_var <- names(categorical_data)[1]
  num_var <- names(numeric_data)[1]
  
  # Check if categorical variable has exactly 2 groups for t-test
  groups <- unique(data[[cat_var]])
  groups <- groups[!is.na(groups)]
  
  if(length(groups) == 2) {
    cat(sprintf("\\nTwo-sample t-test: %s by %s\\n", num_var, cat_var))
    
    group1_data <- data[data[[cat_var]] == groups[1], num_var]
    group2_data <- data[data[[cat_var]] == groups[2], num_var]
    
    group1_data <- group1_data[!is.na(group1_data)]
    group2_data <- group2_data[!is.na(group2_data)]
    
    # Perform t-test
    t_test_result <- t.test(group1_data, group2_data)
    print(t_test_result)
    
    # Levene's test for equality of variances
    levene_result <- leveneTest(data[[num_var]] ~ as.factor(data[[cat_var]]), data = data)
    cat("\\nLevene's test for equality of variances:\\n")
    print(levene_result)
  }
  
  # ANOVA for multiple groups
  if(length(groups) > 2 && length(groups) <= 10) {
    cat(sprintf("\\nOne-way ANOVA: %s by %s\\n", num_var, cat_var))
    
    # Perform ANOVA
    anova_result <- aov(data[[num_var]] ~ as.factor(data[[cat_var]]), data = data)
    print(summary(anova_result))
    
    # Post-hoc test (Tukey HSD)
    if(summary(anova_result)[[1]][1, "Pr(>F)"] < 0.05) {
      tukey_result <- TukeyHSD(anova_result)
      print(tukey_result)
    }
  }
}

# =================================
# 6. REGRESSION ANALYSIS
# =================================
if(ncol(numeric_data) > 1) {
  cat("\\n=== REGRESSION ANALYSIS ===\\n")
  
  # Simple linear regression (first two numeric variables)
  var_names <- names(numeric_data)
  y_var <- var_names[1]
  x_var <- var_names[2]
  
  cat(sprintf("\\nSimple Linear Regression: %s ~ %s\\n", y_var, x_var))
  
  # Fit the model
  lm_model <- lm(data[[y_var]] ~ data[[x_var]], data = data)
  
  # Model summary
  print(summary(lm_model))
  
  # Model diagnostics
  cat("\\nModel Diagnostics:\\n")
  par(mfrow = c(2, 2))
  plot(lm_model)
  par(mfrow = c(1, 1))
  
  # Additional diagnostic tests
  cat("\\nDurbin-Watson test for autocorrelation:\\n")
  print(durbinWatsonTest(lm_model))
  
  cat("\\nBreusch-Pagan test for heteroscedasticity:\\n")
  print(bptest(lm_model))
  
  # Multiple regression (if more variables available)
  if(ncol(numeric_data) > 2) {
    cat("\\nMultiple Linear Regression:\\n")
    
    # Use all numeric variables except the first one as predictors
    formula_str <- paste(y_var, "~", paste(var_names[-1], collapse = " + "))
    multiple_lm <- lm(as.formula(formula_str), data = data)
    
    print(summary(multiple_lm))
    
    # Variable selection using stepwise regression
    cat("\\nStepwise Variable Selection:\\n")
    step_model <- stepAIC(multiple_lm, direction = "both", trace = FALSE)
    print(summary(step_model))
  }
}

# =================================
# 7. OUTLIER DETECTION
# =================================
cat("\\n=== OUTLIER DETECTION ===\\n")

if(ncol(numeric_data) > 0) {
  outlier_summary <- data.frame(
    Variable = names(numeric_data),
    IQR_Outliers = NA,
    Z_Score_Outliers = NA,
    Total_Observations = NA
  )
  
  for(i in 1:ncol(numeric_data)) {
    var_data <- numeric_data[, i]
    var_data <- var_data[!is.na(var_data)]
    
    # IQR method
    Q1 <- quantile(var_data, 0.25)
    Q3 <- quantile(var_data, 0.75)
    IQR_val <- Q3 - Q1
    iqr_outliers <- sum(var_data < (Q1 - 1.5 * IQR_val) | var_data > (Q3 + 1.5 * IQR_val))
    
    # Z-score method
    z_scores <- abs(scale(var_data))
    z_outliers <- sum(z_scores > 3, na.rm = TRUE)
    
    outlier_summary[i, "IQR_Outliers"] <- iqr_outliers
    outlier_summary[i, "Z_Score_Outliers"] <- z_outliers
    outlier_summary[i, "Total_Observations"] <- length(var_data)
  }
  
  print(outlier_summary)
}

cat("\\n=== STATISTICAL ANALYSIS COMPLETE ===\\n")
cat("Consider additional analyses: time series, survival analysis, clustering\\n")`
    }
  }
};

// Helper functions for template selection
export const getTemplatesByLanguage = (language: string): CodeTemplate[] => {
  return Object.values(codeTemplates[language.toLowerCase()] || {});
};

export const getTemplatesByCategory = (category: string): CodeTemplate[] => {
  const templates: CodeTemplate[] = [];
  Object.values(codeTemplates).forEach(languageTemplates => {
    Object.values(languageTemplates).forEach(template => {
      if (template.category === category) {
        templates.push(template);
      }
    });
  });
  return templates;
};

export const getAllTemplates = (): CodeTemplate[] => {
  const templates: CodeTemplate[] = [];
  Object.values(codeTemplates).forEach(languageTemplates => {
    Object.values(languageTemplates).forEach(template => {
      templates.push(template);
    });
  });
  return templates;
};

export default codeTemplates; 