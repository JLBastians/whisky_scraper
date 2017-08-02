from os import listdir, path, getcwd
import pandas as pd
import matplotlib.pyplot as plt

#This assumes the desired spreadsheets are contained in: working_directory/spreadsheets
LOAD_PATH = path.join(getcwd(), "spreadsheets")


directoryList = listdir(LOAD_PATH)

# This will make a DF containing the prices against dates for all whiskies of a particular brand and barrel code.
# E.G: For Auchroisk HHR we get a DF containing the dates/prices of Auchroisk HHR with all the different bond dates.
def GenerateGroupWhiskyDF(whiskyName, barrelCode):
    listOfWhiskies = []
    df = pd.DataFrame(columns=["Date", "Price"])
    df_index = 0
    for directoryFile in directoryList:
        if ".xlsx" not in directoryFile:
            continue

        print("Working on: " + directoryFile)

        # UNCOMMENT TO CREATE DF FOR ALL WHISKIES INSTEAD OF THE ONE PASSED
        # Getting the whisky name and barrel code from the file name.
        directoryFileFormatted = directoryFile.replace("_", " ")
        splitString = directoryFileFormatted.split()
        newWhiskyName = splitString[0]
        period = splitString[1]
        newBarrelCode = splitString[2]

        if newWhiskyName == whiskyName and newBarrelCode == barrelCode:
            listOfWhiskies.append(directoryFile)
            print("Adding " + whiskyName + " " + period + " " + barrelCode)
            file = path.join(LOAD_PATH, directoryFile)
            newdf = pd.read_excel(file)
            dates = newdf["Date"][0:]

            newdf_index = 0
            # df.loc[df_index] = newdf.loc[newdf_index]
            for date in dates:
                if date not in df["Date"][0:]:
                    df_index += 1
                    df.loc[df_index] = newdf.loc[newdf_index]
                # for main_df_date in df["Date"][0:]:
                #     # print(main_df_date)
                #     if date > main_df_date:
                #         df_index += 1
                #         df.loc[df_index] = newdf.loc[newdf_index]
                #         break
                newdf_index += 1

    df = pd.DataFrame(index=df["Date"].values)  # This is a dataframe with only an index and no columns
    df.sort_index(inplace=True)
    print(listOfWhiskies)
    print(df)
    for whiskyFileName in listOfWhiskies:
        file = path.join(LOAD_PATH, whiskyFileName)
        temp_df = pd.read_excel(file, index_col="Date")
        # print(temp_df[:5])
        df = df.join(temp_df, how="outer")
    df = df[~df.index.duplicated(keep='first')]
    df.fillna(method="ffill", inplace=True)
    return df

        # oldWhiskyName = whiskyName
        # oldBarrelCode = barrelCode

whisky = "inchgower"
barrelCode = "HHR"
df = GenerateGroupWhiskyDF(whisky, barrelCode)
df.to_excel("output.xlsx", "sheet1")
print(df)
# df.plot()
# plt.show()

# fig = plt.figure()
# fig.suptitle(whisky.capitalize() + ": " + barrelCode, fontsize=14, fontweight="bold")
# chart = fig.add_subplot(111)
# chart.set_xlabel("Date")
# chart.set_ylabel("Average Daily Deal Price")
df.plot()
plt.show()

# Adjust for age and line up


