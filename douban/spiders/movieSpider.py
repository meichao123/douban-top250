# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban.items import DoubanItem

class MoviespiderSpider(CrawlSpider):
    name = 'movieSpider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250?start=']
    page_link = LinkExtractor(allow='start=\d+')
    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        movies = response.xpath("//div[@class='info']")
        item = DoubanItem()
        for each in movies:
            # 标题
            item['title'] = each.xpath(".//span[@class='title'][1]/text()").extract()[0]
            # 信息
            item['bd'] = each.xpath(".//div[@class='bd']/p/text()").extract()[0]
            # 评分
            item['star'] = each.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract()[0]
            # 简介
            quote = each.xpath(".//div[@class='bd']/p[@class='quote']/span/text()").extract()
            if len(quote) != 0:
                item['quote'] = quote[0]
            yield item



