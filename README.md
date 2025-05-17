
# 🧠 Chrome AI Summerizer Extension – Gemini api

A lightweight Flask server that summarizes webpage content using Google Gemini API.
Designed to integrate with a Chrome Extension.

---

## 📋 Prerequisites

*   Python 3.x
*   `pip` (Python package installer)
*   Access to Google Gemini API and a corresponding API Key.

---

## ⚙️ Setup Instructions

### ✅ 1. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

```python
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### ✅ 2. Install requirements

```bash
pip install -r requirements.txt
```

### 🧪 (Optional) Install Flask CORS manually (If not already included in your requirements.txt:)
```bash
pip install flask-cors
```

### ✅ 3. Run the server
```bash
python backend/src/app.py
```

The server will start on:
http://localhost:8081

🧩 Load the Chrome Extension
```bash
To test the extension locally:
    Go to chrome://extensions/
    Enable Developer Mode (top right)
    Click Load unpacked
    Select the frontend/ or extension/ directory
```

###🔚 To deactivate the virtual environment
```bash
deactivate
```