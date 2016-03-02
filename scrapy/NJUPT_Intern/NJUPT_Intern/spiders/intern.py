import scrapy
from scrapy.spiders import Spider  
from scrapy.selector import Selector  

from NJUPT_Intern.items import NjuptInternItem
import sys
from scrapy.http import Request

class NjuptInternSpider(Spider):  
    reload(sys)  
    sys.setdefaultencoding('utf8')
    global file 
    file = open('D:\\train\\scrapy\\NJUPT.txt','w')
    name = "njuptintern"  
    allowed_domains = ["njupt.91job.gov.cn"]  
    start_urls = [  
      #  "http://bbs.seu.edu.cn/bbsdoc.php?board=Intern&page=497",  
       "http://njupt.91job.gov.cn/job/search?d_category%5B0%5D=0&d_category%5B1%5D=101&d_category%5B2%5D=102&page=1"  
    ]  
  
    def parse(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//ul[@class='infoList']")
        
        page_num = 34
        for info in infos:  
            item = NjuptInternItem()  
            item['intern_info'] = ''.join(info.xpath("li[@class='span1']/a/@title").extract())
            item['intern_url'] =  "http://njupt.91job.gov.cn"+''.join(info.xpath("li[@class='span1']/a/@href").extract())
          #  item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            item['intern_date'] =''.join(info.xpath("li[@class='span4']/text()").extract())
           # item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
            item['intern_source'] = str('NJUPT')
            deep_url =  "http://njupt.91job.gov.cn"+''.join(info.xpath("li[@class='span1']/a/@href").extract())
            yield Request( deep_url, meta={'item':item}, callback=self.parse_item) 
        for i in range(2,page_num):
            next_url = "http://njupt.91job.gov.cn/job/search?d_category%5B0%5D=0&d_category%5B1%5D=101&d_category%5B2%5D=102&page=" + str(i)
            yield  scrapy.Request(next_url,callback = self.parse_info)
            
            
            
    def parse_info(self, response):  
        sel = Selector(response)  
        infos = sel.xpath("//ul[@class='infoList']")
        
        for info in infos:  
            item = NjuptInternItem()  
            item['intern_info'] = ''.join(info.xpath("li[@class='span1']/a/@title").extract())
            item['intern_url'] =  "http://njupt.91job.gov.cn"+''.join(info.xpath("li[@class='span1']/a/@href").extract())
           # item['intern_location'] = ''.join(info.xpath("li[@class='span3']/text()").extract())
            item['intern_date'] =''.join(info.xpath("li[@class='span4']/text()").extract())
            #item['intern_company'] = ''.join(info.xpath("li[@class='span2']/a/text()").extract())
            item['intern_source'] = str('NJUPT')
            deep_url =  "http://njupt.91job.gov.cn"+''.join(info.xpath("li[@class='span1']/a/@href").extract())
            yield Request( deep_url, meta={'item':item}, callback=self.parse_item) 
            yield Request(item['intern_url'], meta={'item':item}, callback=self.parse_item)
            
            
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        detail = sel.xpath('//div[@class="vContent cl"]/div')
        intern_detail= ''.join(detail.xpath('string(.)').extract())
        if intern_detail.strip()=='':
             item['intern_detail'] = 'null'
        else:
             item['intern_detail'] = ''.join(detail.xpath('string(.)').extract())
        line = item['intern_date']+'\t'+item['intern_info']+'\t'+item['intern_url']+'\t'+item['intern_detail']+'\n'
        file.writelines(line)
        return item      