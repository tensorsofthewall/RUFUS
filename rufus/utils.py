# Utility functions for RUFUS
import logging
import numpy as np
from urllib.parse import urlparse
import aiohttp, asyncio
import yaml, json

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

# Method to structure output of crawl/ranked crawl
def format_results(output, start_url=None, prompt=None):
    structured_data = {
        "start_url": start_url,
        "prompt": prompt,
        "results": []
    }
    
    if is_ranked(output) is True:
        structured_data['results'] = [
            {
                "doc": doc,
                "rank_score": rank_score,
            }
            for doc, rank_score in output
        ]
    elif is_ranked(output) is False:
        structured_data['results'] = [{"doc": doc} for doc in output]
    else:
        # Unexpected data format in search results
        structured_data['results'] = output

    return structured_data


# Load YAML Config File
def load_config(filename="config.yaml"):
    """Load YAML config file."""
    try:
        with open(filename, 'r') as stream:
            config = yaml.safe_load(stream)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found: {filename}")
        return {}
    except yaml.YAMLError as exc:
        print(f"Error reading config file '{filename}': {exc}")
        return {}
    
# Save output to JSON
def save_dict_to_json(data, filename="data.json"):
    """
    Save a dictionary to a JSON file.

    Args:
        data (dict): The dictionary to save.
        filename (str): The name of the JSON file to save to.
    """
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Dictionary successfully saved to '{filename}'")
    except (IOError, TypeError) as e:
        print(f"Error saving dictionary to JSON file: {e}")

def is_ranked(obj):
    if isinstance(obj, list):
        if all(isinstance(item, str) for item in obj):
            return False
        elif all(isinstance(item, tuple) for item in obj):
            return True
        else:
            return None
    return None
    
# Method to check to URL validity and formatting
def is_valid_url(url):
    """Check if the URL is valid and properly formatted."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme in ["http", "https"] and parsed_url.netloc)

# Async bool method to check if a URL is online
async def is_url_online(url, timeout=5):
    """Check if the URL is online by sending a HEAD request."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=timeout) as response:
                return response.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return False

# Async method for handling retries in requests
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

# Euclidean distance computation using Numpy
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