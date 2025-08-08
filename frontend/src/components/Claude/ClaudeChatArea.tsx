import React, { useState, useEffect } from 'react';
import { useSidebar, useChat } from '../../App';
import WelcomeLayout from './WelcomeLayout';
import ConversationLayout from './ConversationLayout';
import { chatService } from '../../services/api';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

type TypingStage = 'thinking' | 'analyzing' | 'processing' | 'generating';

const ClaudeChatArea: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [typingStage, setTypingStage] = useState<TypingStage>('thinking');
  const { toggleSidebar } = useSidebar();
  const { hasMessages, setHasMessages, onNewChat } = useChat();
  
  // Listen for new chat trigger
  useEffect(() => {
    const handleNewChat = () => {
      setMessages([]);
      setInputValue('');
      setIsTyping(false);
      setHasMessages(false);
    };
    
    // Store the function globally for the context to call
    (window as any).triggerNewChat = handleNewChat;
    
    return () => {
      delete (window as any).triggerNewChat;
    };
  }, [setHasMessages]);
  
  // Update hasMessages when messages change
  useEffect(() => {
    setHasMessages(messages.length > 0);
  }, [messages, setHasMessages]);
  
  const generateAIResponse = (userMessage: string): string => {
    // Enhanced AI responses for data science context
    const responses = {
      dataset: `Thank you for your question about: "${userMessage}"

I'm DataSoph AI, your professional data science assistant. Here's how I can help you:

**📊 Data Analysis Approach**
- Statistical analysis and hypothesis testing
- Exploratory data analysis (EDA) with visualizations
- Data quality assessment and cleaning recommendations

**🤖 Machine Learning Solutions**
- Predictive modeling and classification
- Feature engineering and selection strategies
- Model evaluation and validation techniques

**💼 Business Intelligence**
- KPI development and tracking
- Dashboard creation and reporting
- Data-driven decision making frameworks

**🔧 Technical Implementation**
- Python/R code generation for analysis
- SQL queries for data extraction
- Best practices for data pipeline development

To provide more specific guidance, please:
1. **Upload your dataset** (CSV, Excel, JSON supported)
2. **Describe your business objective** and success metrics
3. **Share any specific challenges** or constraints

What would you like to focus on first?`,
      
      model: `Excellent question about: "${userMessage}"

**🎯 Machine Learning Strategy**

For building effective predictive models, I recommend this systematic approach:

**1. Problem Definition**
- Classification vs. Regression vs. Clustering
- Success metrics (Accuracy, Precision, Recall, RMSE, etc.)
- Business constraints and requirements

**2. Data Preparation**
- Feature engineering and transformation
- Handling missing values and outliers
- Train/validation/test split strategies

**3. Model Selection**
- Algorithm comparison (Tree-based, Linear, Neural Networks)
- Cross-validation and hyperparameter tuning
- Ensemble methods for improved performance

**4. Evaluation & Deployment**
- Model interpretability and explainability
- Performance monitoring and drift detection
- Production deployment considerations

**Next Steps:**
Upload your dataset and describe your prediction target. I'll provide specific model recommendations and implementation code.

What type of prediction problem are you working on?`,
      
      visualization: `Great question about: "${userMessage}"

**📈 Data Visualization Strategy**

I'll help you create compelling visualizations that tell your data story:

**1. Exploratory Visualizations**
- Distribution plots and histograms
- Correlation matrices and scatter plots
- Time series trend analysis

**2. Statistical Visualizations**
- Box plots for outlier detection
- Violin plots for distribution comparison
- Statistical test result visualizations

**3. Business Dashboard Components**
- KPI indicators and gauge charts
- Interactive filtering and drill-down
- Real-time data monitoring displays

**4. Advanced Analytics Plots**
- Feature importance visualizations
- Model performance comparison charts
- Prediction confidence intervals

**Tools & Libraries:**
- Python: Matplotlib, Seaborn, Plotly, Streamlit
- R: ggplot2, Shiny, plotly
- Business Intelligence: Tableau, Power BI integration

Share your data and visualization goals - I'll create the perfect charts for your analysis!`,
      
      statistics: `Excellent statistical question: "${userMessage}"

**🔍 Statistical Analysis Framework**

I'll guide you through rigorous statistical analysis:

**1. Descriptive Statistics**
- Central tendency and variability measures
- Distribution shape and normality testing
- Outlier detection and treatment

**2. Inferential Statistics**
- Hypothesis testing (t-tests, ANOVA, chi-square)
- Confidence intervals and effect sizes
- Power analysis and sample size calculations

**3. Advanced Statistical Methods**
- Regression analysis (Linear, Logistic, Polynomial)
- Time series analysis and forecasting
- Bayesian statistics and probabilistic modeling

**4. Experimental Design**
- A/B testing and randomized controlled trials
- Factorial and fractional factorial designs
- Causal inference techniques

**Statistical Software:**
- Python: SciPy, Statsmodels, PyMC3
- R: Base stats, tidyverse, brms
- Specialized tools for specific analyses

What specific statistical question or hypothesis would you like to investigate?`
    };
    
    const message = userMessage.toLowerCase();
    if (message.includes('dataset') || message.includes('data') || message.includes('analyze')) {
      return responses.dataset;
    } else if (message.includes('model') || message.includes('predict') || message.includes('machine learning')) {
      return responses.model;
    } else if (message.includes('visual') || message.includes('chart') || message.includes('plot')) {
      return responses.visualization;
    } else if (message.includes('statistic') || message.includes('test') || message.includes('hypothesis')) {
      return responses.statistics;
    } else {
      return responses.dataset; // Default response
    }
  };
  
  const handleSendMessage = async (message: string, fileId?: string) => {
    if (!message.trim() || isTyping) return;
    
    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: message.trim(),
      timestamp: new Date().toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
      })
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    
    // Enhanced typing stages with spiral logo animations
    setTypingStage('thinking');
    
    setTimeout(() => setTypingStage('analyzing'), 800);
    setTimeout(() => setTypingStage('processing'), 1600);
    setTimeout(() => setTypingStage('generating'), 2400);
    
    try {
      // If there's a fileId, call the real API for file analysis
      if (fileId) {
        const response = await chatService.sendMessage({
          message: message.trim(),
          user_id: 'user-' + Date.now(),
          file_id: fileId
        });
        
        const aiMessage: Message = {
          id: Date.now() + 1,
          type: 'assistant',
          content: response.response,
          timestamp: new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
          })
        };
        
        setMessages(prev => [...prev, aiMessage]);
        setIsTyping(false);
      } else {
        // Use the existing mock response for regular chat
        setTimeout(() => {
          const aiMessage: Message = {
            id: Date.now() + 1,
            type: 'assistant',
            content: generateAIResponse(message),
            timestamp: new Date().toLocaleTimeString('en-US', { 
              hour: 'numeric', 
              minute: '2-digit',
              hour12: true 
            })
          };
          
          setMessages(prev => [...prev, aiMessage]);
          setIsTyping(false);
        }, 3200);
      }
    } catch (error) {
      console.error('Chat error:', error);
      
      // Fallback to mock response on error
      setTimeout(() => {
        const aiMessage: Message = {
          id: Date.now() + 1,
          type: 'assistant',
          content: "I apologize, but I'm having trouble processing your request right now. Please try again or upload your file again.",
          timestamp: new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
          })
        };
        
        setMessages(prev => [...prev, aiMessage]);
        setIsTyping(false);
      }, 3200);
    }
  };
  
  return (
    <div className="flex flex-col h-full">
      {/* Header with Sidebar Toggle */}
      <div className="flex items-center p-3 border-b border-[var(--border-light)] bg-[var(--bg-main)] flex-shrink-0">
        <button
          onClick={toggleSidebar}
          className="p-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] rounded-md transition-colors"
          title="Toggle sidebar"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div className="flex-1" />
      </div>
      
      {/* Main Content Area */}
      <div className="flex-1 min-h-0">
        {hasMessages ? (
          // Conversation Layout (Input at Bottom)
          <ConversationLayout 
            messages={messages}
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
            isTyping={isTyping}
            typingStage={typingStage}
          />
        ) : (
          // Welcome Layout (Input Centered)
          <WelcomeLayout
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSendMessage={handleSendMessage}
          />
        )}
      </div>
    </div>
  );
};

export default ClaudeChatArea; 