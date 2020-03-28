"""
A module to get json data from COVID19py and translate them to pandas.DataFrame or csv files.
"""

import attr
from enum import Enum
import socket

import COVID19Py
import pandas as pd


class DataSource(Enum):
    """
    Available data sources from COVID19Py:

    JHU: https://github.com/CSSEGISandData/COVID-19 - Worldwide Data repository operated by the
    Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE).

    CSBS: https://www.csbs.org/information-covid-19-coronavirus - U.S. County data that comes
    from the Conference of State Bank Supervisors.
    """

    JHU = 1
    CSBS = 2


@attr.s(auto_attribs=True)
class AvailableCountryData:
    """
    Docs: TODO
    """

    all_data: dict = None
    data_source: DataSource = DataSource.JHU
    _source: str = None

    def __attrs_post_init__(self):
        if not self._has_internet_connection():  # pragma: no cover
            RuntimeError(
                "Internet connection is unavailable. However, internet connection is required."
            )

        if self.data_source == DataSource.JHU:
            self._source = "jhu"
        elif self.data_source == DataSource.CSBS:
            self._source = "csbs"
        else:
            raise ValueError("Unavailable data source.")

        covid19 = COVID19Py.COVID19(data_source=self._source)
        self.all_data = covid19.getAll()

    @property
    def get_dataframe_for_available_countries(self):
        """
        Docs: TODO
        :return:
        """
        country_names = list()
        country_codes = list()
        country_provinces = list()
        for entry in self.all_data["locations"]:
            country_name = entry["country"]
            country_names.append(country_name)

            country_code = entry["country_code"]
            country_codes.append(country_code)

            country_province = entry["province"]
            country_provinces.append(country_province)

        country_database_dict = {
            "name": country_names,
            "code": country_codes,
            "province": country_provinces,
        }

        df_available_countries = pd.DataFrame(country_database_dict)

        return df_available_countries

    @staticmethod
    def _has_internet_connection():
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False