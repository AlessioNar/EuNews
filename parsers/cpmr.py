from scraper import Scraper
import bs4
import time

class CPMRScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//span[@id="reject_cookies"]'
        self.container_xpath = '//div[@id="posts-container"]'
        self.url = 'https://cpmr.org/news/'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        counter = 1
        is_paginated = True

        while is_paginated:

            soup = self.extract_html()

            list_item = soup.find_all('div', {'class':'fusion-post-content post-content'})
            for item in list_item:
                title = item.h2.text.strip()
                url = item.h2.a['href']
                snippet = item.div.p.text.strip()
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
            list_item = soup.find_all('div', {'class':'fusion-date-box'})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                counter = counter + 1
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

        return titles, pub_dates, snippets, urls
