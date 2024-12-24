import pandas as pd
from dotenv import load_dotenv
import os

data_cache = {}

def read_driver(
    p_name
    , p_app = 'housing'
    , p_purge = False
    , p_data_path = 'R_DATA_PATH'
):
    if p_purge or p_name not in data_cache:

        data_path = os.getenv(p_data_path)

        filename = os.path.join(data_path, p_app, 'drivers', f"{p_name}.csv")
        data_cache[p_name] = pd.read_csv(filename)
    
#   read_driver(p_name = 'cities', p_purge = True)

def read_data(
    p_name = 'dummy'
    , p_app = 'housing'
    , p_path = 'data_clean'
    , p_purge = False
    , p_data_path = 'PYCHE_DATA_PATH'
    , p_obj_name = None
):

    object_name = p_name if p_obj_name is None else p_obj_name

    if p_purge or object_name not in data_cache:

        data_path = os.getenv(p_data_path)

        filename = os.path.join(data_path, p_app, p_path, f"{p_name}.csv")

        data_cache[object_name] = pd.read_csv(filename)

#   read_data(p_name = 'hpi_diffs')
#   read_data(p_name = 'hpi_highs')
