import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

from shared.utilities import *
from datetime import datetime
from statsmodels.distributions.empirical_distribution import ECDF

read_data(p_name = 'hpi_diffs', p_app = 'housing', p_path = 'data_clean')
read_data(p_name = 'hpi_highs', p_app = 'housing', p_path = 'data_clean')

read_driver(p_app = 'housing', p_name = 'year_colors')

def load_city_melted(
    p_city = 'Ottawa'
    , p_variable = 'count'
    , p_start_year = 1972
):

    hpi_diffs = data_cache['hpi_diffs']
    
    hpi_diffs['date'] = pd.to_datetime(hpi_diffs['date'])
    hpi_diffs['year'] = hpi_diffs['date'].dt.year
    hpi_diffs['month'] = hpi_diffs['date'].dt.month

    start_date = pd.to_datetime(f'{p_start_year}-01-01')

    result = hpi_diffs[(hpi_diffs['date'] >= start_date) & (hpi_diffs['city'] == p_city)][['date', 'year', 'month', 'city', p_variable]]

    result.rename(columns = {p_variable: 'value'}, inplace = True)

    return result
#   load_city_melted()
#   load_city_melted(p_variable = 'index')

def load_all_cities_melted(
    p_variable = 'change1'
    , p_date = hpi_diffs['date'].max()
):
    count_data = hpi_diffs[
        (hpi_diffs['date'].dt.year < p_date.year) 
        & (hpi_diffs['date'].dt.month == p_date.month)
        ][['date', 'city', 'index', p_variable]]

    count_data['year'] = count_data['date'].dt.year
    count_data['month'] = count_data['date'].dt.month

    count_data.rename(columns = {p_variable: 'value'}, inplace = True)

    medians = (
        count_data[count_data['date'].dt.year != p_date.year]
        .groupby('city')['value']
        .median()
        .reset_index(name = 'median')
    )

    result = pd.merge(
        count_data[count_data['value'].notnull()]
        , medians
        , on = 'city'
        , how = 'inner'
    )

    return result
#   load_all_cities_melted()

def ecdf_fun(values, perc):
    val = ECDF(values)(perc)

    if len(val) == 0:
        val = 0

    return val

def get_city_percentiles(
    p_city = 'Ottawa'
    , p_variable = 'change1'
    , p_date = None
    , p_month_count = 12
):

    if p_date is None:
        p_date = hpi_diffs['date'].max()

    dt = load_city_melted(p_city = p_city
                          , p_variable = p_variable)

    dates = pd.date_range(p_date - pd.DateOffset(months = p_month_count), p_date, freq = 'MS')
    
    # Initialize an empty list to store the results
    result_list = []

    for d in dates:

        result = ecdf_fun(dt[(dt['date'] < d)
                              & (dt['date'].dt.month == d.month)]['value']
                        , dt[dt['date'] == d]['value']
                )

        # Append the result to the list
        result_list.append(result)

    return result_list

get_city_percentiles()
get_city_percentiles(p_date = datetime.strptime('2022-05-01'))
