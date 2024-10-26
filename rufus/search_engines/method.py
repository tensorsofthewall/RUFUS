from .google_search_handler import GoogleSearchHandler

def get_search_results(query, handler_type="google", num_results=10):
    if handler_type == "google":
        handler = GoogleSearchHandler()
    else:
        # Add more search engines
        raise ValueError(f"Unsupported search engine: {handler_type}")

    return handler.get_search_results(query, num_results=num_results)
