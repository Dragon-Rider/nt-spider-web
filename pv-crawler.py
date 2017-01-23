import urllib, urllib2, re, cookielib
import requests
import codecs
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import re

class JSONResolve:
    def __init__(self, htmlContent):
        self.htmlContent = htmlContent
        
    def resolveHTML(self):
        jsonFormat = [];
        soup = BeautifulSoup(self.htmlContent, "html.parser");
        PVData = soup.select("[data-role='header'] h1");
        tempSoup = BeautifulSoup(str(PVData[0]), "html.parser");
        reChinese = re.compile('[\u4e00-\u9fa5]+')
        strResult = str(reChinese.findall(tempSoup.text)[0])[1:]
        print "view:" + strResult
        return int(strResult)
if __name__ == "__main__":
    preURL = 'http://www.ioffershow.com:8000/offerdetail/';
    jsonDatas = [];
    totalViewTimes = 0;
    for i in range(1, 999):
        mainURL = preURL + str(i);
        response = requests.session().get(mainURL);        
        print "crawling No " + str(i) + "..."
        if response.text.find("div") == -1:
            print "BAD PAGE"
            continue;
        else: 
            tempJSONResolve = JSONResolve(response.text)
            totalViewTimes += tempJSONResolve.resolveHTML();
    print "total view times:" + str(totalViewTimes)