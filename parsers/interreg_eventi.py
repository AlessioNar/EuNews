from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class InterregEventScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.interregeurope.eu/search/?tx_tevsearch_search%5B__referrer%5D%5B%40extension%5D=TevSearch&tx_tevsearch_search%5B__referrer%5D%5B%40vendor%5D=Tev&tx_tevsearch_search%5B__referrer%5D%5B%40controller%5D=Search&tx_tevsearch_search%5B__referrer%5D%5B%40action%5D=index&tx_tevsearch_search%5B__referrer%5D%5Barguments%5D=YToyOntzOjExOiJlbnRpdHlUeXBlcyI7YToxOntpOjA7czo0OiJuZXdzIjt9czo5OiJmaWx0ZXJNYXAiO3M6MTU6Im5ld3NfYW5kX2V2ZW50cyI7fQ%3D%3Dd24a8395b5c8b63b4e145dc8d9ae52b4381d0347&tx_tevsearch_search%5B__trustedProperties%5D=a%3A12%3A%7Bs%3A9%3A%22filterMap%22%3Bi%3A1%3Bs%3A8%3A%22keywords%22%3Bi%3A1%3Bs%3A11%3A%22entityTypes%22%3Ba%3A2%3A%7Bi%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A1%3B%7Ds%3A15%3A%22eventCategories%22%3Ba%3A4%3A%7Bi%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A1%3Bi%3A3%3Bi%3A1%3B%7Ds%3A13%3A%22eventFromDate%22%3Bi%3A1%3Bs%3A11%3A%22eventToDate%22%3Bi%3A1%3Bs%3A14%3A%22newsCategories%22%3Ba%3A4%3A%7Bi%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A1%3Bi%3A3%3Bi%3A1%3B%7Ds%3A12%3A%22newsFromDate%22%3Bi%3A1%3Bs%3A10%3A%22newsToDate%22%3Bi%3A1%3Bs%3A17%3A%22thematicInterests%22%3Ba%3A4%3A%7Bi%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A1%3Bi%3A3%3Bi%3A1%3B%7Ds%3A8%3A%22sortType%22%3Bi%3A1%3Bs%3A7%3A%22sortDir%22%3Bi%3A1%3B%7Dc8f665d365ff65c39f89e2126abb014d7f61cc88&tx_tevsearch_search%5BfilterMap%5D=news_and_events&tx_tevsearch_search%5Bkeywords%5D=&tx_tevsearch_search%5BentityTypes%5D=&tx_tevsearch_search%5BentityTypes%5D%5B%5D=event&tx_tevsearch_search%5BeventCategories%5D=&tx_tevsearch_search%5BeventFromDate%5D=&tx_tevsearch_search%5BeventToDate%5D=&tx_tevsearch_search%5BnewsCategories%5D=&tx_tevsearch_search%5BnewsFromDate%5D=&tx_tevsearch_search%5BnewsToDate%5D=&tx_tevsearch_search%5BthematicInterests%5D=&tx_tevsearch_search%5Bcountry%5D=&tx_tevsearch_search%5BsortType%5D=&tx_tevsearch_search%5BsortDir%5D=desc'
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
            list_item = soup.find_all('section', {'class','search-result__item search-result__item--event'})
            for item in list_item:
                title = item.find('div', {'class':'search-result__item__title'})
                url = title.a['href']
                title = title.a.text.strip()
                pub_date = item.find('span', {'class': 'bold'}).text
                pub_date = pub_date.split('-')[0].strip()
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
