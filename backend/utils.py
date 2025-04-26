# utils.py

import requests
from bs4 import BeautifulSoup

class Utils:
    @staticmethod
    def extract_text_from_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove unnecessary elements
            for element in soup(["script", "style", "noscript"]):
                element.extract()

            text = ' '.join(soup.stripped_strings)
            return text
        except Exception as e:
            print(f"Error extracting text from URL: {e}")
            return ""
        