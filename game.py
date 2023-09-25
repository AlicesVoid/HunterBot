# Alice Void 
# L.E: 9/24/2023
# HUNTER GAME!!! A VSBW GAME FOR MY LOVELY WIFE <3 

import requests
import random
import re
from bs4 import BeautifulSoup

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
        if(first[1] > second[1]):
            return 1
        elif(first[1] == second[1]):
            if(first[0] == "High" and second[0]==("Low" or '')):
                return 1
            elif(first[0] == "Low" and second[0] == ''):
                return -1
            elif(first[0] == '' and second[0] == "Low"):
                return 1
            else: 
                return 0
    return -1

    
# Determines the Greatest Tier in a String
def get_greatest_tier(string):
    tiers = extract_tiers(string)
    greatest_tier = "11-C"
    for tier in tiers:
        if compare_tiers(tier, greatest_tier) == 1:
            greatest_tier = tier
    return greatest_tier

#----------------HUNTER GAME--------------------------------

# Operates The Entire Game:
class HunterGame:
    _player = "Nobody..."
    _score = 0
    _best_score = 0
    _game = True
    
    # Function to Run The Menu
    def main_game_loop(self):
        self._player = input("Please Input Your Name, Player: ")
        self.Hunter = HunterGameInstance(self._player)
        print(f"Welcome, {self._player}\n")
        print(f"Your Best Recorded Score Is: {self._best_score}\n\n")
        
        # While Loop that Facilitates the Menu
        while self._game:
            menu_choice = input("Please Input 1 to Play The Game, or 0 to Exit:\n")
            print()
            
            if(menu_choice == '1'):
                self._game = True
                while self.Hunter.is_correct == True:
                    self.Hunter.game_instance()
                    self.cmdline_ui()
            else:
                self._game = False
                print(f"Your Best Recorded Score is: {self._best_score}, GoodBye!\n\n")
        
        exit()

    # Function to Run the User Interface in CMDLine
    def cmdline_ui(self):
        # Print each attribute of first_opp and second_opp to the console.
        print("First Opponent:")
        for attribute in self.Hunter.first_opp[:2]:
            print(attribute)
        print("\nSecond Opponent:")
        for attribute in self.Hunter.second_opp[:2]:
            print(attribute)
        print()  # Space between the two lists

        # Prompt the user to make their guess.
        self.Hunter.guess = input("Enter '1' if you think the first opponent is stronger,\nor '2' if you think the second opponent is stronger, \n or 3 if it's a tie.\n")
        
        # Evaluate user's guess
        self.Hunter.is_correct = False

        if self.Hunter.guess == '1' and self.Hunter.first_opp[0] == self.Hunter.stronger_opp[0]:
            self.Hunter.is_correct = True
        elif self.Hunter.guess == '2' and self.Hunter.second_opp[0] == self.Hunter.stronger_opp[0]:
            self.Hunter.is_correct = True
        elif self.Hunter.guess == '3' and self.Hunter.stronger_opp[0] is None:
            self.Hunter.is_correct = True

        # Display feedback to user
        if self.Hunter.is_correct:
            print("CORRECT!")
        else:
            print("WRONG...")

        for statement in self.Hunter.strongest:
            print(statement)
            print()

        # Update user's score
        if self.Hunter.is_correct:
            self._score += 1
            if(self._best_score < self._score): 
                self._best_score = self._score
            print(f"Current Score: {self._score}")  
        else:
            if(self._best_score < self._score): 
                self._best_score = self._score
            print(f"Total Score: {self._best_score}")  
            self._score = 0
            

        
        return self.Hunter.is_correct
        
#----------------HUNTER GAME INSTANCE-----------------------
# Operates an Instance Of The Game
class HunterGameInstance:
    
    _player = "Nobody..."
    _strongest = [None, None]
    _first_opp, _second_opp, _stronger_opp = [None, None, None]
    _guess = 0
    _is_correct = True
    
    # CONSTRUCTOR
    def __init__(self, player_name):
        self._player = player_name

    # Runs One Instance of The Game
    def game_instance(self):
        # Create two opponents using get_character_info and store them in class attributes.
        self._first_opp, self._second_opp = self.get_character_info()

        # Use test_tiers to determine which opponent is strongest and store the results in class attributes.
        self._strongest, self._stronger_opp = self.test_tiers(self._first_opp, self._second_opp)
    
    # Checks Two Opponents To See Who Is Stronger
    def test_tiers(self, first_opp, second_opp):  
        
        # Determine the strongest tier for each character
        first_tier = get_greatest_tier(first_opp[-1])
        second_tier = get_greatest_tier(second_opp[-1])

        # Determine which character is stronger based on their tiers
        strongest = ["Equal Strength", "Tie"]
        stronger_opp = [None, None]
        
        comparison_result = compare_tiers(first_tier, second_tier)
        if comparison_result == 1:
            strongest[0] = first_opp[0] + " is stronger than " + second_opp[0]
            strongest[1] = first_tier + " is more powerful than " + second_tier
            stronger_opp = first_opp

        elif comparison_result == -1:
            strongest[0] = second_opp[0] + " is stronger than " + first_opp[0]
            strongest[1] = second_tier + " is more powerful than " + first_tier
            stronger_opp = second_opp

        return strongest, stronger_opp

    # Collects the Info For Each Character
    def get_character_info(self):
        character_urls = self.rand_chars()  # Get the two random character URLs
        
        # Collects Character Info from the Site
        def parse_character(url):
            """Helper function to parse individual character info"""
            page = requests.get(url)  # strip() is used to remove any trailing newline
            soup = BeautifulSoup(page.content, "html.parser")

            # Extract the character's full name
            name_span = soup.find("span", class_="mw-page-title-main")
            name = name_span.text if name_span else None
            
            # Find the main div containing the character's info
            main_div = soup.find("div", class_="mw-parser-output")
            if not main_div:
                return [name, None, None]
            
            # Extract the character's image link
            floatright_div = main_div.find("div", class_="floatright")
            image_element = floatright_div.find("a", class_="image") if floatright_div else None
            image_link = image_element["href"] if image_element else "src/blank.png"

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
    
    # ---------- GETTER AND SETTER METHODS --------- 
    # Getter for player
    @property
    def player(self):
        return self._player

    # Setter for player
    @player.setter
    def player(self, value):
        self._player = value

    # Getter for strongest
    @property
    def strongest(self):
        return self._strongest

    # Setter for strongest
    @strongest.setter
    def strongest(self, value):
        self._strongest = value

    # Getter for first_opp
    @property
    def first_opp(self):
        return self._first_opp

    # Setter for first_opp
    @first_opp.setter
    def first_opp(self, value):
        self._first_opp = value

    # Getter for second_opp
    @property
    def second_opp(self):
        return self._second_opp

    # Setter for second_opp
    @second_opp.setter
    def second_opp(self, value):
        self._second_opp = value

    # Getter for stronger_opp
    @property
    def stronger_opp(self):
        return self._stronger_opp

    # Setter for stronger_opp
    @stronger_opp.setter
    def stronger_opp(self, value):
        self._stronger_opp = value

    # Getter for guess
    @property
    def guess(self):
        return self._guess

    # Setter for guess
    @guess.setter
    def guess(self, value):
        self._guess = value

    # Getter for is_correct
    @property
    def is_correct(self):
        return self._is_correct

    # Setter for is_correct
    @is_correct.setter
    def is_correct(self, value):
        self._is_correct = value

Wife = HunterGame()
Wife.main_game_loop()
