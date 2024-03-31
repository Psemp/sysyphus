import pandas as pd

from sysyphus.models.meteorite import Meteorite


def show_properties(
        meteorite_list: list, ommit: list = [], as_pd: bool = True) -> dict | pd.DataFrame:
    """
    Function:
    - Collects and displays properties of meteorite objects in a structured format.

    - Iterates through a list of Meteorite objects, collecting specified properties
    for each. The properties to be collected can be customized via the `ommit` list.

    - The output can be formatted as either a pandas DataFrame or a standard Python dictionary.

    Args:
        - meteorite_list (list): A list of Meteorite objects whose properties are to be displayed.
        - ommit (list): A list of property names (strings) to be ommitted from the output.
        - as_pd (bool): If True, returns the data as a pandas DataFrame; otherwise, returns a dictionary.

    Returns:
        pd.DataFrame | dict: A pandas DataFrame or dictionary containing the collected meteorite properties,
                                depending on the value of `as_pd`. Each meteorite is represented by a row (DataFrame)
                                or a set of key-value pairs in the dictionary, with properties as columns/keys.

    Raises:
        TypeError: If any object in `meteorite_list` is not an instance of the Meteorite class.
    """

    for meteorite in meteorite_list:
        if not isinstance(meteorite, Meteorite):
            raise TypeError(f"At least one of the objects ({meteorite}) is not of the class Meteorite")

    # Define the columns to be displayed
    columns = [
            "name", "type", "mass", "pieces", "coordinates", "latitude", "longitude", "fall_country",
            "weathering_g", "shock_stage", "mag_sus", "fa_content", "fs_content", "wo_content",  "tsm", "type_spec_loc"
            ]

    columns = [col for col in columns if col not in ommit]
    data_dict = {property: [] for property in columns}

    for meteorite in meteorite_list:
        for property in columns:
            value = getattr(meteorite, property, None)
            data_dict[property].append(value)

    if as_pd:
        df = pd.DataFrame(data_dict)
        return df.set_index("name")
    else:
        return data_dict
