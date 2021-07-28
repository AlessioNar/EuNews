from scraper import Scraper, PaginatedScraper
import bs4
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

## I don't know why but it does not take up all the articles but only the first 4
class ECGenericScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/info/news_it?department=All&field_announcement_type_value_i18n=All&persons=All&research_areas=All'
        self.cookie_xpath = "//a[@class='cck-actions-button']"
        self.container_xpath = '//div[@class="view-content"]'
        self.next_xpath = "//a[@title='Vai alla pagina successiva']"
        self.popup = "//div[@class='spinner__overlay active']"

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def cookies_removal(self):
        try:
            closepopup = self.driver.find_element_by_xpath("//a[@id='ec-survey-pop-up-body-button-do-not-participate']")
            closepopup.click()
        except:
            print('no survey')

        try:
            cookies = self.driver.find_element_by_xpath("//a[@class='cck-actions-button']")
            cookies.click()
            closecookies = self.driver.find_element_by_xpath("//a[@href='#close']")
            closecookies.click()
        except:
            print('no cookies')

    def turn_page(self):
        button = self.driver.find_element_by_xpath(self.next_xpath)
        button.click()
        wait = WebDriverWait(self.driver, 20)
        wait.until(ec.invisibility_of_element_located((By.XPATH, self.popup)))

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            soup = self.extract_html()
            list_item = soup.find_all("div", {"class": "listing__column-main"})
            for item in list_item:
                title = item.div.next_sibling.text.strip()
                url = item.div.next_sibling.a['href']
                pub_date = item.div.span.next_sibling.text.strip()
                pub_date = self.std_date(pub_date)
                snippet = '' #item.find_all('p')
                #if snippet == '':
                #    snippet = ''
                #else:
                #    snippet = snippet.text.strip()
                titles.append(title)
                pub_dates.append(pub_date)
                urls.append(url)
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()
                time.sleep(3)

        return titles, pub_dates, snippets, urls
