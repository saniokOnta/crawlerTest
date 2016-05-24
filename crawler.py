from lxml import html
import urllib2 
from StringIO import StringIO

class Response:
    def navigateToUrl(self,url):
        html.parse(StringIO(urllib2.urlopen(url).read()))

    def getValueByXpath(seld,xpath):
        response = html.xpath(xpaht)
        print('-------intri pe aici')
        for i in range(0,len(response)):
            print (response[i])

       

