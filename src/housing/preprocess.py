import pandas as pd
from os import getenv

from dotenv import load_dotenv
load_dotenv()

def read_hpi():
    hpi_can = pd.read_feather(path = f'{getenv('PYCHE_DATA_PATH')}/housing/working/hpi_canada.feather')

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
    process_hpi_diffs().to_feather(path = getenv('PYCHE_DATA_PATH') + 'housing/data_clean/hpi_diffs.feather')
#   write_hpi_diffs()

def process_hpi_highs():
    diffs = process_hpi_diffs()

    highs = diffs.groupby('city')['index'].max().reset_index(name = 'index')

    joined = pd.merge(diffs, highs, on = ['city', 'index'], how = 'inner')

    return joined[['city', 'index', 'date']]
#   process_hpi_highs()

def write_hpi_highs():
    process_hpi_highs().to_feather(path = getenv('PYCHE_DATA_PATH') + 'housing/data_clean/hpi_highs.feather')
#   write_hpi_highs()
