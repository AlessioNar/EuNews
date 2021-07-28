from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EurostatScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/eurostat/news/whats-new'
        #self.cookie_xpath = '//a[contains(text(), "Accept only essential cookies")]'
        self.container_xpath = '//ul[@class="product-list"]'
        self.next_xpath = '//a[contains(text(), "Next")]'


    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            soup = self.extract_html()

            list_item = soup.find_all("div", {"class": "product-title"})
            for item in list_item:
                title = item.text.strip()
                url = item.a['href']
                snippet = ''

                titles.append(title)
                urls.append(url)
                snippets.append(snippet)

            list_item = soup.find_all("div", {"class": "product-date"})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
