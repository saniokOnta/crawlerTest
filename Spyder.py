import urllib2
from lxml import etree
from StringIO import StringIO

class  Scrapy():
    # def __init__(self):
    #     response = Response()

    def Request(self,url):
        r = Response().load(urllib2.urlopen(url).read())
        return r



class Response():
    def __init__(self):
       tree = None

    def load(self,htmlSource):
    	p = etree.HTMLParser()
        self.tree = etree.parse(StringIO(htmlSource),p)
        return self

    def xpath(self,xpath):
        l = self.tree.xpath(xpath)
        li = []
        for e in l:
        	li.append(str(e))
    	return li