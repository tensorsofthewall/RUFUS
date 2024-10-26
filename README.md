# RUFUS: Retrieval and Understanding Framework for Unstructured Sources

RUFUS is an intelligent web data extraction tool designed for seamless integration with Retrieval-Augmented Generation (RAG) pipelines. Using AI-powered web crawling, Rufus navigates complex web structures to selectively retrieve and synthesize relevant data into structured JSON format.  This simplifies the process of collecting and structuring online data for AI models and applications.

Disclaimer: This project was developed as a solution to a timed case study by Chima AI.

# Features

- Intelligent Web Scraping: Extract structured data from websites effortlessly.
- Seamless RAG Integration: Works smoothly with RAG pipelines for improved data retrieval.
- Customizable Configs: Tailor extraction rules with YAML configuration files.
- Efficient & Scalable: Handles recursive URL traces with optimized scraping algorithms.

# Project Structure
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
This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.