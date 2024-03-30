import pandas as pd
import json


def search_by_name(df, name_query, numeric_range: int | list = None):
    """
    Searches for meteorites based on a name query (ignoring digits in the name) and an optional numeric range.

    Args:
    - df (pd.DataFrame): DataFrame containing meteorite data.
    - name_query (str): The character part of the meteorite names to match.
    - numeric_range (list, optional): A list specifying the start and end of the numeric range for filtering.

    Returns:
    - pd.DataFrame: DataFrame containing the search results.
    """

    name_filtered = df[
        df["name"].str.replace(r"\d+", "", regex=True).str.strip().str.lower().str.contains(name_query.lower())
        ]

    # Further filter by numeric range if specified
    if isinstance(numeric_range, list):
        start = numeric_range[0]
        end = numeric_range[1]
        result = name_filtered[(name_filtered["numeric_id"] >= start) & (name_filtered["numeric_id"] <= end)]
    elif isinstance(numeric_range, int):
        result = name_filtered[name_filtered["numeric_id"] == numeric_range]
    else:
        result = name_filtered

    if result.empty:
        return f"ERROR: No meteorite matching '{name_query}' with numeric_id in range {numeric_range} found."

    return result


def search_by_type(df: pd.DataFrame, query: str) -> pd.DataFrame | str:
    """
    Returns the dataframe
    """
    query_lower = query.lower()
    df["type_lower"] = df["type"].str.lower()

    matched_df = df[df["type_lower"].str.match(f"^{query_lower}$", case=False, na=False)]

    result_df = matched_df.drop(columns=["type_lower"])
    df.drop(columns=["country_lower", "type_lower"], errors="ignore", inplace=True)

    if result_df.empty:
        return f"ERROR: No meteorite type exactly matching '{query}' found."
    return result_df.drop(columns=["type_lower"], errors="ignore")


def search_by_country(df: pd.DataFrame, query: str) -> pd.DataFrame | str:
    query_lower = query.lower()
    df["country_lower"] = df["country"].str.lower()

    matched_df = df[df["country_lower"].str.match(f"^{query_lower}$", case=False, na=False)]

    result_df = matched_df.drop(columns=["country_lower", "type_lower"], errors="ignore")
    df.drop(columns=["country_lower", "type_lower"], errors="ignore", inplace=True)
    if result_df.empty:
        return f"ERROR: No meteorite found with country exactly matching '{query}' found."
    return result_df


def validate_name(name: str) -> tuple:
    """Checks if name is valid, returning the name or None and an error message."""
    if len(name) >= 2 and any(char.isalpha() for char in name):
        return name, None
    return None, "Name must be at least 2 characters long and include letters."


def validate_numeric_range(num_range: str) -> tuple:
    """Checks if numeric range is valid, returning the range (or int for exact match) and an error message."""

    nums = num_range.split(',')

    if len(nums) == 1 and nums[0].isdigit():
        return int(nums[0]), None

    if len(nums) == 2 and all(num.isdigit() for num in nums):
        return sorted([int(nums[0]), int(nums[1])]), None

    return None, "Numeric ID range must be one or two integers (e.g., 100 or 100,200)."


def validate_country(country: str, validation_file: str) -> tuple:
    """Checks if country is valid, returning the country and an error message, if relevant."""
    with open(file=validation_file, mode="r") as file:
        countries = json.load(file)

    country = country.lower().strip()
    if len(country) > 0:
        if country.lower() in countries:
            return country, None
        else:
            return None, "Country not found in the list of countries. Check entire list in utils"

    elif len(country) == 0:
        return None, "blank selected"


def validate_mtype(mtype: str, validation_file: str) -> tuple:
    """Checks if meteorite type is valid, returning the mtype and an error message, if relevant."""
    with open(file=validation_file, mode="r") as file:
        countries = json.load(file)

    mtype = mtype.lower().strip()
    if len(mtype) > 0:
        if mtype.lower() in countries:
            return mtype.lower(), None
        else:
            return None, "mtype not found in the list of types. Check entire lists utils"

    elif len(mtype) == 0:
        return None, "blank selected"


def get_prompt(prompt_message: str, validation_function: callable = None) -> str | tuple | None:
    """
    Asks for user input and validates it. Re-prompts if the validation fails

    Args:
    - prompt_message: the message prompted to the user
    - validation_function : a callable function (boolean) to validate the user input

    Returns:
    - user prompt (or None if user prompt is empty), type str or tuple of ints
    """
    while True:
        user_input = input(prompt_message).strip()
        if not user_input:  # Skips
            return None
        if validation_function:
            if validation_function == validate_country:
                validation_file = "sysyphus/utils/country_validation.json"
                validation_result, error_message = validation_function(user_input, validation_file)
            elif validation_function == validate_mtype:
                validation_file = "sysyphus/utils/type_validation.json"
                validation_result, error_message = validation_function(user_input, validation_file)
            else:
                validation_result, error_message = validation_function(user_input)

            if validation_result is not None:
                return validation_result
            else:
                print(error_message)
        else:
            return user_input


def search_prompts() -> dict:
    """Prompts the user for search parameters, offering validation and guidance."""
    print("Refine your search. Press Enter to skip any criterion.")

    prompts_and_validation = {
        "namespace": ("Enter name to filter dataset (min. 2 chars): ", validate_name),
        "numeric_range": ("Enter numeric ID range (e.g., 100,200): ", validate_numeric_range),
        "country": ("Refine search by fall country: ", validate_country),
        "type": ("Refine results by types: ", validate_mtype)
    }

    user_inputs = {}
    for param, (message, validation_function) in prompts_and_validation.items():
        user_input = get_prompt(message, validation_function)
        if user_input is not None:
            user_inputs[param] = user_input

    return user_inputs
