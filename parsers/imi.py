from scraper import Scraper, PaginatedScraper
import bs4
import time


## I don't know why but it does not take up all the articles but only the first 4
class IMIScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://www.imi.europa.eu/news-events/newsroom'
        self.container_xpath = '//div[@class="view-grouping-content info-box light-grey-bg"]'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()
        soup = self.extract_html()
        # Parse html
        list_item = soup.find_all("div", {"class": "views-row article-row"})
        for item in list_item:
            title = item.div.span.article.div.div.h4.text
            url = 'https://www.imi.europa.eu' + item.div.span.article.div.div.h4.a['href']
            titles.append(title)
            urls.append(url)

        list_item = soup.find_all("span", {"class": "published-date"})
        for item in list_item:
            pub_date = item.text
            pub_date = self.std_date(pub_date)
            pub_dates.append(pub_date)

        list_item = soup.find_all("div", {"class": "field field--name-body field--type-text-with-summary field--label-hidden field--item"})
        for item in list_item:
            snippet = item.text
            snippets.append(snippet)

        return titles, pub_dates, snippets, urls
