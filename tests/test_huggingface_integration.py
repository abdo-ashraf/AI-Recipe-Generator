#!/usr/bin/env python
"""Test Hugging Face adapter integration."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from langchain_components.llm_providers.huggingface_adapter import HuggingFaceProvider
    print("✓ HuggingFaceProvider imported successfully")
except Exception as e:
    print(f"✗ Failed to import HuggingFaceProvider: {e}")
    sys.exit(1)

try:
    from langchain_components.llm_wrapper import get_llm_provider
    print("✓ get_llm_provider imported successfully")
except Exception as e:
    print(f"✗ Failed to import get_llm_provider: {e}")
    sys.exit(1)

# Test factory function with openai
try:
    provider_openai = get_llm_provider("openai", api_key="test_openai_key")
    print("✓ OpenAI provider created via factory")
except Exception as e:
    print(f"✗ Failed to create OpenAI provider: {e}")
    sys.exit(1)

# Test factory function with huggingface
try:
    provider_hf = get_llm_provider("huggingface", api_key="test_hf_key")
    print("✓ Hugging Face provider created via factory")
except Exception as e:
    print(f"✗ Failed to create Hugging Face provider: {e}")
    sys.exit(1)

# Test factory function with openrouter
try:
    provider_or = get_llm_provider("openrouter", api_key="test_openrouter_key")
    print("✓ OpenRouter provider created via factory")
except Exception as e:
    print(f"✗ Failed to create OpenRouter provider: {e}")
    sys.exit(1)

# Test invalid provider
try:
    provider_invalid = get_llm_provider("invalid_provider")
    print("✗ Should have raised ValueError for invalid provider")
    sys.exit(1)
except ValueError as e:
    print(f"✓ Correctly raised error for invalid provider: {e}")

print("\n✓ Provider integration tests passed!")
