from lxml import etree
import urllib2 
from StringIO import StringIO

class Response:
    def __init__(self):
	tree =None 

    def navigateToUrl(self,url):
        self.tree = etree.parse(StringIO(urllib2.urlopen(url).read()))

    def getValueByXpath(self,xpath):
        l = self.tree.xpath(xpath)
	return l[0] if l else None

    def getValuesByXpath(self,xpath):
	l = self.tree.xpath(xpath)
	return l


       

