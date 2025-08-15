import React, { useState } from 'react';
import CodeBlock from './UI/CodeBlock.tsx';
import DataScienceCodeBlock from './UI/DataScienceCodeBlock.tsx';
import { AIMessage } from './UI/MessageParser.tsx';
import InlineCode from './UI/InlineCode.tsx';

const CodeBlockDemo: React.FC = () => {
  const [currentDemo, setCurrentDemo] = useState<string>('basic');

  const pythonCode = `# Data Analysis with Pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('sales_data.csv')
print(f"Dataset shape: {df.shape}")

# Basic statistics
print("\\nDataset Overview:")
print(df.info())
print("\\nSummary Statistics:")
print(df.describe())

# Data visualization
plt.figure(figsize=(12, 8))

# Revenue trend over time
plt.subplot(2, 2, 1)
df.groupby('month')['revenue'].sum().plot(kind='line', marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')

# Top products by sales
plt.subplot(2, 2, 2)
top_products = df.groupby('product')['quantity'].sum().nlargest(10)
top_products.plot(kind='bar')
plt.title('Top 10 Products by Quantity Sold')
plt.xticks(rotation=45)

# Customer distribution
plt.subplot(2, 2, 3)
df['customer_segment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Customer Segment Distribution')

# Correlation heatmap
plt.subplot(2, 2, 4)
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')

plt.tight_layout()
plt.show()

# Advanced analysis
print("\\n=== ADVANCED INSIGHTS ===")

# Customer lifetime value calculation
clv = df.groupby('customer_id').agg({
    'revenue': 'sum',
    'order_id': 'count',
    'order_date': ['min', 'max']
}).round(2)

print("Customer Lifetime Value Statistics:")
print(clv['revenue'].describe())`;

  const sqlCode = `-- Customer Analytics Dashboard Queries
-- Advanced SQL for business intelligence insights

-- 1. Customer Lifetime Value with Cohort Analysis
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        COUNT(*) as total_orders,
        SUM(order_value) as lifetime_value,
        AVG(order_value) as avg_order_value
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_id
),
cohort_performance AS (
    SELECT 
        cohort_month,
        COUNT(*) as cohort_size,
        AVG(lifetime_value) as avg_clv,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY lifetime_value) as median_clv,
        AVG(total_orders) as avg_orders_per_customer,
        AVG(avg_order_value) as avg_aov
    FROM customer_cohorts
    GROUP BY cohort_month
    ORDER BY cohort_month
)
SELECT 
    cohort_month,
    cohort_size,
    ROUND(avg_clv, 2) as avg_customer_lifetime_value,
    ROUND(median_clv, 2) as median_clv,
    ROUND(avg_orders_per_customer, 1) as avg_orders,
    ROUND(avg_aov, 2) as avg_order_value,
    ROUND(avg_clv * cohort_size, 2) as cohort_total_value
FROM cohort_performance;

-- 2. RFM Segmentation Analysis
WITH rfm_calculation AS (
    SELECT 
        customer_id,
        CURRENT_DATE - MAX(order_date) as recency_days,
        COUNT(*) as frequency,
        SUM(order_value) as monetary,
        AVG(order_value) as avg_order_value
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        avg_order_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) as recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) as monetary_score
    FROM rfm_calculation
),
rfm_segments AS (
    SELECT 
        *,
        CASE 
            WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
            WHEN recency_score >= 3 AND frequency_score >= 3 THEN 'Loyal Customers'
            WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'New Customers'
            WHEN recency_score <= 2 AND frequency_score >= 3 THEN 'At Risk'
            WHEN recency_score <= 2 AND frequency_score <= 2 THEN 'Lost Customers'
            WHEN monetary_score >= 4 THEN 'High Value'
            ELSE 'Developing'
        END as segment
    FROM rfm_scores
)
SELECT 
    segment,
    COUNT(*) as customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percentage,
    ROUND(AVG(recency_days), 1) as avg_recency,
    ROUND(AVG(frequency), 1) as avg_frequency,
    ROUND(AVG(monetary), 2) as avg_monetary_value,
    ROUND(SUM(monetary), 2) as segment_total_value
FROM rfm_segments
GROUP BY segment
ORDER BY customer_count DESC;`;

  const rCode = `# Advanced Statistical Analysis in R
# Comprehensive data science workflow

library(tidyverse)
library(corrplot)
library(randomForest)
library(caret)
library(VIM)
library(mice)
library(ggplot2)
library(plotly)

# Load and explore data
data <- read.csv("dataset.csv")
cat("Dataset Dimensions:", dim(data), "\\n")

# =================================
# 1. EXPLORATORY DATA ANALYSIS
# =================================

# Data structure and summary
str(data)
summary(data)

# Missing value analysis
missing_pattern <- VIM::aggr(data, col = c('navyblue','red'), 
                           numbers = TRUE, sortVars = TRUE)

# Create comprehensive EDA plots
eda_plots <- function(df) {
  numeric_vars <- sapply(df, is.numeric)
  numeric_data <- df[, numeric_vars]
  
  # Distribution plots
  p1 <- numeric_data %>%
    gather() %>%
    ggplot(aes(value)) +
    facet_wrap(~ key, scales = "free") +
    geom_histogram(bins = 30, alpha = 0.7, fill = "steelblue") +
    theme_minimal() +
    labs(title = "Distribution of Numeric Variables")
  
  # Correlation matrix
  cor_matrix <- cor(numeric_data, use = "complete.obs")
  corrplot(cor_matrix, method = "color", type = "upper", 
           order = "hclust", tl.cex = 0.8)
  
  # Box plots for outlier detection
  p2 <- numeric_data %>%
    gather() %>%
    ggplot(aes(x = key, y = value)) +
    geom_boxplot(fill = "lightblue", alpha = 0.7) +
    facet_wrap(~ key, scales = "free") +
    theme_minimal() +
    theme(axis.text.x = element_blank()) +
    labs(title = "Outlier Detection - Box Plots")
  
  return(list(distributions = p1, boxplots = p2))
}

plots <- eda_plots(data)
print(plots$distributions)
print(plots$boxplots)

# =================================
# 2. DATA PREPROCESSING
# =================================

# Handle missing values using MICE
if(sum(is.na(data)) > 0) {
  cat("Imputing missing values...\\n")
  
  # Multiple imputation
  imputed_data <- mice(data, m = 5, method = 'pmm', 
                       printFlag = FALSE, seed = 123)
  
  # Complete the data
  data_complete <- complete(imputed_data)
  
  cat("Missing values after imputation:", sum(is.na(data_complete)), "\\n")
} else {
  data_complete <- data
}

# Feature scaling for numeric variables
numeric_cols <- sapply(data_complete, is.numeric)
data_scaled <- data_complete
data_scaled[numeric_cols] <- scale(data_complete[numeric_cols])

# =================================
# 3. MACHINE LEARNING MODELING
# =================================

# Assuming 'target' is your response variable
if("target" %in% names(data_complete)) {
  
  # Split data
  set.seed(123)
  train_index <- createDataPartition(data_complete$target, p = 0.8, list = FALSE)
  train_data <- data_complete[train_index, ]
  test_data <- data_complete[-train_index, ]
  
  cat("Training set size:", nrow(train_data), "\\n")
  cat("Test set size:", nrow(test_data), "\\n")
  
  # Random Forest Model
  rf_model <- randomForest(target ~ ., data = train_data, 
                          ntree = 500, importance = TRUE)
  
  # Model predictions
  train_pred <- predict(rf_model, train_data)
  test_pred <- predict(rf_model, test_data)
  
  # Model evaluation
  if(is.factor(data_complete$target)) {
    # Classification metrics
    train_accuracy <- mean(train_pred == train_data$target)
    test_accuracy <- mean(test_pred == test_data$target)
    
    cat("\\n=== CLASSIFICATION RESULTS ===\\n")
    cat("Training Accuracy:", round(train_accuracy, 4), "\\n")
    cat("Test Accuracy:", round(test_accuracy, 4), "\\n")
    
    # Confusion Matrix
    conf_matrix <- confusionMatrix(test_pred, test_data$target)
    print(conf_matrix)
    
  } else {
    # Regression metrics
    train_rmse <- sqrt(mean((train_pred - train_data$target)^2))
    test_rmse <- sqrt(mean((test_pred - test_data$target)^2))
    train_r2 <- cor(train_pred, train_data$target)^2
    test_r2 <- cor(test_pred, test_data$target)^2
    
    cat("\\n=== REGRESSION RESULTS ===\\n")
    cat("Training RMSE:", round(train_rmse, 4), "\\n")
    cat("Test RMSE:", round(test_rmse, 4), "\\n")
    cat("Training R²:", round(train_r2, 4), "\\n")
    cat("Test R²:", round(test_r2, 4), "\\n")
  }
  
  # Feature importance
  importance_df <- data.frame(
    Feature = rownames(importance(rf_model)),
    Importance = importance(rf_model)[, "MeanDecreaseGini"]
  ) %>%
    arrange(desc(Importance))
  
  # Plot feature importance
  p_importance <- ggplot(importance_df[1:15, ], aes(x = reorder(Feature, Importance), y = Importance)) +
    geom_col(fill = "steelblue", alpha = 0.8) +
    coord_flip() +
    labs(title = "Top 15 Feature Importance", x = "Features", y = "Importance") +
    theme_minimal()
  
  print(p_importance)
  
  # Cross-validation
  cv_control <- trainControl(method = "cv", number = 10, savePredictions = TRUE)
  cv_model <- train(target ~ ., data = train_data, method = "rf",
                   trControl = cv_control, ntree = 100)
  
  cat("\\n=== CROSS-VALIDATION RESULTS ===\\n")
  print(cv_model$results)
}

cat("\\n=== ANALYSIS COMPLETE ===\\n")
cat("Consider: hyperparameter tuning, ensemble methods, feature selection\\n")`;

  const messageWithCode = `Here's a comprehensive data analysis workflow for your sales dataset:

## Data Analysis Pipeline

I'll walk you through a complete analysis of your sales data, from initial exploration to advanced modeling.

### 1. Data Exploration

\`\`\`python Data Loading and Initial Exploration
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('sales_data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Check for missing values
print("\\nMissing values:")
print(df.isnull().sum())

# Basic statistics
print("\\nDataset summary:")
print(df.describe())
\`\`\`

This code will give you a comprehensive overview of your data structure and quality.

### 2. Customer Segmentation Analysis

For business insights, let's analyze customer behavior patterns:

\`\`\`sql Customer RFM Analysis
-- Recency, Frequency, Monetary analysis
WITH customer_metrics AS (
    SELECT 
        customer_id,
        CURRENT_DATE - MAX(order_date) as recency_days,
        COUNT(*) as frequency,
        SUM(order_value) as monetary
    FROM orders
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        NTILE(5) OVER (ORDER BY recency_days DESC) as recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) as monetary_score
    FROM customer_metrics
)
SELECT 
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 3 THEN 'Loyal'
        ELSE 'Developing'
    END as segment,
    COUNT(*) as customer_count
FROM rfm_scores
GROUP BY 1;
\`\`\`

### 3. Advanced Statistical Modeling

For predictive insights, here's a machine learning approach:

\`\`\`r Statistical Analysis
library(randomForest)
library(caret)

# Load and prepare data
data <- read.csv("sales_data.csv")

# Create model
model <- randomForest(revenue ~ ., data = data, ntree = 500)

# Feature importance
importance(model)
\`\`\`

Would you like me to customize any of these analyses for your specific use case?`;

  const demos: Record<string, { title: string; content: JSX.Element }> = {
    basic: {
      title: 'Basic Code Blocks',
      content: (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3">Python Code Block</h3>
            <CodeBlock
              code={pythonCode}
              language="python"
              title="Sales Data Analysis"
              executable={true}
              showLineNumbers={true}
            />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-3">SQL Code Block</h3>
            <CodeBlock
              code={sqlCode}
              language="sql"
              title="Customer Analytics Queries"
              fileName="customer_analytics.sql"
              executable={true}
            />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-3">R Code Block</h3>
            <CodeBlock
              code={rCode}
              language="r"
              title="Statistical Analysis"
              executable={true}
            />
          </div>
        </div>
      )
    },
    
    datascience: {
      title: 'Data Science Enhanced Blocks',
      content: (
        <div className="space-y-6">
          <DataScienceCodeBlock
            code={pythonCode}
            language="python"
            title="Exploratory Data Analysis"
            analysisType="eda"
            complexity="beginner"
            estimatedRuntime="3-5 minutes"
            memoryUsage="< 500MB"
            datasetInfo={{
              name: "sales_data.csv",
              rows: 50000,
              columns: 12,
              size: "8.5MB"
            }}
            executable={true}
          />
          
          <DataScienceCodeBlock
            code={`# Advanced Machine Learning Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

# Advanced feature engineering
def create_features(df):
    df['revenue_per_customer'] = df['total_revenue'] / df['customer_count']
    df['seasonal_index'] = df['month'].map({12:1, 1:1, 2:1, 3:2, 4:2, 5:2, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4})
    df['is_weekend'] = df['day_of_week'].isin([6, 7]).astype(int)
    return df

# Ensemble modeling
models = {
    'rf': RandomForestRegressor(n_estimators=200, random_state=42),
    'gbm': GradientBoostingRegressor(n_estimators=200, random_state=42),
    'xgb': xgb.XGBRegressor(n_estimators=200, random_state=42)
}

results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    results[name] = scores.mean()
    print(f"{name.upper()} CV R²: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Select best model
best_model = max(results, key=results.get)
print(f"\\nBest model: {best_model.upper()} with R² = {results[best_model]:.4f}")`}
            language="python"
            title="Advanced ML Pipeline"
            analysisType="modeling"
            complexity="advanced"
            estimatedRuntime="15-30 minutes"
            memoryUsage="2-4GB"
            datasetInfo={{
              name: "processed_sales_data.csv",
              rows: 100000,
              columns: 25,
              size: "45MB"
            }}
            executable={true}
          />
        </div>
      )
    },
    
    parsing: {
      title: 'AI Message with Code Parsing',
      content: (
        <div className="space-y-6">
          <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">AI Response with Mixed Content</h3>
            <AIMessage content={messageWithCode} executable={true} />
          </div>
        </div>
      )
    },
    
    inline: {
      title: 'Inline Code Examples',
      content: (
        <div className="space-y-6">
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <h3>Data Science Workflow</h3>
            <p>
              Start by importing the essential libraries: <InlineCode>pandas</InlineCode>, <InlineCode>numpy</InlineCode>, 
              and <InlineCode>matplotlib.pyplot</InlineCode>. Then load your data using <InlineCode>pd.read_csv()</InlineCode>.
            </p>
            
            <p>
              For statistical analysis, you'll often need functions like <InlineCode>df.describe()</InlineCode>, 
              <InlineCode>df.corr()</InlineCode>, and <InlineCode>scipy.stats.pearsonr()</InlineCode>.
            </p>
            
            <p>
              SQL queries should start with basic operations: <InlineCode>SELECT</InlineCode>, <InlineCode>FROM</InlineCode>, 
              <InlineCode>WHERE</InlineCode>, and <InlineCode>GROUP BY</InlineCode>.
            </p>
            
            <p>
              In R, common functions include <InlineCode>summary()</InlineCode>, <InlineCode>str()</InlineCode>, 
              and <InlineCode>ggplot()</InlineCode> for visualization.
            </p>
          </div>
        </div>
      )
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Datasoph Code Blocks Demo</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Explore the professional code block features with syntax highlighting, execution capabilities, and data science enhancements.
        </p>
      </div>

      {/* Demo Navigation */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          {Object.entries(demos).map(([key, demo]) => (
            <button
              key={key}
              onClick={() => setCurrentDemo(key)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentDemo === key
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              {demo.title}
            </button>
          ))}
        </div>
      </div>

      {/* Demo Content */}
      <div className="min-h-screen">
        <h2 className="text-2xl font-semibold mb-6">{demos[currentDemo].title}</h2>
        {demos[currentDemo].content}
      </div>
    </div>
  );
};

export default CodeBlockDemo; 