# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from TextSpider.items import TextspiderItem


class NewsweekspiderSpider(scrapy.Spider):
    curPage = 0
    name = 'NewsweekSpider'
    allowed_domains = ['www.newsweek.com']
    url_head = "https://www.newsweek.com"
    ## 有反爬虫，需要在setting文件中设置代理 USER_AGENT
    start_urls = ['https://www.newsweek.com/us',
                  'https://www.newsweek.com/world',
                  'https://www.newsweek.com/business',
                  'https://www.newsweek.com/tech-science',
                  'https://www.newsweek.com/culture',
                  'https://www.newsweek.com/sports',
                  'https://www.newsweek.com/health',
                  'https://www.newsweek.com/opinion', ]

    ### 遍历每一个topic
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parsePage)
        #yield Request(self.start_urls[0], callback=self.parsePage)
        #yield Request("https://www.newsweek.com/us?page=2324", callback=self.parsePage)
        #yield Request("https://www.newsweek.com/2019/04/19/beto-orourke-ted-cruz-presidential-elections-donald-trump-1365360.html", callback=self.parse)



    ### 解析每一个主题页面,提取每一页中的新闻详情入口
    def parsePage(self, response):
        #print("================当前页面")
        #print(response.request.url)
        urls = response.xpath('//h3/a/@href').extract()
        ## print(len(urls))
        for url in urls:
            url = self.url_head + url
            ### 解析详情页
            yield Request(url, callback=self.parse)

        ### 下一页
        nextPage = response.xpath('//li[@class="pager-next last"]/a/@href').extract()
        if len(nextPage) > 0:  ###如果有下一页
            #print("=======有下一页")
            nextPage = self.url_head + nextPage[0]
            yield Request(nextPage, callback=self.parsePage)
            # print("===========next page:")
            # print(nextPage)
        # else:
        #     print("=======没有下一页")


    ### 解析详情页面
    def parse(self, response):
        self.curPage = self.curPage + 1
        print("========================正在爬取第%d 个页面......" % self.curPage)
        print(response.request.url)
        content = ""

        ### 三种div标签包含正文
        divs = response.xpath('//div[@class="article-body v_text"]')
        for p in divs.xpath('.//p/text()'):
            content += p.extract().strip()
        divs = response.xpath('//div[@class="article-body"]')
        for p in divs.xpath('.//p/text()'):
            content += p.extract().strip()
        divs = response.xpath('//div[@class="article-body clearfix"]')
        for p in divs.xpath('.//p/text()'):
            content += p.extract().strip()

        # div = response.xpath('//div[@class="article-body v_text"]')[0]
        # ps = div.xpath('string(.)').extract()
        # for p in ps:
        #     content += p.strip().replace('\n', ' ').replace('\t', ' ').strip()
        #print(content)

        item = TextspiderItem()
        request = response.request.url
        item["url"] = request
        item["content"] = content
        yield item
