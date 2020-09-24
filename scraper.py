import scrapy


class BriefingsSpider(scrapy.Spider):
    name = "briefings_spinder"
    start_urls = ['http://1997-2001.state.gov/briefings/2000_index.html']

    def parse(self, response):
        for ref in response.xpath('//*/td/a'):
            linked_page = ref.xpath('@href').extract_first()
            if linked_page:
                yield scrapy.Request(
                    response.urljoin(linked_page),
                    self.parse_briefing
                )
                #yield { 'ref' : linked_page,} #scrapy.Request(response.urljoin(ref), self.parse)
    
    def parse_briefing(self, response):
        header = response.xpath('//h1/center/text()').extract_first()
        title = response.xpath('//h2/center/text()').extract_first()
        info =  response.xpath('/html/body/nextid/center/text()').getall()
        index = []

        for block in response.xpath('//p'):
            for index_row in block.xpath('p/table/tbody/tr'):
                # Looping through the index if it exists
                index.append({
                    index_row.xpath('td[1]/text()'),
                    index_row.xpath('td[2]/text()'),
                })

        # Some pages are formatted differently (and all of them look terrible)
        # so try to handle those different cases here
        if header is None:
            return
            header = response.xpath('//center/font/text()').extract_first()
        if title is None:
            title = response.xpath('//center/font/br/br/following::text()').extract_first()

        page_data = {
            'header': header,
            'title': title,
            'info': info
        }
        yield page_data