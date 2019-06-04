# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from TextSpider.items import TextspiderItem


class MyspiderSpider(scrapy.Spider):
    name = 'MySpider'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/a/201906/04/WS5cf54b0ca310519142700d0b.html',] ##最后面有个逗号
    MAX_PAGE = 100
    curPage = 0

    def parse(self, response):

        item = TextspiderItem()
        item["url"] = response.request.url

        if response.request.url.endswith("html") or response.request.url.endswith("htm"):
            # 记录爬取页面数量
            self.curPage += 1
            if self.curPage > self.MAX_PAGE:
                return
            print("=======================正在爬取第 %d 个页面......" % self.curPage)

            p_content = ""
            content_list = response.xpath('//p/text()').extract()
            for c in content_list:
                 p_content += c.strip()

            item["content"] = p_content
            yield item

        a_list = response.xpath('//a/@href').extract()
        for a in a_list:

            if a.startswith("//"):
                a = a[2:]
                a = "http://" + a
                yield Request(url=a, callback=self.parse, dont_filter=True)


        # p_content = ""
        # a_content = ""

        #获取页面文本数据
        # divClasses = ["//div[@class='tle-header__intro-text']","//div[@class='tle-section__description']"]
        # for divClass in divClasses:
        #     divs = response.xpath(divClass)
        #     for i in range(len(divs)):
        #         p_list = divs[i].xpath('//p/text()').extract()
        #         for p in p_list:
        #             p_content += p.strip()
        #         a_list = divs[i].xpath('//p/a/text()').extract()
        #         for a in a_list:
        #             a_content += (a.strip() + " ")
        #
        # item = TextspiderItem()
        # item["url"] = response.request.url
        # item["content"] = p_content + a_content

        # 获取页面链接
        # a_list = response.xpath('//a/@href').extract()
        # for link in a_list:
        #     index = link.find('#')
        #     link = link[0:index]
        #     if link.startswith("http"):
        #         yield Request(url=link,callback=self.parse,dont_filter=True)
        #     else:
        #         url = self.url_head + link
        #         yield Request(url=url, callback=self.parse, dont_filter=True)





