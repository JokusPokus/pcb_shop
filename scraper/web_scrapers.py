import time
import bs4

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

from context_managers import WebDriver


class Crawler(ABC):
    @abstractmethod
    def __init__(self, url):
        self.url = url
        self.doc = self._get_doc()

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

    def _get_doc(self):
        html = self._get_html()
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def get_board_options(self):
        pass


class JLCCrawler(Crawler):
    url = "https://cart.jlcpcb.com/quote"

    def __init__(self):
        super().__init__(self.url)

    def _get_html(self):
        with WebDriver("Chrome") as driver:
            driver.get(self.url)

            time.sleep(2)
            return driver.page_source

    def _get_board_option_divs(self):
        def is_div_with_label(tag):
            return (
                tag.name == "div"
                and any([child.name == "label" for child in tag.contents])
            )
        main_div = self.doc.find("div", class_="home-orderadd-pcb")
        return main_div.find_all(is_div_with_label)

    @staticmethod
    def _parse_single_option(option):
        first_div_in_label = option.label.find("div")

        if first_div_in_label is None:
            return None

        siblings = first_div_in_label.previous_siblings

        for sibling in siblings:
            if isinstance(sibling, bs4.element.Comment):
                continue

            elif isinstance(sibling, bs4.element.NavigableString) and sibling.strip() != "":
                return str(sibling).strip()

            elif isinstance(sibling, bs4.element.Tag):
                return str(sibling.string).strip()
        return None

    def _parse_board_options(self):
        board_options = self._get_board_option_divs()

        option_labels = []
        for option in board_options:
            label = self._parse_single_option(option)
            if label is not None:
                option_labels.append(label)
        return option_labels

    def get_board_options(self):
        pass


if __name__ == "__main__":
    crawler = JLCCrawler()
    print(crawler._parse_board_options())
