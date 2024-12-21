import pandas as pd
from dotenv import load_dotenv
import os

data_cache = {}

def read_driver(
    p_name,
    p_app = 'housing',
    p_purge = False,
    p_data_path = 'R_DATA_PATH'
):
    if p_purge or p_name not in data_cache:

        data_path = os.getenv(p_data_path)

        filename = os.path.join(data_path, p_app, 'drivers', f"{p_name}.csv")
        data_cache[p_name] = pd.read_csv(filename)
    
    return data_cache[p_name]

#   read_driver(p_name = 'cities', p_purge = True)
