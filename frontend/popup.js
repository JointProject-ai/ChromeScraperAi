// popup.js
document.addEventListener("DOMContentLoaded", () => {
  const summaryDiv = document.getElementById("summary");
  const outputDiv = document.getElementById("output");
  const summarizeButton = document.getElementById("summarizeButton");
  const summarizeButtonText = document.getElementById("summarizeButtonText");
  const customQuestionButton = document.getElementById("customQuestionButton");
  const questionButtonText = document.getElementById("questionButtonText");
  const customQuestionInput = document.getElementById("customQuestionInput");
  
  const BASE_URL = "https://pagewise-hbie.onrender.com";

  // Helper function to show loading state
  function setLoading(button, buttonText, isLoading) {
    if (isLoading) {
      button.disabled = true;
      buttonText.innerHTML = '<span class="loading"></span>Processing...';
    } else {
      button.disabled = false;
      if (button === summarizeButton) {
        buttonText.textContent = "Summarize Page";
      } else {
        buttonText.textContent = "Ask Question";
      }
    }
  }

  // Helper function to display error
  function showError(element, message) {
    element.textContent = message;
    element.classList.add("error");
    element.classList.remove("placeholder-text");
  }

  // Helper function to display success
  function showSuccess(element, content) {
    element.textContent = content;
    element.classList.remove("error", "placeholder-text");
    element.classList.add("success");
  }

  // Summarize button click handler
  summarizeButton.addEventListener("click", async () => {
    try {
      setLoading(summarizeButton, summarizeButtonText, true);
      summaryDiv.textContent = "Analyzing page content...";
      summaryDiv.classList.remove("error", "placeholder-text");

      // Get the active tab's URL
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const pageUrl = tab.url;

      // Check if the URL is a restricted chrome:// URL
      if (pageUrl.startsWith("chrome://") || pageUrl.startsWith("chrome-extension://")) {
        showError(summaryDiv, "Cannot summarize Chrome internal pages. Please navigate to a regular webpage.");
        setLoading(summarizeButton, summarizeButtonText, false);
        return;
      }

      // Execute script to get the page content
      const result = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.body.innerText
      });

      const pageText = result[0]?.result || "";

      // Ensure pageText is not empty
      if (!pageText.trim()) {
        showError(summaryDiv, "No readable content found on this page. Please try a different page.");
        setLoading(summarizeButton, summarizeButtonText, false);
        return;
      }

      summaryDiv.textContent = "Generating summary...";

      // Make the POST request to the backend
      const response = await fetch(`${BASE_URL}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: pageText })
      });

      // Handle the response
      if (!response.ok) {
        showError(summaryDiv, `Failed to generate summary. Please try again later. (${response.status})`);
        setLoading(summarizeButton, summarizeButtonText, false);
        return;
      }

      const data = await response.json();

      // Display the summary or an error message
      if (data.error) {
        showError(summaryDiv, `Error: ${data.error}`);
      } else {
        showSuccess(summaryDiv, data.summary || "No summary available.");
      }
    } catch (error) {
      showError(summaryDiv, `Network error: ${error.message}. Please check your connection and try again.`);
    } finally {
      setLoading(summarizeButton, summarizeButtonText, false);
    }
  });

  // Custom question button click handler
  customQuestionButton.addEventListener("click", async () => {
    const question = customQuestionInput.value.trim();
    
    if (!question) {
      showError(outputDiv, "Please enter a question first.");
      return;
    }

    try {
      setLoading(customQuestionButton, questionButtonText, true);
      outputDiv.textContent = "Processing your question...";
      outputDiv.classList.remove("error", "placeholder-text");

      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const pageUrl = tab.url;

      // Check if the URL is a restricted chrome:// URL
      if (pageUrl.startsWith("chrome://") || pageUrl.startsWith("chrome-extension://")) {
        showError(outputDiv, "Cannot process questions on Chrome internal pages. Please navigate to a regular webpage.");
        setLoading(customQuestionButton, questionButtonText, false);
        return;
      }

      const result = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.body.innerText,
      });

      const text = result[0]?.result || "";

      if (!text.trim()) {
        showError(outputDiv, "No readable content found on this page. Please try a different page.");
        setLoading(customQuestionButton, questionButtonText, false);
        return;
      }

      outputDiv.textContent = "Finding answer...";

      const response = await fetch(`${BASE_URL}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, question }),
      });

      if (!response.ok) {
        showError(outputDiv, `Failed to process question. Please try again later. (${response.status})`);
        setLoading(customQuestionButton, questionButtonText, false);
        return;
      }

      const data = await response.json();

      if (data.error) {
        showError(outputDiv, `Error: ${data.error}`);
      } else {
        showSuccess(outputDiv, data.summary || data.error || "No response available.");
      }
    } catch (error) {
      showError(outputDiv, `Network error: ${error.message}. Please check your connection and try again.`);
    } finally {
      setLoading(customQuestionButton, questionButtonText, false);
    }
  });

  // Allow Enter key to submit question
  customQuestionInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      customQuestionButton.click();
    }
  });
});