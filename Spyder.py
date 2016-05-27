import urllib2
from lxml import etree
from StringIO import StringIO

class  Scrapy():
    
    def Request(self,url,callBack = None):
        r = Response().load(urllib2.urlopen(url).read())
        return callBack(r) if callBack else r



class Response():
    def __init__(self):
       tree = None

    def load(self,htmlSource):
    	p = etree.HTMLParser()
        self.tree = etree.parse(StringIO(htmlSource),p)
        return self

    def xpath(self,xpath,elementListCallBack = None):
        l = self.tree.xpath(xpath)
        return elementListCallBack(l) if elementListCallBack else self.list_to_string(l)

    def list_to_string(self,lst):
        new_lst = []
        for i in lst:
            new_lst.append(str(i))
        return new_lst
            
