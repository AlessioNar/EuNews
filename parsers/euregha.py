from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EureghaScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//div[@class="et_pb_blog_grid clearfix  et_pb_text_align_center"]'
        self.url = 'http://www.euregha.net/news/'


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
            list_item = soup.find_all('article')
            for item in list_item:
                title = item.h4.text
                url = item.h4.a['href']
                pub_date = item.p.text
                pub_date = self.std_date(pub_date)
                snippet = ''
                titles.append(title)
                urls.append(url)
                pub_dates.append(pub_date)
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath("//a[contains(text(), 'Older Entries')]")
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
