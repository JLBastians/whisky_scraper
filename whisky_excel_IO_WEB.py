'''
This should be run first.
It scrapes for the price data of each whisky to the current date and saves the data in excel files
'''

from whisky_scraper import GetNewData
import os.path
from os import listdir
import pandas as pd

SAVE_PATH_HISTORICAL = "C:/Users/Joshu/Documents/Python/whisky_scraper/spreadsheets/historical"
SAVE_PATH_CURRENT = "C:/Users/Joshu/Documents/Python/whisky_scraper/spreadsheets/current"
URL_BASE = "https://www.whiskyinvestdirect.com/"

# STANDARD_COLUMNS = ["Date",
#                     "Cheapest Buy Price", "Cheapest Buy Quantity",
#                     "Middle Buy Price", "Middle Buy Quantity",
#                     "Expensive Buy Price", "Expensive Buy Quantity",
#                     "Average Buy Price", "Average Buy Quantity"]

STANDARD_COLUMNS = ["Date",
                    "Cheapest Buy Price", "Cheapest Buy Quantity",
                    "Middle Buy Price", "Middle Buy Quantity",
                    "Expensive Buy Price", "Expensive Buy Quantity",
                    "Average Buy Price", "Average Buy Quantity",
                    "Cheapest Sell Price", "Cheapest Sell Quantity",
                    "Middle Sell Price", "Middle Sell Quantity",
                    "Expensive Sell Price", "Expensive Sell Quantity",
                    "Average Sell Price", "Average Sell Quantity"
                    ]

'''
This updates prices for all whiskies once and saves it in their respective .xlsx files. The files are separate
from the files containing historic data.
'''
def ScrapeNewData():
    directoryList = listdir(SAVE_PATH_CURRENT)
    currentMarketJSON = GetNewData()

    whiskyList = currentMarketJSON["market"]["pitches"]
    for whisky in whiskyList:
        distillery = whisky["distillery"]
        categoryName = whisky["categoryName"]
        barrelTypeCode = whisky["barrelTypeCode"]
        bondYear = whisky["bondYear"]
        bondQuarter = whisky["bondQuarter"]

        filename = distillery + "_" + str(bondYear) + bondQuarter + "_" + barrelTypeCode + "_prices.xlsx"
        file = os.path.join(SAVE_PATH_CURRENT, filename)
        if filename in directoryList:
            df = pd.read_excel(file, columns=STANDARD_COLUMNS)
            df.set_index("Date", inplace=True)
            fileIsNew = False
        else:
            df = pd.DataFrame(columns=["Date", "Price", "Quantity"])
            fileIsNew = True


        buyPriceOrderedList = []
        buyQuantityOrderedList = []
        sellPriceOrderedList = []
        sellQuantityOrderedList = []
        totalBuyQuantity = averageBuyPrice = 0
        totalSellQuantity = averageSellPrice = 0


        for priceTier in range(0,3):
            try:
                buyPriceOrderedList.append(whisky["sellPrices"][priceTier]["limit"])
                buyQuantityOrderedList.append(whisky["sellPrices"][priceTier]["quantity"])
                totalBuyQuantity += buyQuantityOrderedList[priceTier]
                averageBuyPrice += buyPriceOrderedList[priceTier] * buyQuantityOrderedList[priceTier]
            except:
                buyPriceOrderedList.append("N/A")
                buyQuantityOrderedList.append("N/A")

            try:
                sellPriceOrderedList.append(whisky["buyPrices"][priceTier]["limit"])
                sellQuantityOrderedList.append(whisky["buyPrices"][priceTier]["quantity"])
                totalSellQuantity += sellQuantityOrderedList[priceTier]
                averageSellPrice += sellPriceOrderedList[priceTier] * sellQuantityOrderedList[priceTier]
            except:
                sellPriceOrderedList.append("N/A")
                sellQuantityOrderedList.append("N/A")

        try:
            averageBuyPrice = averageBuyPrice / totalBuyQuantity
        except:
            averageBuyPrice = "N/A"
        try:
            averageSellPrice = averageSellPrice / totalSellQuantity
        except:
            averageSellPrice = "N/A"


        time = currentMarketJSON["updateTimeString"]

        row = [time,
               buyPriceOrderedList[0], buyQuantityOrderedList[0],
               buyPriceOrderedList[1], buyQuantityOrderedList[1],
               buyPriceOrderedList[2], buyQuantityOrderedList[2],
               averageBuyPrice, totalBuyQuantity,
               sellPriceOrderedList[0], sellQuantityOrderedList[0],
               sellPriceOrderedList[1], sellQuantityOrderedList[1],
               sellPriceOrderedList[2], sellQuantityOrderedList[2],
               averageSellPrice, totalSellQuantity
               ]

        temp_df = pd.DataFrame([row], columns=STANDARD_COLUMNS)
        temp_df.set_index("Date", inplace=True)
        if fileIsNew:
            df = temp_df
        else:
            df = df.append(temp_df)

        df.to_excel(file, "Price and Volume")
