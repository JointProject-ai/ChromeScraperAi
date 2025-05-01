import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup  # Import BeautifulSoup

# Load local .env only in development
if not os.getenv("GITHUB_ACTIONS"):  # assume GitHub Secrets are injected in prod
    load_dotenv()


class GeminiWebSummarizer:  # Renamed class for clarity
    """
    Class to fetch content from a URL, extract text,
    and interface with Gemini API to summarize the text content.
    """

    def __init__(self):
        """Initializes the summarizer, loading the API key and setting the API URL."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # Handle missing API key more explicitly
            raise ValueError("GEMINI_API_KEY environment variable not found.")

        # Consider making the model configurable if needed
        self.model_name = "gemini-1.5-flash"  # Using a recommended model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        self.session = requests.Session()  # Use a session for potential connection reuse
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })  # Add a common User-Agent

    def _fetch_content(self, url):
        """Fetches HTML content from a given URL."""
        try:
            response = self.session.get(url, timeout=15)  # Add timeout
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return None  # Return None on error

    def _extract_text(self, html_content):
        """Extracts meaningful text content from HTML."""
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content,
                                 'html.parser')  # Use html.parser (built-in) or 'lxml' (faster, needs install)

            # Remove script and style elements
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            # Try common main content tags first
            main_content = soup.find('main') or soup.find('article') or soup.find('div', role='main')

            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                # Fallback to body if no main content area found
                body = soup.find('body')
                if body:
                    text = body.get_text(separator='\n', strip=True)
                else:
                    return None  # No body tag found? Unlikely but possible

            # Basic cleaning: replace multiple newlines/spaces
            cleaned_text = ' '.join(text.split())
            return cleaned_text
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return None

    def _summarize_text_with_gemini(self, text):
        """Sends the extracted text to Gemini API for summarization."""
        if not text:
            return {"error": "No text content provided or extracted."}

        # Consider adding length limits if the API has them
        # text = text[:20000] # Example limit

        payload = {
            "contents": [
                {
                    "parts": [{"text": f"Summarize the following web page content concisely:\n\n{text}"}]
                }
            ],
            # Optional: Add generation config (temperature, safety settings etc.)
            # "generationConfig": {
            #     "temperature": 0.7,
            #     "topK": 40,
            #     "topP": 0.95,
            # },
            # "safetySettings": [ ... ]
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(self.api_url, headers=headers, json=payload, timeout=30)  # Add timeout
            response.raise_for_status()  # Check for HTTP errors from API
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Gemini API: {e}")
            # Try to return a structured error
            error_detail = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                except requests.exceptions.JSONDecodeError:
                    error_detail = e.response.text
            return {"error": "Failed to communicate with Gemini API", "details": error_detail}
        except Exception as e:  # Catch other potential errors
            print(f"An unexpected error occurred during API call: {e}")
            return {"error": "An unexpected error occurred", "details": str(e)}

    def summarize_url(self, url):
        """
        Fetches content from a URL, extracts text, and returns the summary from Gemini.
        This is the main public method to use.
        """
        print(f"Fetching content from: {url}")
        html_content = self._fetch_content(url)
        if not html_content:
            return {"error": f"Failed to fetch content from URL: {url}"}

        print("Extracting text from HTML...")
        extracted_text = self._extract_text(html_content)
        if not extracted_text:
            return {"error": "Failed to extract meaningful text from the page."}

        print(f"Sending extracted text (length: {len(extracted_text)}) to Gemini API...")
        summary_response = self._summarize_text_with_gemini(extracted_text)

        # Basic processing of the expected Gemini response structure
        # Adjust based on the actual API response format you receive
        if 'error' in summary_response:
            return summary_response  # Return the error dictionary directly
        elif 'candidates' in summary_response and summary_response['candidates']:
            try:
                summary = summary_response['candidates'][0]['content']['parts'][0]['text']
                return {"summary": summary.strip()}
            except (IndexError, KeyError, TypeError) as e:
                print(f"Error parsing Gemini response structure: {e}")
                return {"error": "Failed to parse summary from Gemini response", "details": str(summary_response)}
        elif 'promptFeedback' in summary_response and 'blockReason' in summary_response['promptFeedback']:
            reason = summary_response['promptFeedback']['blockReason']
            details = summary_response['promptFeedback'].get('safetyRatings', 'No specific ratings provided.')
            print(f"Content blocked by API: {reason}")
            return {"error": f"Content blocked by API safety filters: {reason}", "details": details}
        else:
            print("Unexpected response format from Gemini API.")
            return {"error": "Received an unexpected response format from Gemini API", "details": str(summary_response)}


# --- Example Usage (for testing) ---
if __name__ == "__main__":
    # Make sure you have a .env file with GEMINI_API_KEY=your_key
    # or have the environment variable set.
    try:
        summarizer = GeminiWebSummarizer()
        # Replace with a URL you want to test
        test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        result = summarizer.summarize_url(test_url)

        print("\n--- Result ---")
        if "summary" in result:
            print("Summary:")
            print(result["summary"])
        elif "error" in result:
            print(f"Error: {result['error']}")
            if "details" in result:
                print(f"Details: {result['details']}")
        else:
            print("Unknown result format.")
            print(result)

    except ValueError as e:
        print(f"Initialization Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
