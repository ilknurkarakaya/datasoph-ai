"""
DataSoph AI Backend - Entry Point
World-class AI Data Scientist with comprehensive analysis capabilities
"""

import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"""
🚀 DataSoph AI - World's Most Advanced Data Science Platform
===============================================================
🔬 Machine Learning: XGBoost, LightGBM, CatBoost, TensorFlow, PyTorch
📊 Statistics: Advanced statistical tests, Bayesian analysis
📈 Visualization: Plotly, Seaborn, Bokeh, Altair
⏰ Time Series: Prophet, ARIMA, Feature extraction
🧠 NLP: spaCy, NLTK, Transformers, Word clouds
👁️ Computer Vision: OpenCV, scikit-image
🗺️ Geospatial: GeoPandas, Folium
🚀 Performance: Numba JIT, Dask parallel computing
📋 Data Quality: Great Expectations, Pandera validation
🏗️ Feature Engineering: Automated feature creation
📊 Model Monitoring: MLflow, Weights & Biases

Starting on: http://localhost:8000
API Docs: http://localhost:8000/docs
===============================================================
    """)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 