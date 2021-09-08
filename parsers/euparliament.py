from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EUParliamentScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//div[@class="ep_gridrow ep-o_productlist"]'
        self.url = 'https://www.europarl.europa.eu/news/it/press-room'
        self.cookie_xpath = '//span[contains(text(), "Rifiuto i cookie analitici")]'

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

            list_item = soup.find_all("div", {"class":"ep_title"})
            for item in list_item:
                title = item.a.div.span.text.strip()
                url = item.a['href']
                titles.append(title)
                urls.append(url)
            list_item = soup.find_all("div", {"class":"ep-a_text"})
            for item in list_item:
                snippet = item.text.strip()
                snippets.append(snippet)

            list_item = soup.find_all("time", {"itemprop": "datePublished"})
            for item in list_item:
                pub_date = item['datetime']
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath('//a[@id="continuesLoading_button"]')
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
