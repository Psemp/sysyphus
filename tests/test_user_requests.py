import unittest
import pandas as pd

from unittest.mock import patch
from sysyphus.scripts.user_requests import request_selected, make_meteorites
from sysyphus.models.meteorite import Meteorite


class TestUserRequests(unittest.TestCase):

    def test_request_selected(self):
        # Create a list of meteorite objects
        meteorites = [
            Meteorite(name="Meteorite 1", year=2000, country="USA", type="L", mass=100, url="https://example.com"),
            Meteorite(name="Meteorite 2", year=2005, country="Canada", type="H", mass=200, url="https://example.com"),
            Meteorite(name="Meteorite 3", year=2010, country="Australia", type="L", mass=300, url="https://example.com")
        ]

        # Mock the extract_properties method of the Meteorite class
        with patch.object(Meteorite, 'extract_properties') as mock_extract_properties:
            # Call the request_selected function
            request_selected(meteorites)

            # Assert that the extract_properties method is called for each meteorite object
            self.assertEqual(mock_extract_properties.call_count, len(meteorites))

    def test_make_meteorites(self):
        # Create a sample DataFrame
        selected_meteorites = pd.DataFrame({
            'name': ['Meteorite 1', 'Meteorite 2', 'Meteorite 3'],
            'year': [2000, 2005, 2010],
            'country': ['USA', 'Canada', 'Australia'],
            'type': ['L', 'H', 'L'],
            'mass': [100, 200, 300],
            'URL': ['https://example.com', 'https://example.com', 'https://example.com']
        })

        # Call the make_meteorites function
        meteorite_objects = make_meteorites(selected_meteorites)

        # Assert that the number of meteorite objects created is equal to the number of rows in the DataFrame
        self.assertEqual(len(meteorite_objects), len(selected_meteorites))

        # Assert that each meteorite object has the correct attributes
        for i, mtuple in enumerate(selected_meteorites.itertuples(index=False)):
            self.assertEqual(meteorite_objects[i].name, mtuple.name)
            self.assertEqual(meteorite_objects[i].fall_year, mtuple.year)
            self.assertEqual(meteorite_objects[i].fall_country, mtuple.country)
            self.assertEqual(meteorite_objects[i].type, mtuple.type)
            self.assertEqual(meteorite_objects[i].mass, mtuple.mass)
            self.assertEqual(meteorite_objects[i].url, mtuple.URL)


if __name__ == '__main__':
    unittest.main()
