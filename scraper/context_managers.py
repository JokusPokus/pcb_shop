import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
os.environ['WDM_LOG_LEVEL'] = '0'


class WebDriver:
    """Context Manager for clean web scraping."""
    def __init__(self, browser: str = "Chrome"):
        if browser not in ["Chrome"]:
            raise Exception(f"The browser '{browser}' is currently not supported")

        self.browser = browser
        self.opts = Options()
        self.opts.headless = True
        self.opts.add_argument('log-level=3')

        if self.browser == "Chrome":
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                chrome_options=self.opts
            )

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()