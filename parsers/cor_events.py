from scraper import Scraper
import bs4
import time

class COREventScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//div[@class="cbq-layout-main"]'
        self.url = 'https://cor.europa.eu/it/events/Pages/default.aspx'

    def cookies_removal(self):
        refuse = self.driver.find_element_by_xpath(self.cookie_xpath)
        refuse.click()
        time.sleep(1)

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        counter = 1
        is_paginated = True

        soup = self.extract_html()

        list_item = soup.find_all("div", {"class":"col-md-6 card"})
        for item in list_item:
            title = item.div.h5.text.strip()
            print(title)
            url = item.a['href']
            pub_date = item.find("div", {"class":"HighlightDateLine"})
            pub_date = pub_date.text
            print(pub_date)
            try:
                pub_date = pub_date.split('Meeting')[1]
            except:
                pass
            pub_date = pub_date.split('|')[0].strip()
            pub_date = self.std_date(pub_date)
            snippet_item = item.find('div',{'class':'description'})
            snippet = snippet_item.text.strip()
            titles.append(title)
            urls.append(url)
            pub_dates.append(pub_date)
            snippets.append(snippet)


        return titles, pub_dates, snippets, urls
