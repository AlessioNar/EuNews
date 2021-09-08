from scraper import Scraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class EUCommissionScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.container_xpath = '//section[@id="news-block"]'
        self.url = 'https://ec.europa.eu/commission/presscorner/home/it'
        self.cookie_xpath = '//button[@class="agree-button"]'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        counter = 1
        while is_paginated:
            soup = self.extract_html()

            list_item = soup.section.ul.find_all("div", {"_ngcontent-c1": ""})
            for item in list_item:
                article = item.li
                if type(article) is bs4.element.Tag:
                    category = item.div.div.span.text
                    pub_date = item.div.div.find_all("span", {"ngcontent-c1":""})[1].text
                    pub_date = self.std_date(pub_date)
                    url = 'https://ec.europa.eu/commission/presscorner/' + article.a['href']
                    if type(item.div.h3) is bs4.element.Tag:
                        title = item.div.h3.text
                    else:
                        title = ''
                    if type(item.div.p) is bs4.element.Tag:
                        snippet = item.div.p.text
                    else:
                        snippet = ''

                    titles.append(title)
                    pub_dates.append(pub_date)
                    urls.append(url)
                    snippets.append(snippet)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                counter = counter + 1
                pagenum = "Go to page " + str(counter) + '\"]'
                button = self.driver.find_element_by_xpath('//a[@title=\"' + pagenum)
                button.click()
                time.sleep(2)

        return titles, pub_dates, snippets, urls
