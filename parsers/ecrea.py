from scraper import Scraper, PaginatedScraper
import bs4
import time

class ECReaScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/chafea/agri/newsroom-and-events/news'
        self.cookie_xpath ="//a[@class='wt-cck-btn-refuse']"
        self.close_cookies_xpath = "//a[@href='#close']"
        self.container_xpath = '//div[@class="region region-content"]'
        self.next_xpath = "//span[contains(text(), 'Next page')]"

    def cookies_removal(self):
        try:
            time.sleep(2)
            cookies = driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)
            closecookies = driver.find_element_by_xpath(self.close_cookies_xpath)
            closecookies.click()
            time.sleep(1)
        except:
            print('Cookies are ok')


    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            soup = self.extract_html()

            list_item = soup.find_all('div', {'class':'views-field views-field-title'})
            for item in list_item:
                title = item.h3.a.text.strip()
                url = 'https://ec.europa.eu' + item.h3.a['href']
                titles.append(title)
                urls.append(url)
            list_item = soup.find_all('div', {'class':'views-field views-field-created'})
            for item in list_item:
                pub_date = item.span.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)
            list_item = soup.find_all('div', {'class':'views-field views-field-body fieldset clearfix'})
            for item in list_item:
                snippet = item.span.text.strip()
                snippets.append(snippet)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
