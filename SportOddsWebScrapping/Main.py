""" Script to do scrapping for sports odds """

#######################################################
# LIBRARIES IMPORT                                    #
#######################################################
from selenium import webdriver
from selenium.webdriver.common.by import By

#######################################################
# GLOBAL VARIABLES                                    #
#######################################################

# Set the variable with the url's event
url_event = 'https://www.oddsportal.com/soccer/spain/laliga/ath-bilbao-rayo-vallecano-2uVLNgsi/'



#######################################################
# FUNCTIONS                                           #
#######################################################

def get_data_by_xpath(driver):
    # With the browser open in url we want now get the data by xpath
    data_by_xpath = {}
    # Get the local team. The rpartition divide the string from a character introduced
    data_by_xpath['local_team'] = driver.find_elements(By.XPATH, '//*[@id="col-content"]/h1')[0].text.rpartition('-')[0][:-1] # Remove the last character that is a space
    # Get the away team
    data_by_xpath['away_team'] = driver.find_elements(By.XPATH, '//*[@id="col-content"]/h1')[0].text.rpartition('-')[2][1:] # Remove the last character that is a space
    # Get the match date
    data_by_xpath['date'] = driver.find_elements(By.XPATH, '//*[@id="col-content"]/p[1]')[0].text

    return data_by_xpath


def complete_match_data(url_event, data_by_xpath):
    match_dictionary = {}
    # Add the url
    match_dictionary['url'] = url_event
    # Add the sport. This is without scrapping but splitting the url where are a lot of information
    match_dictionary['sport'] = url_event.split('/')[3]
    # Add the match country
    match_dictionary['country'] = url_event.split('/')[4]
    # Add the match category
    match_dictionary['category'] = url_event.split('/')[5]
    # Add the match code event
    match_dictionary['code_event'] = url_event.split('/')[6].split('-')[2]
    # Add the teams
    match_dictionary['local_team'] = data_by_xpath['local_team']
    match_dictionary['away_team'] = data_by_xpath['away_team']
    # Add the date
    match_dictionary['date'] = data_by_xpath['date']

    return match_dictionary

def get_all_markets(driver):
    
    # When access into the web there are a table with the markets and their odds. Of all this tables just one are shown and the others are hidden. 
    # First, would be process the active and the the others. This is storaged into dictionary variables
    active_markets = []
    hide_markets = []

    markets_list = driver.find_elements(By.XPATH, '//*[@id="bettype-tabs"]/ul/li')

    # Process the markets and get associated with an index
    for idx, val in enumerate(markets_list):
        # Filter for get the markets with the values we want
        if val.text not in ['', 'More bets']:
            active_markets.append([idx, val.text])



#######################################################
# MAIN LOGIC                                          #
#######################################################

# Initiate the virtual web browser. For this is needed a driver in the same directory that this file

# To use the driver is possible add some options to browser. Initiate the options
driverOptions = webdriver.chrome.options.Options()
# Headless command open the window if is false
driverOptions.headless = False

driver = webdriver.Chrome(options=driverOptions)

# Access to the url
driver.get(url_event)

# Get the data with xpath method
data_by_xpath = get_data_by_xpath(driver)

# Initialize the script output that is a dictionary and set the values
match_dictionary = complete_match_data(url_event, data_by_xpath)

# Get the label for the odds. Example: 1 X 2
label_element = driver.find_element(By.XPATH, '//*[@id="odds-data-table"]/div[1]/table/thead/tr')
label = label_element.text.split(' ')[1:-1]

# Get the odds table into a variable
odds_table = driver.find_elements(By.XPATH, '//*[@id="odds-data-table"]/div[1]/table/tbody/tr')

# Declare the variable to storaged the odds 
odd_dict = {}

# Process all elements storaged in odds_table variable
for row in odds_table:
    # Odds information like portal web and the odds are in the text section from rows got from url
    odds_information = row.text     # Example: 10x10bet  \n4.40\n3.53\n1.93\n97.2%

    # odds_table has been completed with some data it's not neccessary and that have empty information so this has to be controlled
    if odds_information == '':
        continue

    # Remove the spaces and separates for each component with split getting a list 
    odds_list = odds_information.replace(' ','').split('\n')

    number_list = []
    string_list = []
    # Get in separate variables the portal web name and the odds number
    for component in odds_list:
        # Try convert into float. If fail is because is a string and not a number
        try:
            number_list.append(float(component))
        except:
            string_list.append(component)

    # Variable to the portal web
    bookie = string_list[0]

    # Dictionary variable related with the bookie to storaged the odds
    odd_dict[bookie] = {}

    # Process the label comparing with odds value
    for i in range(len(label)):
        odd_dict[bookie][label[i]] = number_list[i]







