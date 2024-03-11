import pandas as pd


def search_by_name(df, name_query, numeric_range: int | tuple = None):
    """
    Searches for meteorites based on a name query (ignoring digits in the name) and an optional numeric range.

    Args:
    - df (pd.DataFrame): DataFrame containing meteorite data.
    - name_query (str): The character part of the meteorite names to match.
    - numeric_range (tuple, optional): A tuple specifying the start and end of the numeric range for filtering.

    Returns:
    - pd.DataFrame: DataFrame containing the search results.
    """

    name_filtered = df[
        df["name"].str.replace(r"\d+", "", regex=True).str.strip().str.lower().str.contains(name_query.lower())
        ]

    # Further filter by numeric range if specified
    if isinstance(numeric_range, tuple):
        start, end = numeric_range
        result = name_filtered[(name_filtered["numeric_id"] >= start) & (name_filtered["numeric_id"] <= end)]
    elif isinstance(numeric_range, int):
        result = name_filtered[name_filtered["numeric_id"] == numeric_range]
    else:
        result = name_filtered

    if result.empty:
        return f"ERROR: No meteorite matching '{name_query}' with numeric_id in range {numeric_range} found."

    return result


def search_by_type(df: pd.DataFrame, query: str) -> pd.DataFrame | str:
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
