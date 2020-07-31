import pandas as pd
from cssaw_central.Session import Session


# method that takes a date in as an argument and reformats it to remove the day
def reformatDate(date):
    month = date[0:date.index("-")]
    year = date[-4:]
    if len(month) == 1:
        month = "0{}".format(month)
    
    return "{}{}".format(year, month)

def get_monthly_saws_data(startDate, endDate, sess):
    """ Returns a pandas df with monthly saws data
        args:
            startDate ---- a string in the YYYYMMDD format for the start of the desired data
            endDate ---- a string in the YYYYMMDD format for the end of the desired data
            sess ---- a cssaw-central session used to query the database
            station ---- a string representing the desired station. ex: 'A2H056'
    """
    startMonth, startDay, startYear = startDate[4:6], startDate[-2:], startDate[0:4]
    endMonth, endDay, endYear = endDate[4:6], endDate[-2:], endDate[0:4]

    # remove leading 0s from month and day entries to match the dates in the database
    if startDay[0] == '0':
        startDay = startDay[1:]
    if startMonth[0] == '0':
        startMonth = startMonth[1:]
    if endDay[0] == '0':
        endDay = endDay[1:]
    if endMonth[0] == '0':
        endMonth = endMonth[1:]

    # parse the current month and year to be the starting month and year as integers
    currentMonth = int(startMonth)
    currentYear = int(startYear)

    # get the dataframe for the starting month and year
    currentDate = "{}-1-{}".format(currentMonth, currentYear)
    query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
    # get data by date from the database through a query and set dataframe = to the results
    dataFrame = sess.execute_query(query, pandas=True)

    # increment currentMonth and make sure it stays in range of 12 months, incrementing the year after 12 months
    currentMonth += 1
    if currentMonth > 12:
        currentMonth = 1
        currentYear += 1

    # loop through all the months and years until you reach the end month and year
    while currentMonth != int(endMonth) and currentYear != endYear:
        currentDate = "{}-1-{}".format(currentMonth, currentYear)
        query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"

        # increment currentMonth and make sure it stays in range of 12 months, incrementing the year after 12 months
        currentMonth += 1
        if currentMonth > 12:
            currentMonth = 1
            currentYear += 1

        # get data by date from the database through a query and append results to the dataframe
        dataFrame = dataFrame.append(sess.execute_query(query, pandas=True), ignore_index=True)

    # make sure that the start date and end date are not within the same month and year
    if startMonth != endMonth or startYear != endYear:
        # handle the end month, year here
        currentDate = "{}-1-{}".format(currentMonth, currentYear)
        query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
        # get data by date from the database and append to the dataframe
        dataFrame = dataFrame.append(pd.DataFrame(sess.execute_query(query, pandas=True)), ignore_index=True)

    # The line below gets rid of the Day portion of the Date column
    dataFrame["Date"] = dataFrame["Date"].apply(reformatDate) 


    return dataFrame

if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username,password, host, db='CENTRAL')

    # NOTE: saws data starts Jan 1 2012 and is current up to the last full month (June 30 2020 as of right now)
    startDate = '20120310'
    endDate = '20120511'
   
    testDf = get_monthly_saws_data(startDate,endDate, sess)
    
    print(testDf.head())
    