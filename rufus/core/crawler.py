import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..llms.method import generate_search_query, get_google_search_results
from ..utils import setup_logging, persistent_request, is_valid_url, is_url_online

class Crawler:
    def __init__(self, max_depth=2, delay=1.5, log_file="rufus.log", log_level="DEBUG", headers=None, num_search_results=10):
        self.url_tracker = set()
        self.max_depth = max_depth
        self.request_delay = delay # Delay between consequtive requests in seconds
        self.logger = setup_logging(log_file=log_file, level=log_level)
        self.headers = headers # Option to add headers to requests
        self.num_search_results = num_search_results
        
    # Asynchronous page fetch method 
    async def fetch_page(self, url, session, retries=3):
        return await persistent_request(
            url,
            session=session,
            retries=retries,
            delay=self.request_delay,
            logger=self.logger,
            headers=self.headers
        )
    
    # Validate url
    def validate_url(self, url):
        "Check if the URL is valid"
        return is_valid_url(url)
    
    # Check if URL resource is available
    async def check_url_online(self, url):
        """Check if the URL is online"""
        return await is_url_online(url)
    
    # Link fetching from existing HTML content
    def parse_links(self, soup, curr_url):
        """Find all valid links and return a list of valid links on current page
        """
        links = []
        for link in soup.find_all("a", href=True):
            url = urljoin(curr_url, link["href"])
            if url not in self.url_tracker:
                links.append(url)
        return links
    
    async def crawl(self, url, depth=0, session=None):
        """Recursively crawl the given URL and follow links up to max_depth asynchronously."""
        if depth > self.max_depth or url in self.url_tracker:
            return []  # Base case: Stop if the maximum depth is reached or URL is visited

        self.logger.info(f"Crawling: {url}")
        self.url_tracker.add(url)
        
        if not session:
            raise ValueError("A session is required for asynchronous crawling.")

        html_content = await self.fetch_page(url, session)
        if html_content is None:
            return []

        soup = BeautifulSoup(html_content, "lxml")
        data = [html_content]

        links = self.parse_links(soup, url)
        tasks = [self.crawl(link, depth + 1, session) for link in links]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            data.extend(result)
        
        return data

    async def start_crawl(self, start_url, prompt):
        """Start crawling the given URL asynchronously."""
        if not self.validate_url(start_url):
            self.logger.error(f"Invalid URL: {start_url}")
            query = generate_search_query(prompt, start_url)
            self.logger.info(f"Generated Google Search query: {query}")
            search_results = get_google_search_results(query, self.num_search_results)
            self.logger.info(f"Using Google search results: {search_results}")
        else:
            is_online = await self.check_url_online(start_url)
            if not is_online:
                self.logger.error(f"URL is not online: {start_url}")
                query = generate_search_query(prompt, start_url)
                self.logger.info(f"Generated Google Search query: {query}")
                search_results = get_google_search_results(query, self.num_search_results)
                self.logger.info(f"Using Google search results: {search_results}")
            else:
                search_results = [start_url]
        
        # Start crawling the available URLS in search results    
        async with aiohttp.ClientSession() as session:
            search_data = []
            for url in search_results:
                data = await self.crawl(url, session=session, depth=0)
                search_data.extend(data)
        return search_data