from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class PromisScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.promisalute.it/servizi/notizie/notizie_fase01.aspx?categoriaVisualizzata=7'
        self.container_xpath = '//div[@id="boxNotizieArchivio"]'
        self.next_xpath = '//a[@id="formid_ElencoNotizie_Paginazione_Paginazione_Link_Successiva"]'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:

            soup = self.extract_html()
            list_item = soup.find_all('div', {'class':'notiziaConFoto'})
            for item in list_item:
                title = item.find('h1').text.strip()
                url = 'https://www.promisalute.it' + item.find('a')['href']
                snippet = item.find('h3').text.strip()
                pub_date = item.find('h2').text.strip()
                pub_date = pub_date.split('\n')[1].strip()
                pub_date = self.std_date(pub_date)
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
                pub_dates.append(pub_date)


            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls
