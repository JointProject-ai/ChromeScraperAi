# ChromeScraper AI – Gemini Summarizer

**Project Process and Workflow Documentation**

---

## Table of Contents

1.  [Introduction](#1-introduction)
    *   [1.1 Project Purpose](#11-project-purpose)
    *   [1.2 Key Technologies](#12-key-technologies)
    *   [1.3 High-Level Architecture](#13-high-level-architecture)
2.  [System Architecture](#2-system-architecture)
    *   [2.1 Frontend (Chrome Extension)](#21-frontend-chrome-extension)
    *   [2.2 Backend (Flask Server)](#22-backend-flask-server)
    *   [2.3 Google Gemini API](#23-google-gemini-api)
3.  [Workflow Diagram](#3-workflow-diagram)
4.  [Detailed Workflow](#4-detailed-workflow)
    *   [4.1 User Interaction](#41-user-interaction)
    *   [4.2 Request to Backend](#42-request-to-backend)
    *   [4.3 Content Processing & Summarization](#43-content-processing--summarization)
    *   [4.4 Response to Extension](#44-response-to-extension)
5.  [Backend Setup and Configuration](#5-backend-setup-and-configuration)
    *   [5.1 Prerequisites](#51-prerequisites)
    *   [5.2 Virtual Environment](#52-virtual-environment)
    *   [5.3 API Key Configuration](#53-api-key-configuration)
    *   [5.4 Installing Dependencies](#54-installing-dependencies)
    *   [5.5 Running the Server](#55-running-the-server)
    *   [5.6 CORS Configuration](#56-cors-configuration)
6.  [Chrome Extension Setup](#6-chrome-extension-setup)
7.  [Backend API Endpoint(s)](#7-backend-api-endpoints)
    *   [7.1 Example: `/summarize` (POST)](#71-example-summarize-post)
8.  Error Handling
9.  Troubleshooting
10. Future Enhancements (Optional)

---

## 1. Introduction

### 1.1 Project Purpose
The **ChromeScraper AI – Gemini Summarizer** is a system designed to provide users with quick summaries of web page content. It leverages the power of Google's Gemini API for advanced text summarization, accessed via a custom backend server, and integrated into the user's browsing experience through a Chrome Extension.

### 1.2 Key Technologies
*   **Backend:** Python, Flask (a lightweight WSGI web application framework)
*   **AI Model:** Google Gemini API (for natural language processing and summarization)
*   **Frontend:** Chrome Extension (HTML, CSS, JavaScript)
*   **Environment Management:** Python Virtual Environments, `pip`
*   **Communication:** HTTP/S, JSON

### 1.3 High-Level Architecture
The system consists of two main components:
1.  **Chrome Extension (Frontend):** Runs in the user's browser, captures the URL of the active tab (and potentially pre-processes content), and communicates with the backend.
2.  **Flask Server (Backend):** A Python-based server that exposes an API. It receives requests from the Chrome Extension, interacts with the Google Gemini API to perform summarization, and returns the result.

---

## 2. System Architecture

### 2.1 Frontend (Chrome Extension)
*   **Role:** Provides the user interface within the Chrome browser. It allows users to trigger the summarization process for the currently active web page.
*   **Key Components:**
    *   `manifest.json`: Defines the extension's properties, permissions (e.g., access to active tab URL), and scripts.
    *   `popup.html/js`: (If applicable) The UI displayed when the extension icon is clicked.
    *   `content_script.js`: (If applicable) Scripts that can run in the context of web pages to extract content or interact with the DOM.
    *   `background_script.js`: Handles events and manages communication with the backend.
*   **Interaction Flow:**
    1.  User clicks the extension icon or activates it via a shortcut.
    2.  The extension retrieves the URL of the active tab.
    3.  It sends an HTTP request (e.g., POST) containing the URL (or pre-extracted content) to the backend Flask server's designated API endpoint.
    4.  It receives the summary (or an error message) from the backend and displays it to the user.

### 2.2 Backend (Flask Server)
*   **Role:** Acts as the intermediary between the Chrome Extension and the Google Gemini API. It handles the logic for fetching web page content (if needed), preparing data for the Gemini API, calling the API, and processing its response.
*   **Location:** `backend/src/app.py`
*   **Key Components:**
    *   **Flask Application (`app.py`):** Defines API routes, handles incoming requests, and orchestrates the summarization process.
    *   **API Endpoints:** Specific URLs (e.g., `/summarize`) that the Chrome Extension calls.
    *   **Gemini API Integration:** Code responsible for authenticating with and sending requests to the Google Gemini API. This requires a secure way to store and access the API key (e.g., via environment variables).
    *   **Content Scraping/Fetching (Potentially):** If the extension only sends a URL, the backend might need libraries (e.g., `requests`, `BeautifulSoup`) to fetch and parse the web page content. The project name "ChromeScraper AI" suggests this capability.
    *   **CORS Handling:** `Flask-CORS` is used to allow cross-origin requests from the Chrome Extension (which runs on a `chrome-extension://` origin) to the backend server (e.g., `http://localhost:8081`).

### 2.3 Google Gemini API
*   **Role:** The core AI service that performs the text summarization. The backend server sends the extracted web page content (or relevant text) to this API.
*   **Interaction:** The backend authenticates using an API key and sends a prompt (containing the text to be summarized) to the Gemini API. The API processes the text and returns a concise summary.

---

## 3. Workflow Diagram
Please see photo 

---

## 4. Detailed Workflow

### 4.1 User Interaction
1.  The user navigates to a web page they wish to summarize.
2.  The user clicks the ChromeScraper AI extension icon in their browser toolbar (or uses a defined shortcut).

### 4.2 Request to Backend
1.  The Chrome Extension's script (background or popup) captures the URL of the active tab.
    *   *Alternative:* The extension might attempt to extract the main textual content from the page directly.
2.  The extension constructs an HTTP request (typically a `POST` request) to the Flask backend's summarization endpoint (e.g., `http://localhost:8081/summarize`).
3.  The request payload includes the necessary data, such as the `url` or the `content` to be summarized, formatted as JSON.

### 4.3 Content Processing & Summarization
1.  **Request Reception:** The Flask server receives the incoming request at the defined endpoint (e.g., `/summarize` in `backend/src/app.py`).
2.  **Data Extraction:** The server parses the JSON payload from the request to get the URL or content.
3.  **Content Fetching/Scraping (If URL provided):**
    *   If a URL is provided, the backend uses HTTP libraries (e.g., `requests`) to fetch the HTML content of the web page.
    *   It may then use parsing libraries (e.g., `BeautifulSoup`) to extract the main textual content, stripping away HTML tags, navigation, ads, etc. This step is crucial for providing clean text to the Gemini API.
4.  **API Key Retrieval:** The backend securely retrieves the Google Gemini API key, typically from an environment variable (loaded from an `.env` file).
5.  **Gemini API Call:**
    *   The backend formats the extracted text into a suitable prompt for the Gemini API.
    *   It makes an authenticated API call to the Google Gemini service, sending the text to be summarized.
6.  **Response Handling:**
    *   The Gemini API processes the text and returns a summary.
    *   The backend receives this summary. It should also handle potential errors from the Gemini API (e.g., rate limits, content policy violations, API errors).

### 4.4 Response to Extension
1.  The Flask backend formats the summary (or an error message) into a JSON response.
2.  It sends this JSON response back to the Chrome Extension.
3.  The Chrome Extension receives the response, parses the JSON, and displays the summary to the user within its UI (e.g., a popup window or a notification).

---

## 5. Backend Setup and Configuration

These instructions are based on the project's `README.md`.

### 5.1 Prerequisites
*   Python 3.x
*   `pip` (Python package installer)
*   Access to Google Gemini API and a corresponding API Key.

### 5.2 Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies and avoid conflicts.

1.  **Create the virtual environment:**
    ```bash
    python3 -m venv venv
    ```
2.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

### 5.3 API Key Configuration
The application requires a Google Gemini API key. This should be stored securely and not committed to version control. The common practice is to use an `.env` file.

1.  Ensure the `python-dotenv` library is listed in your `requirements.txt` and installed. This library allows your Python application to load environment variables from an `.env` file.
    ```python
    # Example: In your app.py
    from dotenv import load_dotenv
    import os
    load_dotenv() # Loads variables from .env file into environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ```
2.  Create a file named `.env` in the root directory of the project (or alongside `app.py` if preferred, adjust `load_dotenv()` path if needed).
3.  Add your Google Gemini API key to the `.env` file:
    ```env
    GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
    ```
4.  Ensure `.env` is listed in your `.gitignore` file to prevent accidental commits.

### 5.4 Installing Dependencies
All required Python packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```
This typically includes Flask, google-generativeai (or the relevant Google AI SDK), python-dotenv, Flask-CORS, and any scraping libraries like requests or beautifulsoup4.

### 5.5 Running the Server
Once the virtual environment is activated, dependencies are installed, and the API key is configured:
python backend/src/app.py

The server will typically start on http://localhost:8081 (as per the README, though this port can be configured in app.py).

### 5.6 CORS Configuration
Cross-Origin Resource Sharing (CORS) is essential for the Chrome Extension (running on chrome-extension://<ID>) to communicate with your backend server (running on http://localhost:8081). Flask-CORS should be configured in app.py to allow requests from the extension's origin.

# Example: In backend/src/app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# Configure CORS, potentially restricting to specific origins in production
CORS(app) # Allows all origins by default, refine for production

# ... rest of your Flask app
### 6. Chrome Extension Setup
To test and use the Chrome Extension locally:

Open Google Chrome.
Navigate to chrome://extensions/.
Enable Developer Mode (usually a toggle switch in the top right corner).
Click the "Load unpacked" button.
Select the directory that contains the Chrome Extension's manifest.json file (this might be named frontend/, extension/, or similar, depending on your project's structure).
The extension icon should now appear in your Chrome toolbar.

### 7. Backend API Endpoint(s)
The primary API endpoint exposed by the Flask backend is for summarization.

7.1 Example: /summarize (POST)
Method: POST
URL: http://localhost:8081/summarize (or the configured server address + endpoint)
Description: Receives a URL or text content and returns a summary.
Request Body (JSON): Option 1 (Sending URL):
{
  "url": "https://example.com/article-to-summarize"
}

Option 2 (Sending pre-extracted content):
{
  "content": "The full text of the article to be summarized goes here..."
}

Success Response (JSON - Status 200 OK):
{
  "summary": "This is the concise summary generated by the Gemini API."
}

Error Response (JSON - Status 4xx/5xx):
{
  "error": "A description of the error, e.g., 'Failed to fetch URL', 'Gemini API error', 'Invalid input'"
}

### 8. Error Handling
Robust error handling is important at various stages:

Chrome Extension:
Handle network errors when communicating with the backend.
Display user-friendly messages if the backend returns an error or if the summary cannot be generated.
Flask Backend:
Validate incoming requests (e.g., ensure url or content is provided).
Handle errors during web page fetching/scraping (e.g., invalid URL, request timeouts, non-HTML content).
Gracefully manage errors from the Google Gemini API (e.g., authentication failures, rate limits, API downtime, content processing issues).
Return appropriate HTTP status codes and error messages in the JSON response.
Gemini API Interaction:
Implement retries for transient errors if appropriate.
Log detailed error information from the API for debugging.

### 9. Troubleshooting
Common issues and their potential solutions:

Backend server not running:
Ensure you have activated the virtual environment (source venv/bin/activate or venv\Scripts\activate).
Run python backend/src/app.py and check the console for errors.
API Key Issues (GEMINI_API_KEY):
Verify the .env file exists in the correct location and contains the correct API key.
Ensure python-dotenv is installed and load_dotenv() is called in app.py before the key is accessed.
Check for typos in the environment variable name.
CORS Errors (Extension cannot connect to backend):
Verify Flask-CORS is installed and configured in app.py.
Check the browser's developer console (in the extension's context or the background page) for CORS-related error messages.
Dependency Issues:
Ensure all packages in requirements.txt are installed correctly (pip install -r requirements.txt).
Extension not working:
Check the extension's error console: Go to chrome://extensions/, find your extension, click "Details", and if there's an "Errors" button, click it. Or, inspect the popup/background page.
Ensure the backend server URL in the extension's code matches the running server's address (e.g., http://localhost:8081).
Gemini API Errors:
Check the backend server logs for specific error messages from the Google Gemini API.
Ensure your API key is valid and has the necessary permissions/quotas.

### 10. Future Enhancements (Optional)
Customizable Summary Length: Allow users to specify desired summary length (short, medium, long).
Language Support: Extend to summarize content in multiple languages if supported by Gemini.
Caching: Implement caching on the backend to store summaries for frequently accessed URLs to reduce API calls and improve response time.
User Authentication: If storing user preferences or history becomes a feature.
Advanced Content Extraction: Improve the scraping logic to better identify and extract the main article content from diverse web page layouts.
Batch Summarization: Allow summarizing multiple URLs at once.
UI/UX Improvements: Enhance the Chrome Extension's user interface for a more polished experience.

