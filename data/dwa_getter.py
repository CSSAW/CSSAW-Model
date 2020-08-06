import pandas as pd
from cssaw_central.Session import Session

def get_monthly_dwa_data(startDate, endDate, sess, station):
    """ Returns a pandas df with monthly dwa data
        args:
            startDate ---- a string in the YYYYMMDD format for the start of the desired data
            endDate ---- a string in the YYYYMMDD format for the end of the desired data
            sess ---- a cssaw-central session used to query the database
            station ---- a string representing the desired station. ex: 'A2H056'
    """
    tableName = 'dwa_preprocessed'
    query = "SELECT * from CENTRAL." + tableName \
         + " WHERE station = '" + station + "'" \
         + " AND `date` >= " + startDate \
         + " AND `date` <= " + endDate 
    dataFrame = sess.execute_query(query, pandas=True)
    dataFrame = dataFrame.drop("TIME", axis='columns')
    dataFrame = dataFrame.drop("QUA", axis='columns')
    dataFrame = dataFrame.drop("QUA.1", axis='columns')
    dataFrame = dataFrame.drop("id", axis='columns')
    dataFrame = dataFrame.drop("Unnamed: 0", axis='columns')

    # The line below gets rid of the Day portion of the Date column,
    # it is used in the groupby to return monthly data. 
    dataFrame["DATE"] = dataFrame["DATE"].apply(lambda x: (int)(x / 100))
    dataFrame = dataFrame.groupby("DATE").mean()

    return dataFrame


def runDWA():
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username,password, host, db='CENTRAL')

    startDate = '19800000'
    endDate = '19850000'
   
    testDf = get_monthly_dwa_data(startDate,endDate, sess, 'A2H056')
    
    return testDf.head()

if __name__ == "__main__":
    print(run()))

if __name__ == "__main__":
    print(run()))

if __name__ == "__main__":
    print(run()))

if __name__ == "__main__":
    print(run))

if __name__ == "__main__":
    r)

if __name__ == "__main_")

if __name__ == "__main")

if n)