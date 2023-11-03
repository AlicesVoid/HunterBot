# Alice Void 
# L.E: 9/24/2023
# Compiles the List of Characters

import requests
import random
from bs4 import BeautifulSoup

# Gets the Next Page from a vsBW link
def get_page(url="https://vsbattles.fandom.com/wiki/Category:Characters"):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    next_button = soup.find("a", class_="category-page__pagination-next")

    if next_button is None:
        link = "<https://vsbattles.fandom.com/wiki/Category:Characters>"
    else:
        link = next_button["href"]
        
    return link

# SLOWEST but DYNAMIC-EST
def make_page_list():
    page_list = [get_page()]
    current_page = page_list[0]

    while current_page != "<https://vsbattles.fandom.com/wiki/Category:Characters>":
        next_page = get_page(current_page)
        page_list.append(next_page)
        current_page = next_page

    return page_list

# Gets a Random Character from a Page
def get_random_character(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find the main container holding all collections of characters
    container = soup.find("div", class_="category-page__members")
    if not container:
        return None

    # Find all collections of characters within the main container
    collections = container.find_all("div", class_="category-page__members-wrapper")
    if not collections:
        return None

    # Randomly select a collection
    random_collection = random.choice(collections)

    # Find all individual character links within the selected collection
    character_links = random_collection.find_all("a", class_="category-page__member-link")
    if not character_links:
        return None

    # Randomly select a character link
    random_link = random.choice(character_links)
    
    # Extract and return the href value of the randomly selected link
    character_url = random_link.get("href")
    if not character_url:
        return None
    
    return character_url

# Gets all Characters on a Specific Page
def get_all_characters(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find the main container holding all collections of characters
    container = soup.find("div", class_="category-page__members")
    if not container:
        return []

    # Find all collections of characters within the main container
    collections = container.find_all("div", class_="category-page__members-wrapper")
    if not collections:
        return []

    all_character_urls = []

    # For each collection, extract all individual character URLs
    for collection in collections:
        character_links = collection.find_all("a", class_="category-page__member-link")
        for link in character_links:
            character_url = link.get("href")
            if character_url:
                all_character_urls.append(character_url)
    
    return all_character_urls

# Writes all the Characters to the File 
def write_chars():
    # Use the provided function to get a list of all character pages
    pages = make_page_list()
    
    with open("charlist.txt", "w") as file:
        for page in pages:
            # For each page, extract all character URLs
            character_urls = get_all_characters(page)
            for url in character_urls:
                # Write each character URL to the file
                file.write("https://vsbattles.fandom.com" + url + "\n")

# pages = make_page_list()
# print(pages[1:3], '\n')
# page = "https://vsbattles.fandom.com/wiki/Category:Characters"
# randChar = get_random_character(page)
# print(randChar, '\n')
# allChar = get_all_characters(page)
# print(allChar[1:10], '\n')
