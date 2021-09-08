from scraper import Scraper
import bs4
import time

class CORScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//div[@class="cbq-layout-main"]'
        self.url = 'https://cor.europa.eu/it/news/Pages/default.aspx'

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

        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all("div", {"class":"col-md-6 card"})
            for item in list_item:
                try:
                    if item['hidden'] == '':
                        dummy = 'hidden'
                except:
                    title = item.text.strip()
                    url = item.a['href']
                    pub_date = item.find("div", {"class":"HighlightDateLine"})
                    try:
                        pub_date = pub_date.text.split('Press release')[1]
                    except:
                        pub_date = pub_date.text
                    pub_date = pub_date.split('|')[0].strip()
                    pub_date = self.std_date(pub_date)
                    snippet = item.a.div.div.div.next_sibling.text.strip()
                    titles.append(title)
                    urls.append(url)
                    pub_dates.append(pub_date)
                    snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                if counter == 1:
                    # trova navbar e clicca per andare sul 3
                    navbar = self.driver.find_element_by_xpath('//div[@class="cor-pagination-container bottom-pagination"]')
                    navbar.click()

                    # torna sul 2
                    navbar = self.driver.find_element_by_xpath('//i[@class="fa fa-arrow-left"]')
                    navbar.click()
                    counter = counter + 1
                elif counter == 5:
                    break
                else:
                    navbar = self.driver.find_element_by_xpath('//li[@class="page-item next"]')
                    navbar.click()
                    counter = counter + 1

                time.sleep(3)

        return titles, pub_dates, snippets, urls
