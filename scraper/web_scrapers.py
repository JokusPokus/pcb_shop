import time

from typing import Dict, List, TypeVar, Optional
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment

from context_managers import WebDriver


HtmlString = str


class Crawler(ABC):
    @abstractmethod
    def __init__(self, url):
        self.url = url
        self.doc = self._get_doc()

    def _get_html(self) -> HtmlString:
        """Returns a string representation of the HTML returned from a GET request
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
        """Returns a BeautifulSoup object around the crawler instance's html page."""
        html = self._get_html()
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def get_board_options(self) -> Dict:
        """Returns a dictionary with all current option labels as keys
        and lists of the according choices as values."""
        pass


class JLCCrawler(Crawler):
    url = "https://cart.jlcpcb.com/quote"

    def __init__(self):
        super().__init__(self.url)

    def _get_html(self) -> HtmlString:
        """Uses a webdriver to send a GET request to the crawler instance's <self.url>.

        The returned html page is already (dynamically) rendered by the web driver and
        is represented as a string.
        """
        with WebDriver("Chrome") as driver:
            driver.get(self.url)

            # Ensure that html is fully rendered through JavaScript
            time.sleep(2)
            return driver.page_source

    def _get_board_option_divs(self) -> List[Tag]:
        """On the JLCPCB site, information about each board option is encapsulated in an html div
        that contains a label tag. This function returns a list of such container divs.
        """
        def is_div_with_label(tag: Tag) -> bool:
            """Returns True if the <tag> is an html div that contains a label div,
            otherwise False.
            """
            return (
                tag.name == "div"
                and any([child.name == "label" for child in tag.contents])
            )
        # All divs containing board option information are located within
        # a large div with the class "home-orderadd-pcb":
        main_div = self.doc.find("div", class_="home-orderadd-pcb")
        return main_div.find_all(is_div_with_label)

    @staticmethod
    def _get_option_label(option_div: Tag) -> Optional[str]:
        """Accepts an option container div and returns the label of that option,
        or None if no label can be found."""
        first_div_in_label = option_div.label.find("div")

        if first_div_in_label is None:
            return None

        siblings = first_div_in_label.previous_siblings

        for sibling in siblings:
            if isinstance(sibling, Comment):
                continue

            elif isinstance(sibling, NavigableString) and sibling.strip() != "":
                return str(sibling).strip()

            elif isinstance(sibling, Tag):
                return str(sibling.string).strip()
        return None

    @staticmethod
    def _get_option_values_from_form_group(option_div: Tag) -> List:
        """In the JLCPCB html, most option values are represented as buttons
        within a div with css class 'formgroup'.

        This function returns a list of all option values found in such a
        formgroup div.
        """
        form_group_div = option_div.find("div", class_="formgroup")
        try:
            option_values = [button.string.strip() for button in form_group_div.find_all("button")]
            return option_values
        except Exception:
            return None

    def _parse_board_options(self) -> Dict[str, List]:
        board_option_divs = self._get_board_option_divs()

        board_options = {}
        for div in board_option_divs:
            label = self._get_option_label(div)
            if label is not None:
                values = self._get_option_values_from_form_group(div)
                board_options[label] = values
        return board_options

    def get_board_options(self):
        return self._parse_board_options()

    def show_option_div(self):
        print(self._get_board_option_divs()[0].prettify())

    def show_option_divs(self):
        for div in self._get_board_option_divs():
            print(div.prettify())


if __name__ == "__main__":
    crawler = JLCCrawler()
    # crawler.show_option_divs()
    print(crawler.get_board_options())
