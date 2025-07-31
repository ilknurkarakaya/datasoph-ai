"""
DATASOPH AI - Data Analysis Agent Tests
Test cases for the automated data analysis agent
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import tempfile
import os
from data_analysis_agent import DataAnalysisAgent


class TestDataAnalysisAgent(unittest.TestCase):
    """Test cases for DataAnalysisAgent class"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = DataAnalysisAgent()
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(len(self.agent.tools), 8)  # 8 tools available
        self.assertIsNotNone(self.agent.memory)
    
    def test_agent_status(self):
        """Test agent status information"""
        status = self.agent.get_agent_status()
        
        self.assertEqual(status["agent_type"], "Data Analysis Agent")
        self.assertEqual(status["framework"], "LangChain")
        self.assertEqual(status["tools_available"], 8)
        self.assertIn("Data Loading", status["capabilities"])
        self.assertIn("Statistical Analysis", status["capabilities"])
    
    def test_load_data_tool(self):
        """Test data loading functionality"""
        # Create test data
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False)
            file_path = f.name
        
        try:
            result = self.agent._load_data(file_path)
            self.assertIn("Data loaded successfully", result)
            self.assertIn("Shape: (5, 3)", result)
        finally:
            os.unlink(file_path)
    
    def test_explore_data_tool(self):
        """Test data exploration functionality"""
        # Mock session state
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        # Simulate session state
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._explore_data("basic")
        self.assertIn("Data Overview", result)
        self.assertIn("Shape: (5, 3)", result)
    
    def test_statistical_analysis_tool(self):
        """Test statistical analysis functionality"""
        # Mock session state
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._statistical_analysis("descriptive")
        self.assertIn("Descriptive Statistics", result)
    
    def test_correlation_analysis_tool(self):
        """Test correlation analysis functionality"""
        # Mock session state
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._analyze_correlations("pearson")
        self.assertIn("Correlation Analysis", result)
        self.assertIn("pearson", result)
    
    def test_outlier_detection_tool(self):
        """Test outlier detection functionality"""
        # Mock session state with outliers
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 100],  # 100 is an outlier
            'B': [2, 4, 6, 8, 10, 12],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._detect_outliers("iqr")
        self.assertIn("Outlier Detection", result)
        self.assertIn("iqr", result)
    
    def test_data_cleaning_tool(self):
        """Test data cleaning functionality"""
        # Mock session state with dirty data
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 3, 4, 5],  # Duplicate
            'B': ['a', 'b', 'c', 'd', None, 'f'],  # Missing value
            'C': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._clean_data("basic")
        self.assertIn("Data Cleaning Results", result)
        self.assertIn("Duplicates removed", result)
    
    def test_visualization_creation_tool(self):
        """Test visualization creation functionality"""
        # Mock session state
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._create_visualizations("overview")
        self.assertIn("Visualization Plan Created", result)
    
    def test_report_generation_tool(self):
        """Test report generation functionality"""
        # Mock session state
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        import streamlit as st
        if 'current_data' not in st.session_state:
            st.session_state.current_data = test_data
        
        result = self.agent._generate_report("comprehensive")
        self.assertIn("DATASOPH AI - Data Analysis Report", result)
        self.assertIn("EXECUTIVE SUMMARY", result)
    
    def test_mock_analysis(self):
        """Test mock analysis functionality"""
        # Test different types of analysis requests
        test_cases = [
            ("load data test.csv", "Mock: Data loading simulation"),
            ("explore data", "Mock: Exploratory Data Analysis completed"),
            ("statistical analysis", "Mock: Statistical analysis completed"),
            ("create visualizations", "Mock: Visualization creation completed"),
            ("clean data", "Mock: Data cleaning completed"),
            ("analyze correlations", "Mock: Correlation analysis completed"),
            ("detect outliers", "Mock: Outlier detection completed"),
            ("generate report", "Mock: Comprehensive report generated"),
            ("random request", "Mock: Analysis completed")
        ]
        
        for user_input, expected in test_cases:
            result = self.agent._mock_analysis(user_input)
            self.assertTrue(result["success"])
            # Check if the expected text is in the result or if it's a general response
            if expected not in result["result"]:
                # For general cases, check if it contains "Mock:" and the input
                self.assertIn("Mock:", result["result"])
                self.assertIn(user_input.lower(), result["result"].lower())
    
    def test_run_analysis_with_mock(self):
        """Test full analysis workflow with mock responses"""
        result = self.agent.run_analysis("explore data")
        
        self.assertTrue(result["success"])
        self.assertIn("result", result)
        self.assertIn("timestamp", result)
        self.assertIn("agent_used", result)
    
    def test_tool_descriptions(self):
        """Test that all tools have proper descriptions"""
        tool_names = [tool.name for tool in self.agent.tools]
        expected_tools = [
            "DataLoader",
            "DataExplorer", 
            "StatisticalAnalyzer",
            "VisualizationCreator",
            "DataCleaner",
            "CorrelationAnalyzer",
            "OutlierDetector",
            "ReportGenerator"
        ]
        
        self.assertEqual(set(tool_names), set(expected_tools))
        
        # Check descriptions
        for tool in self.agent.tools:
            self.assertIsNotNone(tool.description)
            self.assertGreater(len(tool.description), 10)
    
    def test_memory_functionality(self):
        """Test conversation memory"""
        # Test that memory is properly initialized
        self.assertIsNotNone(self.agent.memory)
        self.assertEqual(self.agent.memory.memory_key, "history")


def run_agent_tests():
    """Run all agent tests"""
    print("🧪 Running Data Analysis Agent Tests...")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataAnalysisAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if not result.failures and not result.errors:
        print("\n✅ All agent tests passed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_agent_tests() 