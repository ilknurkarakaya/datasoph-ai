"""
DATASOPH AI - AI Chat Feature Tests
Test cases for the AI chat functionality
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import json
from ai_chat_feature import AIChatFeature


class TestAIChatFeature(unittest.TestCase):
    """Test cases for AIChatFeature class"""
    
    def setUp(self):
        """Set up test environment"""
        self.ai_chat = AIChatFeature()
    
    def test_initialization(self):
        """Test AI Chat Feature initialization"""
        self.assertIsNotNone(self.ai_chat)
        self.assertEqual(self.ai_chat.model, "anthropic/claude-3-sonnet")
        self.assertEqual(len(self.ai_chat.conversation_history), 0)
    
    def test_add_message_to_history(self):
        """Test adding messages to conversation history"""
        self.ai_chat.add_message_to_history("user", "Hello")
        self.ai_chat.add_message_to_history("assistant", "Hi there!")
        
        self.assertEqual(len(self.ai_chat.conversation_history), 2)
        self.assertEqual(self.ai_chat.conversation_history[0]["role"], "user")
        self.assertEqual(self.ai_chat.conversation_history[0]["content"], "Hello")
        self.assertEqual(self.ai_chat.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.ai_chat.conversation_history[1]["content"], "Hi there!")
    
    def test_get_conversation_context(self):
        """Test getting conversation context"""
        # Add some messages
        self.ai_chat.add_message_to_history("user", "Hello")
        self.ai_chat.add_message_to_history("assistant", "Hi there!")
        self.ai_chat.add_message_to_history("user", "How are you?")
        
        context = self.ai_chat.get_conversation_context()
        
        self.assertEqual(len(context), 3)
        self.assertEqual(context[0]["role"], "user")
        self.assertEqual(context[0]["content"], "Hello")
    
    def test_mock_response_generation(self):
        """Test mock response generation"""
        # Test hello response
        response = self.ai_chat._get_mock_response("hello")
        self.assertIn("DATASOPH AI", response)
        self.assertIn("data science assistant", response)
        
        # Test data analysis response
        response = self.ai_chat._get_mock_response("data analysis")
        self.assertIn("data analysis", response)
        self.assertIn("CSV", response)
        
        # Test statistics response
        response = self.ai_chat._get_mock_response("statistics")
        self.assertIn("statistics", response)
        self.assertIn("t-tests", response)
        
        # Test help response
        response = self.ai_chat._get_mock_response("help")
        self.assertIn("help", response)
        self.assertIn("data analysis", response)
    
    def test_chat_functionality(self):
        """Test main chat functionality"""
        result = self.ai_chat.chat("Hello")
        
        self.assertTrue(result["success"])
        self.assertIn("response", result)
        self.assertIn("model_used", result)
        self.assertIn("timestamp", result)
        self.assertIn("conversation_length", result)
        
        # Check that conversation history was updated
        self.assertEqual(len(self.ai_chat.conversation_history), 2)  # user + assistant
    
    def test_conversation_summary(self):
        """Test conversation summary generation"""
        # Add some messages
        self.ai_chat.chat("Hello")
        self.ai_chat.chat("How are you?")
        
        summary = self.ai_chat.get_conversation_summary()
        
        self.assertIn("total_messages", summary)
        self.assertIn("user_messages", summary)
        self.assertIn("ai_messages", summary)
        self.assertIn("start_time", summary)
        self.assertIn("last_message", summary)
        
        self.assertEqual(summary["user_messages"], 2)
        self.assertEqual(summary["ai_messages"], 2)
        self.assertEqual(summary["total_messages"], 4)
    
    def test_clear_conversation(self):
        """Test clearing conversation history"""
        # Add some messages
        self.ai_chat.chat("Hello")
        self.assertEqual(len(self.ai_chat.conversation_history), 2)
        
        # Clear conversation
        self.ai_chat.clear_conversation()
        self.assertEqual(len(self.ai_chat.conversation_history), 0)
    
    def test_export_conversation(self):
        """Test conversation export functionality"""
        # Add some messages
        self.ai_chat.chat("Hello")
        self.ai_chat.chat("How are you?")
        
        # Export conversation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            exported_file = self.ai_chat.export_conversation(filename)
            
            # Check that file was created
            self.assertTrue(os.path.exists(exported_file))
            
            # Check file content
            with open(exported_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn("conversation", data)
            self.assertIn("summary", data)
            self.assertIn("export_timestamp", data)
            
        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
    
    @patch('requests.post')
    def test_api_call_with_key(self, mock_post):
        """Test API call when API key is provided"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response
        
        # Create AI chat with API key
        ai_chat = AIChatFeature(api_key="test_key")
        
        # Test API call
        messages = [{"role": "user", "content": "Hello"}]
        response = ai_chat.call_openrouter_api(messages)
        
        self.assertEqual(response, "Test response")
        mock_post.assert_called_once()
    
    def test_api_call_without_key(self):
        """Test API call when no API key is provided"""
        ai_chat = AIChatFeature(api_key=None)
        
        messages = [{"role": "user", "content": "Hello"}]
        response = ai_chat.call_openrouter_api(messages)
        
        # Should return mock response
        self.assertIn("DATASOPH AI", response)
        self.assertIn("data science assistant", response)


def run_tests():
    """Run all tests"""
    print("🧪 Running AI Chat Feature Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAIChatFeature)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
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
        print("\n✅ All tests passed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests() 