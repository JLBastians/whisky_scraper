'''

This contains proforma templates that are used elsewhere.

'''
from os import path, getcwd
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

METADATA_FILENAME = "whisky_metadata.xlsx"

SAVE_PATH_HISTORICAL = path.join(getcwd(), path.join("spreadsheets", "historical"))
SAVE_PATH_CURRENT = path.join(getcwd(), path.join("spreadsheets", "current"))