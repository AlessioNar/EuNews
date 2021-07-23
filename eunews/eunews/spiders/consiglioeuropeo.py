import scrapy
from bs4 import BeautifulSoup

## I need to implement pagination

class ConsiglioEuropeoSpider(scrapy.Spider):
    name = "consiglioeuropeo"

    def start_requests(self):
        urls = [
            'https://www.consilium.europa.eu/it/press/press-releases/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        list_item = soup.find_all("ul", {"class": "list-group"})

        for item in list_item:
            pub_date = item.li.h2.time['datetime']
            container = item.li.ul
            for article in container:
                if type(article) is bs4.element.Tag:
                    yield {
                        'title': article.div.h3.text
                        #'pub_date':pub_date,
                        #'snippet': article.p.text,
                        #'url':'https://www.consilium.europa.eu' + article.div.h3.a['href']
                    }
        while True:
            try:
                snippets.remove("")
            except ValueError:
                break
