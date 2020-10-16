from io import FileIO
import scrapy
from scrapy.http import request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Field, Item
import os
from scrapy import Request
from urllib.parse import unquote


# A data storage class(like directory) to store the extracted data
class PageContentItem(Item):
    url = Field()
    status = Field()
    referer = Field()
    canonical = Field()
    title = Field()
    canonicalMistmach = Field()
    images = Field()
    ogTags = Field()
    twTags = Field()
    metaDesc = Field()
    metaKeywords = Field()
    details = Field()
    redirect_url = Field()
    breadcrumb=Field()


class CrawlPens(CrawlSpider):
    name = 'me'
    print(os.getenv('site'))
    domain = os.getenv('site').split('/')[2]
    allow = os.getenv('site') + "*"
    url_for_og=os.getenv('check_social_in_urls')  #social tags is Open graph tags, Twitter tags ,etc
    handle_httpstatus_list = [404, 500, 404, 501, 403, 301, 302, 304]
    # delete existing report
    if os.path.exists('./results.csv'):
        os.remove('./results.csv')
        print('File deleted!!')
    rules = (
        # Extract link from this path only
        Rule(
            LxmlLinkExtractor(
                restrict_xpaths=["//a[@href]"], allow_domains=domain),
            callback='parse_items', follow=True
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
            yield Request(url=url, headers={'User-Agent': 'np-site-crawler'},encoding='UTF-8')

    def parse_items(self, response):
        item = PageContentItem()
        url = unquote(response.url, encoding='UTF-8')
        item['url'] = url  # for handling encoding
        item['status'] = response.status
        item['referer'] = response.request.headers.get('Referer')
        canonical = response.css("link[rel='canonical']::attr(href)").get()
        if canonical != item['url']:
            item['canonicalMistmach'] = "true"
        else:
            item['canonicalMistmach'] = "false"

        item['canonical'] = canonical
        item['title'] = response.css("title::text").get()
        img_list = response.css("img[alt][title]::attr(src)").getall()
        item['images'] = img_list

        if self.url_for_og in url:
            og_list: list = response.css("meta[property^='og:']::attr('content')").getall()
            tw_list = response.css("meta[name^='twitter']::attr('content')").getall()
            print(og_list)
            print(tw_list)
            item['ogTags'] = '-'.join(og_list)
            item['twTags'] = '-'.join(tw_list)

        # custom xpath used here based on project
        breadcrumb_list = response.xpath("//div[@class='breadcrumbs']//ul/li//text()").getall() 
        if breadcrumb_list is not None:
            breadcrumb = [x.strip() for x in breadcrumb_list if x.strip() != '']
            print('->'.join(breadcrumb))
            item['breadcrumb'] = '->'.join(breadcrumb)

        item['metaDesc'] = response.css("meta[name='description']::attr('content')").getall()
        item['metaKeywords'] = response.css("meta[name='keywords']::attr('content')").getall()
        if response.status in [301, 302]:

            redirect_list = response.request.meta
            print(redirect_list)
            item['redirect_url'] = redirect_list
        yield item
