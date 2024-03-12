# import requests
# import pandas as pd

import warnings

from sysyphus.scripts import remote_load
from sysyphus.scripts import search


class Boulder:
    def __init__(self, use_json: bool = True) -> None:
        """
        Initialises the Boulder object, loads remote data from
        https://github.com/Psemp/sysyphus_notebooks , either pkl or json.
        Json seems faster but pkl is still an option just in case.
        """

        if not remote_load.check_internet_connection():
            raise ConnectionError("The application has no access to the internet")
        self.sy_df = remote_load.get_remote_data(as_pd=True, use_json=True)

    def make_search(self) -> None:
        """
        Prompts the users for search parameters (the user can leave the prompts blank to ignore some).
        Uses the filters to get the meteorites matching the user's request. Returns the dataframe and
        keeps the search in memory to refine and request on in later stages.

        Returns:
        - result : a pd.DataFrame: A filtered DataFrame containing meteorite entries that match the specified
        search parameters. If no parameters are matched, an empty DataFrame is returned.
        """

        result = self.sy_df.copy(deep=True)
        search_parameters = search.search_prompts()

        if len(search_parameters.keys()) < 1:
            raise ValueError("No search parameters provided, please retry.")

        if "namespace" in search_parameters.keys():
            if "numeric_range" in search_parameters.keys():
                numeric_range = search_parameters["numeric_range"]
            else:
                numeric_range = None
            result = search.search_by_name(
                df=result, name_query=search_parameters["namespace"], numeric_range=numeric_range
                )
        if "country" in search_parameters.keys():
            result = search.search_by_country(df=result, query=search_parameters["country"])
        if "type" in search_parameters.keys():
            result = search.search_by_type(df=result, query=search_parameters["type"])

        if result.__len__() == 0:
            warnings.warn(
                message=f"No meteorites found for the requested search parameters:\n{search_parameters}")
        if result.__len__() > 0:
            self.selected_meteorites = result

        return result

    def __repr__(self) -> str:
        return f"Boulder(sy_df={self.sy_df.shape})"  # Example: shows the shape of the DataFrame

    def __str__(self) -> str:
        return f"This Boulder object contains {self.sy_df.shape[0]} rows of meteorite data."
