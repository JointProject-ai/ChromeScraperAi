document.getElementById("summarizeBtn").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript(
    {
      target: { tabId: tab.id },
      function: getPageText,
    },
    async (results) => {
      const pageText = results[0].result;
      const response = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: pageText }),
      });
      const data = await response.json();
      document.getElementById("summaryResult").innerText =
        data.candidates?.[0]?.content?.parts?.[0]?.text || "No summary found.";
    }
  );
});

function getPageText() {
  return document.body.innerText;
}
