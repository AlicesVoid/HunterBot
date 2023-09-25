# Alice Void 
# L.E: 9/24/2023

import requests
import random
import re
from bs4 import BeautifulSoup

# HUNTER GAME!!! A VSBW GAME FOR MY LOVELY WIFE <3 

"""
I want to create a class named "HunterGame" that has a few attributes:
1. Player: a string designed to hold the name of the current player 
2. CharacterList: a list containing the vsBW url to each and every character.
"""

#---------------DATA FORMATTING FUNCTIONS-----------------

# Remove Newlines Tabs (Redundancy Works Sometimes)
def remove_newlines_tabs(s):
    s = s.replace('\\n', '')
    s = s.replace('\\t', '')
    s = s.replace('\\xa0', '')
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace('\xa0', '')
    s = s.replace("\n", '')
    s = s.replace("\n", '')
    s = s.replace("\xa0", '')
    return s

# Extracts a list of Tiers from a String
def extract_tiers(string):
    pattern = r"(High |Low )?([0-9]|1[0-1])-[ABC]"
    matches = re.finditer(pattern, string)
    tiers = []
    for match in matches:
        tiers.append(match.group())
    return tiers

# Separates Tiers into their Three Core Components
def separate_tiers(string):
    pattern = r"^(High |Low )?([0-9]|1[0-1])-(A|B|C)$"
    match = re.match(pattern, string)
    if match:
        word = match.group(1).strip() if match.group(1) else ""
        letter = match.group(3)
        number = int(match.group(2))
        return [word, letter, number]
    else:
        return None

# Compares Two Tiers
def compare_tiers(tier1, tier2):
    first = separate_tiers(tier1)
    second = separate_tiers(tier2)
    
    if(first[-1] < second[-1]):
        return 1
    elif(first[-1] == second[-1]):
        if(first[1] < second[1]):
            return 1
        elif(first[1] == second[1]):
            if(first[0] == "High" and second[0==("Low" or '')]):
                return 1
            elif(first[0] == "Low" and second[0] == ''):
                return -1
            elif(first[0] == '' and second[0] == "Low"):
                return 1
            else: 
                return 0
    return -1
            
    return None
    
# Determines the Greatest Tier in a String
def get_greatest_tier(string):
    tiers = extract_tiers(string)
    greatest_tier = "11-C"
    for tier in tiers:
        if compare_tiers(tier, greatest_tier) == 1:
            greatest_tier = tier
    print("greatest tier is: " + greatest_tier)
    return greatest_tier


class HunterGame:
    
    # CONSTRUCTOR
    def __init__(self, player_name):
        self.player = player_name
        self.score = 0

    # Runs One Instance of The Game
    def game_instance(self):
        # Create two opponents using get_character_info and store them in variables.
        first_opp, second_opp = self.get_character_info()

        # Use test_tiers to determine which opponent is strongest.
        strongest, stronger_opp = self.test_tiers(first_opp, second_opp)

        # Print each attribute of first_opp and second_opp to the console.
        print("First Opponent:")
        for attribute in first_opp[:2]:
            print(attribute)
        print("\nSecond Opponent:")
        for attribute in second_opp[:2]:
            print(attribute)
        print()  # Space between the two lists

        # Prompt the user to make their guess.
        guess = input("Enter '1' if you think the first opponent is stronger,\nor '2' if you think the second opponent is stronger, \n or 3 if it's a tie.\n")
        print()
        
        # Evaluate user's guess
        is_correct = False

        if guess == '1' and first_opp[0] == stronger_opp[0]:
            is_correct = True
        elif guess == '2' and second_opp[0] == stronger_opp[0]:
            is_correct = True
        elif guess == '3' and stronger_opp[0] is None:
            is_correct = True

        # Display feedback to user
        if is_correct:
            print("CORRECT!")
        else:
            print("WRONG...")

        for statement in strongest:
            print(statement)

        # Update user's score
        if is_correct:
            self.score += 1
        else:
            self.score = 0

        print(f"Current Score: {self.score}")  # Optionally display current score

        return guess 

    # Checks Two Opponents To See Who Is Stronger
    def test_tiers(self, first_opp, second_opp):  
        
        # Determine the strongest tier for each character
        first_tier = get_greatest_tier(first_opp[-1])
        second_tier = get_greatest_tier(second_opp[-1])

        # Determine which character is stronger based on their tiers
        strongest = ["Equal Strength", "Tie"]
        stronger_opp = [None, None]
        
        comparison_result = compare_tiers(first_tier, second_tier)
        if comparison_result == -1:
            strongest[0] = first_opp[0] + " is stronger than " + second_opp[0]
            strongest[1] = first_tier + " is more powerful than " + second_tier
            stronger_opp = first_opp

        elif comparison_result == 1:
            strongest[0] = second_opp[0] + " is stronger than " + first_opp[0]
            strongest[1] = second_tier + " is more powerful than " + first_tier
            stronger_opp = second_opp

        return strongest, stronger_opp

    # Collects the Info For Each Character
    def get_character_info(self):
        character_urls = self.rand_chars()  # Get the two random character URLs
        print(character_urls)
        
        # Collects Character Info from the Site
        def parse_character(url):
            """Helper function to parse individual character info"""
            page = requests.get(url)  # strip() is used to remove any trailing newline
            soup = BeautifulSoup(page.content, "html.parser")

            # Extract the character's full name
            name_span = soup.find("span", class_="mw-page-title-main")
            name = name_span.text if name_span else None
            print(name)
            
            # Find the main div containing the character's info
            main_div = soup.find("div", class_="mw-parser-output")
            if not main_div:
                return [name, None, None]
            
            # Extract the character's image link
            floatright_div = main_div.find("div", class_="floatright")
            image_element = floatright_div.find("a", class_="image") if floatright_div else None
            image_link = image_element["href"] if image_element else None

            # Extract the character's tier (keeping the logic unchanged)
            tier = None
            for p in main_div.find_all("p"):
                a = p.find("a", title="Tiering System")
                if a is not None:
                    tier = p.text.strip()
                    break

            return [name, image_link, tier]

        # Parse info for each character
        first_character_info = parse_character(character_urls[0])
        second_character_info = parse_character(character_urls[1])

        return first_character_info, second_character_info

    # Collects Two Random Characters From The List
    def rand_chars(self):
        with open("src/charlist.txt", "r") as file:
            all_chars = [line.strip() for line in file.readlines()]
        
        return random.sample(all_chars, 2)
    

    
Hunter = HunterGame("alice")
Hunter.game_instance()
