import unittest
from sysyphus.models import boulder as test_boulder


class TestBoulder(unittest.TestCase):
    def setUp(self):
        self.boulder = test_boulder.Boulder()

    # def test_make_search(self):  # Requires input or mock
    #     result = self.boulder.make_search()
    #     self.assertIsInstance(result, pd.DataFrame)

    def test_validate_selection(self):
        with self.assertRaises(AttributeError):
            self.boulder.validate_selection()

    def test_dump_search(self):
        self.boulder.dump_search()
        self.assertFalse(hasattr(self.boulder, "selected_meteorites"))
        self.assertFalse(hasattr(self.boulder, "met_list"))

    def test_request_metbull(self):
        with self.assertRaises(ValueError):
            self.boulder.request_metbull(rate_limiter="invalid")

    def test_display_search(self):
        with self.assertRaises(AttributeError):
            self.boulder.display_search()

    def tearDown(self):
        del self.boulder


if __name__ == "__main__":
    unittest.main()
