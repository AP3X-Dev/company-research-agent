import sys
import os

print("Python Path:")
for path in sys.path:
    print(path)

print("\nChecking for tavily package:")
for path in sys.path:
    tavily_path = os.path.join(path, 'tavily')
    if os.path.exists(tavily_path):
        print(f"Found tavily package at: {tavily_path}")
        print(f"Contents: {os.listdir(tavily_path)}")
