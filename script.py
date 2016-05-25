from Spyder import Scrapy
import xpaths

class rat_Crawler:
    def __init__(self):
        self.scrapy = Scrapy()

    def get_absolute_url(self,url):
    	return 'http://www.ratbv.ro'+ url

    def request(self,url):
        return self.scrapy.Request(self.get_absolute_url(url))

    def get_clean_line_url(self,lineUrl):
        r = self.request(lineUrl)
        l = r.xpath(xpaths.viewSchendulerXpath)
        lineUrl = l[0] if l else None
        if lineUrl :
            r = self.request(lineUrl)
            l = r.xpath(xpaths.viewOldVersonSchenXpath)
            lineUrl =self.get_absolute_url(l[0]) if l else None
        return lineUrl
    
    def parse_line(self,lineUrl):    
        if 'tour' in lineUrl:
            lineUrl = self.get_clean_line_url(lineUrl)
        else :
            lineUrl = self.get_absolute_url(lineUrl)
        print (lineUrl)


def doWork():
    c = rat_Crawler()
    response = c.scrapy.Request(xpaths.startUrl)
    lst = response.xpath(xpaths.allLinesXpath)
    for url in lst:
        c.parse_line(url)


            
if __name__ == "__main__":
    doWork()
