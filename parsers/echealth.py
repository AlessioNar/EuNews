from scraper import Scraper, PaginatedScraper
import bs4
import time

class ECHealthScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/health/latest_updates_it'
        self.cookie_xpath ="//a[@class='wt-cck-btn-refuse']"
        self.container_xpath = '//div[@class="region region-content"]'
        self.next_xpath = "//span[contains(text(), 'Next page')]"

    def cookies_removal(self):
        try:
            time.sleep(2)
            cookies = driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
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
            print(list_item)
            for item in list_item:
                title = item.h4.a.text.strip()
                url = item.h4.a['href']
                titles.append(title)
                urls.append(url)
            list_item = soup.find_all('div', {'class':'healt-node-date'})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)
                snippet = ''
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
