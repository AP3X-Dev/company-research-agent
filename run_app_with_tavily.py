import sys
import os
import importlib.util

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Add the tavily package to the Python path
tavily_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages', 'tavily')
if os.path.exists(tavily_path):
    print(f"Found tavily package at: {tavily_path}")
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages'))
    
    # Check if tavily can be imported
    try:
        import tavily
        print(f"Successfully imported tavily package: {tavily}")
        print(f"Tavily package path: {tavily.__file__}")
    except ImportError as e:
        print(f"Failed to import tavily: {e}")
else:
    print(f"Tavily package not found at: {tavily_path}")

# Import and run the application
try:
    import application
except Exception as e:
    print(f"Failed to import application: {e}")
    import traceback
    traceback.print_exc()
