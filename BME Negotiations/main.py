from data_collect import data_collect
import pandas as pd


#######################################################
# GLOBAL VARIABLES                                    #
#######################################################
companies_to_scraping = 'empresas.json'


#######################################################
# MAIN LOGIC                                          #
#######################################################

# Load the json file with the companies that we want to scrap
companies = pd.read_json(companies_to_scraping)

for index, company in companies.iterrows():
    ticker = company['ticker']
    # Get the company negotiations
    df = data_collect(company)



    # Now set the data with the correct format to english notation for pandas
    df_pandas = pd.DataFrame(df, columns=['Hour', 'Prize', 'Volume', 'Id'])
    df_pandas['Prize'] = pd.to_numeric(df_pandas['Prize'].str.replace(',', '.'), errors='coerce')
    df_pandas['Volume'] = pd.to_numeric(df_pandas['Volume'].str.replace('.', ''), errors='coerce')
    df_pandas['Id'] = pd.to_numeric(df_pandas['Id'])           
    # Order by id
    df_pandas = df_pandas.sort_values(by=['Id'])
    df_pandas = df_pandas.reset_index(drop=True)



    # Variable definition to storaged the data we want
    df_same_operation = []
    start_prize = 0
    previous_prize = 0
    volume_sum = 0
    last_hour = df_pandas['Hour'][0]
    operations = 0
    operation_performed = 'Initial Operation'



    # Process each operation in df_pandas to clean the data in the format we want
    for index_ops, operation in df_pandas.iterrows():
        # There are some operations that ocurred in the same milisecond so it's obvious that owns to the same person so accumulate all this operations into one row
        if last_hour == operation['Hour']:
            # This is for operations in the same milisecond
            volume_sum = volume_sum + operation['Volume']
            previous_prize = operation['Prize']
            operations = operations + 1
        else:
            
            if start_prize == 0:
                operation_performed = 'Initial Operation'
            elif start_prize > previous_prize:
                operation_performed = 'Buy'
            elif start_prize < previous_prize:

                operation_performed = 'Sell'
            # If the prize is the same we guess that is a continuation operation

            # Add the data to a row into the dataframe
            df_row = [operation_performed, last_hour, previous_prize, volume_sum, operations, previous_prize * volume_sum]
            df_same_operation.append(df_row)

            # Restart the variables
            last_hour = operation['Hour']
            operations = 1
            volume_sum = operation['Volume']
            start_prize = previous_prize

    # Record the last operation
    df_row = ['Final Operation', last_hour, previous_prize, volume_sum, operations, previous_prize * volume_sum]
    df_same_operation.append(df_row)

    # DataFrame with the operations
    df_pandas_same_operations = pd.DataFrame(df_same_operation, columns=["Operation", "Hour", "Prize", "Volume", "Num. Operations", "Import"])

    day = df_pandas['Hour'][0].split(" ")[0].replace('/', '_')

    # Generate the excel file
    with pd.ExcelWriter('Results/operations_' + ticker + '_' + day + '.xlsx') as writer:
        df_pandas_same_operations.to_excel(writer, sheet_name='Resume', engine='xlsxwriter')
        df_pandas.to_excel(writer, sheet_name='All', engine='xlsxwriter')

