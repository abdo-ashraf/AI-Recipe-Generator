#!/usr/bin/env python
"""Quick smoke test for the AI Recipe Generator."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test 1: Import base classes
try:
    from langchain_components.llm_providers.base import BaseLLMProvider
    print("✓ BaseLLMProvider imported")
except Exception as e:
    print(f"✗ Failed to import BaseLLMProvider: {e}")
    sys.exit(1)

# Test 2: Import OpenAI adapter
try:
    from langchain_components.llm_providers.openai_adapter import OpenAIProvider
    print("✓ OpenAIProvider imported")
except Exception as e:
    print(f"✗ Failed to import OpenAIProvider: {e}")
    sys.exit(1)

# Test 3: Import chains
try:
    from langchain_components.chains import Orchestrator
    print("✓ Orchestrator imported")
except Exception as e:
    print(f"✗ Failed to import Orchestrator: {e}")
    sys.exit(1)

# Test 4: Import output parser
try:
    from langchain_components.output_parser import parse_recipe_output
    print("✓ parse_recipe_output imported")
except Exception as e:
    print(f"✗ Failed to import parse_recipe_output: {e}")
    sys.exit(1)

# Test 5: Test output parser with sample data
sample_output = """---RECIPE-START---
Title: Tomato Soup
Language: English
Ingredients:
- 2 tomatoes
- 1 onion
- Salt
Steps:
1. Chop tomatoes and onion
2. Boil water and add vegetables
3. Season with salt
Estimated time: 20 minutes
Estimated calories: 150 kcal
Estimated cost: USD 5
Alternatives:
- tomatoes -> canned tomatoes
---RECIPE-END---"""

try:
    result = parse_recipe_output(sample_output)
    print(f"✓ Output parser works")
    print(f"  - Title: {result.get('title')}")
    print(f"  - Time: {result.get('time')}")
    print(f"  - Calories: {result.get('calories')}")
    print(f"  - Cost: {result.get('cost')}")
except Exception as e:
    print(f"✗ Output parser failed: {e}")
    sys.exit(1)

print("\n✓ All smoke tests passed!")
