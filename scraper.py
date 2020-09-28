import json
import os
import scrapy

page_count = 0

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


    def parse_briefing(self, response):
        global page_count

        url = response.request.url
        header = response.xpath('//h1/center/text()').extract_first()
        title = response.xpath('//h2/center/text()').extract_first()
        info =  response.xpath('/html/body/nextid/center/text()').getall()
        page_text = ''

        for block in response.xpath('//p'):
            text_header = block.xpath('b/text()').extract()
            text_block = block.xpath('text()').extract()

            text_header = ''.join(text_header)
            text_block = ''.join(text_block)

            if text_block is not None:
                text_block = text_header + text_block

            #''.join(text_block).replace('\\\\n', '\\n')

            if text_block is not None and text_block:
                page_text += f'{text_block}'


        # Some pages are formatted differently (and all of them look terrible)
        # so try to handle those different cases here
        if header is None:
            return
            header = response.xpath('//center/font/text()').extract_first()
        if title is None:
            title = response.xpath('//center/font/br/br/following::text()').extract_first()

        page_data = {
            'url': url,
            'header': header,
            'title': title,
            'text': page_text.strip()
        }
        # Write out the scraped data to a file
        if not os.path.isdir('data'):
            os.mkdir('data')
        with open(f'data/{page_count}.json', 'w') as f:
            json.dump(page_data, f)

        page_count += 1

        return page_data