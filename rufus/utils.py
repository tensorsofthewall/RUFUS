# Utility functions for RUFUS
import logging
import torch
import numpy as np
import requests
import time
import aiohttp, asyncio

# Set up logging for RUFUS
def setup_logging(log_file="rufus.log", level="DEBUG"):
    """Set up logging for RUFUS.

    By default, sets up root logger with DEBUG level.
    
    :param file: string, path to log file
    :param level: string, one of "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    """
    logging.basicConfig(
        filename=log_file,
        filemode='a', # Append mode
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=getattr(logging, level),
    )
    
    logger = logging.getLogger("RUFUSLogger")
    return logger

# Request method for handling retries
# def persistent_request(url, session=None, retries=3, delay=1.5, headers=None, timeout=5, logger=None):
#     """Attempts to fetch the content of a webpage using a GET request, using a requests.Session object if provided"""
#     if logger is None:
#         logger = logging.getLogger("RUFUSLogger")
    
#     attempts = 0
#     while attempts < retries:
#         try:
#             if session:
#                 response = session.get(url, headers=headers, timeout=timeout)
#             else:
#                 response = requests.get(url, headers=headers, timeout=timeout)
#             response.raise_for_status()
#             return response.text
#         except requests.RequestException as e:
#             attempts += 1
#             logger.warning(f"Attempt {attempts} for {url} failed: {e}")
#             time.sleep(delay)
#     logger.error(f"All {attempts} attemps failed for {url}")
#     return None
    

async def persistent_request(url, session=None, retries=3, delay=1.5, headers=None, timeout=5, logger=None):
    """Attempts to fetch the content of a webpage using an async GET request, using an aiohttp.ClientSession object if provided."""
    if logger is None:
        logger = logging.getLogger("RUFUSLogger")

    attempts = 0
    while attempts < retries:
        try:
            if session:
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    response.raise_for_status()
                    return await response.text()
            else:
                async with aiohttp.ClientSession() as temp_session:
                    async with temp_session.get(url, headers=headers, timeout=timeout) as response:
                        response.raise_for_status()
                        return await response.text()
        except aiohttp.ClientError as e:
            attempts += 1
            logger.warning(f"Attempt {attempts} for {url} failed: {e}")
            await asyncio.sleep(delay)
    
    logger.error(f"All {attempts} attempts failed for {url}")
    return None

# Compute similarity
def compute_similarity(model, ref_txt, candidate_txt, similarity_metric="cosine"):
    # Compute similarity
    ref_embeddings = model.encode(ref_txt, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidate_txt, convert_to_tensor=True)
    
    # Run operations based on device used by embedding model
    if model.device.type == "cuda":
        # For GPU-optimized operations
        if similarity_metric == "cosine":
            similarity_func = torch.nn.functional.cosine_similarity
        elif similarity_metric == "euclidean":
            similarity_func = torch.nn.functional.pairwise_distance
        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
    elif model.device.type == "cpu":
        # For CPU-optimized operations
        if similarity_metric == "cosine":
            similarity_func = cosine_similarity
        elif similarity_metric == "euclidean":
            similarity_func = pairwise_distance
        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
    
    similarity = similarity_func(ref_embeddings, candidate_embeddings)
    
    return similarity


# Cosine similarity computation using Numpy, works better than PyTorch on CPU tensors/arrays
def cosine_similarity(a, b) -> np.ndarray:
    """
    Computes the pairwise cosine similarity between two n-dimensional tensors.

    Parameters:
    a: A tensor/array of shape (..., d).
    b: A tensor/array of shape (..., d).

    Returns:
    An array of cosine similarities with shape matching the batch dimensions of `a` and `b`.
    """
    # Normalize along the last dimension
    a_norm = a / np.linalg.norm(a, axis=-1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=-1, keepdims=True)
    
    # Compute cosine similarity along the last dimension
    similarity = np.sum(a_norm * b_norm, axis=-1)
    return similarity

def pairwise_distance(a, b) -> np.ndarray:
    """
    Computes the pairwise Euclidean similarity between two n-dimensional tensors.

    Parameters:
    a: A tensor/array of shape (..., d).
    b: A tensor/array of shape (..., d).

    Returns:
    An array of Euclidean similarities with shape matching the batch dimensions of `a` and `b`.
    """
    # Expand dimensions to enable broadcasting
    diff = a[..., np.newaxis, :] - b[np.newaxis, ...]
    
    # Calculate squared differences, sum across the last dimension, and then take the square root
    distances = np.sqrt(np.sum(diff ** 2, axis=-1))
    
    # Convert distances to similarity (1 / (1 + distance))
    similarity = 1 / (1 + distances)
    return similarity