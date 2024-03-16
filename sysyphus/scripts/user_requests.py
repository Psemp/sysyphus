import concurrent.futures
import pandas as pd

from tqdm import tqdm
from sysyphus.models.meteorite import Meteorite


def request_selected(meteorites: list, rate_limiter: int = 25, missing_verbose: bool = False) -> None:
    """
    Function:
        - Uses threading to request all the meteorites in the meteorites list in parallel.
        All objects in the list must be of the class meteorite, the rate limit is set by
        default to 25 and should not be set higher as a consideration for other traffic on the
        MetBull website.

    Args:
        - meteorites : a list that must consist of meteorites instanciated via the search_meteorites() method

    Returns:
        - None, the script executes the object method in parallel and updates the objects directly
    """

    if rate_limiter > 25:
        print(f"Rate limiter of {rate_limiter} > 25, reducing it to 25 for fair use of the app")
        rate_limiter = 25

    for meteorite in meteorites:
        if not isinstance(meteorite, Meteorite):
            raise TypeError(f"At least one of the objects ({meteorite}) is not of the class Meteorite")

    with concurrent.futures.ThreadPoolExecutor(max_workers=rate_limiter) as executor:
        futures = [executor.submit(meteorite.extract_properties) for meteorite in meteorites]

        # Should show a progress bar, fingers crossed
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing meteorites"):
            pass

        # Hopefully no error but this should be useful for debug
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")


def make_meteorites(selected_meteorites: pd.DataFrame):
    meteorite_objects = []
    for mtuple in selected_meteorites.itertuples(index=False):
        meteorite_object = Meteorite(
            name=mtuple.name,
            year=mtuple.year,
            country=mtuple.country,
            type=mtuple.type,
            mass=mtuple.mass,
            url=mtuple.URL
        )

        meteorite_objects.append(meteorite_object)

    return meteorite_objects
