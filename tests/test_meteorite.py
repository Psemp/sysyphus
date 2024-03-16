import unittest
from sysyphus.models.meteorite import Meteorite


class TestMeteorite(unittest.TestCase):

    def setUp(self):
        self.meteorite = Meteorite(
            name="Sample Meteorite",
            year="2022",
            country="USA",
            type="Iron",
            mass="1000 kg",
            url="https://example.com"
        )

    def test_purge_html(self):
        self.meteorite.purge_html()
        self.assertIsNone(self.meteorite.table_soup)

    # def test_extract_properties(self):
    #     self.meteorite.extract_properties()
    #     # Add assertions to validate the extracted properties

    def test_get_properties(self):
        properties = self.meteorite.get_properties()
        self.assertIsInstance(properties, dict)

    def test_str(self):
        string_representation = str(self.meteorite)
        # Add assertions to validate the string representation

    def test_repr(self):
        repr_representation = repr(self.meteorite)
        # Add assertions to validate the repr representation


if __name__ == '__main__':
    unittest.main()
