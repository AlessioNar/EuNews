from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class ECItaliaScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://italy.representation.ec.europa.eu/notizie-ed-eventi/notizie-0_it'
        self.popup_xpath = "//a[@id='ec-survey-pop-up-body-button-do-not-participate']"
        self.cookie_xpath ="//a[@class='cck-actions-button']"
        self.close_cookies_xpath = "//a[@href='#close']"
        self.container_xpath = '//div[@class="ecl-content-item-block"]'
        self.next_xpath = "//a[@class='ecl-link ecl-link--standalone ecl-link--icon ecl-link--icon-after ecl-pagination__link']"


    def cookies_removal(self):
        try:
            closepopup = driver.find_element_by_xpath(self.popup)
            closepopup.click()
        except:
            print('no survey')
        try:
            cookies = driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            closecookies = driver.find_element_by_xpath(self.close_cookies_xpath)
            closecookies.click()
        except:
            print('Cookies are ok')


    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            soup = self.extract_html()

            list_item = soup.find_all("article")
            for item in list_item:
                title = item.div.next_sibling.div.next_sibling.a.text.strip()
                url = 'https://italy.representation.ec.europa.eu' + item.div.next_sibling.div.next_sibling.a['href']
                pub_date = item.div.next_sibling.div.time['datetime']
                pub_date = self.std_date(pub_date)
                snippet = ''
                titles.append(title)
                pub_dates.append(pub_date)
                urls.append(url)
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
