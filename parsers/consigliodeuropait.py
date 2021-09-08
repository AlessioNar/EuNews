from scraper import Scraper

class ConsiglioDEuropaITScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date

        self.container_xpath = '//div[@class="newsroom "]'
        self.url = 'https://www.coe.int/it/web/portal/full-news'
        self.next_btn = "//a[contains(text(), 'seguente')]"

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        is_paginated = True

        while is_paginated:
            soup = self.extract_html()

            list_item = soup.find_all("div", {"class": "element clearfix"})
            for item in list_item:
                title = item.h3.text.strip()
                url = item.h3.a['href']
                upper = item.find_all("div", {"class": "upper"})[0]
                pub_date = upper.find_all("span", {"class":"date"})[0].text
                snippet = item.p.text.strip()
                pub_date = self.std_date(pub_date)
                titles.append(title)
                urls.append(url)
                pub_dates.append(pub_date)
                snippets.append(snippet)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                button = self.driver.find_element_by_xpath(self.next_btn)
                button.click()

        return titles, pub_dates, snippets, urls
