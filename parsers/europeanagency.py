from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EuropeanAgencyScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.european-agency.org/news'
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
        while is_paginated:

            soup = self.extract_html()

            list_item = soup.find_all('h3', {'class':'views-field views-field-title'})
            for item in list_item:
                title = item.a.text.strip()
                url = 'https://www.europeanagency.org' + item.a['href']
                snippet = item.next_sibling
                titles.append(title)
                urls.append(url)
                if snippet != '':
                    snippets.append(snippet)

            list_item = soup.find_all('footer', {'class':'views-field views-field-created'})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
