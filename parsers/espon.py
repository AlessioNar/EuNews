from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EsponScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//ul[@class="recent-posts"]'
        self.url = 'https://www.espon.eu/news-events/news/latest-news'


    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def extract_html(self):
        container = self.driver.find_elements_by_xpath(self.container_xpath)[3]
        container = container.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(container, 'lxml')
        return soup

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        counter = 1
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all('div', {'class':'views-field views-field-title'})
            for item in list_item:
                title = item.span.a.text
                url = 'https://www.espon.eu' + item.span.a['href']
                titles.append(title)
                urls.append(url)
                print(titles)
            list_item = soup.find_all('div', {'class':'views-field views-field-created'})
            for item in list_item:
                pub_date = item.span.small.span.next_sibling
                pub_date = self.std_date(pub_date)
                print(pub_date)
                pub_dates.append(pub_date)
            list_item = soup.find_all('li')
            for item in list_item:
                snippet = item.find('p').text.strip()
                snippets.append(snippet)


            #if pub_dates[len(pub_dates) - 1] <= self.max_date:
            is_paginated = False
            #else:
            #    counter = counter + 1
            #    pagenum = "Go to page " + str(counter) + '\"]'
            #    button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            #    button.click()

        return titles, pub_dates, snippets, urls
