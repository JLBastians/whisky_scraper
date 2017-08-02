from datetime import datetime, timedelta

def FormatDate(initialDateString, dateIncrement):

    initialDateString = initialDateString.replace("/", " ")
    initialDateString = initialDateString.split()
    day = int(initialDateString[0])
    month = int(initialDateString[1])
    year = int(initialDateString[2])

    date = datetime(year, month, day)
    newDate = date + timedelta(days = dateIncrement)

    # Reformatting date to fit the standard in whisky_excel_IO.py
    newDateSplit = str(newDate).split()
    newDateFormatted = newDateSplit[0].replace("-", " ")
    newDateFormatted = newDateFormatted.split()[2] + "/" + newDateFormatted.split()[1] + "/" + newDateFormatted.split()[0]

    return newDateFormatted

