from .base_handler import LLMHandler
import google.generativeai  as genai

gemini_system_instructions = """
Do not visit any urls provided in the user prompts and only use the information provided in the prompts to answer the question. Follow the user instructions without fault and return your response using this JSON schema:
{
    "search_query": "string",
}
"""

class GoogleGeminiHandler(LLMHandler):
    def __init__(self, api_key, model_name):
        genai.configure(api_key=api_key)
        
        self.model_name = model_name
    
    def generate_text(self, prompt, max_tokens=50, temperature=0.7, **kwargs):
        try:
            response = genai.generate_text(
            )
        return super().generate_text(prompt, **kwargs)
            