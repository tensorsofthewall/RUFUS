import pytest
from rufus.core.crawler import Crawler
import aiohttp
import asyncio

@pytest.mark.asyncio
async def test_crawl():
    crawler = Crawler(max_depth=1, delay=0.5)
    
    start_url = "https://stackoverflow.com/"
    
    async with aiohttp.ClientSession() as session:
        result = await crawler.crawl(start_url, session=session)
    
    assert len(result) > 0  # Ensure that at least one page was crawled
