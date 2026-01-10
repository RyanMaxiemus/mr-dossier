#!/usr/bin/env python3
"""
Very simple Ollama test with minimal data
"""

try:
    from langchain_community.llms import Ollama

    print("Testing minimal Ollama call...")
    llm = Ollama(
        model="llama3",
        timeout=15,
        base_url="http://localhost:11434"
    )

    # Very simple, short prompt
    response = llm.invoke("What is 2+2? Answer in one word.")
    print(f"✅ Ollama response: {response}")

except Exception as e:
    print(f"❌ Simple test failed: {e}")
    print("This suggests Ollama might be overloaded or the model is too slow.")
