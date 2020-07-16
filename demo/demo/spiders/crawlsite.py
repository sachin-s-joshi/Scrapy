import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Field,Item
import os
from scrapy import Request
from urllib.parse import unquote

class PageContentItem(Item): # A data storage class(like directory) to store the extracted data
    url = Field()
    status = Field()
    referer=Field()
    canonical=Field()
    title=Field()
    canonicalMistmach=Field()

class CrawlPens(CrawlSpider):
    name = 'quotes'
    print(os.getenv('site'))
    domain=os.getenv('site').split('/')[2]
    reg=os.getenv('site').split('/')[3]
    allow=os.getenv('site') + "*"
    print(allow,domain,reg)
    handle_httpstatus_list=[404,500,404,501,403]
   

    rules=(
           # Extract link from this path only
        Rule(
            LxmlLinkExtractor(restrict_xpaths=["//a[@href='/dk/']"], allow_domains=domain), 
            callback='parse_items',follow=True
        ),
        # link should match this pattern and create new requests
        Rule(
            LxmlLinkExtractor(allow=allow, allow_domains=domain), 
            callback='parse_items', follow=True
        )
    )

    def start_requests(self):
        urls = [os.getenv('site')]
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url,cookies={'loginCookie':os.getenv('cookie'),'fake':'true'},headers={'User-Agent':'np-site-crawler'})

    def parse_items(self, response):
        item=PageContentItem()
        item['url']=unquote(response.url,encoding='UTF-8') #for handling encoding 
        item['status']=response.status
        item['referer']=response.request.headers.get('Referer')
        canonical=response.css("link[rel='canonical']::attr(href)").get()
        if canonical != item['url'] :
            item['canonicalMistmach'] = "true"
        else:
            item['canonicalMistmach'] = "false"
        
        item['canonical']=canonical
        item['title']=response.css("title::text").get()
        yield item
