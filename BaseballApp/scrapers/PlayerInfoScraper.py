import requests
import time
import json
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import numpy as np
import logging
from collections import defaultdict

from utils.utils import capitalize_correct, format_name
import re

ALL_PLAYER_LINKS = "./static_data/players.json"
SALARY_EXCEL_PATH = "./static_data/MLB_Salaries.xlsx"

BASE_URL = "https://www.baseball-reference.com"

AUTO_SAVE_TIME = 2 # minute
SCRAPING_DELAY = 5 # seconds

# Create and configure logger
logging.basicConfig(filename="./logs/scrapingPlayerInfo.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

""" Via Baseball Almanac https://www.baseball-almanac.com/charts/salary/major_league_salaries.shtml
Used to compute default salary values"""
MLB_MIN_SALARY_BY_YEAR = {
    "2005": 316000,
    "2006": 327000,
    "2007": 380000,
    "2008": 390000,
    "2009": 400000,
    "2010": 400000,
    "2011": 414000,
    "2012": 480000,
    "2013": 490000,
    "2014": 500000,
    "2015": 507500,
    "2016": 507500,
    "2017": 535000,
    "2018": 545000,
    "2019": 555000,
    "2020": 563500,
    "2021": 570500,
    "2022": 700000,
    "2023": 720000,
    "2024": 740000,
    "2025": 760000,
    "2025": 780000
}

""" Define the years to search over for the salary data """
YEARS_OF_SALARY_SEARCH = {"2022", "2023", "2024"}
SPECIAL_CASES = {  # players who have information for batting and pitching. the value is the position they primarily play.
    "shohei ohtani": "batting",
    "michael lorenzen": "pitching",
    "anthony gose": "pitching"
}

class PlayerScraper:
    yearly_salary_data = {} # Cache for dataframes    
    def __init__(self):
        with open(ALL_PLAYER_LINKS, 'r') as file:
            logger.info(f"Loading player links. {time.time()}")
            self._players = json.load(file)
        logger.info(f"Size of players before popping {len(self._players)}")
        start = time.time()
        logger.info(f"Loading player salary dataframes @ {start}")
        self._load_salary_sheet_to_cache() # create pandas dataframe in initialization. Converts dataframe to simple key lookup.
        logger.info(f"Player salary dataframes loaded successfully, {time.time() - start}s elapsed.")

        with open("./static_data/player_salary_info.json", 'w') as file:
            json.dump(self.yearly_salary_data, file, indent=4)

        with open ("./static_data/basic_player_data.json", "r") as file:
            all_players = json.load(file)

        for player in all_players.keys(): # Get rid of all the players already scraped
            self._players.pop(player)
        logger.info(f"Size of players after popping {len(self._players)}")
    
    def _get_response(self, query):
        """
            Args:
                query (string): Player first_name last_name in lower case formatting.
            Return:
                Response object or raises exception if the query is invalid. 
        
        """
        if (query not in self._players):
            logging.error(f"Invalid query made: {query}. Player is not in the list.")
            raise ValueError(f"Invalid query: {query}. Player is not in the list.")
        return requests.get(BASE_URL + self._players[query])
    
    def _get_player_stats(self, soup, position_tag):
        # Acquire the player's primary statistics table
        standard_stats_table = soup.find(attrs={ "id": f"players_standard_{position_tag}" })
        header = standard_stats_table.thead.find_all("th")

        stat_labels = [label['data-stat'] for label in header] # Corresponds to the id for the statistical categories in the players page
        stat_labels.pop(0) # Don't need the first stat label which corresponds to year_id
        return standard_stats_table, stat_labels

    def _get_player_salary(self, soup):
        # Acquire the players salary table
        full_salary_div = soup.find_all(attrs={'id':'all_br-salaries'})[0]
        # Salary information is buried in comment within the page
        # Credit to seeiespi: https://stackoverflow.com/questions/48856479/unable-to-scrape-content-that-comes-after-a-comment-python-beautifulsoup
        comment = full_salary_div.find_all(string=lambda x: isinstance(x, Comment))[0] # Comments in salaries table needs to be unpacked
        newsoup = BeautifulSoup(comment, 'html.parser')

        # Get the salaries container
        salary_table = newsoup.find(attrs={"id": "br-salaries"})
        salary_header = salary_table.thead.find_all("th") # Table find the column headers in the table head
        salary_labels = [label['data-stat'] for label in salary_header] # Corresponds to the id for the salary categories in the players page
        salary_labels.pop(0) # Corresponds to year_id

        return salary_table, salary_labels
    
    def get_player_info(self, query): 
        """
            Main method to acquire a players statistical and salary info. 
            Args: 
                query (str): A player name with first_name last_name format.
            Return:
                Player json object containing player's statistical information and salary information if present.
                Formatted as 
                {
                    "202X": 
                    {
                        ...statistical categories
                        "salary_info": 
                        {
                            ...salary categories
                        }
                    }
                
                }
        
        """
        response = self._get_response(query.lower()) # Name needs to be lower case

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the position of the player and set the tag to either batting or pitching
        # Shohei Ohtani is an exception
        if (query in SPECIAL_CASES):
            position_tag = SPECIAL_CASES[query]
        else:
            position_tag = "pitching" if (soup.find("strong", string=re.compile(r"^Positions?:$")).next_sibling.strip() == "Pitcher") else "batting"

        # Get the table containing standard statistical information
        player_standard_stats_table, stat_labels = self._get_player_stats(soup, position_tag)

        # Get the table containing salary information from baseball reference
        # player_salary_table, salary_labels = self._get_player_salary(soup)

        player_info = { } # Current players info to populate

        self._add_player_stats(player_info, player_standard_stats_table, stat_labels)
        self._add_player_salary_cots(player_info, query)
        self._calculate_player_value(player_info, position_tag)

        return player_info
    
    def _add_player_stats(self, player_info, stats_table, stat_labels):
        stats_table_rows = stats_table.tbody.find_all("tr")
        # Add the statistical information to the players json body
        for row in stats_table_rows:
            if row is not None:
                year = row.th.a.string if row.th.a else row.th.string
                if (year not in YEARS_OF_SALARY_SEARCH): continue # Limiting scope of data retrieval
                stats = row.find_all("td") # Get the table cells
                # If the player didn't play then the length of td will be 1. Write None to each statistic
                yearly_stats = { stat_labels[i]: stats[i].string for i in range(len(stat_labels))} if (len(stats) > 1) else { stat_labels[i]: "None" for i in range(len(stat_labels)) }
                player_info[year] = yearly_stats
            else:
               player_info[year] = { stat_labels[i]: "None" for i in range(len(stat_labels)) }

    def _add_player_salary_br(self, player_info, name, salary_table, salary_labels):
        """
            Salary scraping via baseball reference. The data is often sparse so this is not the preferred method.
            Falls back to Cots. This method could be tested against Cots to see if it improves accuracy.
            Args:
                player_info (dict)
                name (string): Must be supplied to complete the cots query.
                salary_table (BeautifulSoup.tag)
                salary_labels (list)
        """
        salary_table_rows = salary_table.tbody.find_all("tr")

        # Go through the yearly salary information
        for row in salary_table_rows:
            year = row.th.string
            if (year not in YEARS_OF_SALARY_SEARCH): continue # Only get the data for the recent 3 years
            salary = row.find_all("td")
            if (len(salary) == len(salary_labels)): # Check that the row is valid
                logger.info(f"Player {name} has valid contract data for {year}")
                yearly_salary = {salary_labels[i] : salary[i].string for i in range(len(salary_labels))}
                yearly_salary["Salary"] = float(yearly_salary["Salary"].replace("$", "").replace(",", ""))
                player_info[year]["salary_info"] = yearly_salary["Salary"]
            else: # Fallback to Cots data
                logger.info(f"Falling back to Cots data for {name}")
                self._add_player_salary_cots(player_info, name)

    def _add_player_salary_cots(self, player_info, name):
        """
            Acquire salary data from the yearly_salary_data table which came via data from Cots.
            Args:
                player_info (dict)
                name (string): Must be supplied to complete the cots query.
            Returns:
                None.
                Adds player salary data to his json body for the defined years.

        """
        for year, info in player_info.items():
            if (year not in YEARS_OF_SALARY_SEARCH): continue
            try:
                info["salary_info"] = self.yearly_salary_data[year][name]  # Check if the player's salary is available in the cache
                logger.info(f"Player {name} found in Cots data for {year}.")
            except Exception:
                info["salary_info"] = MLB_MIN_SALARY_BY_YEAR[year] # Last resort, set default salary to minimum at that year
                logger.warning(f"Player {name} not found in Cots data for {year}. Defaulting to rookie salary.")

    def _calculate_player_value(self, player_info, position_tag):
        """
        Main function to calculate player value per dollar.
        """
        player_info['position'] = position_tag  # Save the player's position

        for year, info in player_info.items():
            if year not in YEARS_OF_SALARY_SEARCH:
                continue  # Only process data for specific years

            formatted_salary = self._validate_salary(info)
            if formatted_salary is None:
                continue  # Skip if salary is invalid

            if position_tag == 'batting':
                self._calculate_batting_value(info, formatted_salary)
            elif position_tag == 'pitching':
                self._calculate_pitching_value(info, formatted_salary)

    def _validate_salary(self, info):
        """
        Validate and return the player's salary as a float, or None if invalid.
        """
        if 'salary_info' in info and info['salary_info'] is not None:
            try:
                salary = float(info['salary_info'])
                if salary > 0:  # Ensure salary is positive
                    return salary
            except (ValueError, TypeError):
                pass
        return None

    def _calculate_batting_value(self, info, salary):
        """
        Calculate batting stats per dollar.
        """
        keys_to_divide = [
            'b_war', 'b_h', 'b_hr', 'b_doubles', 'b_triples', 
            'b_sb', 'b_bb', 'b_tb', 'b_games'
        ]
        for key in keys_to_divide:
            try:
                stat_value = info.get(key)
                if stat_value is not None:
                    info[f'{key}_per_dollar'] = float(stat_value) / salary
                else:
                    info[f'{key}_per_dollar'] = None
            except (ValueError, TypeError):
                info[f'{key}_per_dollar'] = None

        # Handle the special case for OPS+
        try:
            ops_plus = info.get('b_onbase_plus_slugging_plus')
            if ops_plus is not None:
                info['ops_plus_per_dollar'] = (float(ops_plus) - 100) / salary
            else:
                info['ops_plus_per_dollar'] = None
        except (ValueError, TypeError):
            info['ops_plus_per_dollar'] = None

    def _calculate_pitching_value(self, info, salary):
        """
        Calculate pitching stats per dollar.
        """
        keys_to_divide = [
            'p_g', 'p_war', 'p_w', 'p_g', 'p_ip', 'p_so', 'p_so_per_nine'
        ]
        for key in keys_to_divide:
            try:
                stat_value = info.get(key)
                if stat_value is not None:
                    info[f'{key}_per_dollar'] = float(stat_value) / salary
                else:
                    info[f'{key}_per_dollar'] = None
            except (ValueError, TypeError):
                info[f'{key}_per_dollar'] = None

        # Handle the special case for ERA+
        try:
            era_plus = info.get('p_earned_run_avg_plus')
            if era_plus is not None:
                info['p_earned_run_avg_plus_per_dollar'] = (float(era_plus) - 100) / salary
            else:
                info['p_earned_run_avg_plus_per_dollar'] = None
        except (ValueError, TypeError):
            info['p_earned_run_avg_plus_per_dollar'] = None
    
    def _load_salary_sheet_to_cache(self):
        for year in YEARS_OF_SALARY_SEARCH:
            player_salaries = pd.read_excel(SALARY_EXCEL_PATH, engine="openpyxl", sheet_name=f"{year}.xls")
            player_salaries.columns = player_salaries.iloc[0] # Swap the first row with the column headers and 
            player_salaries = player_salaries.iloc[1:] # skip the first row
            player_salaries = player_salaries.rename(columns={float(year): 'Salary'}) # Default column title is year e.g. 2024.0. Change to Salary
            player_salaries["Salary"] = player_salaries["Salary"].fillna(MLB_MIN_SALARY_BY_YEAR[year]) # Replace null values with league minimum salary
            players = player_salaries["Player"].to_list()
            salaries = player_salaries["Salary"].to_list()

            # Reformat the player strings
            players = [format_name(player) for player in players]
            # Add the json to the cache

            self.yearly_salary_data[year] = { player: salary for player, salary in zip(players, salaries) }
            
    @property
    def players(self):
        return self._players
    
def dump_data(filepath, data):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    player_scraper = PlayerScraper()
    
    all_player_data = {}
    start = time.time()
    logger.info(f"Started at {start}")
    for i, player in enumerate(list(player_scraper.players.keys())): # Iterate through entire list of active players 
        player_info = player_scraper.get_player_info(player)
        all_player_data[player] = player_info
        if (i % ((AUTO_SAVE_TIME * 60) / SCRAPING_DELAY) == 0):
            dump_data('./static_data/all_player_data.json', all_player_data) # Write back every 20 players as a precaution, approximately every 2 minutes as default 
        time.sleep(SCRAPING_DELAY) # Throttle lookups to avoid violation of Baseball Reference requirements
    dump_data('./static_data/all_player_data.json', all_player_data) # Dump remaining data

    # player_file = "_".join(player.split())
    

    logger.info(f"Player info for all players written to JSON file.")
    logger.info(f"Completed after a duration of {(time.time() - start)/60}m")

if __name__ == "__main__":
    main()