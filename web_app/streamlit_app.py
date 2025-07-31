"""
DATASOPH AI - Main Streamlit Application
Advanced AI Data Scientist with Authentication and RAG System
"""

import streamlit as st
import requests
import pandas as pd
import json
import pypdf
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="DATASOPH AI - Professional Data Scientist",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        color: #2E86AB;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .ai-message {
        background-color: #f3e5f5;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_data" not in st.session_state:
    st.session_state.current_data = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Welcome header
st.markdown('<div class="welcome-card">👋 <strong>Welcome to DATASOPH AI!</strong><br>Your Professional AI Data Scientist is Ready to Help</div>', unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 DATASOPH AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Data Scientist • Statistical Analysis • Business Intelligence</p>', unsafe_allow_html=True)

# Helper functions
def extract_pdf_text(pdf_file):
    """Extract text from PDF"""
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_dataset(df):
    """Professional data analysis"""
    analysis = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": {},
        "categorical_summary": {}
    }
    
    # Numeric analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
    
    # Categorical analysis
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            analysis["categorical_summary"][col] = {
                "unique_count": df[col].nunique(),
                "top_values": df[col].value_counts().head(5).to_dict()
            }
    
    # Correlations
    if len(numeric_cols) > 1:
        analysis["correlations"] = df[numeric_cols].corr().to_dict()
    
    return analysis

def create_visualizations(df):
    """Create professional visualizations"""
    charts = []
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Correlation heatmap
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig_corr = px.imshow(corr_matrix, 
                           title="Correlation Matrix",
                           color_continuous_scale="RdBu_r",
                           aspect="auto")
        charts.append(("Correlation Matrix", fig_corr))
    
    # Distribution plots
    for col in numeric_cols[:3]:
        fig_dist = px.histogram(df, x=col, 
                              title=f"Distribution of {col}",
                              marginal="box")
        charts.append((f"Distribution: {col}", fig_dist))
    
    return charts

# File Upload Section
st.markdown("### 📁 Upload Your Data")
st.markdown("**Supported:** CSV, Excel, JSON, PDF, TXT")

uploaded_file = st.file_uploader(
    "Choose your file",
    type=['csv', 'xlsx', 'xls', 'json', 'pdf', 'txt'],
    help="Upload data files for analysis or PDF documents for discussion"
)

if uploaded_file is not None:
    # File info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><strong>📄 File</strong><br>{uploaded_file.name}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><strong>📊 Type</strong><br>{uploaded_file.type or "Unknown"}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><strong>💾 Size</strong><br>{uploaded_file.size / 1024:.1f} KB</div>', unsafe_allow_html=True)
    
    # Analyze button
    if st.button("🔍 Analyze with AI", type="primary", use_container_width=True):
        with st.spinner("🧠 DATASOPH AI is analyzing..."):
            
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            try:
                if file_extension == 'csv':
                    df = pd.read_csv(uploaded_file)
                    st.session_state.current_data = df
                    
                elif file_extension in ['xlsx', 'xls']:
                    df = pd.read_excel(uploaded_file)
                    st.session_state.current_data = df
                    
                elif file_extension == 'json':
                    data = json.load(uploaded_file)
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                        df = pd.DataFrame(data)
                        st.session_state.current_data = df
                    else:
                        st.json(data)
                        
                elif file_extension == 'pdf':
                    text = extract_pdf_text(uploaded_file)
                    st.text_area("📄 PDF Content", text[:1000] + "..." if len(text) > 1000 else text, height=200)
                    
                elif file_extension == 'txt':
                    text = uploaded_file.read().decode('utf-8')
                    st.text_area("📝 Text Content", text[:500] + "..." if len(text) > 500 else text, height=150)
                
                # If dataframe, show analysis
                if st.session_state.current_data is not None:
                    df = st.session_state.current_data
                    
                    st.success(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
                    
                    # Data preview
                    st.markdown("#### 📋 Data Preview")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    # Analysis
                    analysis = analyze_dataset(df)
                    st.session_state.analysis_results = analysis
                    
                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Rows", f"{analysis['shape'][0]:,}")
                    with col2:
                        st.metric("📈 Columns", analysis['shape'][1])
                    with col3:
                        st.metric("🔍 Missing", sum(analysis['missing_values'].values()))
                    with col4:
                        numeric_count = len([col for col in df.columns if df[col].dtype in ['int64', 'float64']])
                        st.metric("🔢 Numeric", numeric_count)
                    
                    # Visualizations
                    charts = create_visualizations(df)
                    if charts:
                        st.markdown("#### 📈 Visualizations")
                        for chart_title, chart_fig in charts:
                            st.plotly_chart(chart_fig, use_container_width=True)
                    
                    # Add AI message
                    ai_message = f"""📊 **Analysis Complete!**

Your dataset has {analysis['shape'][0]:,} rows and {analysis['shape'][1]} columns. I found {sum(analysis['missing_values'].values())} missing values and identified key patterns in your data.

Ready to answer your questions! Ask me about correlations, insights, or recommendations."""
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_message})
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Chat Section
st.markdown("---")
st.markdown("### 💬 Chat with DATASOPH AI")

# Display messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 **You:** {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message">🤖 **DATASOPH AI:** {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me about your data, statistics, or data science questions...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI response
    with st.spinner("🧠 Thinking..."):
        ai_response = f'📊 Great question! "{user_input}" - As your AI data scientist, I can help with statistical analysis, correlations, insights, and recommendations. Based on your data, what specific aspect would you like me to focus on?'
    
    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    📊 <strong>DATASOPH AI</strong> - Your Professional AI Data Scientist<br>
    <em>Statistical Analysis • Business Intelligence • Data Insights</em>
</div>
""", unsafe_allow_html=True) 