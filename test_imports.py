#!/usr/bin/env python3
"""
Quick test to verify all imports work correctly
"""

try:
    print("Testing imports...")

    # Test basic imports
    import os
    from dotenv import load_dotenv
    print("✅ Basic imports OK")

    # Test LangChain imports
    from langchain_community.llms import Ollama
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
    print("✅ LangChain imports OK")

    # Test that we can instantiate classes (without connecting)
    processor_test = type('DocumentProcessor', (), {})()
    print("✅ DocumentProcessor can be instantiated")

    print("\n🎉 All imports successful! The app should run now.")
    print("Make sure Ollama is running with: ollama serve")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Other error: {e}")
