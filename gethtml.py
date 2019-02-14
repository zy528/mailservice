#coding:utf8
import urllib2


def gethtml():
    url = r'http://rpt.oa.easyhin.com/pentaho/api/repos/%3Apublic%3Atest%3Atest.wcdf/generatedContent'
    res = urllib2.urlopen(url)
    html = res.read()
    return html

if __name__=="__main__":
    print gethtml()