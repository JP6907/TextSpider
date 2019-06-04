# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from TextSpider.items import TextspiderItem


class MyspiderSpider(scrapy.Spider):
    name = 'MySpider'
    allowed_domains = ['www.chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/',] ##最后面有个逗号
    MAX_PAGE = 100
    curPage = 0

    def parse(self, response):

        request = response.request.url
        item = TextspiderItem()
        item["url"] = request

        if request.endswith("html") or request.endswith("htm"):
            # 记录爬取页面数量
            self.curPage += 1
            print("=======================正在爬取第 %d 个页面......" % self.curPage)
            content_list = response.xpath('//p/text()').extract()
            p_content = ""
            for c in content_list:
                 p_content += c.strip()

            item["content"] = p_content
            # 如果不是图片页面
            if p_content.startswith("Copyright") is False:
                yield item

        a_list = response.xpath('//a/@href').extract()
        for a in a_list:
            if self.curPage < self.MAX_PAGE:
                if a.startswith("//"):
                    a = a[2:]
                    a = "http://" + a
                    ##这种格式开头的网页才是英文新闻的内容，否则有些是中文的，或者不是内容详情页面
                    if a.startswith("http://www.chinadaily.com.cn/a/"):
                        yield Request(url=a, callback=self.parse)






