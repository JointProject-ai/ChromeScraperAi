#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error when substituting.
# Pipestatus of the last command that exited with a non-zero status will be returned.
set -euo pipefail

# === CONFIGURATION ===
PROJECT_NAME="ChromeScraperAI"
APP_DIR="backend"
MAIN_MODULE="src.app:app"  # Adjust if your app entry point changes
VENV_DIR=".venv"

echo "🚀 Starting deployment for $PROJECT_NAME..."
echo "--------------------------------------------------"

# === CREATE & ACTIVATE VENV ===
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "✅ Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# === INSTALL REQUIREMENTS ===
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found. Skipping dependency installation."
fi
echo "--------------------------------------------------"

# === EXPORT ENV VARS ===
if [ -f ".env" ]; then
    echo "🔐 Loading environment variables from .env..."
    # Temporarily enable auto-export for variables defined during sourcing
    set -a
    # Source the .env file after filtering out comments and empty lines.
    # This handles spaces in values if they are properly quoted in the .env file (e.g., VAR="value with spaces")
    # or even unquoted (e.g., VAR=value with spaces).
    # sed 's/\r$//' handles Windows-style line endings if .env was created on Windows.
    source <(grep -vE '^\s*#|^\s*$' .env | sed 's/\r$//')
    # Disable auto-export
    set +a
else
    echo "⚠️ .env file not found. Skipping environment variable loading from file."
fi
echo "--------------------------------------------------"

# === RUN GUNICORN SERVER ===
echo "🌀 Starting Gunicorn server..."
gunicorn "$APP_DIR.$MAIN_MODULE" \
  --bind 0.0.0.0:8080 \
  --workers 1 \  # For production, consider increasing workers, e.g., (2 * CPU_CORES) + 1
  --reload       # Enable auto-reload for development; disable for production

# === DONE ===
echo "--------------------------------------------------"
echo "✅ Deployment complete. Server running on http://localhost:8080 (or http://<your-ip>:8080)"