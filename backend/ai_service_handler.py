# ai_service_handler.py

import requests

class AIServiceHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"

    def summarize_text(self, text):
        if not text.strip():
            return "Error: No text provided for summarization."

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Summarize the following content in a concise paragraph:\n\n{text}"
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("DEBUG - Gemini API response:", data)

            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {e}"

        except (KeyError, IndexError) as e:
            return f"Error: Unexpected response format - {e}"
        
# Note: The API key should be kept secure and not hardcoded in production code.
# This class handles the interaction with the Gemini API for text summarization.
# It includes error handling for network issues and unexpected response formats.        