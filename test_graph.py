import sys
import os
import asyncio

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Graph class
from backend.graph import Graph

async def test_graph():
    # Create a graph instance
    graph = Graph(
        company="Test Company",
        url="https://example.com",
        hq_location="Test Location",
        industry="Test Industry"
    )
    
    # Run the graph
    state = {}
    try:
        async for s in graph.run(thread={}):
            state.update(s)
            print(f"Current node: {s.get('current_node', 'unknown')}")
            print(f"State keys: {list(s.keys())}")
            print("---")
        
        print("Graph execution completed successfully!")
        print(f"Final state keys: {list(state.keys())}")
        
        # Check if the report was generated
        if "report" in state:
            print(f"Report generated (length: {len(state['report'])})")
        else:
            print("No report found in the final state")
            
    except Exception as e:
        print(f"Graph execution failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_graph())
