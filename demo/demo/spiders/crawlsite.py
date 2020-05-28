import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Field,Item
import os

class PageContentItem(Item): # A data storage class(like directory) to store the extracted data
    url = Field()
    status = Field()
    referer=Field()
    canonical=Field()
    title=Field()
    canonicalMistmach=Field()

class CrawlPens(CrawlSpider):
    name = 'quotes'
    unique_urls=set()
    print(os.getenv('site'))
    start_urls = [os.getenv('site')]
    handle_httpstatus_list=[404,500,404,501]
   

    rules=(
           # Extract link from this path only
        Rule(
            LxmlLinkExtractor(restrict_xpaths=["//a[contains(@href,'')]"], allow_domains=[os.getenv('domain')]), 
            callback='parse_items',follow=True
        ),
        # link should match this pattern and create new requests
        Rule(
            LxmlLinkExtractor(allow=[os.getenv('allow')], allow_domains=[os.getenv('domain')]), 
            callback='parse_items', follow=True
        )
    )
    def parse_items(self, response):
        item=PageContentItem()
        item['url']=response.url
        item['status']=response.status
        item['referer']=response.request.headers.get('Referer')
        canonical=response.css("link[rel='canonical']::attr(href)").get()
        if canonical != response.url :
            item['canonicalMistmach'] = "true"
        else:
            item['canonicalMistmach'] = "false"
        
        item['canonical']=canonical
        item['title']=response.css("title::text").get()
        yield item
