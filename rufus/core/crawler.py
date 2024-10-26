import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from rufus.core.extraction import extract_text
from rufus.llms import generate_search_query
from rufus.search_engines import get_search_results
from rufus.content_rankers import rank_content
from rufus.utils import setup_logging, persistent_request, is_valid_url, is_url_online, format_results

class Crawler:
    def __init__(self, max_depth=2, delay=1.5, log_file="rufus.log", log_level="DEBUG", headers=None, num_search_results=10, **kwargs):
        self.url_tracker = set()
        self.max_depth = max_depth
        self.request_delay = delay # Delay between consequtive requests in seconds
        self.logger = setup_logging(log_file=log_file, level=log_level)
        self.headers = headers # Option to add headers to requests
        self.num_search_results = num_search_results
        self.timeout = kwargs.get("timeout", 5)
        
    # Asynchronous page fetch method 
    async def _fetch_page(self, url, session, retries=3):
        return await persistent_request(
            url,
            session=session,
            retries=retries,
            delay=self.request_delay,
            logger=self.logger,
            headers=self.headers, 
            timeout=self.timeout
        )
    
    # Validate url
    def _validate_url(self, url):
        "Check if the URL is valid"
        return is_valid_url(url)
    
    # Check if URL resource is available
    async def _check_url_online(self, url):
        """Check if the URL is online"""
        return await is_url_online(url)
    
    # Link fetching from existing HTML content
    def _parse_links(self, soup, curr_url):
        """Find all valid links and return a list of valid links on current page
        """
        links = []
        for link in soup.find_all("a", href=True):
            url = urljoin(curr_url, link["href"])
            if url not in self.url_tracker:
                links.append(url)
        return links
    
    async def _crawl(self, url, depth=0, session=None):
        """Recursively crawl the given URL and follow links up to max_depth asynchronously."""
        if depth > self.max_depth or url in self.url_tracker:
            return []  # Base case: Stop if the maximum depth is reached or URL is visited

        self.logger.info(f"Crawling: {url}")
        self.url_tracker.add(url)
        
        if not session:
            raise ValueError("A session is required for asynchronous crawling.")

        html_content = await self._fetch_page(url, session)
        if html_content is None:
            return []
        
        cleaned_text = extract_text(html_content)

        soup = BeautifulSoup(html_content, "lxml")
        data = [cleaned_text]

        links = self._parse_links(soup, url)
        tasks = [self._crawl(link, depth + 1, session) for link in links]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            data.extend(result)
        
        return data

    async def start_crawl(self, start_url, prompt, do_rank=True, structured_output=True, **kwargs):
        """Start crawling the given URL asynchronously, ranking optional, then return documents."""
        if not self._validate_url(start_url):
            self.logger.error(f"Invalid URL: {start_url}")
            query = generate_search_query(prompt, start_url)
            self.logger.info(f"Generated Google Search query: {query}")
            search_results = get_search_results(query, self.num_search_results, **kwargs)
            self.logger.info(f"Using Google search results: {search_results}")
        else:
            is_online = await self._check_url_online(start_url)
            if not is_online:
                self.logger.error(f"URL is not online: {start_url}")
                query = generate_search_query(prompt, start_url)
                self.logger.info(f"Generated Google Search query: {query}")
                search_results = get_search_results(query, self.num_search_results, **kwargs)
                self.logger.info(f"Using Google search results: {search_results}")
            else:
                search_results = [start_url]
        
        # Crawling function with semaphore
        async def crawl_with_semaphore(url, session):
            """Helper function to perform crawl with sempahore"""
            async with semaphore:
                return await self._crawl(url, session=session, depth=0)
        
        search_data = []
        max_concurrent_tasks = 10 # Maximum number of concurrent tasks
        semaphore = asyncio.Semaphore(max_concurrent_tasks)
        
        # Start crawling the available URLS in search results    
        async with aiohttp.ClientSession() as session:
            tasks = [
                crawl_with_semaphore(url, session)
                for url in search_results
            ]
            
            results = await asyncio.gather(*tasks)
        
        # Extend search_data with results
        for result in results:
            if result:
                search_data.extend(result)
        
        if do_rank:
            search_data = rank_content(ref_txt=[prompt]*len(search_data), candidate_txt=search_data, **kwargs)
        
        if structured_output:
            search_data = format_results(search_data, start_url=start_url, prompt=prompt)
            
        return search_data
    
    
        