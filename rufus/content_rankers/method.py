import torch
from ..utils import cosine_similarity, pairwise_distance
from .google_text_embedding_reranker import GoogleTextEmbeddingReranker

# Compute similarity scores and return ranked content in descending order
def rank_content(ref_txt, candidate_txt, similarity_metric="cosine", embd_model_provider="google",**kwargs):
    # Initialize reranker
    if embd_model_provider == "google":
        reranker = GoogleTextEmbeddingReranker(kwargs.get("embd_model_api_key"), kwargs.get("embd_model_name"))
    else:
        raise ValueError(f"Unsupported embedding model provider: {embd_model_provider}")
    
    # Compute embeddings for input prompt and content text
    ref_embeddings = reranker.get_embeddings(ref_txt)
    candidate_embeddings = reranker.get_embeddings(candidate_txt)
    
    # If reranker is hosted locally
    if reranker.is_local_hosted:
        if reranker.device.type == "cuda":
            # For GPU-optimized operations
            if similarity_metric == "cosine":
                similarity_func = torch.nn.functional.cosine_similarity
            elif similarity_metric == "euclidean":
                similarity_func = torch.nn.functional.pairwise_distance
            else:
                raise ValueError(f"Unknown similarity metric: {similarity_metric}")
        elif reranker.device.type == "cpu":
            # For CPU-optimized operations
            if similarity_metric == "cosine":
                similarity_func = cosine_similarity
            elif similarity_metric == "euclidean":
                similarity_func = pairwise_distance
            else:
                raise ValueError(f"Unknown similarity metric: {similarity_metric}")
    else:
        # Reranker is cloud hosted / api access only
        # Use Numpy operations for performance
        if similarity_metric == "cosine":
            similarity_func = cosine_similarity
        elif similarity_metric == "euclidean":
            similarity_func = pairwise_distance
        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
    
    # Compute selected similarity scores
    scores = similarity_func(ref_embeddings, candidate_embeddings)
    
    ranked_content = sorted(zip(candidate_txt, scores), key=lambda x: x[1], reverse=True)
    
    return ranked_content
