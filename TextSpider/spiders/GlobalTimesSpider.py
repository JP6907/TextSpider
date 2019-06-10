# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class GlobaltimesspiderSpider(scrapy.Spider):
    name = 'GlobalTimesSpider'
    allowed_domains = ['www.globaltimes.cn']

    start_urls = ['http://http://www.globaltimes.cn//']
    menu_url = ['http://www.globaltimes.cn/includes/navmenu.html', ]

    def start_requests(self):
        ##yield Request(self.menu_url[0], callback=self.searchMenuUrl)
        yield Request("http://www.globaltimes.cn/china/politics/index.html",callback=self.parsePage)
        ##yield Request("http://www.globaltimes.cn/content/1147508.shtml",callback=self.parse)

    ### 从导航栏所有的标签入口开始
    def searchMenuUrl(self, response):
        ### 获取标签
        menurlList = []
        topics = response.xpath('//ul[@class="dropdown-menu"]/li')
        for topic in topics:
            url = topic.xpath("a/@href").extract()[0]
            fields = url.split("/")
            if (fields[-3] != "video") and (fields[-3] != "photos"):
                menurlList.append(url)

        ### 开始爬取
        for url in menurlList:
            #print(url)
            yield Request(url, callback=self.parsePage)

    ### 解析每一个主题页面,提取每一页中的新闻详情入口
    def parsePage(self, response):
        urls = response.xpath('//div[@class="row-content"]/div/h4/a/@href').extract()
        for url in urls:
            c = 0
            ##提取每一页的内容
            yield Request(url,callback=self.parse)
            #print(url)

        ### 下一页
        pages = response.xpath('//div[@class="row-fluid text-center pages"]/a/@href').extract()
        count = len(pages)
        lastPage = pages[count-1]  ### 这种格式index10.html#list
        nextPage = pages[count-2]
        request = response.request.url ### http://www.globaltimes.cn/china/politics/index.html
        if not request.endswith(lastPage): ### 不是最后一页，则访问下一页
            url = request.split('index')[-2] + nextPage
            yield Request(url, callback=self.parsePage)
            #print("=======================下一页")
            print(request.split('index')[-2] + nextPage) ### http://www.globaltimes.cn/opinion/observer/index2.html#list


    ### 读取详情页的正文
    def parse(self, response):
        print("===================")
        print(response.request.url)
        div = response.xpath('//div[@class="span12 row-content"]')[0]
        content = div.xpath('string(.)').extract()[0]
        print(content)
