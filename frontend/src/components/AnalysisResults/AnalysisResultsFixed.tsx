import React, { useState, useEffect } from 'react';

interface AnalysisResultsProps {
  analysisData: {
    success: boolean;
    response: string;
    charts_generated?: number;
    processing_time?: number;
    session_id?: string;
    analysis_completed?: boolean;
    message?: string;
  } | null;
  onClose?: () => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysisData, onClose }) => {
  const [charts, setCharts] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'insights' | 'charts'>('insights');
  
  useEffect(() => {
    const loadCharts = async () => {
      if (analysisData && analysisData.success) {
        try {
          console.log('📊 Loading charts for analysis results...');
          
          // List of possible chart names
          const possibleCharts = [
            'correlation_heatmap.png',
            'distributions.png',
            'boxplots.png',
            'missing_values_analysis.png',
            'outlier_analysis.png',
            'business_revenue_by_date.png',
            'business_revenue_by_product_category.png',
            'business_revenue_by_region.png',
            'timeseries_date_analysis.png'
          ];
          
          // Generate chart URLs
          const chartUrls = possibleCharts.map(name => 
            `http://localhost:8000/static/figures/${name}`
          );
          
          setCharts(chartUrls);
          console.log('✅ Chart URLs set:', chartUrls.length);
          
        } catch (error) {
          console.error('❌ Error loading charts:', error);
        }
      }
    };
    
    loadCharts();
  }, [analysisData]);

  if (!analysisData) {
    return null;
  }

  const styles = {
    modal: {
      position: 'fixed' as const,
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    },
    container: {
      backgroundColor: 'white',
      borderRadius: '12px',
      maxWidth: '900px',
      width: '100%',
      maxHeight: '80vh',
      overflow: 'hidden',
      boxShadow: '0 10px 25px rgba(0, 0, 0, 0.2)'
    },
    header: {
      background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
      color: 'white',
      padding: '20px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    tabs: {
      display: 'flex',
      borderBottom: '1px solid #e5e7eb',
      backgroundColor: '#f9fafb'
    },
    tab: {
      padding: '12px 24px',
      cursor: 'pointer',
      borderBottom: '2px solid transparent',
      fontSize: '14px',
      fontWeight: '500'
    },
    activeTab: {
      borderBottomColor: '#4f46e5',
      color: '#4f46e5',
      backgroundColor: 'white'
    },
    content: {
      padding: '20px',
      maxHeight: '60vh',
      overflowY: 'auto' as const
    },
    insightsBox: {
      background: 'linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%)',
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '20px'
    },
    responseText: {
      lineHeight: '1.6',
      whiteSpace: 'pre-wrap' as const,
      color: '#1f2937'
    },
    statsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '15px',
      marginTop: '20px'
    },
    statItem: {
      backgroundColor: '#f3f4f6',
      padding: '12px 16px',
      borderRadius: '8px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    chartsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
      gap: '20px',
      marginTop: '20px'
    },
    chartContainer: {
      backgroundColor: 'white',
      borderRadius: '8px',
      padding: '15px',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
      border: '1px solid #e5e7eb'
    },
    chartImage: {
      width: '100%',
      height: 'auto',
      borderRadius: '6px',
      maxHeight: '300px',
      objectFit: 'contain' as const
    },
    closeButton: {
      backgroundColor: 'transparent',
      border: 'none',
      color: 'white',
      fontSize: '24px',
      cursor: 'pointer',
      padding: '5px 10px',
      borderRadius: '4px'
    },
    errorBox: {
      background: 'linear-gradient(135deg, #fef2f2 0%, #fecaca 100%)',
      padding: '20px',
      borderRadius: '8px',
      color: '#dc2626',
      textAlign: 'center' as const
    }
  };

  return (
    <div style={styles.modal}>
      <div style={styles.container}>
        {/* Header */}
        <div style={styles.header}>
          <div>
            <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>
              🎯 DataSoph AI Analysis Results
            </h2>
            <p style={{ margin: '5px 0 0 0', opacity: 0.9 }}>
              Comprehensive Data Science Analysis
            </p>
          </div>
          {onClose && (
            <button 
              style={styles.closeButton}
              onClick={onClose}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.1)'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
              ×
            </button>
          )}
        </div>

        {/* Tabs */}
        <div style={styles.tabs}>
          <div 
            style={{
              ...styles.tab,
              ...(activeTab === 'insights' ? styles.activeTab : {})
            }}
            onClick={() => setActiveTab('insights')}
          >
            🧠 AI Insights
          </div>
          <div 
            style={{
              ...styles.tab,
              ...(activeTab === 'charts' ? styles.activeTab : {})
            }}
            onClick={() => setActiveTab('charts')}
          >
            📊 Charts ({charts.length})
          </div>
        </div>

        {/* Content */}
        <div style={styles.content}>
          {analysisData.success ? (
            <>
              {/* AI Insights Tab */}
              {activeTab === 'insights' && (
                <div>
                  <div style={styles.insightsBox}>
                    <h3 style={{ margin: '0 0 15px 0', color: '#0369a1' }}>
                      🧠 AI Expert Analysis
                    </h3>
                    <div style={styles.responseText}>
                      {analysisData.response || analysisData.message || 'Analysis completed successfully!'}
                    </div>
                  </div>

                  {/* Statistics */}
                  <div style={styles.statsGrid}>
                    <div style={styles.statItem}>
                      <span>Status:</span>
                      <span style={{ color: '#059669', fontWeight: 'bold' }}>Completed</span>
                    </div>
                    {analysisData.charts_generated && (
                      <div style={styles.statItem}>
                        <span>Charts Generated:</span>
                        <span style={{ color: '#2563eb', fontWeight: 'bold' }}>
                          {analysisData.charts_generated}
                        </span>
                      </div>
                    )}
                    {analysisData.processing_time && (
                      <div style={styles.statItem}>
                        <span>Processing Time:</span>
                        <span style={{ color: '#7c3aed', fontWeight: 'bold' }}>
                          {analysisData.processing_time.toFixed(2)}s
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Charts Tab */}
              {activeTab === 'charts' && (
                <div>
                  <h3 style={{ marginTop: 0 }}>📊 Generated Visualizations</h3>
                  
                  {charts.length > 0 ? (
                    <div style={styles.chartsGrid}>
                      {charts.map((chartUrl, index) => (
                        <div key={index} style={styles.chartContainer}>
                          <img
                            src={chartUrl}
                            alt={`Analysis Chart ${index + 1}`}
                            style={styles.chartImage}
                            onError={(e) => {
                              console.log(`❌ Failed to load chart: ${chartUrl}`);
                              const target = e.target as HTMLElement;
                              target.style.display = 'none';
                            }}
                            onLoad={() => {
                              console.log(`✅ Loaded chart: ${chartUrl}`);
                            }}
                          />
                          <div style={{ 
                            marginTop: '10px', 
                            textAlign: 'center', 
                            fontSize: '12px',
                            color: '#6b7280',
                            fontWeight: '500'
                          }}>
                            {chartUrl.split('/').pop()?.replace('.png', '').replace(/_/g, ' ').toUpperCase()}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div style={{ textAlign: 'center', padding: '40px 0' }}>
                      <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                      <h3 style={{ color: '#374151', marginBottom: '8px' }}>
                        No charts available yet
                      </h3>
                      <p style={{ color: '#6b7280' }}>
                        Charts will appear here once analysis is complete.
                      </p>
                    </div>
                  )}
                </div>
              )}
            </>
          ) : (
            <div style={styles.errorBox}>
              <h3 style={{ margin: '0 0 10px 0' }}>❌ Analysis Error</h3>
              <p style={{ margin: 0 }}>
                {analysisData.response || analysisData.message || 'Unknown error occurred'}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults; 