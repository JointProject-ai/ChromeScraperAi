from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import GeminiWebSummarizer

import traceback


# Initialize Flask app
app = Flask(__name__)

# Allow only the Chrome extension's origin
#CORS(app, origins=["chrome-extension://lddnmlbeachmkggobobeegjpcblfmffo"]) #TODO: Update with the actual extension ID

CORS(app) 
# Endpoint: Summarize raw text (sent by frontend)
@app.route("/summarize", methods=["POST"])
def summarize():
    """
    Accepts a JSON body like: { "text": "text to summarize" }
    Sends it to Gemini API and returns the summary.
    """
    try:
        data = request.get_json()
        text = data.get("text")
        question = data.get("question")

        if not text:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        summarizer = GeminiWebSummarizer()
        # result = summarizer._summarize_text_with_gemini(text, question)
            
        if question:
            result = summarizer.ask_question_with_gemini(text, question)
        else:
            result = summarizer._summarize_text_with_gemini(text)
            
        # Extract summary from Gemini API response
        if (
                "candidates" in result and
                result["candidates"] and
                "content" in result["candidates"][0] and
                "parts" in result["candidates"][0]["content"]
        ):
            summary = result["candidates"][0]["content"]["parts"][0]["text"]
            print("Gemini API result:", result)
            return jsonify({"summary": summary.strip()})

        # Handle errors
        elif "error" in result:
            return jsonify(result)

        else:
            return jsonify({"error": "Unexpected Gemini API response", "details": result})


    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)