from .google_gemini_handler import GoogleGeminiHandler

# The only method that should be called by RUFUS
def generate_search_query(prompt, url, llm_provider="google", **kwargs):
    """
    Using an LLM to generate a Search query from the prompt and URL.
    Avaliable Models and Providers:
        - Google
            -- Gemini Flash
            -- Gemini Pro
    """
    if llm_provider == "google":
        handler = GoogleGeminiHandler(api_key=kwargs.get("api_key"), model_name=kwargs.get("model_name"))
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    full_prompt = f"Generate a search engine query for the given prompt: {prompt}, related to the URL: {url}."
    return handler.generate_text(full_prompt, **kwargs)