from Spyder import Scrapy
import xpaths

class rat_Crawler:
    def __init__(self):
        self.scrapy = Scrapy()

    def get_absolute_url(self,url):
    	return 'http://www.ratbv.ro'+ (url if url[0] == '/' else '/' + url)

    def request(self,url):
	    print('-----------the url is:'+url)
	    if url:
	       u = url if 'http' in url else self.get_absolute_url(url)
	       print (u)
	       return self.scrapy.Request(u)
       	    else:
	        print('-------------the url is empty')
	        return None

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
	r = self.request(lineUrl)
	r = self.request('/afisaje/'+r.xpath('//frame[2]/@src')[0])
	stationLst = r.xpath('//div[contains(@class,"list")]//a/@href')
	print (stationLst)


def doWork():
    c = rat_Crawler()
    response = c.scrapy.Request(xpaths.startUrl)
    lst = response.xpath(xpaths.allLinesXpath)
    #for url in lst:
    c.parse_line(lst[0])
    #dsadsa


            
if __name__ == "__main__":
    doWork()
