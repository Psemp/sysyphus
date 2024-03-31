import re
import requests
import gc

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from sysyphus.scripts.preprocessing import handle_coordinates, remove_uncertainty


class Meteorite:
    def __init__(
            self, name: str, year: str, country: str,
            type: str, mass: str, url: str,
            ) -> None:

        self.name = name

        try:
            self.fall_year = int(year)
        except (ValueError, TypeError):
            self.fall_year = None

        if country is not None and "," in country:
            self.fall_country = country.split(",")[-1].replace(" ", "")
        elif country is not None:
            self.fall_country = country
        elif country is None:
            self.fall_country = "unknown"

        if type is not None and not pd.isna(type):
            self.type = re.sub(r"[^\w\s]", "", type)
        else:
            self.type = None
        self.url = url
        self.mass = mass

        self.latitude = np.nan
        self.longitude = np.nan
        self.weathering_g = None
        self.mag_sus = np.nan
        self.fs_content = None
        self.wo_content = None
        self.fa_content = None
        self.tsm = np.nan
        self.pieces = None
        self.type_spec_loc = None
        self.shock_stage = None
        self.coordinates = None

        self.table_soup = None

        # This dictionary maps the textual references to the class attributes
        self.property_map = {
            "Latitude:": "latitude",
            "Longitude:": "longitude",
            "Mass": "mass",
            "Weathering grade:": "weathering_g",
            "Magnetic suscept.:": "mag_sus",
            "Ferrosilite (mol%):": "fs_content",
            "Wollastonite (mol%):": "wo_content",
            "Fayalite (mol%):": "fa_content",
            "Type spec mass (g):": "tsm",
            "Pieces:": "pieces",
            "Type spec location:": "type_spec_loc",
            "Shock stage:": "shock_stage"
        }

    def get_soup(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        }

        try:
            r = requests.get(url=self.url, headers=headers)
            r.raise_for_status()  # Raises an HTTPError for bad responses

            soup = BeautifulSoup(r.content, "html.parser")
            main_table = soup.find("table", id="maintable")
            data_from_element = main_table.find(lambda tag: tag.name == "big" and "Data from:" in tag.text)

            if data_from_element:
                data_from_td = data_from_element.find_parent("td")
                self.table_soup = data_from_td.find_next_sibling("td")
            else:
                self.table_soup = None

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            self.table_soup = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.table_soup = None

    def purge_html(self):
        """
        Frees memory by purging the html cace of the object
        """
        self.table_soup = None
        gc.collect()

    def extract_properties(self, purge_after: bool = True):
        if self.table_soup is None:
            self.get_soup()
        if self.table_soup is not None:
            for reference, attr_name in self.property_map.items():
                prop_td = self.table_soup.find("td", text=lambda text: text and reference in text)

                if prop_td:
                    value_td = prop_td.find_next_sibling("td")
                    if value_td:
                        setattr(self, attr_name, value_td.text.strip())
        else:
            self.get_soup()
            if self.table_soup is None:
                print("The table couldnt be found")
                print(f"You can find more informations for this meteorite here : {self.url}")

        self.coordinates = handle_coordinates(latitude=self.latitude, longitude=self.longitude)

        if self.fa_content is not None:
            self.fa_content = remove_uncertainty(to_process=self.fa_content)

        if self.fs_content is not None:
            self.fs_content = remove_uncertainty(to_process=self.fs_content)

        if self.wo_content is not None:
            self.wo_content = remove_uncertainty(to_process=self.wo_content)
        if purge_after:
            self.purge_html()

    def get_properties(self, as_pd: bool = False):

        property_dict = {
                "Name": self.name, "Year": self.fall_year, "Coordinates (dec)": self.coordinates,
                "Mass": self.mass, "Weathering grade": self.weathering_g, "Magnetic susceptibility": self.mag_sus,
                "Ferrosilite": self.fs_content, "Fayalite": self.fa_content,
                "Type specific mass": self.tsm, "Pieces": self.pieces,
                "Location of the subsample": self.type_spec_loc, "Shock stage": self.shock_stage
            }

        if not as_pd:
            return property_dict

        if as_pd:
            data = [[value] for value in property_dict.values()]
            property_df = pd.DataFrame(data, columns=["Value"], index=property_dict.keys())
            property_df = property_df.T
            return property_df

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
