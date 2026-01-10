#!/usr/bin/env python3
"""
Test if faster Ollama models are available
"""

from langchain_community.llms import Ollama

models_to_try = [
    "llama3.2:1b",  # Much faster, smaller model
    "llama3.2:3b",  # Medium speed
    "llama3",       # Current model
]

for model in models_to_try:
    try:
        print(f"Testing {model}...")
        llm = Ollama(model=model, timeout=10, base_url="http://localhost:11434")
        response = llm.invoke("Say 'OK' in one word.")
        print(f"✅ {model} works: {response.strip()}")
        break
    except Exception as e:
        print(f"❌ {model} failed: {e}")

print("\nTo install a faster model, try:")
print("ollama pull llama3.2:1b")
