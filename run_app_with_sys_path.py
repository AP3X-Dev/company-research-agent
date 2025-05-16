import sys
import os
import importlib.util
import multiprocessing

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Add the site-packages directory to the Python path
site_packages_dir = os.path.join(current_dir, '.venv', 'Lib', 'site-packages')
sys.path.insert(0, site_packages_dir)

# Print the Python path
print("Python Path:")
for path in sys.path:
    print(path)

# Import the tavily package
try:
    import tavily
    print(f"Successfully imported tavily package: {tavily}")
    print(f"Tavily package path: {tavily.__file__}")
except ImportError as e:
    print(f"Failed to import tavily: {e}")

# Import the application
try:
    import uvicorn
    print(f"Successfully imported uvicorn package: {uvicorn}")
    print(f"Uvicorn package path: {uvicorn.__file__}")
except ImportError as e:
    print(f"Failed to import uvicorn: {e}")
    import traceback
    traceback.print_exc()

def main():
    # Run the application
    uvicorn.run("application:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    # Fix for multiprocessing on Windows
    multiprocessing.freeze_support()
    main()
