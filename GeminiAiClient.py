import json
import google.generativeai as genai

class GeminiAiClient:
    def __init__(self, model_name="models/gemini-pro"):
        # Here is where you paste your own Gemini API key
        #self.api_key = api_key
        self.model_name = model_name
        
        # Configure the API key with Gemini
        genai.configure(api_key="API key")
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)

    def generate_text(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error: {str(e)}"
    
    def analyze_scraped_data(self, json_path, analysis_prompt=None):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if analysis_prompt is None:
                title = data.get('title', 'Untitled page')
                meta_desc = data.get('meta_description', 'No description')

                analysis_prompt = f"""
                Analyze the following web page content and provide insights:

                Title: {title}
                Description: {meta_desc}

                Key points to address:
                1. What is the main topic of this page?
                2. Summarize the key information in 6-7 sentences.
                3. What is the apparent purpose of this page (educational, commercial, news, etc.)?
                4. Who appears to be the target audience?

                Base your analysis only on the provided data.
                """
            
            prompt = f"{analysis_prompt}\n\nAvailable data includes: {', '.join(data.keys())}"
            return self.generate_text(prompt)
        
        except Exception as e:
            print(f"Error analyzing data with Gemini: {e}")
            return f"Error: {str(e)}"
