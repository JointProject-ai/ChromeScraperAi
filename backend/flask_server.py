# flask_server.py

from flask import Flask, request, jsonify
from ai_service_handler import AIServiceHandler

app = Flask(__name__)

# Default API key to use (or replace manually)
DEFAULT_API_KEY = "AIzaSyBPwCj4z8cjpjJRScB0hmAu2om1lrPYF1w"

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()

    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    api_key = data.get("api_key", DEFAULT_API_KEY).strip()
    if not api_key:
        return jsonify({"error": "No API key provided"}), 400

    ai_handler = AIServiceHandler(api_key)
    summary = ai_handler.summarize_text(text)

    if summary.startswith("Error"):
        return jsonify({"error": summary}), 500

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(port=5000)
# Note: Make sure to replace "your_real_gemini_api_key_here" with your actual API key or handle it securely in production.
# This Flask server provides an endpoint to summarize text using the Gemini API.
# It expects a JSON payload with "text" and optionally "api_key".
# The server will return a JSON response with the summary or an error message.          