import pandas as pd
from cssaw_central.Session import Session

def getQueriesInRange(startMonth, startYear, endMonth, endYear):
    currentMonth = int(startMonth)
    currentYear = int(startYear)

    queries = []
    while currentMonth != int(endMonth) and currentYear != endYear:
        currentDate = "{}-1-{}".format(currentMonth, currentYear)
        queries.append("SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'")
        currentMonth += 1
        if currentMonth > 12:
            currentMonth = 1
            currentYear += 1
    currentDate = "{}-1-{}".format(currentMonth, currentYear)
    queries.append("SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'")
    
    return queries

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

    queries = getQueriesInRange(startMonth, startYear, endMonth, endYear)
    print(queries)

    # format the date to match the dates in the database, fixing a 1 in for day since model is using months for data anyways
    # startDate = "{}-1-{}".format(startMonth, startYear)
    # endDate = "{}-1-{}".format(endMonth, endYear)
    # # print(startDate, endDate)
    # tableName = 'saws_precipitation'
    # query = "SELECT * from CENTRAL." + tableName \
    #      + " WHERE `Date` LIKE '" + startDate + "'" 
    #      #+ " AND `Date` <= " + endDate 

    dataFrame = pd.DataFrame()

    currentMonth = int(startMonth)
    currentYear = int(startYear)

    currentDate = "{}-1-{}".format(currentMonth, currentYear)
    query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
    dataFrame = sess.execute_query(query, pandas=True)
    currentMonth += 1
    if currentMonth > 12:
        currentMonth = 1
        currentYear += 1

    while currentMonth != int(endMonth) and currentYear != endYear:
        currentDate = "{}-1-{}".format(currentMonth, currentYear)
        query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"

        currentMonth += 1
        if currentMonth > 12:
            currentMonth = 1
            currentYear += 1
 
        dataFrame = dataFrame.append(sess.execute_query(query, pandas=True), ignore_index=True)

    currentDate = "{}-1-{}".format(currentMonth, currentYear)
    query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
    dataFrame = dataFrame.append(pd.DataFrame(sess.execute_query(query, pandas=True)), ignore_index=True)

    # The line below gets rid of the Day portion of the Date column,
    # it is used in the groupby to return monthly data. 
    # dataFrame["DATE"] = dataFrame["DATE"].apply(lambda x: "{}{}".format(x[-4:], x[4:-5]))
    # dataFrame = dataFrame.groupby("DATE").mean()

    return dataFrame

if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username,password, host, db='CENTRAL')

    startDate = '20120310'
    endDate = '20120511'
   
    testDf = get_monthly_saws_data(startDate,endDate, sess)
    
    print(testDf.head())
    print(testDf.size)
    print(testDf.loc[[370]])
    print(testDf.loc[[900]])
    
    testDf.to_json (r'.\df.json')
    pass