import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..utils import setup_logging, persistent_request

class Crawler:
    def __init__(self, max_depth=2, delay=1.5, log_file="rufus.log", log_level="DEBUG", headers=None):
        self.url_tracker = set()
        self.max_depth = max_depth
        self.session = requests.Session() # Use session for 
        self.request_delay = delay # Delay between consequtive requests in seconds
        self.logger = setup_logging(log_file=log_file, level=log_level)
        self.headers=headers # Option to add headers to requests
        
    async def fetch_page(self, url):
        return await persistent_request(
            url,
            session=self.session,
            retries=3,
            delay=self.request_delay,
            logger=self.logger,
            headers=self.headers
        )
    
    def parse_links(self, soup, curr_url):
        """Find all valid links and return a list of valid links on current page
        """
        links = []
        for link in soup.find_all("a", href=True):
            url = urljoin(curr_url, link["href"])
            if url not in self.url_tracker:
                links.append(url)
        return links
        

