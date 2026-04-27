#!/usr/bin/env python
"""
Comprehensive integration test for both OpenAI and Hugging Face providers.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=== AI Recipe Generator - Comprehensive Integration Test ===\n")

# Test 1: Import all core modules
print("Test 1: Importing core modules...")
try:
    from langchain_components.llm_providers.base import BaseLLMProvider
    from langchain_components.llm_providers.openai_adapter import OpenAIProvider
    from langchain_components.llm_providers.huggingface_adapter import HuggingFaceProvider
    from langchain_components.llm_providers.openrouter_adapter import OpenRouterProvider
    from langchain_components.chains import Orchestrator
    from langchain_components.output_parser import parse_recipe_output
    from langchain_components.llm_wrapper import get_llm_provider
    print("✓ All core modules imported successfully\n")
except Exception as e:
    print(f"✗ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Test provider factory
print("Test 2: Testing provider factory...")
providers_to_test = [
    ("openai", OpenAIProvider),
    ("huggingface", HuggingFaceProvider),
    ("openrouter", OpenRouterProvider),
]

for provider_name, expected_class in providers_to_test:
    try:
        provider = get_llm_provider(provider_name, api_key=f"test_{provider_name}_key")
        if isinstance(provider, expected_class):
            print(f"✓ {provider_name.capitalize()} provider created successfully")
        else:
            print(f"✗ {provider_name} provider is not an instance of {expected_class.__name__}")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Failed to create {provider_name} provider: {e}")
        sys.exit(1)

print()

# Test 3: Test output parser
print("Test 3: Testing output parser...")
sample_outputs = [
    """---RECIPE-START---
Title: Simple Tomato Soup
Language: English
Ingredients:
- 3 tomatoes
- 1 onion
- 2 cups water
Steps:
1. Chop vegetables
2. Boil water
3. Add vegetables and simmer
Estimated time: 25 minutes
Estimated calories: 120 kcal
Estimated cost: USD 4
Alternatives:
- tomatoes -> canned tomatoes (cheaper)
---RECIPE-END---""",
    """---RECIPE-START---
Title: حساء الطماطم البسيط
Language: Arabic
Ingredients:
- 3 طماطم
- 1 بصلة
- 2 كوب ماء
Steps:
1. قطع الخضار
2. غلي الماء
3. أضيف الخضار واترك على نار هادئة
Estimated time: 25 دقيقة
Estimated calories: 120 كيلو كالوري
Estimated cost: درهم 4
Alternatives:
- طماطم -> طماطم معلبة (أرخص)
---RECIPE-END---""",
]

for i, sample in enumerate(sample_outputs, 1):
    try:
        result = parse_recipe_output(sample)
        assert result.get("title"), "Missing title"
        assert result.get("time"), "Missing time"
        assert result.get("calories"), "Missing calories"
        assert result.get("cost"), "Missing cost"
        assert isinstance(result.get("ingredients", []), list), "Ingredients should be a list"
        assert isinstance(result.get("steps", []), list), "Steps should be a list"
        print(f"✓ Sample {i} parsed successfully (Language: {result.get('language')})")
    except Exception as e:
        print(f"✗ Failed to parse sample {i}: {e}")
        sys.exit(1)

print()

# Test 4: Test Orchestrator instantiation
print("Test 4: Testing Orchestrator with all providers...")
for provider_name in ["openai", "huggingface", "openrouter"]:
    try:
        orchestrator = Orchestrator(provider_name=provider_name, api_key=f"test_{provider_name}_key")
        print(f"✓ Orchestrator created with {provider_name} provider")
    except Exception as e:
        print(f"✗ Failed to create Orchestrator with {provider_name}: {e}")
        sys.exit(1)

print()

# Test 5: Test error handling
print("Test 5: Testing error handling...")
try:
    invalid_provider = get_llm_provider("invalid")
    print("✗ Should have raised ValueError for invalid provider")
    sys.exit(1)
except ValueError as e:
    if "invalid" in str(e).lower():
        print(f"✓ Correctly raised error for invalid provider")
    else:
        print(f"✗ Unexpected error message: {e}")
        sys.exit(1)

print()

# Test 6: Verify SOLID principles
print("Test 6: Verifying SOLID architecture...")
checks = [
    ("Base class defines interface", hasattr(BaseLLMProvider, "generate")),
    ("OpenAI adapter implements interface", hasattr(OpenAIProvider, "generate")),
    ("Hugging Face adapter implements interface", hasattr(HuggingFaceProvider, "generate")),
    ("OpenRouter adapter implements interface", hasattr(OpenRouterProvider, "generate")),
    ("Factory pattern used", callable(get_llm_provider)),
    ("Output parser is standalone", callable(parse_recipe_output)),
]

for check_name, result in checks:
    if result:
        print(f"✓ {check_name}")
    else:
        print(f"✗ {check_name}")
        sys.exit(1)

print()
print("=" * 60)
print("✓ ALL INTEGRATION TESTS PASSED!")
print("=" * 60)
print("\nThe application is ready to:")
print("  1. Switch between OpenAI, Hugging Face, and OpenRouter LLMs")
print("  2. Parse and structure recipe outputs reliably")
print("  3. Support easy addition of new providers")
print("\nTo run the Streamlit app:")
print("  streamlit run app.py")
print("\nTo test with demo script:")
print("  python demo.py openai 'tomatoes, garlic, basil' 'your_api_key'")
print("  python demo.py huggingface 'tomatoes, garlic, basil' 'your_api_key'")
print("  python demo.py openrouter 'tomatoes, garlic, basil' 'your_api_key'")
