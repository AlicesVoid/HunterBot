# Alice Void, Nov. 3rd 2023
import json
from bs4 import BeautifulSoup
import requests

class Character:
    # == CONSTRUCTOR =======================================
    def __init__(self, url):
        # Stores the URL of the Character's Page
        self.url = url
        
        # Stores the Character's Data as a Dictionary
        self.char_data = {}
        
        # Fetches The Data 
        self.fetch_data()

    # == METHODS ===========================================
    
    # Fetches the Data for the Character
    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            # Parse the content with BeautifulSoup directly
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the character's image link
            image_element = soup.select_one('a[class="image"][href^="https://static.wikia.nocookie.net/"] > img[src][loading="lazy"]')
            if image_element:
                # Use 'data-src' if it exists, otherwise use 'src'
                image_link = image_element.get('data-src', image_element.get('src', 'blank.png'))
            else:
                image_link = "blank.png"
            
            # Update char_data dictionary with the image link
            self.char_data["image"] = image_link
        else:
            raise ValueError(f"Failed to retrieve data, status code: {response.status_code}")

            
    # Returns the value associated with the given key in the char_data dictionary
    def get_char_data(self, key=""):
        # Check if the key is provided and exists in the dictionary
        if key and key in self.char_data:
            return self.char_data[key]
        elif key:  # Key provided but not in the dictionary
            return f"No data found for key: {key}"
        else:  # No key provided, return the whole char_data dictionary
            return self.char_data



saitama_url = "https://vsbattles.fandom.com/wiki/Saitama#Post-Training"
Saitama = Character(saitama_url)
print(Saitama.get_char_data("image"))