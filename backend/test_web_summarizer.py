from summarizer import GeminiWebSummarizer

class TestGeminiWebSummarizer:
    """
    Test class to verify URL-based summarization with GeminiWebSummarizer.
    """

    def __init__(self):
        self.summarizer = GeminiWebSummarizer()

    def run(self, test_url):
        print(f"Testing summarization for URL: {test_url}")
        result = self.summarizer.summarize_url(test_url)

        print("\n--- Summary Result ---")
        if "summary" in result:
            print(result["summary"])
        elif "error" in result:
            print(f"❌ Error: {result['error']}")
            if "details" in result:
                print(f"Details: {result['details']}")
        else:
            print("Unknown result format:")
            print(result)


if __name__ == "__main__":
    # Change this URL to any live webpage for testing
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    tester = TestGeminiWebSummarizer()
    tester.run(url)
