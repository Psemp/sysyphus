import pytest
from unittest.mock import Mock, patch
import pandas as pd
from sysyphus.models.meteorite import Meteorite
from sysyphus.scripts.rendering import show_properties


@pytest.fixture
def meteorite_list():
    # Mock Meteorite objects
    mock_meteorite1 = Mock(spec=Meteorite)
    mock_meteorite2 = Mock(spec=Meteorite)
    # Set up mock properties as needed for the test
    mock_meteorite1.configure_mock(**{
        "name": "MeteoriteA", "type": "Type1",
        "latitude": 10.0, "longitude": 20.0,
        "fall_country": "Country1"
        })
    mock_meteorite2.configure_mock(**{
        "name": "MeteoriteB", "type": "Type2",
        "latitude": 15.0, "longitude": 25.0,
        "fall_country": "Country2"
        })
    return [mock_meteorite1, mock_meteorite2]


# Use patch to override the behavior of isinstance for the duration of the test
@patch("sysyphus.scripts.rendering.isinstance")
def test_show_properties_as_df(mock_isinstance, meteorite_list):
    # Configure the mock to always return True for isinstance checks within the test scope
    mock_isinstance.return_value = True

    # Proceed with the test as normal, now bypassing the isinstance check
    result_df = show_properties(meteorite_list, as_pd=True)
    assert isinstance(result_df, pd.DataFrame), "Expected a pandas DataFrame"
    assert "name" in result_df.index.names, "Expected 'name' to be an index of the DataFrame"
