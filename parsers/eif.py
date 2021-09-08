from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EIFScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//table[@class="datatable"]'
        self.url = 'https://www.eif.org/news_centre/press_releases/all/index.htm?year=0000&category=&keywordList='
        self.cookie_xpath = "//button[@class='btn btn-close btn-close--cookie']"

    def cookies_removal(self):

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(1)
        #popup = self.driver.find_element_by_xpath("//div[@class='optanon-alert-box-body']")
        #popup.click()
        #cookies = self.driver.find_element_by_xpath(self.cookie_xpath)
        #cookies.click()
        #time.sleep(1)

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all("tr")
            list_item = list_item[1:len(list_item) -1]
            for item in list_item:
                pub_date = item.td.text.strip()
                pub_date = self.std_date(pub_date)
                title = item.td.next_sibling.next_sibling.a.text.strip()
                url = 'https://www.eif.org' + item.td.next_sibling.next_sibling.a['href']
                titles.append(title)
                urls.append(url)
                pub_dates.append(pub_date)
                snippets.append('')


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath('//div[@title="Next"]')
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
