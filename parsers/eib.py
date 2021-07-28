from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EIBScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        #self.cookie_xpath = '//a[@class="wt-cck-btn-refuse"]'
        self.container_xpath = '//div[@class="search-filter__results row card-row-items"]'
        self.url = 'https://www.eib.org/en/press/all/index.htm?q=&sortColumn=startDate&sortDir=desc&pageNumber=0&itemPerPage=10&pageable=true&language=EN&defaultLanguage=EN&mediaTypes=press-release&mediaTypes=media-new&mediaTypes=media-speech&mediaTypes=generic-video&ormediaTypes=true&yearFrom=&yearTo=&orMediaTypes=true&orTags=true&orCountries=true&orRegions=true&orSubjects=true'
        self.cookie_xpath = "//button[@id='accept_cookies_footer']"

    def cookies_removal(self):
        try:
            time.sleep(1)
            cookies = self.driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)

            banner = self.driver.find_element_by_xpath("//a[@class='fa fa-close color-eib-blue close-btn']")
            banner.click()
            time.sleep(1)
        except:
            print('Cookies already set')

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all("h3", {"class": "card-row-title margin-right-20"})
            for item in list_item:
                title = item.a.text.strip()
                url = 'https://www.eib.org' + item.a['href']
                titles.append(title)
                urls.append(url)
            list_item = soup.find_all("span", {"class": "card-row-date"})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)

            list_item = soup.find_all("div", {"class": "card-row-text"})
            for item in list_item:
                snippet = item.text.strip()
                snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath('//a[@class="nextPrevPagination nextPagination"]')
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
