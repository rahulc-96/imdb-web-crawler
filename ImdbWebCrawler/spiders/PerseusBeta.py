# -*- coding: utf-8 -*-

import scrapy
from ImdbWebCrawler.items import MovieItem
from ImdbWebCrawler.constants import DIRECTOR,PRODUCER,WRITER,CINEMATOGRAPHER
import re

class PerseusSpider(scrapy.Spider):
    name = "PerseusBetaSpider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top",]
    
    def parse(self,response):
        links = response.css('.lister-list').css('.titleColumn').xpath('./a/@href').getall()
        i = 1
        for link in links:
            next_url = response.urljoin(link)
            if(i <= len(links)):
                i = i + 1
                yield scrapy.Request(next_url, callback = self.parseInDetail, meta={'key':link})
    
    def parseInDetail(self , response):
        title =  response.css('.title_wrapper').css('h1::text').extract()[0][:-1]
        year = response.css('#titleYear').css('a::text').get()
        duration = "".join(re.findall("[a-zA-Z0-9]+",response.css('.subtext').css('time::text').get())).replace('h','h ')
        rating = response.css('span[itemprop=ratingValue]::text').get()
        if response.css('span[class=popularityUpOrFlat]').get() is not None:
           popularity = '+' + str(response.css('span[class=popularityUpOrFlat]::text').get())
        else:
             popularity = '-' + str(response.css('span[class=popularityDown]::text').get())
    
        releaseDate = response.css('.subtext').css('a::text').extract()[-1][:-1]
        genre = ",".join(response.css('.subtext').css('a::text').extract()[:-1])
        poster_url = response.css('.poster').css('img::attr(src)').get()
        poster_url =  poster_url[:poster_url.find('_')-1]+poster_url[-4:]
        creditsUrl = response.urljoin('fullcredits')
        yield scrapy.Request(creditsUrl, callback = self.parseCast, meta = {'key':response.meta['key'],'title': title, 'year': year, 'rating':rating,'duration' : duration, 'popularity': popularity, 'release':releaseDate, 'genre': genre, 'poster': poster_url})
        
    def parseCast(self , response):
        item = MovieItem() 
        key = response.meta['key'][1:]
        item['key']= key[key.find('/')+1:-1]
        item['title'] =  response.meta['title']
        item['year'] = int(response.meta['year'])
        item['duration'] = response.meta['duration']
        item['rating'] =float( response.meta['rating'])
        item['releaseDate'] = response.meta['release']
        item['genre'] = response.meta['genre']
        item['posterUrl'] = response.meta['poster'] 
        item['popularity'] = int(response.meta['popularity'])
        cast = response.css('table[class=cast_list]').css('td:not([class^="character"])').css('a::text').extract()
        if(len(cast) > 7):
            cast = cast[:7]
        cast = [ actorName[:-1] for actorName in cast]
        creditsMap = {}
        creditsNames = response.css('#fullcredits_content').xpath('//h4/text()').extract()
        creditsNames = [ nonEmptyCredit for nonEmptyCredit in [ "".join(re.findall("[a-zA-Z0-9]+",credits)) for credits in creditsNames] if nonEmptyCredit]
        creditsNames.remove("Cast")
        i=0
        for credit in response.css('#fullcredits_content').xpath('//table/tbody'):
            if(i <=len(creditsNames)):
                creditsMap[creditsNames[i]]=[credit[1:-1] for credit in credit.css('.name').css('a::text').extract()]
                i= i + 1
            else:
                break
        item['cast'] = cast
        item['director'] = "UNCREDITED" if DIRECTOR not in creditsMap else creditsMap[DIRECTOR]
        item['producer'] = "UNCREDITED" if PRODUCER not in creditsMap else (creditsMap[PRODUCER][:5] if len(creditsMap[PRODUCER]) > 5 else creditsMap[PRODUCER])
        item['writer'] = "UNCREDITED" if WRITER not in creditsMap else (creditsMap[WRITER][:5] if len(creditsMap[WRITER]) > 5 else creditsMap[WRITER])
        item['cinematographer'] = "UNCREDITED" if CINEMATOGRAPHER not in creditsMap else creditsMap[CINEMATOGRAPHER]
        return item
      
       
       
       
        


                
        
        


