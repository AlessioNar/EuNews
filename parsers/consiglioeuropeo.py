from scraper import Scraper
import bs4
import time

class ConsiglioEuropeo(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//span[@id="reject_cookies"]'
        self.container_xpath = '//div[@class="col-md-9 council-flexify-item pull-right"]'
        self.url = 'https://www.consilium.europa.eu/it/press/press-releases/'
        self.next_btn = "//a[contains(text(), 'seguente')]"

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        counter = 1
        is_paginated = True

        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all("ul", {"class": "list-group"})
            for item in list_item:
                pub_date = item.li.h2.time['datetime']
                pub_date = self.std_date(pub_date)
                article_containers = item.li.ul
                for article in article_containers:
                    if type(article) is bs4.element.Tag:
                        title = article.div.h3.text
                        url = 'https://www.consilium.europa.eu' + article.div.h3.a['href']
                        snippet = article.p.text
                        urls.append(url)
                        titles.append(title)
                        snippets.append(snippet)
                        pub_dates.append(pub_date)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                counter = counter + 1
                self.driver.get(self.url+'?Page='+str(counter))
                time.sleep(3)

        return titles, pub_dates, snippets, urls
