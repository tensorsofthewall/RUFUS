import pytest
from rufus.core.crawler import Crawler
import aiohttp
import asyncio

@pytest.mark.asyncio
async def test_crawl():
    crawler = Crawler(max_depth=0, delay=0.5)
    
    start_url = "https://www.wikipedia.org/"
    prompt="What are the different names of mango in each language on Wikipedia?"
    
    llm_config = {
        "llm_provider": "google",
        "llm_api_key": "YOUR GOOGLE GEMINI API KEY",
        "llm_name": "models/gemini-1.5-flash-latest"
    }
    
    embd_config = {
        "embd_model_provider": "google",
        "embd_model_api_key": "AIzaSyCt72QY6V6zkIz-qQo9Q8kh02LHKEo4wKc",
        "embd_model_name": "models/text-embedding-004"
    }
    
    async with aiohttp.ClientSession() as session:
        result = await crawler.start_crawl(start_url, prompt=prompt, session=session, **llm_config, **embd_config)
    
    assert len(result) > 0  # Ensure that at least one page was crawled
