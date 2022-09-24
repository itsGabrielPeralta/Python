""" Script to scraping the Bolsa de Madrid web and get company's negotations """

#######################################################
# LIBRARIES IMPORT                                    #
#######################################################
from operator import truediv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl.workbook import Workbook


#######################################################
# GLOBAL VARIABLES                                    #
#######################################################
url = "https://www.bolsamadrid.es/esp/aspx/Empresas/Negociaciones.aspx?ISIN="
companies_to_scraping = 'empresas.json'


#######################################################
# MAIN LOGIC                                          #
#######################################################

# Load the json file with the companies that we want to scrap
companies = pd.read_json(companies_to_scraping)

# Process each company allocated into the json file
for index, company in companies.iterrows():

    # The company ISIN parameter is added to the url to access to the negotiations section in web page
    individual_url = url + company['isin']
    ticker = company['ticker']

    # Send the request to the web page
    page = requests.get(individual_url)

    # Check if request is ok
    if page.status_code != 200:
        break

    # Define variables to after storage the information
    df = []
    progress = ['To the next page']  # This is fill with some silly information to pass the next filter

    # Check if there are a next page. The first attempt always will be it's for this that next variable is completed with silly information
    while len(progress) > 0:
        # Parsing the web page with Beutifulsoup library
        web_page_soup = BeautifulSoup(page.content, 'html.parser')

        # For each Table Row(tr in html) get the Table Data (td in html)
        for row in web_page_soup.find_all('tr', align="right"):
            tds = row.find_all('td')

            # Check if tds obtained are greater than 5 because the last column we want is the fifth
            if len(tds) > 5:
                # Get the data. The data we want has the format
                # Hour --> column 0
                # Prize --> column 1
                # Volume --> column 2
                # Operation Id --> column 5
                df_row = [tds[0].text, tds[1].text, tds[2].text, tds[5].text]
                # Append this row into the general df where we will get allocated all rows
                df.append(df_row)

        # Until this we have processed the first page but it's possible that web page has more than 1 page with operations
        # Get if there are a next button using his element type and element id
        progress = web_page_soup.find_all('a', id='ctl00_Contenido_SiguientesArr')

        if len(progress) > 0:
            # Copying the cURL Poxis code for POST request to manually advanced to the next page this is the result
            # data = {
            # '__EVENTTARGET': 'ctl00$Contenido$SiguientesArr',
            # '__EVENTARGUMENT': '',
            # '__VIEWSTATE': 'kayBDEeOhuKXDdiQaZADRwqbH+u4+yExqxkJQBr3MCirbP+1I8w4w6jMRMYCuBfaGYle5ZPWzEl89AsSnCdZmV8l63+DA8esF7R2c/sCEI4Xb8MBl5ooPaMF1YbxEpjyVabpcVknXVOhoaMXFbRzXJM1avd1QCEwanrfBZUj3qUpsi6y',
            # '__VIEWSTATEGENERATOR': '8D1B082E',
            # '__EVENTVALIDATION': 'QvQfGfUpbFcQRALTgiIWJXVep0RaAyNVj9W8Fw8RgXngHAGRsPf3x2ysCA8YOLSwxKgepIYGNnU5dRSN8mxq1eCEiwa3YDLpRzUiyYI/F08MwjvGCLOFHQ81acm8cAa/NNovMDS8PBgAlBlDZBykU/EbALZYbNOqirwpw5vX2Do94v59',
            # }
            # We make this code dynamically for get all pages

            __EVENTTARGET = 'ctl00_Contenido_SiguientesArr'
            __EVENTARGUMENT = ''
            __VIEWSTATE = web_page_soup.find('input', id='__VIEWSTATE')['value']
            __VIEWSTATEGENERATOR = web_page_soup.find_all('input', id='__VIEWSTATEGENERATOR')[0]['value']
            __EVENTVALIDATION = web_page_soup.find_all('input', id='__EVENTVALIDATION')[0]['value']

            payload = {'__EVENTTARGET': __EVENTTARGET, '__EVENTARGUMENT': __EVENTARGUMENT, '__VIEWSTATE': __VIEWSTATE,
                           '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR, '__EVENTVALIDATION': __EVENTVALIDATION}
            page = requests.post(individual_url, data=payload)

    # Until here we have obtained all data for a company
    # Now set the data with the correct format to english notation for pandas
    df_pandas = pd.DataFrame(df, columns=['Hour', 'Prize', 'Volume', 'Id'])
    df_pandas['Prize'] = pd.to_numeric(df_pandas['Prize'].str.replace(',', '.'), errors='coerce')
    df_pandas['Volume'] = pd.to_numeric(df_pandas['Volume'].str.replace('.', ''), errors='coerce')
    df_pandas['Id'] = pd.to_numeric(df_pandas['Id'])
            
    # Order by id
    df_pandas = df_pandas.sort_values(by=['Id'])
    df_pandas = df_pandas.reset_index(drop=True)

    # Format to date
    day = df_pandas['Hour'][0].split(" ")[0].replace('/', '_')

    # Generate excel file
    with pd.ExcelWriter('Results/operations' + ticker + '_' + day + '.xlsx') as writer:
        df_pandas.to_excel(writer, sheet_name='All', engine='xlsxwriter')

            
            
