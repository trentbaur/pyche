import pandas as pd
from os import getenv

from dotenv import load_dotenv
load_dotenv()

from shared.utilities import read_driver, data_cache

def read_drivers():

    read_driver(p_app = 'housing', p_name = 'cities')

def read_hpi_canada():
    
    return pd.read_csv(os.getenv('R_DATA_PATH') + 'housing/raw/Cdn Econ Data/teranet.csv')
    
def get_hpi_canada_city(p_city = 'Ottawa'):
    
    read_drivers()
    teranet = read_hpi_canada()

    cities = data_cache['cities']

    city_code = cities.loc[cities['city'] == p_city, 'city_code'].iloc[0]

    city_col = teranet.columns.get_loc(city_code)
    tran_col = teranet.columns.get_loc('Transaction Date')

    hpi = teranet.iloc[1:, [tran_col, city_col, city_col + 4]]

    hpi.columns = ['date', 'index', 'count']

    hpi['index'] = pd.to_numeric(hpi['index'])
    hpi['count'] = pd.to_numeric(hpi['count'])
    hpi['city'] = p_city

    return hpi[hpi['index'] > 0]
#   get_hpi_canada_city()

def preprocess_hpi_canada():

    read_drivers()
    
    cities = data_cache['cities']

    cdn_cities = cities.loc[cities['country'] == 'Canada', 'city']

    # Initialize an empty list to store the results
    result_list = []

    # Loop through each row in the filtered DataFrame
    for city in cdn_cities:
        
        # Call the function and get the result
        city_hpi = get_hpi_canada_city(city)
        
        # Append the result to the list
        result_list.append(city_hpi)

    # Combine all results into a single DataFrame
    combined_results = pd.concat(result_list, ignore_index = True)

    combined_results['date'] = pd.to_datetime('01-' + combined_results['date'], format = '%d-%b-%Y')

    return combined_results
#   preprocess_hpi_canada()

def write_hpi_canada():

    preprocess_hpi_canada().to_csv(path_or_buf = os.getenv('PYCHE_DATA_PATH') + 'housing/working/hpi_canada.csv', index = False)
#   write_hpi_canada()
