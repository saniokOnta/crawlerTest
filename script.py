from Spyder import Scrapy
import xpaths,re,json

class rat_Crawler:
    def __init__(self):
        self.scrapy = Scrapy()
        self._lines = []
        self.days =['mon_fri','saturday','sunday']

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
        l = response.xpath(xpath)
        return l[0] if len(l)>0 else None
    
    def parse_line(self,lineUrl):
        lineUrl = self.get_clean_line_url(lineUrl)
        r = self.request(lineUrl)
        r = self.request('/afisaje/'+r.xpath('//frame[2]/@src')[0])
        stationLst = r.xpath('//div[contains(@class,"list")]//a/@href')
        self.parse_stations(stationLst,lineUrl)

    def get_node_list(self,lst):
        return lst


    def getDaySchedulerHanAndExtra(self,response,dayIndex):
        count = len(response.xpath(xpaths.hoursPath.format(dayIndex)))-1
        li = []
        for i in range(count):
            minutes = []
            for n in response.xpath(xpaths.minXpath.format(dayIndex,i+2),elementListCallBack=self.get_node_list):
                hand = False;
                extraStat = False;
                if n.xpath('@id')[0] == 'web_min_blue':
                    hand = True
                if len(n.xpath('b'))>0:
                    extraStat = True
                minutes.append({'min' : n.xpath('text()')[0].strip(),'hasHandicapRide' : hand,'hasExtraStations' : extraStat})
            li.append({ self.get_Inertext(response,xpaths.hourXpath.format(dayIndex,i+2)).strip(): minutes })
        return li

    def parse_stations(self,stationLst,lineUrl):
        line_model = {'name' : None,'nr' : None,'hasExtraStations' : None,'hasHandicapPalces' : None,'stations' : []}        
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
            if not(line_model['hasExtraStations']):
                line_model['hasExtraStations'] = True if self.get_Inertext(r,xpaths.hasExtraStationsPath) else False
            if not(line_model['hasHandicapPalces']):
                line_model['hasHandicapPalces'] = True if self.get_Inertext(r,xpaths.hasHandicapRidePath) else False
            station = {}
            program = {}
            station['name'] =  self.get_Inertext(r,xpaths.stationNamePath)
            for i in range(3):
                program[self.days[i]] = self.getDaySchedulerHanAndExtra(r, i+1)
            station['program'] = program
            line_model['stations'].append(station)
        self._lines.append(line_model)

    def get_result(self):
        response = self.scrapy.Request(xpaths.startUrl)
        lst = response.xpath(xpaths.allLinesXpath)
        for i in range(0,len(lst)):
            print ('start parsing ------------>' + str(i))
            self.parse_line(lst[i])
        return self._lines

def doWork():
    c = rat_Crawler()
    r = c.get_result()
    with open('results.json', 'w') as f:
            json.dump(r, f)
    #c.print_s()

if __name__ == "__main__":
    doWork()
