import google.generativeai as genai
from .base_reranker import BaseReranker

class GoogleTextEmbeddingReranker(BaseReranker):
    def __init__(self, embd_model_api_key, embd_model_name):
        self.model_name = embd_model_name
        self.is_local_hosted = False
        genai.configure(api_key=embd_model_api_key)
    
    def get_embeddings(self, texts):
        try:
            response = genai.embed_content(
                model = self.model_name,
                content = texts
            )
            return [embedding for embedding in response['embedding']]
        except Exception as e:
            print(f"Error fetching embeddings from Google model: {e}")
            return []
        