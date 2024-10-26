# RUFUS: Retrieval and Understanding Framework for Unstructured Sources

RUFUS is a Python-based information retrieval system  designed to efficiently retrieve and rank content from various sources on the web and is being developed with the idea of seamless integration with Retrieval-Augmented Generation (RAG) pipelines. Using AI-powered web crawling, RUFUS navigates complex web structures to selectively retrieve and synthesize relevant data into structured JSON format.  This simplifies the process of collecting and structuring online data for AI models and applications.

Disclaimer: This project was developed as a solution to a timed case study by Chima AI.

# Features

- Intelligent Web Scraping: Extract structured data from websites effortlessly.
- Seamless RAG Integration: Works smoothly with RAG pipelines for improved data retrieval.
- Customizable Configs: Tailor extraction rules with YAML configuration files.
- Efficient & Scalable: Handles recursive URL traces with optimized scraping algorithms.

# How does RUFUS work?
RUFUS primarily works on web scraping through recursive HTML scraping from the user-provided URL. Users can configure the maximum depth i.e. the number of nested links that should be opened from the starter URL, along with several other parameters. These configurations can be stored in YAML and provided to the RufusClient API. 

In the event that the URL is invalid or offline, RUFUS leverages LLMs and web search to generate and search the web for links that are likely to yield relevant content for the user's prompt. The collected documents are then processed and structured for use in other applications, including storage and RAG applications.

# Approach

My approach to building RUFUS was centered around creating a modular and scalable architecture. All modules are built with abstraction in mind, meaning that new algorithms can be implemented using the same code structure. I broke down the system into several submodules, each responsible for a specific task:

- **content_rankers**: This submodule contains algorithms for ranking content based on relevance, primarily using embedding models.
- **core**: This submodule provides the core functionality of Rufus, including data ingestion, processing, and storage.
- **llms**: This submodule contains interfaces for various LLMs, allowing flexibility in search query generation.
- **search_engines**: This submodule provides interfaces to various web search engines, allowing Rufus to retrieve content from up-to-date web sources in the event of an invalid or broken URL. 
- **utils**: Utility functions handling validation, formatting, math operations, etc.

# Challenges and Solutions
During the development of RUFUS, I faced some challenges:
- **Asynchronous Execution**: To achieve high performance and scalability, RUFUS needs to execute tasks asynchronously. To achieve this, I used the `asyncio` and `aiohttp` libraries to create a non-blocking, event-driven architecture that allows RUFUS to handle multiple tasks concurrently.
- **Efficiency**: With large volumes of data, efficiency becomes a major concern, both in terms of execution time and memory. I chose to use `aiohttp` and `requests` libraries wherever possible, making a trade-off with the simplicity of using `Selenium`.

# Project Structure
- 
- rufus/ - Main module containing several submodules.
    - core/
    - llms/
    - content_rankers/
    - search_engines/
    - client.py
    - utils.py
- tests/ - Unit tests for ensuring reliability.
- config.yaml - Configurations for scraper parameters.
- example.py - Sample script to demonstrate usage.

# Getting Started
1. Clone the repository:
```bash
git clone https://github.com/tensorsofthewall/RUFUS.git
cd RUFUS
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install RUFUS:
```bash
pip install .
```

4. Run the example:
```bash
python example.py
```

# Usage
Modify config.yaml to set up your configuration parameters, LLMs for search query generation and other parameters. RUFUS currently support the Google Gemini API, giving you access to Google Gemini LLMs and Embedding models.

# License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
