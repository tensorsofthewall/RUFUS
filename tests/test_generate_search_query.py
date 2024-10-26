# tests/test_generate_search_query.py

from rufus.llms import generate_search_query

def test_generate_search_query_with_google():
    config = {
        "llm_provider": "google",
        "llm_api_key": "YOUR API KEY",
        "llm_name": "models/gemini-1.5-flash-latest"
    }
    
    prompt = "Find information about product features and customer FAQs."
    url = "https://apple.com"
    
    query = generate_search_query(prompt, url, **config)
    
    assert isinstance(query, str)
    assert len(query) > 0  # Check that a non-empty string was returned
