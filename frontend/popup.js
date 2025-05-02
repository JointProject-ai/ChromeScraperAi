document.addEventListener("DOMContentLoaded", () => {
  const summaryDiv = document.getElementById("summary");
  const summarizeButton = document.getElementById("summarizeButton");

  summarizeButton.addEventListener("click", async () => {
    try {
      // Get the active tab's URL
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const pageUrl = tab.url;

      // Check if the URL is a restricted chrome:// URL
      if (pageUrl.startsWith("chrome://")) {
        summaryDiv.textContent = "Error: Cannot summarize chrome:// pages.";
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
        summaryDiv.textContent = "Error: No content found on the page to summarize.";
        return;
      }

      // Make the POST request to the backend
      const response = await fetch("http://localhost:8080/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: pageText })
      });

      // Handle the response
      if (!response.ok) {
        summaryDiv.textContent = `Error: ${response.statusText}`;
        return;
      }

      const data = await response.json();

      // Display the summary or an error message
      if (data.error) {
        summaryDiv.textContent = `Error: ${data.error}`;
      } else {
        summaryDiv.textContent = data.summary || "No summary available.";
      }
    } catch (error) {
      summaryDiv.textContent = `Error: ${error.message}`;
    }
  });
});