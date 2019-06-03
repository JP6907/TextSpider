# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from TextSpider.items import TextspiderItem


class MyspiderSpider(scrapy.Spider):
    name = 'MySpider'
    allowed_domains = ['web.mit.edu']
    start_urls = ["http://web.mit.edu/research"]
    MAX_PAGE = 100
    curPage = 0

    def parse(self, response):
        #记录爬取页面数量
        MyspiderSpider.curPage += 1
        print("=======================正在爬取第 %d 个页面......" % MyspiderSpider.curPage)

        p_content = ""
        a_content = ""

        #获取页面文本数据
        divClasses = ["//div[@class='tle-header__intro-text']","//div[@class='tle-section__description']"]
        for divClass in divClasses:
            divs = response.xpath(divClass)
            for i in range(len(divs)):
                p_list = divs[i].xpath('//p/text()').extract()
                for p in p_list:
                    p_content += p.strip()
                a_list = divs[i].xpath('//p/a/text()').extract()
                for a in a_list:
                    a_content += (a.strip() + " ")

        item = TextspiderItem()
        item["url"] = response.request.url
        item["content"] = p_content + a_content

        # 获取页面链接
        a_list = response.xpath('//a/@href').extract()
        for link in a_list:
            if(MyspiderSpider.curPage > MyspiderSpider.MAX_PAGE):
                break
            if link.startswith("http"):
                yield Request(url=link,callback=MyspiderSpider.parse(),dont_filter=True)
            else:
                url = MyspiderSpider.start_urls[0] + link
                yield Request(url=url, callback=MyspiderSpider.parse(), dont_filter=True)

        yield item




