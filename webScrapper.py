import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse 
from datetime import datetime

class WebScrapper:
    def __init__(self, output_dir="scraped_data"):
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def get_user_input(self):
        return input("Please enter the URL to scrap: ")
    
    def scrap_url(self, url=None):
        if url is None:
            url = self.get_user_input()
        
        try:
            # Send request and get response
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse the HTML contents
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract basic page data
            data = {
                'url': url,
                'title': soup.title.text if soup.title else 'No title found',
                'h1_headings': [h1.text.strip() for h1 in soup.find_all('h1')],
                'h2_headings': [h2.text.strip() for h2 in soup.find_all('h2')],
                'paragraphs': [p.text.strip() for p in soup.find_all('p')],
                'links': [{'text': a.text.strip(), 'href': a.get('href')} 
                          for a in soup.find_all('a', href=True)],
                'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] 
                                  if soup.find('meta', attrs={'name': 'description'}) else 'No description found'
            }
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error scrapping URL: {e}")
            return {'error': str(e), 'url': url}
                
    def save_as_json(self, data, filename=None):
        if filename is None:
            # Create a filename from the URL if none provided
            if 'url' in data:
                parsed_url = urlparse(data['url'])
                domain = parsed_url.netloc.replace('.', '_')
                path = parsed_url.path.strip('/').replace('/', '_') if parsed_url.path else 'index'
                filename = f"{domain}_{path}"
                filename += ".json"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scraped_data_{timestamp}.json"
                
        # Ensure the filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def scrap_and_save(self, url=None):
        data = self.scrap_url(url)
        return self.save_as_json(data)

##############################################################################################
#manual testing purpose
def test_web_scraper():
    print("WebScraper Testing Interface")
    
    # Create scraper instance
    output_dir = input("Enter output directory for JSON files (or press Enter for default 'scraped_data'): ")
    if not output_dir:
        output_dir = "scraped_data"
    
    scraper = WebScrapper(output_dir=output_dir)
    
    while True:
        print("\nOptions:")
        print("1. Scrape a URL and save as JSON")
        print("2. View available scraped files")
        print("3. View contents of a scraped file")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == '1':
            url = input("Enter URL to scrape (or press Enter to be prompted later): ")
            if url:
                json_path = scraper.scrap_and_save(url)
            else:
                json_path = scraper.scrap_and_save()
            
            view_content = input(f"Would you like to view the scraped content? (y/n): ").lower()
            if view_content == 'y':
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print("\nScraped data summary:")
                    print(f"Title: {data.get('title', 'N/A')}")
                    print(f"URL: {data.get('url', 'N/A')}")
                    print(f"Number of paragraphs: {len(data.get('paragraphs', []))}")
                    print(f"Number of links: {len(data.get('links', []))}")
                    
                    # Show more details if requested
                    details = input("Show more details? (y/n): ").lower()
                    if details == 'y':
                        print(json.dumps(data, indent=2))
                except Exception as e:
                    print(f"Error reading file: {e}")
            
        elif choice == '2':
            try:
                files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
                if not files:
                    print(f"No JSON files found in {output_dir}")
                else:
                    print(f"\nFound {len(files)} JSON files in {output_dir}:")
                    for i, file in enumerate(files, 1):
                        print(f"{i}. {file}")
            except Exception as e:
                print(f"Error listing files: {e}")
                
        elif choice == '3':
            try:
                files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
                if not files:
                    print(f"No JSON files found in {output_dir}")
                    continue
                    
                print(f"\nAvailable JSON files in {output_dir}:")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                    
                file_num = input("\nEnter file number to view (or 0 to cancel): ")
                try:
                    file_num = int(file_num)
                    if file_num == 0:
                        continue
                    if 1 <= file_num <= len(files):
                        file_path = os.path.join(output_dir, files[file_num-1])
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        print("\n" + "=" * 50)
                        print(f"Contents of {files[file_num-1]}:")
                        print(json.dumps(data, indent=2))
                        print("=" * 50)
                    else:
                        print("Invalid file number.")
                except ValueError:
                    print("Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == '4':
            print("Exiting WebScraper test. Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")

# Entry point for running the script
if __name__ == "__main__":
    test_web_scraper()
