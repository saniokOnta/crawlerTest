from Spyder import Scrapy
import xpaths,re,json

class rat_Crawler:
    def __init__(self):
        self.scrapy = Scrapy()
        self._lines = []

    def log(self,message):
        with open("log.txt", "a") as f:
            f.write(message)
            f.write('\n')

    def get_absolute_url(self,url):
        if not(url):
            return None
        if 'http' in url:
            return url
        elif url[0] == '/':
            return 'http://www.ratbv.ro' + url
        elif '../' in url:
            return 'http://www.ratbv.ro/afisaje' + url.replace('../', '/')
        else:
            return 'http://www.ratbv.ro/'+ url

    #returneaza un obiect de tip Response care poate fi parsat cu ajutorul xpath-urilor
    def request(self,url):
        if url:
            url = self.get_absolute_url(url)
            self.log(url)
            print(url)
            try:
                return self.scrapy.Request(url)
            except Exception, e:
                try:  
                    return self.scrapy.Request(url.lower())
                except Exception, e1:
                    temp = re.search('\d+[a-z]',url).group()
                    self.log(str(e1))
                    return self.scrapy.Request(url.replace(temp,temp.upper()))
                self.log(str(e))
                raise
        else:
            self.append('tried navigate to empty url')
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
    def get_Inertext(self,response,xpath):
        return response.xpath(xpath)[0]
    
    def parse_line(self,lineUrl):
        lineUrl = self.get_clean_line_url(lineUrl)
        r = self.request(lineUrl)
        r = self.request('/afisaje/'+r.xpath('//frame[2]/@src')[0])
        stationLst = r.xpath('//div[contains(@class,"list")]//a/@href')
        self.parse_stations(stationLst,lineUrl)

    def parse_stations(self,stationLst,lineUrl):
        line_model = {'name' : None,'nr' : None,'stations' : []}        
        for s in stationLst:
            if 'intors.html' in s:
                self._lines.append(line_model)
                self.parse_line(s)
                return 
            elif 'dus.html' in s:
                self._lines.append(line_model)
                return
            station = re.search(r'(http.*)\.',lineUrl).groups()[0] + '/'+s
            r = self.request(station)
            if not(line_model['name']):
                line_model['name'] = self.get_Inertext(r,xpaths.lineNamePath)
            if not(line_model['nr']):
                line_model['nr'] = self.get_Inertext(r,xpaths.lineNameNrPath)
            line_model['stations'].append(r.xpath(xpaths.stationNamePath)[0])
        self._lines.append(line_model)

    def printLines(self):
        with open('results.json', 'w') as f:
            json.dump(self._lines, f)
        print (self._lines)

def doWork():
    c = rat_Crawler()
    response = c.scrapy.Request(xpaths.startUrl)
    lst = response.xpath(xpaths.allLinesXpath)
    #c.parse_line('/afisaje/34-dus.html')
    for i in range(0,len(lst)):
        print ('start parsing ------------>' + str(i))
        c.parse_line(lst[i])
    c.printLines()
    #c.print_s()

if __name__ == "__main__":
    doWork()
