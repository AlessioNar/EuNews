from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class JRCEventScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/jrc/en/events'
        self.container_xpath = '//div[@class="block block-system panel panel-default clearfix"]'
        self.next_xpath = '//a[@title="Go to next page"]'

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            soup = self.extract_html()
            list_item = soup.find_all('div', {'class':'ds-1col node node-event view-mode-apache_solr_mode clearfix'})
            for item in list_item:
                print(item)
                titletag = item.find('div', {'class':'field field-name-title field-type-ds field-label-hidden'})
                title = titletag.div.div.h3.text
                url = 'https://ec.europa.eu' + titletag.div.div.h3.a['href']
                snippet = ''#item.find('div', {'property':'content:encoded'}).text.strip()
                pub_date = ''#item.find('div', {'class':'date-cont start-date'}).text.strip()
                #pub_date = self.std_date(pub_date)
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
                pub_dates.append(pub_date)
            is_paginated = False

#            if pub_dates[len(pub_dates) - 1] <= self.max_date:
#                is_paginated = False
#            else:
#                self.turn_page()

        return titles, pub_dates, snippets, urls
