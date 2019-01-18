import scrapy
from scrapy.loader import ItemLoader
from Khaadi.items import KhaadiItem


class Khaadi(scrapy.Spider):

    name = 'khaadi'

    start_urls = ['http://www.khaadionline.com/pk']

    def parse(self, response):

        cat_links = response.xpath(".//ul[@id='nav']/li/a/@href").extract()
        for c in cat_links:
            yield scrapy.Request(c + '?limit=60', self.parse_category)

    def parse_category(self, response):

        item_links = response.xpath('.//h2[@class="product-name"]/a/@href').extract()

        for i in item_links:

            yield scrapy.Request(i, self.parse_items)

        more_pages = set(response.xpath(".//a[@class='next i-next']/@href").extract())
        if more_pages:
            yield scrapy.Request(more_pages.pop(), self.parse_category)

    def parse_items(self, response):

        l = ItemLoader(item=KhaadiItem(), response=response)
        l.add_xpath('title',
                    ".//*[@class='span5 product-shop']/*[@class='product-name']//text()")
        l.add_xpath('regular_price',
                    ".//*[@class='span5 product-shop']/*[@class='price-box']//text()")
        l.add_xpath('description',
                    ".//*[@class='std wth-log']//text()")
        l.add_xpath('detail',
                    ".//*[@class='ecom-detail']/child::*[position() > 1]//text()")
        l.add_xpath('size',
                    ".//*[@id='attribute136']/child::*[position() > 1]/text()")
        l.add_xpath('category',
                    ".//div[@class='span12 breadcrumbs']/child::*[position() < last()]//text()")
        l.add_xpath('image_url',
                    ".//ul[@class='slider1']//a/@href")
        l.add_value('product_url',
                    response.url)

        return l.load_item()
