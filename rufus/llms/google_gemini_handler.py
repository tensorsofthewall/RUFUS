from .base_handler import LLMHandler
import google.generativeai  as genai
import json

gemini_system_instructions = """Do not visit any URLs provided in the user prompts and only use the information provided in the prompts to answer the question. Follow the user prompts without fault and return your response using this JSON schema:
{
    "search_query": "string",
}
"""

class GoogleGeminiHandler(LLMHandler):
    def __init__(self, api_key, model_name):
        self.model_name = model_name
        self.is_safety_set = False
        self.safety_settings = self.get_safety_settings()
        
        genai.configure(api_key=api_key)
        
        self.llm = genai.GenerativeModel(
            self.model_name,
            system_instruction=gemini_system_instructions
        )
        
        
    
    def generate_text(self, prompt, **kwargs):
        try:
            response = self.llm.generate_content(
                [prompt],
                request_options={"timeout": 30},
                safety_settings=self.safety_settings
            )
            return json.loads(response.text.strip("```json\n"))['search_query']
        except Exception as e:
            print(f"Error generating search query with Google Gemini: {e}")
            return ""
    
    def get_safety_settings(self):
        default_safety_settings = {
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        }

        if self.is_safety_set:
            return self.safety_settings

        return default_safety_settings
    
    def set_safety_settings(self, safety_settings):
        self.safety_settings = safety_settings
        # Sanity Checks
        if not isinstance(safety_settings, dict):
            raise ValueError("Safety settings must be a dictionary")
        for harm_category, harm_block_threshold in safety_settings.items():
            if harm_category not in genai.types.HarmCategory.__members__:
                raise ValueError(f"Invalid harm category: {harm_category}")
            if harm_block_threshold not in genai.types.HarmBlockThreshold.__members__:
                raise ValueError(
                    f"Invalid harm block threshold: {harm_block_threshold}"
                )
        
        self.safety_settings = safety_settings
        self.is_safety_set = True
    
    
    def reset_safety_settings(self):
        self.is_safety_set = False
        self.safety_settings = self.get_safety_settings()