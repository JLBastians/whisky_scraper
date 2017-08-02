
import requests
from bs4 import BeautifulSoup
import json

RESPONSE_OKAY = 200 # Request code for good response
WHISKY_MARKET_URL = "https://www.whiskyinvestdirect.com/market-order-board.do"

def GetOldData(url):
    r = requests.get(url)

    if r.status_code == RESPONSE_OKAY:
        print("Response okay.")
        soup = BeautifulSoup(r.text, "lxml")

        for tag in soup.find_all("script"):
            if "Chart.drawChart" in tag.text:
                string = tag.text
                stringWordsList = string.split()
                wordIndex = 0
                for word in stringWordsList:
                    if "chartContainer" in word:
                        chartDataString = stringWordsList[wordIndex + 1]
                        chartDataString = chartDataString.replace(");", "")  # Removes the ');' at the end.
                        chartDataJSON = json.loads(chartDataString)
                        return chartDataJSON
                    wordIndex += 1


def GetWhiskyList(url): # Any whisky's URL will work all the same.
    r = requests.get(url)

    if r.status_code == RESPONSE_OKAY:
        print("Response okay.")
        soup = BeautifulSoup(r.text, "lxml")

        for tag in soup.find_all("script"):
            if "whiskyList" in tag.text:
                string = tag.text
                stringWordsList = string.split()
                wordIndex = 0
                for word in stringWordsList:
                    if "whiskyList" in word:
                        whiskyListString = stringWordsList[wordIndex + 2]
                        whiskyListString = whiskyListString.replace(";", "") # Gets rid of the semicolon at the end.
                        whiskyListJSON = json.loads(whiskyListString)
                        return whiskyListJSON
                    wordIndex += 1


def GetNewData():
    r = requests.get(WHISKY_MARKET_URL)

    if r.status_code == RESPONSE_OKAY:
        print("Response okay.")
        soup = BeautifulSoup(r.text, "lxml")

        for tag in soup.find_all("script"):
            if "initialMarket" in tag.text:
                string = tag.text
                stringWordsList = string.split()
                wordIndex = 0
                for word in stringWordsList:
                    if "initialMarket" in word:
                        currentMarketString = stringWordsList[wordIndex + 1] \
                                              + " " + stringWordsList[wordIndex + 2] \
                                              + " " + stringWordsList[wordIndex + 3] \
                                              + " " + stringWordsList[wordIndex + 4] \
                                              + " " + stringWordsList[wordIndex + 5]
                        currentMarketString = currentMarketString.replace("\"en\"},", "\"en\"}")  # Gets rid of the comma at the end.
                        file = open("dump.txt", "w")
                        file.write(currentMarketString)
                        file.close()
                        currentMarketJSON = json.loads(currentMarketString)
                        return currentMarketJSON
                    wordIndex += 1
