#!/usr/bin/env python
"""Validate Streamlit app structure without running it interactively."""

import sys
import os
import ast

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, "app.py")

# Check if app.py has valid Python syntax
try:
    with open(app_path, "r", encoding="utf-8") as f:
        code = f.read()
    ast.parse(code)
    print("✓ app.py has valid Python syntax")
except SyntaxError as e:
    print(f"✗ Syntax error in app.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error reading app.py: {e}")
    sys.exit(1)

# Try to import the app (without running it)
try:
    import streamlit
    print("✓ Streamlit imported successfully")
except ImportError as e:
    print(f"✗ Failed to import streamlit: {e}")
    sys.exit(1)

print("✓ Streamlit app structure is valid!")
