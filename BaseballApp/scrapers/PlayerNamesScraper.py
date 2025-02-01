import requests
import time
import json

from bs4 import BeautifulSoup
from utils.utils import replace_text

RANGE_ALPHABETICAL_SEARCH = 26
STARTING_INDEX = ord('a')

players = {}

base_url = "https://www.baseball-reference.com/players/"
for i in range(RANGE_ALPHABETICAL_SEARCH):
    print(f"Fetching Player Data at Letter: {chr(STARTING_INDEX + i)}\n")
    # Send a GET request to the website
    url = base_url + chr(STARTING_INDEX + i)
    response = requests.get(url)

    # Parse the HTML content
    current_players = BeautifulSoup(response.content, 'html.parser').find_all(attrs={ "id": "div_players_" })[0].find_all('b') # Bold tags indicate player is active

    print("Players successfully scraped, adding them to the players dictionary!\n")

    # player_names = [replace_text(player.a.string).lower() for player in current_players]
    player_names = [player.a.string.lower() for player in current_players]

    player_links = [player.a["href"] for player in current_players]

    for k, v in zip(player_names, player_links):
        players[k] = v

    time.sleep(6) # Throttle requests to avoid hitting limit of 20 requests per minute per baseball reference


# File path where the JSON will be saved
file_path = "./static_data/players.json"

# Writing the dictionary to a JSON file
# Save list of players for permanent use
with open(file_path, 'w') as json_file:
    json.dump(players, json_file, indent=4)  # 'indent=4' formats the JSON for readability

print(f"Player page links directory written to {file_path}") 







