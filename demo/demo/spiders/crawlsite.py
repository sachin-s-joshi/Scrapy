from io import FileIO
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
    images=Field()
    ogTags=Field()
    twTags=Field()
    metaDesc=Field()
    metaKeywords=Field()
    details=Field()
    description=Field()
    redemption=Field()
    breadcrumb=Field()
    

class CrawlPens(CrawlSpider):
    name = 'quotes'
    print(os.getenv('site'))
    domain=os.getenv('site').split('/')[2]
    # reg=os.getenv('site').split('/')[3]
    allow=os.getenv('site') + "*"
    print(allow,domain)
    handle_httpstatus_list=[404,500,404,501,403]
    # delete existing report
    if os.path.exists('./results.csv'):
        os.remove('./results.csv')
        print('File deleted!!')
    rules=(
           # Extract link from this path only
        Rule(
            LxmlLinkExtractor(restrict_xpaths=["//a[@href]"], allow_domains=domain), 
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
            yield scrapy.Request(url=url,headers={'User-Agent':'np-site-crawler'})

    def parse_items(self, response):
        item=PageContentItem()
        url=unquote(response.url,encoding='UTF-8')
        item['url']=url #for handling encoding 
        item['status']=response.status
        item['referer']=response.request.headers.get('Referer')
        canonical=response.css("link[rel='canonical']::attr(href)").get()
        if canonical != item['url'] :
            item['canonicalMistmach'] = "true"
        else:
            item['canonicalMistmach'] = "false"
        
        item['canonical']=canonical
        item['title']=response.css("title::text").get()
        img_list=response.css("img[alt][title]::attr(src)").get()
        # print(img_list)
        item['images']=img_list

        og_list=response.css("meta[property^='og']::attr('content')").getall()
        tw_list=response.css("meta[name^='twitter']::attr('content')").getall()
        # print(og_list)
        item['ogTags']=og_list
        item['twTags']=tw_list

        if '/gift-cards/' in url:
            text_list=response.xpath("//*[@class='slide-down-content__display']/text()").getall()
            # print(text_list,len(text_list))
            item['details']=text_list[0]
            item['description']=text_list[1]
            item['redemption']= text_list[2]
        breadcrumb_list=response.xpath("//div[@class='breadcrumbs']//ul/li//text()").getall()
        if breadcrumb_list is not None:
            breadcrumb=[x.strip() for x in breadcrumb_list if x.strip()!='']
            print('->'.join(breadcrumb))
            item['breadcrumb']= '->'.join(breadcrumb)
        
        item['metaDesc']=response.css("meta[name='description']::attr('content')").getall()
        item['metaKeywords']=response.css("meta[name='keywords']::attr('content')").getall()
        yield item
