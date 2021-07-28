from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class InterregScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.interregeurope.eu/search/?tx_tevsearch_search%5BentityTypes%5D%5B0%5D=news&tx_tevsearch_search%5BfilterMap%5D=news_and_events&cHash=77de13491bcdbf115bcc65131e10499a'
        self.cookie_xpath = "//a[@class='cc-btn cc-deny']"
        self.container_xpath = '//div[@class="content-area"]'
        self.next_xpath = '//a[@aria-label="Next"]'


    def cookies_removal(self):
        try:
            cookies = self.driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)
        except:
            print("Cookies are already ok")

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def turn_page(self, counter):
        button = self.driver.find_element_by_xpath(self.next_xpath)
        button.click()
        time.sleep(2)
        return counter + 1

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        counter = 1
        while is_paginated:

            soup = self.extract_html()
            list_item = soup.find_all('section', {'class','search-result__item search-result__item--news'})
            for item in list_item:
                title = item.find('div', {'class':'search-result__item__title'})
                url = title.a['href']
                title = title.a.text.strip()
                pub_date = item.find('span', {'class': 'bold'}).text
                pub_date = self.std_date(pub_date)
                snippet = item.find('div', {'class':'clamp-this__2-lines'}).text.strip()
                titles.append(title)
                urls.append(url)
                pub_dates.append(pub_date)
                snippets.append(snippet)


            if (pub_dates[len(pub_dates) - 1] <= self.max_date) | (counter >= 20):
                is_paginated = False
            else:
                counter = self.turn_page(counter)

        return titles, pub_dates, snippets, urls
