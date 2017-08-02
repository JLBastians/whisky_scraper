import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os.path, os.getcwd


LOAD_PATH = os.path.join(os.getcwd(), "spreadsheets")  # Need to fix this directory
SAVE_PATH = os.path.join(LOAD_PATH, "by_brand")

whiskyFile1 = 'benrinnes_2012Q3_HHR_prices.xlsx'
whiskyFile2 = 'benrinnes_2012Q4_HHR_prices.xlsx'

# The file names with directories
whiskyFile1 = os.path.join(LOAD_PATH, whiskyFile1)
whiskyFile2 = os.path.join(LOAD_PATH, whiskyFile2)

# This is indexed by date and has a Price column
df1 = pd.read_excel(whiskyFile1, index_col='Date', columns=['Price'])
df2 = pd.read_excel(whiskyFile2, index_col='Date')

print(df1[:5])

plot = df1.plot()
plot.set_ylabel('Average Deal Price')
plt.show()

