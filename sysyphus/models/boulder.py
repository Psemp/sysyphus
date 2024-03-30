import pandas as pd
import numpy as np

import warnings

from sysyphus.scripts import remote_load, search, rendering
from sysyphus.scripts import user_requests as u_requests


class Boulder:
    def __init__(self, use_json: bool = True) -> None:
        """
        Initializes the Boulder object for streamlined access to meteorite data. This object checks for an internet
        connection and loads the latest meteorite dataset, available as JSON or pickle.
        The dataset is a prepared clone of parsed data from the MetBull database, updated monthly.

        The Boulder class simplifies data analysis and exploration, offering methods to search, refine,
        and request detailed meteorite information. It's designed for ease of use, enabling efficient data
        handling and analysis without needing extensive programming knowledge.

        Attributes:
        - sy_df (pd.DataFrame): Holds the meteorite data.
        - made_requests (bool): Indicates if detailed data requests have been made.
        - selected_meteorites (pd.DataFrame): Holds the user selection pre request on metbull,
        refine directly for better control
        - met_list (list): Holds the meteorite objects created from the selected_meteorites DataFrame.
        - df_searched (pd.DataFrame): Holds the meteorite properties after requests on metbull have been made.
        It would contain all of the publicly available info on the MetBull for each selected met.

        Methods:
        - make_search: Prompts the user for search parameters and returns a filtered DataFrame.
        - validate_selection: Validates and instanciates the selection contained in `self.selected_meteorites`.
        - dump_search: Deletes the attributes `self.selected_meteorites` & `self.meteorite_objects`
        useful for a fresh start and freeing up memory.
        - request_metbull: Uses threading to request all the meteorites in the meteorites list in parallel.
        - display_search: Collects and displays properties of meteorite objects in a structured format.
        - save_search: Saves the search results to a file in the specified format (CSV by default).

        Prefer JSON for quicker data loading and processing. Boulder serves as the primary tool within the package,
        aimed at facilitating the exploration and analysis of meteorite data.
        """

        if not remote_load.check_internet_connection():
            raise ConnectionError("The application has no access to the internet")
        print("cnx: OK")
        self.sy_df = remote_load.get_remote_data(as_pd=True, use_json=use_json)
        self.sy_df["numeric_id"] = self.sy_df["numeric_id"].astype("Int64")
        self.sy_df["year"] = self.sy_df["year"].astype("Int64")

        print("remote content: Loaded")
        self.made_requests = False

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
        """
        Validates and instanciates the selection of the meteorites contained in `self.selected_meteorites` dataframe.
        If the sample is higher than 200, prompts a warning message and invites the user to refine the query or
        potentially face longer loading times.
        """
        if len(self.selected_meteorites) >= 200:
            warnings.warn(f"You have requested information on {len(self.selected_meteorites)} meteorites. "
                          "This may stress the server and the app. Proceed?")

            while True:
                confirm = input("Enter N|No|Blank to abort, Y|Yes to proceed: ").lower().strip()

                if confirm in ["n", "no", ""]:
                    warnings.warn("Search halted. Reduce dataset size or allow potentially slow requests.")
                    break
                elif confirm in ["y", "yes"]:
                    self.met_list = u_requests.make_meteorites(selected_meteorites=self.selected_meteorites)
                    print("Meteorite objects created and ready to request.")
                    return
                else:
                    print("Invalid input. Please enter Y|Yes to proceed or N|No|Blank to abort.")

        self.met_list = u_requests.make_meteorites(selected_meteorites=self.selected_meteorites)

    def dump_search(self):
        """
        Deletes the attributes `self.selected_meteorites` & `self.meteorite_objects` - useful for a fresh start
        and freeing up memory. Error handling will skip the non initialized attributes.
        """
        try:
            del self.selected_meteorites
        except AttributeError:
            pass

        try:
            del self.met_list
        except AttributeError:
            pass

        self.made_requests = False

    def request_metbull(self, rate_limiter: int = 25) -> None:
        """
        Function:
            Uses threading to request all the meteorites in the meteorites list in parallel.
        All objects in the list must be of the class meteorite,
        the rate limit is set by default to 25 and should not be set higher as a
        consideration for other traffic on the MetBull website.
        Will raise errors if invalid rate limiter.

        Args:
        - rate_limiter : maximum concurrent requests (hard ceilling set to 25)
        """

        if not isinstance(rate_limiter, int):
            try:
                rate_limiter = int(rate_limiter)
            except ValueError:
                raise ValueError("rate_limiter should be of type int")
        if rate_limiter < 1:
            print("Invalid rate_limiter value. Setting to default value of 4.")
            rate_limiter = 4

        self.validate_selection()  # The function being called separetely is an unnecessary extra step

        if rate_limiter > len(self.met_list):
            rate_limiter = len(self.met_list)  # limiter not higher than total search : no extra threads

        u_requests.request_selected(meteorites=self.met_list, rate_limiter=rate_limiter)
        self.made_requests = True

    def display_search(self, ommit: list = [], as_pandas: bool = True) -> pd.DataFrame | dict:
        """
        Function:
        - Collects and displays properties of meteorite objects in a structured format.
        - Uses method defined in sysyphus.scripts.rendering.show_properties()
        - The output can be formatted as either a pandas DataFrame or a standard Python dictionary.

        Args:
        - omit (list): A list of property names (strings) to be omitted from the output.
        - as_pd (bool): If True, returns the data as a pandas DataFrame; otherwise, returns a dictionary.

        Returns:
            pd.DataFrame | dict: A pandas DataFrame or dictionary containing the collected meteorite properties,
                                depending on the value of `as_pd`. Each meteorite is represented by a row (DataFrame)
                                or a set of key-value pairs in the dictionary, with properties as columns/keys.
        """

        if hasattr(self, "met_list") and self.made_requests:
            self.df_searched = rendering.show_properties(meteorite_list=self.met_list, as_pd=as_pandas, ommit=ommit)
            try:
                self.df_searched["mass"] = self.df_searched["mass"].astype(np.float32)
            except AttributeError:
                pass
            return self.df_searched
        elif hasattr(self, "met_list") and not self.made_requests:
            warnings.warn(message="Selection made but no requests have been made on metbull server")

            while True:
                proceed = input("Enter N|No|Blank to abort, Y|Yes to make requests : ").lower().strip()

                if proceed in ["n", "no", ""]:
                    warnings.warn("Process halted, selection kept")
                    break
                elif proceed in ["y", "yes"]:
                    self.request_metbull()
                    self.display_search()
                else:
                    print("Invalid input. Please enter Y|Yes to proceed or N|No|Blank to abort.")

        elif not hasattr(self, "met_list"):
            err_message = "No search & selection were made - use this method once selection and obj. creation are made"
            raise AttributeError(err_message)

    def save_search(self, filepath: str, file_format: str = "csv") -> None:
        """
        Function:
        - Saves the search results to a file in the specified format (CSV by default).
        - The file is saved in the specified location with the specified name.

        Supported formats : csv, pickle, json, parquet

        Args:
        - filepath (str): The path to the directory where the file should be saved.
        - file_format (str): The format in which the file should be saved. Default is "csv".
        Options are csv, pickle, json & parquet.

        Returns:
        - None
        """

        if not hasattr(self, "df_searched"):
            raise AttributeError("No search results to save. Please perform a search and display the results first.")

        if file_format not in ["csv", "pickle", "json", "parquet"]:
            raise ValueError(f"Invalid file format '{file_format}'. Options are csv, pickle, json & parquet.")

        try:
            if file_format == "csv":
                self.df_searched.to_csv(f"{filepath}.csv", index=True)
            elif file_format == "pickle":
                self.df_searched.to_pickle(f"{filepath}.pkl")
            elif file_format == "json":
                self.df_searched.to_json(f"{filepath}.json", orient="records", lines=True)
            elif file_format == "parquet":
                self.df_searched.to_parquet(f"{filepath}.parquet")
            print(f"file saved as {file_format} at {filepath}")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

    def __repr__(self) -> str:
        return f"Boulder(sy_df={self.sy_df.shape})"

    def __str__(self) -> str:
        return f"This Boulder object contains {self.sy_df.shape[0]} rows of meteorite data."
