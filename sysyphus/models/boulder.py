# import requests
import pandas as pd

import warnings

from sysyphus.scripts import remote_load, search
from sysyphus.scripts import user_requests as u_requests


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

    def make_search(self, verbose_results: bool = True) -> pd.DataFrame:
        """
        Prompts the users for search parameters (the user can leave the prompts blank to ignore some).
        Uses the filters to get the meteorites matching the user's request. Returns the dataframe and
        keeps the search in memory to refine and request on in later stages.

        Args:
        - verbose_results : boolean, whether or not to return the dataframe of the results
        (which is saved as object.selected_meteorites regardless). Default is True

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
                message=f"No meteorite found for the requested search parameters:\n{search_parameters}")
        if result.__len__() > 0:
            self.selected_meteorites = result

        if verbose_results:
            return result

    def validate_selection(self):
        if len(self.selected_meteorites) > 200:
            warnings.warn(f"You have requested information on {len(self.selected_meteorites)} meteorites. "
                          "This may stress the server and the app. Proceed?")

            while True:
                confirm = input("Enter N|No|Blank to abort, Y|Yes to proceed: ").lower().strip()

                if confirm in ["n", "no", ""]:
                    warnings.warn("Search halted. Reduce dataset size or allow potentially slow requests.")
                    break
                elif confirm in ["y", "yes"]:
                    self.meteorite_objects = u_requests.make_meteorites(selected_meteorites=self.selected_meteorites)
                    print("Meteorite objects created and ready to request.")
                    return
                else:
                    print("Invalid input. Please enter Y|Yes to proceed or N|No|Blank to abort.")

    def dump_search(self):
        try:
            del self.selected_meteorites
        except AttributeError:
            pass

        try:
            del self.meteorite_objects
        except AttributeError:
            pass

    def __repr__(self) -> str:
        return f"Boulder(sy_df={self.sy_df.shape})"

    def __str__(self) -> str:
        return f"This Boulder object contains {self.sy_df.shape[0]} rows of meteorite data."
