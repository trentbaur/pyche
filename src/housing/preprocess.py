import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

def read_hpi():

    hpi_can = pd.read_csv(f'{os.getenv('PYCHE_DATA_PATH')}/housing/working/hpi_canada.csv')
    hpi_can['country'] = 'Canada'

    hpi_can['date'] = pd.to_datetime(hpi_can['date'])
    hpi_can['year'] = hpi_can['date'].dt.year
    hpi_can['month'] = hpi_can['date'].dt.month

    return hpi_can
#   read_hpi()

def process_hpi_diffs():

    changes = read_hpi()

    changes['change1'] = (changes['index'] - changes.groupby('city')['index'].shift(1)) / changes.groupby('city')['index'].shift(1)
    changes['change12'] = (changes['index'] - changes.groupby('city')['index'].shift(12)) / changes.groupby('city')['index'].shift(12)

    changes['countperc1'] = (changes['count'] - changes.groupby('city')['count'].shift(1)) / changes.groupby('city')['count'].shift(1)
    changes['countperc12'] = (changes['count'] - changes.groupby('city')['count'].shift(12)) / changes.groupby('city')['count'].shift(12)

    changes['countraw1'] = changes.groupby('city')['count'].shift(1)
    changes['countraw12'] = changes.groupby('city')['count'].shift(12)

    return changes
#   process_hpi_diffs()

def write_hpi_diffs():

    process_hpi_diffs().to_csv(path_or_buf = os.getenv('PYCHE_DATA_PATH') + 'housing/data_clean/hpi_diffs.csv', index = False)

def process_hpi_highs():

    diffs = process_hpi_diffs()

    highs = diffs.groupby('city')['index'].max().reset_index(name = 'index')

    joined = pd.merge(diffs, highs, on = ['city', 'index'], how = 'inner')

    return joined[['city', 'index', 'date']]

#   process_hpi_highs()

def write_hpi_highs():

    process_hpi_highs().to_csv(path_or_buf = os.getenv('PYCHE_DATA_PATH') + 'housing/data_clean/hpi_highs.csv', index = False)

#   write_hpi_diffs()
#   write_hpi_highs()
