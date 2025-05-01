from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import GeminiWebSummarizer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (e.g., from Chrome extension)

# Endpoint 1: Summarize a URL (server fetches the webpage)
@app.route("/summarize_url", methods=["POST"])
def summarize_url():
    """
    Accepts a JSON body like: { "url": "https://example.com" }
    Fetches the webpage, extracts content, and returns a summary.
    """
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing 'url' in request body"}), 400

        summarizer = GeminiWebSummarizer()
        result = summarizer.summarize_url(url)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Endpoint 2: Summarize raw text (sent by frontend)
@app.route("/summarize_text", methods=["POST"])
def summarize_text():
    """
    Accepts a JSON body like: { "content": "text to summarize" }
    Sends it to Gemini API and returns the summary.
    """
    try:
        data = request.get_json()
        content = data.get("content")

        if not content:
            return jsonify({"error": "Missing 'content' in request body"}), 400

        summarizer = GeminiWebSummarizer()
        result = summarizer._summarize_text_with_gemini(content)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
