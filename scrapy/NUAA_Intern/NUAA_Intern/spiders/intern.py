import scrapy
from scrapy.spiders import Spider  
from scrapy.selector import Selector  

from NUAA_Intern.items import NuaaInternItem
import sys
from scrapy.http import Request
import urlparse
import os

class NuaaInternSpider(Spider):  
    reload(sys)  
    sys.setdefaultencoding('utf8')
    global file 
    file = open('D:\\train\\scrapy\\NUAA.txt','w')
    name = "nuaaintern"  
    allowed_domains = ["www.hkhtu.com"]  
    start_urls = [  
      #  "http://bbs.seu.edu.cn/bbsdoc.php?board=Intern&page=497",  
       "http://www.hkhtu.com/forum-44-1.html" 
    ]  
  
    def parse(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//tbody[contains(@id,'normal')]")
        
        page_num = 40
        for info in infos:  
            item = NuaaInternItem() 
           # item['intern_url'] =  ''.join(info.xpath("tr/th[@class='common']/a[2]/@href").extract())
#             url = info.xpath("tr/th[@class='common']/a[2]/@href").extract()
#             item['intern_url'] = urlparse.urljoin(response.url, url)
            item['intern_url'] = ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/@href").extract())
            item['intern_info'] = ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/text()").extract())
            
           # image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
           # item['intern_info'] = info.xpath("tr/th[@class='common']/a[2]/text()").extract()
           # item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            #if info.xpath("tr/td[@class='by']/em/span/text()" ).extract()!= -1:
            item['intern_date'] = ''.join(info.xpath("tr/td[@class='by']/em/span/text()" ).extract())
            if item['intern_date'].find('1') != -1:
                item['intern_date'] = ''.join(info.xpath("tr/td[@class='by']/em/span/text()" ).extract())   
            else: 
                item['intern_date'] = ''.join(info.xpath( "tr/td[@class='by']/em/span/span/@title").extract())
            item['intern_source'] = str('NUAA') 
            deep_url = ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/@href").extract())
            yield Request(deep_url, meta={'item':item}, callback=self.parse_item) 
        for i in range(2,page_num):
            next_url = "http://www.hkhtu.com/forum-44-" + str(i) + ".html" 
            yield  scrapy.Request(next_url,callback = self.parse_info)
              
    def parse_info(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//tbody[contains(@id,'normal')]")
         
 
        for info in infos:  
            item = NuaaInternItem() 
           # item['intern_url'] = ''.join(info.xpath("tr/th[@class='common']/a[2]/@href").extract())
#             url = info.xpath("tr/th[@class='common']/a[2]/@href").extract()
#             item['intern_url'] = urlparse.urljoin(response.url, url)
#             print item['intern_url'] 
#             item['intern_info'] = info.xpath("tr/th[@class='common']/a[2]/text()").extract()
            item['intern_url'] =  ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/@href").extract())
            item['intern_info'] = ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/text()").extract())
            
           # item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            #if info.xpath("tr/td[@class='by']/em/span/text()" ).extract()!= -1:
            item['intern_date'] = ''.join(info.xpath("tr/td[@class='by']/em/span/text()" ).extract())
            if item['intern_date'].find('1') != -1:
                item['intern_date'] = ''.join(info.xpath("tr/td[@class='by']/em/span/text()" ).extract())   
            else: 
                item['intern_date'] = ''.join(info.xpath( "tr/td[@class='by']/em/span/span/@title").extract())
            item['intern_source'] = str('NUAA')  
           # item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
            deep_url = ''.join(info.xpath("tr/th/a[@onclick='atarget(this)']/@href").extract())
            yield Request(deep_url, meta={'item':item}, callback=self.parse_item) 
            
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        detail = sel.xpath('//td[@class="t_f"][1]')
        item['intern_detail'] = detail.xpath('string(.)').extract()
        item['intern_detail'] = str(''.join(detail.xpath('string(.)').extract())).replace('\n','').replace('\r','').replace(' ','').replace('/t','')
        line = item['intern_date']+'\t'+item['intern_info']+'\t'+item['intern_url']+'\t'+item['intern_detail']+'\n'
        file.writelines(line)
        return item   

#     def parse_info(self, response):  
#         sel = Selector(response)  
#         infos = sel.xpath("//ul[@class='infoList']")
#         
#         for info in infos:  
#             item = NjuptInternItem()  
#             item['intern_info'] = ''.join(info.xpath("li[@class='span1']/a/@title").extract())
#             item['intern_url'] =  "http://njupt.91job.gov.cn"+''.join(info.xpath("li[@class='span1']/a/@href").extract())
#             item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
#             item['intern_date'] =''.join(info.xpath("li[@class='span4']/text()").extract())
#             item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
#             yield item