try:
    import sys
    import os
    
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Try to import the module
    from backend.nodes.grounding import GroundingNode
    print(f"Successfully imported GroundingNode: {GroundingNode}")
except ImportError as e:
    print(f"Failed to import GroundingNode: {e}")
    
    # Print the traceback
    import traceback
    traceback.print_exc()
