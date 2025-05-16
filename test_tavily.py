try:
    import tavily
    print(f"Successfully imported tavily package: {tavily}")
    print(f"Tavily package path: {tavily.__file__}")
    print(f"Tavily package contents: {dir(tavily)}")
    
    from tavily import AsyncTavilyClient
    print(f"Successfully imported AsyncTavilyClient: {AsyncTavilyClient}")
except ImportError as e:
    print(f"Failed to import tavily: {e}")
    
    try:
        import sys
        sys.path.append('C:\\Users\\Guerr\\Documents\\GitHub\\company-research-agent\\.venv\\Lib\\site-packages')
        import tavily
        print(f"Successfully imported tavily package after path modification: {tavily}")
    except ImportError as e:
        print(f"Still failed to import tavily after path modification: {e}")
