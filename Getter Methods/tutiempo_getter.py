import pandas as pd
from cssaw_central.Session import Session


def get_monthly_tutiempo_data(startDate, endDate, sess, station=None):
    """ Returns a pandas df with monthly dwa data
        args:
            startDate ---- a string in the YYYYMMDD format for the start of the desired data
            endDate ---- a string in the YYYYMMDD format for the end of the desired data
            sess ---- a cssaw-central session used to query the database
            station ---- a string representing the desired station. ex: 'A2H056'
    """
    tableName = 'tutiempoMonthly'
    query = "SELECT * from CENTRAL." + tableName \
         + " WHERE station = '" + station + "'" \
         + " AND 'Date' >= " + startDate \
         + " AND 'Date' <= " + endDate 
    dataFrame = sess.execute_query(query, pandas=True)
    dataFrame = dataFrame.drop("id", axis='columns')
    return dataFrame


if __name__ == "__main__":
    credentials = open('credentials.txt', 'r')
    username = credentials.readline().replace('\n', '')
    password = credentials.readline().replace('\n', '')
    host = credentials.readline().replace('\n', '')
    credentials.close()

    sess = Session(username, password, host, db='CENTRAL')

    startDate = '200001'
    endDate = '202101'

    testDf = get_monthly_tutiempo_data(startDate, endDate, sess, None)

    print(testDf.head())
    pass