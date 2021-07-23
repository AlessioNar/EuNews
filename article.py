# Articles.py which scrape article links# imports
import scrapy
from scrapy.http import Request
from TRTWorld.items import TrtworldItem

class ArticlesSpider(scrapy.Spider):
    name = 'Articles'
    allowed_domains = ['apre.it/news']
    start_urls = ['https://apre.it']

def start_requests(self):# Hardcoded URL that contains TURKEY related subjects
    url="https://apre.it/news/"
    print(url)
    # Request to get the HTML content
    request = Request(url, cookies={'store_language':'en'}, callback=self.parse_main_pages)
    yield request

def parse_main_pages(self,response):
    item=TrtworldItem()# Gets HTML content where the article links are stored
    content=response.xpath('//div[@id="items"]//div[@class="article-meta"]')
    # Loops through the each and every article link in HTML 'content'
    for article_link in content.xpath('.//a'):
        # Extracts the href info of the link to store in scrapy item
        item['article_url'] = article_link.xpath('.//@href').extract_first()
        item['article_url'] = "https://www.trtworld.com"+ item['article_url']

yield(item)

def parse(self, response):
    pass
