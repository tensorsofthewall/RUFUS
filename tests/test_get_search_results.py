from rufus.search_engines import get_search_results

def test_get_search_results_with_google():
    query = "Best practices for web crawling"
    
    # You can mock this in actual unit testing if you don't want live requests
    results = get_search_results(query, handler_type="google", num_results=3)
    
    assert isinstance(results, list)
    assert len(results) == 3  # Ensure that we received the requested number of results
    assert all(isinstance(result, str) for result in results)  # Ensure all results are strings