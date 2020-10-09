import json
import os
from re import escape
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

    def parse_briefing(self, response):
        url = response.request.url
        header = response.xpath('//h1/center/text()').extract_first()
        title = response.xpath('//h2/center/text()').extract_first()
        page_text = ''

        # Get all the speech text on a page
        for block in response.xpath('//p'):
            text_header = block.xpath('b/text()').extract()
            text_block = block.xpath('text()').extract()

            text_header = ''.join(text_header)
            text_block = ''.join(text_block)

            if text_block is not None:
                text_block = text_header + text_block
            if text_block is not None and text_block:
                page_text += text_block

        # Some pages are formatted differently (and all of them look terrible)
        # so try to handle those different cases here
        if header is None:
            header = response.xpath('//p[@align = "CENTER"][2]/text()').extract()
            title  = response.xpath('//p[@align = "CENTER"][3]/text()').extract()
            title += response.xpath('//p[@align = "CENTER"][4]/text()').extract()
            title += response.xpath('//p[@align = "CENTER"][5]/text()').extract()
            title += response.xpath('//p[@align = "CENTER"][6]/text()').extract()

        if header is None:
            return

        page_text = page_text.strip().replace("\n", "\\n").replace('"', '\\"')

        page_data = {
            'url': url,
            'header': header,
            'title': title,
            'text': page_text
        }

        # Write out the scraped data to a file
        if os.path.isfile('reports.json'):
            with open('reports.json', 'r') as f:
                report_json = json.load(f)
        else:
            report_json = {}
            
        report_json[url.split('/')[-1]] = page_data  
        with open('reports.json', 'w') as f:
            json.dump(report_json, f, indent=2)

        return page_data