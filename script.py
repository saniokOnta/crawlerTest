from crawler import Response

def doWork():
    response = Response()
    response.navigateToUrl('http://ratbv.ro/afisaje/5-dus/div_list_ro.html')
    response.getValueByXpath('//div[@id="web_traseu"]/b/text()')


            
if __name__ == "__main__":
    doWork()
