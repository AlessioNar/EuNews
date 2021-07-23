import scrapy

## I need to implement pagination 

class ConsiglioDEuropaItSpider(scrapy.Spider):
    name = "consigliodeuropait"

    def start_requests(self):
        urls = [
            'https://www.coe.int/it/web/portal/full-news',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        container = response.xpath("//div[@class='newsroom ']")
        titles = container.xpath("//div[@class='element  clearfix']/h3/a/text()").getall()
        urls = container.xpath("//div[@class='element  clearfix']/h3/a/@href").getall()
        pub_dates = container.xpath("//div[@class='upper']/span[@class='date']/text()").getall()
        snippets = container.xpath("//div[@class='element  clearfix']/p/text()").getall()
        snippets = [snippet.strip() for snippet in snippets]

        while True:
            try:
                snippets.remove("")
            except ValueError:
                break

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
