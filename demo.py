#!/usr/bin/env python
"""
Demo script showing how to use the AI Recipe Generator with different LLM providers.

Usage:
    python demo.py openai "tomatoes, garlic, olive oil" "your_api_key"
    python demo.py huggingface "tomatoes, garlic, olive oil" "your_api_key"
    python demo.py openrouter "tomatoes, garlic, olive oil" "your_api_key"
"""

import sys
import os
from langchain_components.chains import Orchestrator

def main():
    if len(sys.argv) < 4:
        print("Usage: python demo.py <provider> <ingredients> <api_key>")
        print("  provider: 'openai', 'huggingface', or 'openrouter'")
        print("  ingredients: comma-separated ingredient list")
        print("  api_key: provider key (OpenAI or Hugging Face)")
        sys.exit(1)
    
    provider = sys.argv[1].lower()
    ingredients = sys.argv[2]
    api_key = sys.argv[3]
    
    # Validate provider
    if provider not in ["openai", "huggingface", "openrouter"]:
        print(f"Error: Unknown provider '{provider}'. Choose 'openai', 'huggingface', or 'openrouter'")
        sys.exit(1)
    
    print(f"Using provider: {provider}")
    print(f"Ingredients: {ingredients}")
    print("-" * 60)
    
    try:
        # Create orchestrator with selected provider
        orchestrator = Orchestrator(provider_name=provider, api_key=api_key)
        
        # Generate recipe
        print("Generating recipe... (this may take a moment)")
        result = orchestrator.generate_recipe(ingredients, language="English")
        
        # Display results
        print("\n=== RAW OUTPUT ===")
        print(result.get("raw", "No output"))
        
        print("\n=== PARSED OUTPUT ===")
        parsed = result.get("parsed", {})
        print(f"Title: {parsed.get('title', 'N/A')}")
        print(f"Language: {parsed.get('language', 'N/A')}")
        print(f"Time: {parsed.get('time', 'N/A')}")
        print(f"Calories: {parsed.get('calories', 'N/A')}")
        print(f"Cost: {parsed.get('cost', 'N/A')}")
        
        if parsed.get('ingredients'):
            print("\nIngredients:")
            for ing in parsed.get('ingredients', []):
                print(f"  - {ing}")
        
        if parsed.get('steps'):
            print("\nSteps:")
            for i, step in enumerate(parsed.get('steps', []), 1):
                print(f"  {i}. {step}")
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nMake sure you passed a valid API key as the 3rd argument")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
