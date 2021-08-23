from scraper import Scraper
import bs4
import time

class EarlAllEventScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        #self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//ul[@class="list-events"]'
        self.url = 'https://www.earlall.eu/event/'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):
        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        soup = self.extract_html()

        list_item = soup.find_all('li')
        print(list_item)
        for item in list_item[:-1]:
            title = item.h3.text.strip()
            print(title)
            url = item.a['href']
            pub_date = item.p.text.strip()
            pub_date = self.std_date(pub_date)
            snippet = ''
            titles.append(title)
            urls.append(url)
            snippets.append(snippet)
            pub_dates.append(pub_date)


        return titles, pub_dates, snippets, urls
