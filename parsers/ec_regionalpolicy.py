from scraper import Scraper, PaginatedScraper
import bs4
import time

class ECRegionalPolicyScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/regional_policy/en/newsroom/news'
        self.cookie_xpath ="//a[@class='wt-cck-btn-refuse']"
        self.container_xpath = '//li[@class="flex-active-slide"]'
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

            list_item = soup.find_all('div', {'class':'roundedBoxes'})
            for item in list_item:
                title = item.h2.text.strip()
                url = 'https://ec.europa.eu' + item.h2.a['href']
                pub_date = item.span.b.text.strip()
                pub_date = self.std_date(pub_date)
                snippet = item.p.text.strip()
                titles.append(title)
                pub_dates.append(pub_date)
                urls.append(url)
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
