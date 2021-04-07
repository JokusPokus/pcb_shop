import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class Crawler(ABC):
    @abstractmethod
    def __init__(self, url):
        self.url = url

    def _get_html(self):
        """Returns the HTML file returned from a GET request
        to the Crawler instance's URL as bytes.
        """
        try:
            r = requests.get(self.url, timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise Error(http_err)
        except requests.exceptions.RequestException as err:
            raise Error("Connection denied:", err)

        return r.content

    @abstractmethod
    def get_board_options(self):
        pass

