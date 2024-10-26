from bs4 import BeautifulSoup
import re

# Extract text from HTML data and return cleaned version
def extract_text(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    
    # Remove all unnecesary tags from soup
    for data in soup(['style','script','nav','aside','footer','header']):
        data.decompose()
    
    cleaned_txt = re.sub(r'\s+'," ",soup.get_text(separator=" "))
    return cleaned_txt.strip()

# Methods to implement:
# Extract data from tabular and embedded data, if better than HTML text extraction
# Extract information about images (descriptions, metadata, etc)

