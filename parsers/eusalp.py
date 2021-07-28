from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EusalpScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.alpine-region.eu/news'
        self.cookie_xpath = '//button[@class="decline-button eu-cookie-compliance-default-button"]'
        self.container_xpath = '//div[@class="view-content"]'
        self.next_xpath = '//a[@title="Go to next page"]'


    def cookies_removal(self):
        try:
            cookies = self.driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)
        except:
            print("Cookies are already ok")

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        counter = 1
        while is_paginated:

            soup = self.extract_html()
            list_item = soup.find_all("h3", {"class": "views-field views-field-title event-box-title"})
            for item in list_item:
                title = item.span.a.text
                url = 'https://www.alpine-region.eu' + item.span.a['href']
                urls.append(url)
                titles.append(title)

            list_item = soup.find_all("span", {"class": "date-display-single"})
            for item in list_item:
                pub_date = item.text
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)

            list_item = soup.find_all("div", {"class": "views-field views-field-body"})
            for item in list_item:
                snippet = item.span.text
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
