import unittest
from unittest.mock import patch
import requests
from sysyphus.scripts.remote_load import check_internet_connection


class TestRemoteLoad(unittest.TestCase):
    @patch('requests.get')
    def test_check_internet_connection(self, mock_get):
        # Mock the response from requests.get
        mock_get.return_value.status_code = 200

        # Call the function under test
        result = check_internet_connection(url="https://www.qwant.com", timeout=5)

        # Assert that the function returns True when internet connection is available
        self.assertTrue(result)

        # Mock the connection error
        mock_get.side_effect = requests.ConnectionError

        # Call the function under test
        result = check_internet_connection(url="https://www.qwant.com", timeout=5)

        # Assert that the function returns False when internet connection is not available
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
