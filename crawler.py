import urllib, urllib2, re, cookielib
import requests
import codecs
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json

class JSONResolve:
    def __init__(self, htmlContent):
        self.htmlContent = htmlContent
        
    def resolveHTML(self):
        jsonFormat = [];
        soup = BeautifulSoup(self.htmlContent, "html.parser");
        commentDataArr = soup.body.select(".ui-grid li p");
        offerInfoDataArr = soup.body.select(".ui-block-b p");
        offerInfoTitleArr = ["company", "position", "city", "salary", "remark"];
        offerJSON = "";
        for index, item in enumerate(offerInfoDataArr):
            tempSoup = BeautifulSoup(str(item), "html.parser");
            if index == 0:
                offerJSON += "{\"" + offerInfoTitleArr[index] + "\": \"" + tempSoup.text + "\",";
            if index == 1 or index == 2 or index == 3:
                offerJSON += "\"" + offerInfoTitleArr[index] + "\": \"" + tempSoup.text + "\",";
            if index == 6:
                offerJSON += "\"" + offerInfoTitleArr[4] + "\": \"" + tempSoup.text + "\"";
        if len(commentDataArr) != 0:
            offerJSON += ", \"comments\": [" 
            for index, item in enumerate(commentDataArr):
                if index % 2 != 0:
                    strComment = str(item).replace('\n',',').replace('\r\n',',')
                    tempSoup = BeautifulSoup(strComment, "html.parser");
                    offerJSON += "\"" + tempSoup.get_text() + "\",";
            offerJSON = offerJSON[:-1] + "]}"
        else:
            offerJSON += "}"
        return offerJSON
if __name__ == "__main__":
    preURL = 'http://www.ioffershow.com:8000/offerdetail/';
    jsonDatas = [];
    for i in range(1, 999):
        mainURL = preURL + str(i);
        response = requests.session().get(mainURL);
        print "crawling No " + str(i) + "..."
        if response.text.find("div") == -1:
            continue;
        else: 
            tempJSONResolve = JSONResolve(response.text)
            strArrData = tempJSONResolve.resolveHTML()
            strArrData = strArrData + ",\n"
            fp = codecs.open("data.txt", "a", 'utf-8')
            fp.write(strArrData)
           