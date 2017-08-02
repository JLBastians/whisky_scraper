from os import path, makedirs, listdir, getcwd
from datetime import date
import shutil
import time
import sys
from whisky_excel_IO_v2 import scrape_new_data


SOURCE_PATH = path.join(getcwd(), path.join(path.join("spreadsheets", "current")))
BACKUP_PATH = path.join(SOURCE_PATH, "_backup")

NUMBER_OF_MINUTES = 5
UPDATE_DELAY = 60 * NUMBER_OF_MINUTES

'''
This creates a copy of all the files in the "current" directory (I.E: all the "current" data).
The purpose of it is to backup the files that contain all the current data for each whisky. 
Overide will overwrite the current day's archive if it already exists.
'''
def BackUp(override=False):
    # Make a folder in the backup directory for the day
    currentDate = str(date.today())
    backUpPathForDay = BACKUP_PATH + "/" + currentDate
    if not path.exists(backUpPathForDay) or override:
        if override:
            makedirs(backUpPathForDay + "(forced)")

            # Copy files from the directory they are edited in to the safe backup folder for the day.
            source_files = listdir(SOURCE_PATH)
            for fileName in source_files:
                fullFileName = path.join(SOURCE_PATH, fileName)
                if path.isfile(fullFileName):
                    shutil.copy(fullFileName, backUpPathForDay + "(forced)")

            print("Forced back up complete.")

        else:
            makedirs(backUpPathForDay)

            # Copy files from the directory they are edited in to the safe backup folder for the day.
            source_files = listdir(SOURCE_PATH)
            for fileName in source_files:
                fullFileName = path.join(SOURCE_PATH, fileName)
                if path.isfile(fullFileName):
                    shutil.copy(fullFileName, backUpPathForDay)

            print("Back up complete.")

    else:
        print("Back up already completed today.")


def UpdateCurrentPrices():
    print("Updating market prices every " + str(UPDATE_DELAY/60) + " minutes.")
    print("")
    while True:
        currentTime = time.strftime("%H:%M:%S", time.localtime())
        try:
            scrape_new_data()
            print(currentTime + ": Market prices updated.")
        except:
            print(currentTime + ": Market prices failed to update, will try again next tick (" + str(UPDATE_DELAY/60) + " minutes.")

        time.sleep(60)
        count = 1
        while count < NUMBER_OF_MINUTES:
            print("Time until next update: %i minutes" % (NUMBER_OF_MINUTES - count), end='\r')
            count += 1
            time.sleep(60)
        print("\n")
        print("Updating...")




'''
The idea is to run this program once and let it run for the full day.
Backup() will backup all the files containing "current" data so that all the data gathered the previous day will be
archived.
'''
BackUp()
UpdateCurrentPrices()
