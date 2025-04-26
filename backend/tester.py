# tester.py

from ai_service_handler import AIServiceHandler
from utils import Utils

def main():
    url = input("Enter the URL to summarize: ").strip()
    api_key = input("Enter your Gemini API key: ").strip()

    print("\nFetching page text...")
    page_text = Utils.extract_text_from_url(url)

    if not page_text:
        print("Error: No text extracted from URL.")
        return

    print(f"Extracted {len(page_text)} characters. Summarizing with Gemini...")

    ai_handler = AIServiceHandler(api_key)
    summary = ai_handler.summarize_text(page_text)

    print("\n--- Summary ---\n")
    print(summary)

if __name__ == "__main__":
    main()
# This script is a simple tester for the AI service handler and utility functions.
# It prompts the user for a URL and an API key, fetches the text from the URL,
# and then summarizes the text using the Gemini API.        