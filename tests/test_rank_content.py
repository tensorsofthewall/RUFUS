import pytest
from rufus.content_rankers.method import rank_content

@pytest.mark.parametrize("similarity_metric", [
    "cosine",  # Example cosine similarity 
    "euclidean",  # Example Euclidean similarity 
])
def test_rank_content(similarity_metric):
    # Reference and candidate texts
    ref_text = ["How to fix Python ModuleNotFoundError"]
    candidate_texts = ["Python error solution", "Fix Python ModuleNotFoundError"]
    
    # Patch the rank_content function to use the mock reranker
    ranked_results = rank_content(
        ref_txt=ref_text, 
        candidate_txt=candidate_texts, 
        similarity_metric=similarity_metric, 
        embd_model_provider="google",
        embd_model_api_key="YOUR GOOGLE GEMINI API KEY",
        embd_model_name="models/text-embedding-004"
    )

    # Extract scores from ranked results
    scores = [score.item() for _, score in ranked_results]
    
    # print similarity scores
    print(scores)