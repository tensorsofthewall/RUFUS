from .google_search_handler import GoogleSearchHandler

def get_search_results(query, search_engine="google", num_results=10, **kwargs):
    if search_engine == "google":
        handler = GoogleSearchHandler()
    else:
        # Add more search engines
        raise ValueError(f"Unsupported search engine: {search_engine}")

    return handler.get_search_results(query, num_results=num_results)
