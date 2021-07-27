from scraper import Scraper
import bs4
import time

class EEAScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        #self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//div[@class="entries"]'
        self.url = 'https://www.eea.europa.eu/'

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all('div', {'class':'tileItem visualIEFloatFix'})
            for item in list_item:
                title = item.a.img['title']
                link = item.a['href']
                pub_date = item.div.span.text
                pub_date = self.std_date(pub_date)
                snippet = item.p.span.text
                titles.append(title)
                links.append(link)
                pub_dates.append(pub_date)
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath('//a[@class="next"]')
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
