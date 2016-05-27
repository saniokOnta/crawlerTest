from Spyder import Scrapy
import xpaths,re

class rat_Crawler:
    def __init__(self):
        self.scrapy = Scrapy()
        self._stations = set()

    def get_absolute_url(self,url):
        if not(url):
            return None
        if 'http' in url:
            return url
        elif url[0] == '/':
            return 'http://www.ratbv.ro' + url
        elif '../' in url:
            return 'http://ratbv.ro/afisaje' + url.replace('.//', '')
        else:
            return 'http://www.ratbv.ro/'+ url

    #returneaza un obiect de tip Response care poate fi parsat cu ajutorul xpath-urilor
    def request(self,url):
        if url:
            url = self.get_absolute_url(url)
            print(url)
            return self.scrapy.Request(url)
        else:
            print('-------------the url is empty')
            return None

    #returneaza url-ul unei linii de autobuz, (ulr-ul final,care duce catre orar.)

    def get_clean_line_url(self,lineUrl):
        if 'tour' in lineUrl:
            r = self.request(lineUrl)
            l = r.xpath(xpaths.viewSchendulerXpath)
            lineUrl = l[0] if l else None
            if lineUrl :
                r = self.request(lineUrl)
                l = r.xpath(xpaths.viewOldVersonSchenXpath)
                lineUrl = l[0] if l else None
        return self.get_absolute_url(lineUrl)
    
    def parse_line(self,lineUrl):
        lineUrl = self.get_clean_line_url(lineUrl)
        r = self.request(lineUrl)
        r = self.request('/afisaje/'+r.xpath('//frame[2]/@src')[0])
        stationLst = r.xpath('//div[contains(@class,"list")]//a/@href')
        for s in stationLst:
            if 'intors.html' in s:
                break          
            station = re.search(r'(http.*)\.',lineUrl).groups()[0] + '/'+s
            r = self.request(station)
            self._stations.add(r.xpath(xpaths.stationNamePath)[0])

    def print_s(self):
        print('intru pe aic')
        print(self._stations)
        pass


def doWork():
    c = rat_Crawler()
    #response = c.scrapy.Request(xpaths.startUrl)
    #lst = response.xpath(xpaths.allLinesXpath)
    c.parse_line('afisaje/5-dus.html')
    #for url in lst:
        #c.parse_line(lst[0])
    c.print_s()


            
if __name__ == "__main__":
    doWork()
