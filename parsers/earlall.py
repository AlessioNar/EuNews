from scraper import Scraper
import bs4
import time

class EarlAllScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        #self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//div[@id="content-full"]'
        self.url = 'https://www.earlall.eu/news/'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all('li')
            for item in list_item:
                title = item.h3.text.strip()
                url = item.a['href']
                snippet = item.p.find_next().find_next().text
                pub_date = item.p.find_next().find_next().find_next().text
                pub_date = self.std_date(pub_date)
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath('//a[@class="nextpostslink"]')
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
