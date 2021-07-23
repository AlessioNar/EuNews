import scrapy

class ApreSpider(scrapy.Spider):
    name = "apre"

    def start_requests(self):
        urls = [
            'https://apre.it/news/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        container = response.xpath("//main[@class='site-main']")
        titles = container.xpath("//h2/a/text()").getall()
        urls = container.xpath("//h2/a/@href").getall()
        pub_dates = container.xpath("//span[@class='published']/text()").getall()
        snippets = container.xpath("//div[@id='bottom-blog']/p/text()").getall()
        for index, article in enumerate(titles):
            yield {
                'title':titles[index],
                'pub_date':pub_dates[index],
                'snippet':snippets[index],
                'url':urls[index]
            }
            #page = response.url.split("/")[-2]
        #filename = f'apre-{page}.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log(f'Saved file {filename}')
