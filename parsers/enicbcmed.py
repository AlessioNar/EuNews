from scraper import Scraper
import bs4
import time


class EniCbcMedScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//div[@class="block-items"]'
        self.url = 'http://www.enicbcmed.eu/info-center/news'
        self.cookie_xpath = '//button[@class="decline-button eu-cookie-compliance-default-button"]'

    def cookies_removal(self):
        cookies = self.driver.find_element_by_xpath(self.cookie_xpath)
        cookies.click()
        time.sleep(1)

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        counter = 0
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all('div', {'class':'block-body-content'})
            for item in list_item:
                title = item.a.h6.text.strip()
                url = 'http://www.enicbcmed.eu/' + item.a['href']
                snippet = item.p.text.strip()
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
            list_item = soup.find_all('time', {'class':'datetime'})
            for item in list_item:
                pub_date = item['datetime']
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                counter = counter + 1
                next_page = 'http://www.enicbcmed.eu/info-center/news?field_tags_target_id=All&keys=&page=' + str(counter)
                self.driver.get(next_page)
                time.sleep(2)

        return titles, pub_dates, snippets, urls
