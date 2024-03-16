import re
import numpy as np


def dms_to_decimal(dms: str) -> float:
    """
    Converts DMS coordinates to decimal format, accommodating various formats including simple degrees.

    Patterns are mostly formed via autoregex.xyz and GPT-4, both are better at explaining regex than any human
    """
    # On the off chance its already in a decimal format :
    try:
        return float(dms)
    except (ValueError, TypeError):
        if dms is None:
            return np.nan

    dms_cleaned = re.sub(r"\s+", "", dms.replace("''", '"'))
    dms_cleaned = dms_cleaned.replace("~", "")
    # Match various DMS patterns
    patterns = [
        r"(\d+\.?\d*)°([NSWE])",  # Matches simple degrees with direction
        r"(\d+)°(\d+\.?\d*)'([NSWE])",  # Matches degrees and decimal minutes with direction
        r"(\d+)°(\d+)'(\d*\.?\d*)?\"?([NSWE])",  # Matches full DMS with optional seconds
    ]

    for pattern in patterns:
        match = re.match(pattern, dms_cleaned)
        if match:
            parts = match.groups()
            degrees = float(parts[0])
            minutes = float(parts[1]) if len(parts) > 2 else 0
            seconds = float(parts[2]) if len(parts) > 3 else 0
            direction = parts[-1]

            # Calculate decimal value
            decimal = degrees + minutes / 60 + seconds / 3600
            if direction in ('S', 'W'):
                decimal *= -1
            return decimal

    return np.nan


def handle_coordinates(latitude: str, longitude: str) -> tuple:
    """
    Function :
        - Converts lat/lon in degrees, minutes seconds to floating decimals (+/-)
        and returns it as a tuple of lat/lon (decimals)
    Args :
        - latitude : a string AB°CD'EF.GH"N|S
        - latitude : a string IJ°KL'MN.OP"E|W
    Returns :
        - Tuple of lat/lon (decimals)
    """

    lat_decimal = dms_to_decimal(latitude)
    lon_decimal = dms_to_decimal(longitude)

    if lat_decimal is not np.nan and lon_decimal is not np.nan:
        return (lat_decimal, lon_decimal)
    else:
        return (np.nan, np.nan)  # incomplete coordinates will yield a full error if just one param is na


def remove_uncertainty(to_process: str) -> float:
    """
    Removes uncertainty or additional annotations from the string and returns the numeric part as a float.

    Args:
        to_process (str): The string to process, removing any annotations like '±' and '(n=someshit)'.

    Returns:
        float: The floating-point value extracted from the beginning of the input string.
    """

    # This pattern matches optional leading sign, digits, optional decimal point, and more digits
    match = re.match(r"[-+]?\d*\.?\d+", to_process)

    if match:
        value = match.group()
        return float(value.strip())
    else:
        return np.nan
