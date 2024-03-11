import requests
import io

import pandas as pd


def get_remote_data(as_pd: bool = True, use_json: bool = True) -> pd.DataFrame | None:
    """
    Fetches a remote dataset from a the remote metbull monthly clone data
    and loads it into a pandas DataFrame.

    Parameters:
        - as_pd: bool : default = True: whether to return the data as a pandas dataframe or a dict (not implemented yet)

    Returns:
        - pandas.DataFrame: The loaded dataset.
    """

    if not use_json:
        url = "https://github.com/Psemp/sysyphus_notebooks/raw/main/datasets/metbull_data.pkl"
    elif use_json:
        url = "https://github.com/Psemp/sysyphus_notebooks/raw/main/datasets/metbull_data.json"

    response = requests.get(url=url)

    if response.status_code == 200:
        data = io.BytesIO(response.content)
        if not use_json:
            df = pd.read_pickle(data)
        else:
            df = pd.read_json(data, orient="records", lines=True)
        return df
    else:
        raise Exception(f"Failed to fetch dataset: {response.status_code}")


def check_internet_connection(url="https://www.qwant.com", timeout=5):
    """
    Pings qwant to check if internet cnx is available
    """
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
