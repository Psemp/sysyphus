# import requests
# import pandas as pd

from sysyphus.scripts import remote_load, search


class Boulder:
    def __init__(self) -> None:
        if not remote_load.check_internet_connection():
            raise ConnectionError("The application has no access to the internet")
        self.sy_df = remote_load.get_remote_data(as_pd=True)

    def make_search(self, search_kind: str, query: str, numeric_range: int | tuple | None = None) -> None:
        match search_kind:
            case "name":
                result = search.search_by_name(df=self.sy_df, name_query=query, numeric_range=numeric_range)
            case "":
                ...

        return result

    def __repr__(self) -> str:
        return f"Boulder(sy_df={self.sy_df.shape})"  # Example: shows the shape of the DataFrame

    def __str__(self) -> str:
        return f"This Boulder object contains {self.sy_df.shape[0]} rows of meteorite data."
