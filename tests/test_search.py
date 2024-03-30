import pandas as pd
import pytest

from sysyphus.scripts.search import (
    search_by_name,
    search_by_type,
    search_by_country,
    validate_name,
    validate_numeric_range,
    validate_country,
    validate_mtype
)


@pytest.fixture
def sample_dataframe():
    data = {
        "name": ["Meteorite1", "Meteorite2", "Meteorite3"],
        "numeric_id": [100, 200, 300],
        "type": ["Type1", "Type2", "Type3"],
        "country": ["Country1", "Country2", "Country3"],
    }
    return pd.DataFrame(data)


def test_search_by_name(sample_dataframe):
    # Test case 1: Search with name query "Meteorite"
    result = search_by_name(sample_dataframe, "Meteorite")
    assert len(result) == 3

    # Test case 2: Search with name query "Meteorite" and numeric range [100, 200]
    result = search_by_name(sample_dataframe, "Meteorite", [100, 200])
    assert len(result) == 2
    assert result.iloc[0]["name"] == "Meteorite1"

    # Test case 3: Search with name query "Meteorite" and numeric range 200
    result = search_by_name(sample_dataframe, "Meteorite", 200)
    assert len(result) == 1
    assert result.iloc[0]["name"] == "Meteorite2"


def test_search_by_type(sample_dataframe):
    # Test case 1: Search with type query "Type1"
    result = search_by_type(sample_dataframe, "Type1")
    assert len(result) == 1
    assert result.iloc[0]["type"] == "Type1"

    # Test case 2: Search with type query "Type4" (non-existent type)
    result = search_by_type(sample_dataframe, "Type4")
    assert isinstance(result, str)
    assert "No meteorite type exactly matching" in result


def test_search_by_country(sample_dataframe):
    # Test case 1: Search with country query "Country2"
    result = search_by_country(sample_dataframe, "Country2")
    assert len(result) == 1
    assert result.iloc[0]["country"] == "Country2"

    # Test case 2: Search with country query "Country4" (non-existent country)
    result = search_by_country(sample_dataframe, "Country4")
    assert isinstance(result, str)
    assert "No meteorite found with country exactly matching" in result


def test_validate_name():
    # Test case 1: Valid name
    name, error = validate_name("ValidName")
    assert name == "ValidName"
    assert error is None

    # Test case 2: Invalid name (less than 2 characters)
    name, error = validate_name("A")
    assert name is None
    assert "Name must be at least 2 characters long" in error


def test_validate_numeric_range():
    # Test case 1: Valid numeric range (single number)
    num_range, error = validate_numeric_range("100")
    assert num_range == 100
    assert error is None

    # Test case 2: Valid numeric range (range of numbers)
    num_range, error = validate_numeric_range("100,200")
    assert num_range == [100, 200]
    assert error is None

    # Test case 3: Invalid numeric range (non-integer input)
    num_range, error = validate_numeric_range("100,abc")
    assert num_range is None
    assert "Numeric ID range must be one or two integers" in error


def test_validate_country():
    # Test case 1: Valid country
    country, message = validate_country("Chile", validation_file="sysyphus/utils/country_validation.json")
    assert country == "chile"
    assert message is None

    # Test case 2: Invalid country (not in the list of countries)
    country, message = validate_country("This shouldnt work", validation_file="sysyphus/utils/country_validation.json")
    assert country is None
    assert "Country not found in the list of countries" in message

    # Test case 3: Blank country
    country, message = validate_country("", validation_file="sysyphus/utils/country_validation.json")
    assert country is None
    assert "blank selected" in message


def test_validate_mtype():
    # Test case 1: Valid mtype
    mtype, message = validate_mtype("h5", validation_file="sysyphus/utils/type_validation.json")
    assert mtype == "h5"
    assert message is None

    # Test case 2: Invalid mtype (not in the list of countries)
    mtype, message = validate_mtype("This shouldnt work either", validation_file="sysyphus/utils/type_validation.json")
    assert mtype is None
    assert "mtype not found in the list of types. Check entire lists utils" in message

    # Test case 3: Blank mtype
    mtype, message = validate_mtype("", validation_file="sysyphus/utils/type_validation.json")
    assert mtype is None
    assert "blank selected" in message
