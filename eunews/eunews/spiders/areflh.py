import scrapy
import re

class AreflhSpider(scrapy.Spider):
    name = "areflh"

    def start_requests(self):
        urls = [
            'http://www.areflh.org/index.php?lang=en',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        container = response.xpath("//div[@class='uk-container']")[1]
        titles = container.xpath("//h3[@class='el-title uk-card-title uk-margin-top uk-margin-remove-bottom']/text()").getall()
        urls = container.xpath("//a[@class='el-item uk-card uk-card-default uk-card-hover uk-link-toggle uk-display-block']/@href").getall()
        pub_dates = container.xpath("//div[@class='el-meta uk-text-meta uk-margin-top']/text()").getall()
        snippets = container.xpath("//div[@class='el-content uk-panel uk-margin-top']/p/text()").get()
        for index, article in enumerate(titles):
            yield {
                'title':titles[index],
                'pub_date':re.sub('Publié le', '', pub_dates[index]),
                'snippet':snippets[index],
                'url':('https://www.areflh.org' + urls[index])
            }
            #page = response.url.split("/")[-2]
        #filename = f'apre-{page}.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log(f'Saved file {filename}')
