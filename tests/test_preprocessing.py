import pytest
import numpy as np
from sysyphus.scripts.preprocessing import dms_to_decimal, handle_coordinates, remove_uncertainty


def test_dms_to_decimal():
    assert dms_to_decimal("34°12'24\"N") == pytest.approx(34.20666666666667)
    assert dms_to_decimal("34°12.4'S") == pytest.approx(-34.20666666666667)
    assert dms_to_decimal("45.0°N") == 45.0
    assert np.isnan(dms_to_decimal("invalid"))
    assert dms_to_decimal("123.456") == pytest.approx(123.456)
    assert np.isnan(dms_to_decimal(None))


def test_handle_coordinates():
    assert handle_coordinates(
        "34°12'24\"N", "45°12'24\"W") == (
            pytest.approx(34.20666666666667),
            pytest.approx(-45.20666666666667)
            )
    assert handle_coordinates("invalid", "45°12'24\"W") == (np.nan, np.nan)
    assert handle_coordinates("34°12'24\"N", "invalid") == (np.nan, np.nan)
    assert handle_coordinates(None, None) == (np.nan, np.nan)


def test_remove_uncertainty():
    assert remove_uncertainty("123.45±0.67") == pytest.approx(123.45)
    assert remove_uncertainty("-123.45(n=6)") == pytest.approx(-123.45)
    assert remove_uncertainty("+123") == pytest.approx(123)
    assert np.isnan(remove_uncertainty("Not a number"))
    assert np.isnan(remove_uncertainty(""))
    assert np.isnan(remove_uncertainty("±±±"))
