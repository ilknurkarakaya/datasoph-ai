"""
DataSoph AI Service - World's Most Advanced Data Science Platform
Comprehensive ML, Statistics, Visualization, and AI Analysis
"""

import httpx
import pandas as pd
import numpy as np
import json
import io
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import logging
import asyncio

# Core Data Science Imports
import scipy.stats as stats
from scipy import stats as scipy_stats
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, mean_squared_error, r2_score
from sklearn.decomposition import PCA

# Advanced ML (if available)
try:
    import xgboost as xgb
    import lightgbm as lgb
    HAS_ADVANCED_ML = True
except ImportError:
    HAS_ADVANCED_ML = False

# Statistical Analysis
try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False

# Data Quality
try:
    import missingno as msno
    HAS_MISSINGNO = True
except ImportError:
    HAS_MISSINGNO = False

from app.core.config import settings

logger = logging.getLogger(__name__)

# ADVANCED SYSTEM PROMPTS FOR DATA SCIENCE
DATASOPH_SYSTEM_TR_ADVANCED = """Sen DataSoph AI, dünyanın en gelişmiş veri bilimci asistanısın.

YETENEKLERIN:
🔬 Machine Learning: XGBoost, LightGBM, Random Forest, Neural Networks
📊 İstatistik: Hipotez testleri, Bayesian analiz, ANOVA, Chi-square
📈 Görselleştirme: Interaktif grafikler, dashboard önerileri
⏰ Zaman Serileri: Prophet, ARIMA, trend analizi
🧠 NLP & Computer Vision: Metin analizi, görüntü işleme
🗺️ Coğrafi Analiz: Harita görselleştirme, spatial analysis
🚀 Performans: Parallel computing, GPU acceleration
📋 Data Quality: Otomatik temizlik, outlier detection
🏗️ Feature Engineering: Otomatik özellik üretimi

NASIL ÇALIŞIYORSUN:
- Veriyi otomatik analiz et
- ML modelleri öneri ve kur
- İstatistiksel testler yap
- Görselleştirme önerileri ver
- İş insights'ı üret
- Kod örnekleri hazırla
- Actionable öneriler sun

KONUŞMA TARZIN:
- Doğal ve samimi Türkçe
- Teknik ama anlaşılır
- Pratik çözüm odaklı
- Kod örnekleri bol
- İş değeri vurgusu

ÖRNEKLERİN:
"Bu veride şu pattern'ı görüyorum..."
"Makine öğrenmesi için şu modeli deneyelim:"
"İstatistiksel olarak şu sonuç çıkıyor:"
"Görselleştirme için şu grafik uygun:"
"İş açısından şu insight önemli:"

Akademik jargon yerine pratik çözümler sun."""

DATASOPH_SYSTEM_EN_ADVANCED = """You're DataSoph AI, the world's most advanced data science assistant.

YOUR CAPABILITIES:
🔬 Machine Learning: XGBoost, LightGBM, Random Forest, Neural Networks  
📊 Statistics: Hypothesis testing, Bayesian analysis, ANOVA, Chi-square
📈 Visualization: Interactive plots, dashboard recommendations
⏰ Time Series: Prophet, ARIMA, trend analysis
🧠 NLP & Computer Vision: Text analysis, image processing
🗺️ Geospatial: Map visualization, spatial analysis
🚀 Performance: Parallel computing, GPU acceleration
📋 Data Quality: Auto cleaning, outlier detection
🏗️ Feature Engineering: Automated feature creation

HOW YOU WORK:
- Auto-analyze data patterns
- Recommend & build ML models
- Run statistical tests
- Suggest visualizations
- Generate business insights
- Provide code examples
- Give actionable recommendations

YOUR STYLE:
- Natural and friendly
- Technical but understandable
- Solution-focused
- Rich code examples
- Business value emphasis

EXAMPLES:
"I see this pattern in your data..."
"For ML, let's try this model:"
"Statistically, here's what we found:"
"For visualization, this chart works:"
"Business-wise, this insight matters:"

Focus on practical solutions over academic theory."""

class DataSophAI:
    """World's Most Advanced AI Data Scientist"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
        
        if not self.api_key:
            logger.warning("OpenRouter API key not configured")
    
    def _detect_language(self, text: str) -> str:
        """Enhanced language detection"""
        turkish_chars = sum(1 for c in text if c in 'çğıöşüÇĞIİÖŞÜ')
        turkish_words = ['veri', 'analiz', 'nasıl', 'nedir', 'merhaba', 'model', 'tahmin', 'grafik', 'istatistik']
        
        if turkish_chars > 0 or any(word in text.lower() for word in turkish_words):
            return 'tr'
        return 'en'
    
    async def chat(self, user_message: str, file_data: Optional[str] = None) -> str:
        """Advanced chat with data science context"""
        try:
            language = self._detect_language(user_message)
            system_prompt = DATASOPH_SYSTEM_TR_ADVANCED if language == 'tr' else DATASOPH_SYSTEM_EN_ADVANCED
            
            if file_data:
                prompt = f"""Kullanıcı veri yüklemiş ve şunu soruyor: {user_message}

Veri analizi:
{file_data}

Lütfen:
1. Veriyi analiz et (pattern'lar, trends, outliers)
2. ML model önerileri sun
3. İstatistiksel insights ver
4. Görselleştirme öner
5. İş değeri çıkar
6. Pratik kod örnekleri ekle

Doğal konuş, actionable öneriler ver.""" if language == 'tr' else f"""User uploaded data and asks: {user_message}

Data analysis:
{file_data}

Please:
1. Analyze data (patterns, trends, outliers)
2. Suggest ML models
3. Provide statistical insights
4. Recommend visualizations
5. Extract business value
6. Include practical code examples

Be natural, give actionable recommendations."""
            else:
                prompt = user_message
            
            response = await self._call_ai_advanced(system_prompt, prompt)
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Üzgünüm, bir hata oluştu: {str(e)}"
    
    async def analyze_data_comprehensive(self, file_path: str, user_query: str) -> str:
        """Comprehensive data science analysis"""
        try:
            # Advanced data analysis
            analysis_results = await self._perform_advanced_analysis(file_path)
            
            language = self._detect_language(user_query)
            system_prompt = DATASOPH_SYSTEM_TR_ADVANCED if language == 'tr' else DATASOPH_SYSTEM_EN_ADVANCED
            
            if language == 'tr':
                prompt = f"""Kullanıcı sorusu: "{user_query}"

KAPSAMLI VERİ ANALİZİ:
{analysis_results}

Lütfen şunları yap:
1. 📊 VERİ ÖZETİ: Temel istatistikler ve yapı
2. 🔍 PATTERN ANALİZİ: Önemli bulgular ve trends
3. 🤖 ML ÖNERİLERİ: Hangi modeller uygun, neden?
4. 📈 GÖRSELLEŞTİRME: Hangi grafikler yapılmalı
5. ⚠️ DATA QUALITY: Eksik veri, outlier, temizlik önerileri
6. 💡 İŞ INSİGHTS: Pratik çıkarımlar ve öneriler
7. 🛠️ KOD ÖRNEKLERİ: Çalıştırılabilir Python kodu

Kullanıcının sorusuna odaklan ama kapsamlı analiz sun."""
            else:
                prompt = f"""User question: "{user_query}"

COMPREHENSIVE DATA ANALYSIS:
{analysis_results}

Please provide:
1. 📊 DATA SUMMARY: Basic stats and structure
2. 🔍 PATTERN ANALYSIS: Key findings and trends  
3. 🤖 ML RECOMMENDATIONS: Which models fit and why?
4. 📈 VISUALIZATION: What charts to create
5. ⚠️ DATA QUALITY: Missing data, outliers, cleaning tips
6. 💡 BUSINESS INSIGHTS: Practical takeaways and recommendations
7. 🛠️ CODE EXAMPLES: Runnable Python code

Focus on user's question but provide comprehensive analysis."""
            
            response = await self._call_ai_advanced(system_prompt, prompt)
            return response
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}")
            return f"Analiz hatası: {str(e)}"
    
    # Keep the simple method for backward compatibility
    async def analyze_data_simple(self, file_path: str, user_query: str) -> str:
        """Simple analysis (backward compatibility)"""
        return await self.analyze_data_comprehensive(file_path, user_query)
    
    async def _perform_advanced_analysis(self, file_path: str) -> str:
        """Perform comprehensive data science analysis"""
        try:
            results = []
            file_ext = Path(file_path).suffix.lower()
            
            # Load data
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            else:
                return "Desteklenmeyen dosya formatı"
            
            # Basic info
            results.append(f"📊 TEMEL BİLGİLER:")
            results.append(f"Boyut: {df.shape[0]:,} satır × {df.shape[1]:,} sütun")
            results.append(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            # Column analysis
            results.append(f"\n🔍 SÜTUN ANALİZİ:")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            results.append(f"Sayısal sütunlar ({len(numeric_cols)}): {', '.join(numeric_cols[:5])}{'...' if len(numeric_cols) > 5 else ''}")
            results.append(f"Kategorik sütunlar ({len(categorical_cols)}): {', '.join(categorical_cols[:5])}{'...' if len(categorical_cols) > 5 else ''}")
            if datetime_cols:
                results.append(f"Tarih sütunları ({len(datetime_cols)}): {', '.join(datetime_cols)}")
            
            # Missing data analysis
            missing_data = df.isnull().sum()
            missing_pct = (missing_data / len(df)) * 100
            missing_info = missing_data[missing_data > 0].sort_values(ascending=False)
            
            if len(missing_info) > 0:
                results.append(f"\n⚠️ EKSİK VERİ:")
                for col in missing_info.head().index:
                    results.append(f"{col}: {missing_info[col]:,} ({missing_pct[col]:.1f}%)")
            else:
                results.append(f"\n✅ EKSİK VERİ: Yok")
            
            # Statistical summary for numeric columns
            if numeric_cols:
                results.append(f"\n📈 SAYISAL VERİ ÖZETİ:")
                desc = df[numeric_cols].describe()
                for col in numeric_cols[:3]:  # Top 3 numeric columns
                    if col in desc.columns:
                        results.append(f"{col}: μ={desc[col]['mean']:.2f}, σ={desc[col]['std']:.2f}, min={desc[col]['min']:.2f}, max={desc[col]['max']:.2f}")
            
            # Categorical analysis  
            if categorical_cols:
                results.append(f"\n🏷️ KATEGORİK ANALİZ:")
                for col in categorical_cols[:3]:  # Top 3 categorical columns
                    unique_count = df[col].nunique()
                    top_value = df[col].value_counts().index[0] if len(df[col].value_counts()) > 0 else "N/A"
                    results.append(f"{col}: {unique_count:,} benzersiz değer, en çok: '{top_value}'")
            
            # Correlation analysis (if enough numeric columns)
            if len(numeric_cols) >= 2:
                results.append(f"\n🔗 KORELASYON ANALİZİ:")
                corr_matrix = df[numeric_cols].corr()
                # Find highest correlations
                high_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.5:  # Strong correlation
                            high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
                
                if high_corr:
                    high_corr.sort(key=lambda x: abs(x[2]), reverse=True)
                    for col1, col2, corr_val in high_corr[:3]:
                        results.append(f"{col1} ↔ {col2}: {corr_val:.3f}")
                else:
                    results.append("Güçlü korelasyon bulunamadı (|r| > 0.5)")
            
            # Outlier detection for numeric columns
            if numeric_cols:
                results.append(f"\n🎯 OUTLIER ANALİZİ:")
                outlier_info = []
                for col in numeric_cols[:3]:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                    if len(outliers) > 0:
                        outlier_info.append(f"{col}: {len(outliers):,} outlier ({len(outliers)/len(df)*100:.1f}%)")
                
                if outlier_info:
                    results.extend(outlier_info)
                else:
                    results.append("Belirgin outlier tespit edilmedi")
            
            # Machine Learning readiness assessment
            results.append(f"\n🤖 ML HAZıRLıK DEĞERLENDİRMESİ:")
            ml_score = 0
            ml_notes = []
            
            # Data size
            if len(df) >= 1000:
                ml_score += 2
                ml_notes.append("✅ Yeterli veri boyutu")
            elif len(df) >= 100:
                ml_score += 1
                ml_notes.append("⚠️ Orta veri boyutu")
            else:
                ml_notes.append("❌ Az veri")
            
            # Feature variety
            if len(numeric_cols) >= 3:
                ml_score += 2
                ml_notes.append("✅ Yeterli sayısal özellik")
            elif len(numeric_cols) >= 1:
                ml_score += 1
                ml_notes.append("⚠️ Az sayısal özellik")
            
            # Missing data
            missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
            if missing_ratio < 0.1:
                ml_score += 2
                ml_notes.append("✅ Az eksik veri")
            elif missing_ratio < 0.3:
                ml_score += 1
                ml_notes.append("⚠️ Orta eksik veri")
            else:
                ml_notes.append("❌ Çok eksik veri")
            
            results.append(f"ML Hazırlık Skoru: {ml_score}/6")
            results.extend(ml_notes)
            
            # Suggested ML models based on data characteristics
            results.append(f"\n🎯 ÖNERILEN ML MODELLERİ:")
            if len(numeric_cols) >= 2:
                if categorical_cols and df[categorical_cols[0]].nunique() < 10:
                    results.append("🔮 Sınıflandırma: Random Forest, XGBoost, SVM")
                results.append("📈 Regresyon: Linear Regression, Random Forest, XGBoost")
                if len(df) >= 500:
                    results.append("🧠 Gelişmiş: Neural Networks, Ensemble Methods")
            
            if len(numeric_cols) >= 3:
                results.append("🔍 Kümeleme: K-Means, DBSCAN")
                results.append("📊 Boyut Azaltma: PCA, t-SNE")
            
            # Time series check
            if datetime_cols and numeric_cols:
                results.append("⏰ Zaman Serileri: Prophet, ARIMA, LSTM")
            
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"Advanced analysis error: {e}")
            return f"Gelişmiş analiz hatası: {str(e)}"
    
    async def _call_ai_advanced(self, system_prompt: str, user_prompt: str) -> str:
        """Advanced AI call with enhanced capabilities"""
        if not self.api_key:
            return "API key yapılandırılmamış. OPENROUTER_API_KEY ayarlayın."
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 4000,  # Increased for comprehensive responses
                    },
                    timeout=90.0  # Increased timeout for complex analysis
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"AI API error: {response.status_code}")
                    return f"API hatası: {response.status_code}"
                    
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return f"AI servisi hatası: {str(e)}"

# Global AI service instance
datasoph_ai = DataSophAI() 