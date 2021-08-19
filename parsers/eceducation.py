from scraper import Scraper, PaginatedScraper
import bs4
import time

class ECEducationScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/education/news_en'
        self.container_xpath = '//section[@id="block-views-eat-news-page-news-block"]'
        self.next_xpath = '//a[@class="btn btn-secondary btn-show-more"]'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()
            soup = soup.div.find('div', {'class':'view-content'})
            list_item = soup.find_all('div',{'class':'views-field views-field-title'})
            for item in list_item:
                title = item.text.strip()
                url = 'https://ec.europa.eu' + item.a['href']
                snippet = ''
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
            list_item = soup.find_all('span', {'class':'date-display-single'})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
