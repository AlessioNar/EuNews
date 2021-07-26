# Create an abstract class scraper

# Its fields are webdriver, max_date, cookie_xpath, container_xpath, datetype

# Methods: navigate, preprocess, cookies_removal, extract_html, parse, create_df, std_dates
from abc import ABC, abstractmethod
import time
import pandas as pd
import dateparser
import bs4
from datetime import date, datetime

class Scraper(ABC):

    # Take as an input an open Firefox webdriver and the maximum date
    @abstractmethod
    def __init__(self, driver, max_date):
        pass

    def initialize_lists(self):
        titles = []
        urls = []
        pub_dates = []
        snippets = []
        return titles, urls, pub_dates, snippets

    def navigate(self):
        self.driver.get(self.url)
        time.sleep(3)

    def preprocess(self):
        pass

    def cookies_removal(self):
        pass

    def extract_html(self):
        container = self.driver.find_element_by_xpath(self.container_xpath)
        container = container.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(container, 'lxml')
        return soup

    @abstractmethod
    def parse(self):
        pass

    def create_df(self, titles, pub_dates, snippets, urls):
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)), columns =['title', 'pub_date', 'snippet', 'url'])
        df['pub_date'] = df['pub_date'].apply(self.std_date)
        return df

    def std_date_general(self, to_date):
        to_date = dateparser.parse(to_date).date()
        return to_date

    def std_date_day(self, to_date):
        to_date = dateparser.parse(to_date, settings={'DATE_ORDER': 'DMY'}).date()
        return to_date

    @abstractmethod
    def std_date(self, to_date):
        pass

    def scrape(self):
        self.navigate()
        self.preprocess()
        self.cookies_removal()
        titles, pub_dates, snippets, urls = self.parse()
        return self.create_df(titles, pub_dates, snippets, urls)
