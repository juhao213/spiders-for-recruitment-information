#-*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import Spider  
from scrapy.selector import Selector  


from NUST_Intern.items import NustInternItem
import sys
from scrapy.http import Request

class NustInternSpider(Spider):  
    reload(sys)  
    sys.setdefaultencoding('utf8')
    
    global file 
    file = open('D:\\train\\scrapy\\NUST.txt','w')
    
    name = "nustintern"  
    allowed_domains = ["zixiahupan.com"]  
    start_urls = [  
      #  "http://bbs.seu.edu.cn/bbsdoc.php?board=Intern&page=497",  
       "http://zixiahupan.com/forum.php?mod=forumdisplay&fid=107&page=1"  
    ]  
  
    def parse(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//tbody[contains(@id,'normal')]")
        print "infos"
        
        page_num = 35
        for info in infos:  
            item = NustInternItem()  
#             deep_url = info.xpath("tr/th/a[contains(@href,'zixiahupan.com/forum.php?mod=viewthread')]/@href").extract()
            item['intern_url'] =  ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan.com/forum.php?mod=viewthread')]/@href").extract())
            item['intern_info'] = ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan')]/text()").extract())
           # item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            item['intern_date'] =''.join(info.xpath("tr/td[@class='by']/em/span/text()").extract())
            item['intern_date'] = item['intern_date'][:-6]
            item['intern_source'] = str('NUST')
            deep_url =  ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan.com/forum.php?mod=viewthread')]/@href").extract())
           # item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
            yield Request(deep_url, meta={'item':item}, callback=self.parse_item) 
        for i in range(2,page_num):
            next_url = "http://zixiahupan.com/forum.php?mod=forumdisplay&fid=107&page=" + str(i)
            yield  scrapy.Request(next_url,callback = self.parse_info)
                
    def parse_info(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//tbody[contains(@id,'normal')]")
        print "infos"
        
        for info in infos:  
            item = NustInternItem()  
            item['intern_url'] =  ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan.com/forum.php?mod=viewthread')]/@href").extract())
            item['intern_info'] = ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan')]/text()").extract())
           # item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            item['intern_date'] = ''.join(info.xpath("tr/td[@class='by']/em/span/text()").extract())
            item['intern_date'] = item['intern_date'][:-6]
            item['intern_source'] = str('NUST')
            deep_url =  ''.join(info.xpath("tr/th/a[contains(@href,'zixiahupan.com/forum.php?mod=viewthread')]/@href").extract())
           # item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
            yield Request(deep_url, meta={'item':item}, callback=self.parse_item) 
            
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        detail = sel.xpath('//td[@class="t_f"]')
        item['intern_detail'] = str(''.join(detail.xpath('string(.)').extract())).replace('\n','').replace('\r','').replace(' ','').replace('/t','')
        
        
        line = item['intern_date']+'\t'+item['intern_info']+'\t'+item['intern_url']+'\t'+item['intern_detail']+'\n'
        file.writelines(line)
        
        return item   