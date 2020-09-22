import scrapy


class BriefingsSpider(scrapy.Spider):
    name = "briefings_spinder"
    start_urls = ['http://1997-2001.state.gov/briefings/2000_index.html']

    def parse(self, response):
        for ref in response.xpath('//*/td'):
            yield {
                'ref' : ref.xpath('a'),
            } #scrapy.Request(response.urljoin(ref), self.parse)
            