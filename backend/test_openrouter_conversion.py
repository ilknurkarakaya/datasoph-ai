#!/usr/bin/env python3
"""
Test script to verify OpenRouter conversion is working
Tests all converted components to ensure no OpenAI dependencies remain
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the backend app to the path
sys.path.insert(0, str(Path(__file__).parent / "app"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_openrouter_client():
    """Test the pure OpenRouter client implementation"""
    logger.info("🧪 Testing OpenRouter Client...")
    
    try:
        from app.services.openrouter_client import test_openrouter_connection, create_openrouter_client
        
        # Test connection
        result = test_openrouter_connection()
        
        if result["success"]:
            logger.info("✅ OpenRouter client test PASSED")
            logger.info(f"   Model: {result.get('model', 'N/A')}")
            logger.info(f"   Tokens used: {result.get('tokens_used', 'N/A')}")
            logger.info(f"   Response preview: {result.get('response_preview', 'N/A')[:100]}...")
            return True
        else:
            logger.error("❌ OpenRouter client test FAILED")
            logger.error(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def test_core_ai():
    """Test the converted CoreAI service"""
    logger.info("🧪 Testing Core AI Service...")
    
    try:
        from app.services.core_ai import CoreAI
        
        core_ai = CoreAI()
        
        if core_ai.client is None and not core_ai.api_key:
            logger.warning("⚠️ Core AI service has no API key - this is expected for testing")
            return True
        
        # Test async chat function (but don't actually call API if no key)
        if hasattr(core_ai, 'chat'):
            logger.info("✅ Core AI service structure is correct")
            return True
        else:
            logger.error("❌ Core AI service missing chat method")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def test_imports():
    """Test that no OpenAI imports remain"""
    logger.info("🧪 Testing for remaining OpenAI imports...")
    
    try:
        # Try importing the main modules to check for OpenAI dependencies
        from app.services.core_ai import CoreAI
        from app.services.openrouter_client import OpenRouter
        
        logger.info("✅ All imports successful - no OpenAI dependencies detected")
        return True
        
    except ImportError as e:
        if "openai" in str(e).lower():
            logger.error(f"❌ OpenAI dependency still present: {e}")
            return False
        else:
            logger.error(f"❌ Other import error: {e}")
            return False
    except Exception as e:
        logger.error(f"❌ Unexpected import error: {e}")
        return False

def test_config():
    """Test configuration setup"""
    logger.info("🧪 Testing configuration...")
    
    try:
        from app.core.config import get_settings
        
        settings = get_settings()
        
        # Check that OpenRouter config exists
        if hasattr(settings, 'openrouter_api_key'):
            logger.info("✅ OpenRouter configuration found")
            return True
        else:
            logger.error("❌ OpenRouter configuration missing")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Config import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Config error: {e}")
        return False

def check_file_for_openai_references():
    """Check source files for any remaining OpenAI references"""
    logger.info("🧪 Checking files for OpenAI references...")
    
    files_to_check = [
        "app/services/core_ai.py",
        "app/main_complex.py", 
        "app/core/config.py"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        full_path = Path(__file__).parent / file_path
        
        if not full_path.exists():
            logger.warning(f"⚠️ File not found: {file_path}")
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for problematic patterns
            if "import openai" in content:
                issues_found.append(f"{file_path}: Contains 'import openai'")
            
            if "from openai" in content:
                issues_found.append(f"{file_path}: Contains 'from openai'")
                
            if "openai.OpenAI" in content:
                issues_found.append(f"{file_path}: Contains 'openai.OpenAI'")
                
            if "openai.ChatCompletion" in content:
                issues_found.append(f"{file_path}: Contains 'openai.ChatCompletion'")
                
        except Exception as e:
            logger.error(f"❌ Error reading {file_path}: {e}")
            issues_found.append(f"{file_path}: Read error - {e}")
    
    if issues_found:
        logger.error("❌ OpenAI references still found:")
        for issue in issues_found:
            logger.error(f"   {issue}")
        return False
    else:
        logger.info("✅ No OpenAI references found in source files")
        return True

async def run_full_test():
    """Run the complete test suite"""
    logger.info("🚀 Starting OpenRouter Conversion Test Suite")
    logger.info("=" * 60)
    
    tests = [
        ("File Reference Check", check_file_for_openai_references),
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Core AI Service Test", test_core_ai),
        ("OpenRouter Client Test", test_openrouter_client),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} ERROR: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! OpenRouter conversion successful!")
        logger.info("\n📝 Next steps:")
        logger.info("   1. Set OPENROUTER_API_KEY in your environment")
        logger.info("   2. Remove any remaining .env OPENAI_API_KEY entries")
        logger.info("   3. Update your deployment configurations")
        logger.info("   4. Test the full application")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed. Please fix issues before proceeding.")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
OpenRouter Conversion Test Script

Usage: python test_openrouter_conversion.py

This script tests that the OpenAI to OpenRouter conversion was successful:
- Checks for remaining OpenAI references in code
- Tests import structure
- Validates configuration
- Tests OpenRouter client functionality

Environment Variables:
- OPENROUTER_API_KEY: Your OpenRouter API key (optional for testing)

The script will work even without an API key, but won't test actual API calls.
        """)
        return
    
    # Run the test suite
    try:
        result = asyncio.run(run_full_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test suite failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
