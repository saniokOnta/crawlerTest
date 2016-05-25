import scrapy,re
import logging
from rat.items import RatItem
from googlemaps import Client

class ratSpider(scrapy.Spider):

    gKey = 'AIzaSyD6HTdJLDVNyYQZnDp1kZcG0Pks3sRRNh4'
    days =['mon_fri','saturday','sunday']
    lineNameNamePath = '//div[@id="web_traseu"]/b/text()'
    stationPath = '//div[@id="statie_web"]/b/text()'
    lineNameNrPath ='//div[@id="linia_web"]/b/text()'
    hasExtraStationsPath = '//div[@id="nota"]'
    hasHandicapRidePath = '//div[contains(@id,"dizabilitati")]'
    minXpath = '//div[@id="tabel2"][{0}]/div[@id="web_class_minutes"][{1}]/div'
    hourXpath = '//div[@id="tabel2"][{0}]/div[@id="web_class_hours"][{1}]/text()'
    hoursPath = '//div[@id="tabel2"][{0}]/div[@id="web_class_hours"]/text()'
    allLinesXpath = '//a[contains(@class,"linia")]'
    viewSchendulerXpath = '//a[@class="orar-linie"]/@href'
    viewOldVersonSchenXpath = '//h2[@class="titlu-pagina"]/a/@href'


    #logging.log(logging.WARNING, 'handicapvalue : %r\n hasExtraStations : %r',handR,extraS)

    name = "rat"
    allowed_domains = ["ratbv.ro"]
    start_urls = [
        "http://www.ratbv.ro/trasee-si-orare/",
    ]
    def  hasNode(self,response,xpath):
        if response.xpath(xpath).extract():
            return True
        return False

    def getLocation(self,stationName):
        gmaps = Client(key= self.gKey)
        geocode_result = gmaps.geocode('brasov {0}'.format(stationName))
        return geocode_result[0]['geometry']['location']

    def xpathExtractor(self,response,xpath):
        temp = response.xpath(xpath)
        if temp:
            nodes = temp.extract()
            if nodes:
                return nodes[0].strip()
        return ''
    
    # def getDaySchedulerHandicapRide(self,response,dayIndex):

    #     count = len(response.xpath(self.hoursPath.format(dayIndex)).extract())-1
    #     li = []
    #     for i in range(count):
    #         li.append({ self.xpathExtractor(response,self.hourXpath.format(dayIndex,i+2)):response.xpath(self.minXpath.format(dayIndex,i+2)).extract() })
    #     return li

    # def getDaySchedulerExtraStations(self,response,dayIndex):
    #     count = len(response.xpath(self.hoursPath.format(dayIndex)).extract())-1
    #     li = []
    #     for i in range(count):
    #         li.append({ self.xpathExtractor(response,self.hourXpath.format(dayIndex,i+2)):response.xpath(self.minXpath.format(dayIndex,i+2)).extract() })
    #     return li

    def getDaySchedulerHanAndExtra(self,response,dayIndex):
        count = len(response.xpath(self.hoursPath.format(dayIndex)).extract())-1
        li = []
        for i in range(count):
            minutes = []
            for r in response.xpath(self.minXpath.format(dayIndex,i+2)):
                hand = False;
                extraStat = False;
                if r.xpath('@id').extract()[0] == 'web_min_blue':
                    hand = True
                if len(r.xpath('b').extract())>0:
                    extraStat = True
                minutes.append({'min' : r.xpath('text()').extract()[0].strip(),'hasHandicapRide' : hand,'hasExtraStations' : extraStat})
            li.append({ self.xpathExtractor(response,self.hourXpath.format(dayIndex,i+2)): minutes })
        return li
        

    # def getDayScheduler(self,response,dayIndex,hasHandicapRide,hasExtraStations):
    #     if hasExtraStations and hasHandicapRide:
    #         return self.getDaySchedulerHanAndExtra(response, dayIndex)
    #     elif hasHandicapRide:
    #         return self.getDaySchedulerHandicapRide(response, dayIndex)
    #     elif hasExtraStations:
    #         return self.getDaySchedulerExtraStations(response, dayIndex)
    #     else:
    #         count = len(response.xpath(self.hoursPath.format(dayIndex)).extract())-1
    #         li = []
    #         for i in range(count):
    #             li.append({ self.xpathExtractor(response,self.hourXpath.format(dayIndex,i+2)):response.xpath(self.minXpath.format(dayIndex,i+2)).extract() })
    #         return li

    def getStationProgram(self,response):
        program = RatItem()
        program['lineName'] = self.xpathExtractor(response,self.lineNameNamePath)
        program['lineNr'] = self.xpathExtractor(response,self.lineNameNrPath)
        stationName = self.xpathExtractor(response,self.stationPath)
        program['station'] ={'name':stationName,'location' : self.getLocation(stationName)}
        handR = self.hasNode(response, self.hasHandicapRidePath)
        extraS = self.hasNode(response, self.hasExtraStationsPath)
        program['hasExtraStations'] = extraS
        program['hasHandicapRide'] =  handR
        for i in range(3):
            program[self.days[i]] = self.getDaySchedulerHanAndExtra(response, i+1)
        yield program

    def allStations(self,response):
        for href in response.xpath('//div[contains(@class,"list")]//a/@href'):
            url =response.urljoin(href.extract())
            if "dus.html" in url:
                continue
            if "intors.html" in url:
                yield scrapy.Request(url,callback=self.parseLine)
            else:
                yield scrapy.Request(url, callback=self.getStationProgram)


    def parseLine(self,response):
        url = response.urljoin(response.xpath('//frame[2]/@src').extract()[0])
        yield scrapy.Request(url=url, callback=self.allStations)

    def vieOldVersionSchenduler(self,response):
        return response.xpath(self.viewOldVersonSchenXpath).extract()[0]

    def viewLineSchenduler(self,response):
        return scrapy.Request(url=response.xpath(self.viewSchendulerXpath).extract()[0],callback=self.vieOldVersionSchenduler)

    def getURL(self,oldUrl):
        return '/afisaje/{0}-dus.html'.format(re.search(r'linia([0-9A-Za-z]+)',oldUrl).groups()[0])

    def parse(self, response):
        for n in response.xpath(self.allLinesXpath):
        #     url = response.urljoin(self.getURL(n.xpath('@class').extract()[0]))
        #     yield scrapy.Request(url=url,callback=self.parseLine)
        #n = response.xpath(self.allLinesXpath)[0]
            url = response.urljoin(n.xpath('@href').extract()[0])
            if 'tour' in url:
                url = scrapy.Request(url,self.viewLineSchenduler)
        #yield scrapy.Request(url=url,callback=self.parseLine)
            logging.log(logging.WARNING, 'URL : %s',url)
        