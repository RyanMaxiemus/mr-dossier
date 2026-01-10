#!/usr/bin/env python3
"""
Quick test to verify Ollama connectivity
"""

try:
    from langchain_community.llms import Ollama

    print("Testing Ollama connection...")
    llm = Ollama(
        model="llama3",
        timeout=10,
        base_url="http://localhost:11434"
    )

    response = llm.invoke("Say 'Hello, I am working!' in exactly those words.")
    print(f"✅ Ollama response: {response}")

except Exception as e:
    print(f"❌ Ollama test failed: {e}")
    print("\nTroubleshooting:")
    print("1. Start Ollama: ollama serve")
    print("2. Pull model: ollama pull llama3")
    print("3. Test manually: ollama run llama3 'hello'")
    print("4. Check if Ollama is running: curl http://localhost:11434")
