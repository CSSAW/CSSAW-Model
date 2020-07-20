import pandas as pd
from cssaw_central.Session import Session

# Returns a pandas df with monthly data
# Dates are strings in the YYYYMMDD format 
# session is an instance of cssaw-central
# station is a string 
def get_monthly_dwa_data(startDate, endDate, sess, station):
    
    tableName = 'dwa_preprocessed'
    sqlFile = open('temporaryQuery.sql','w')
    query = "SELECT * from CENTRAL." + tableName \
         + " WHERE station = '" + station + "'" \
         + " AND `date` >= " + startDate \
         + " AND `date` <= " + endDate 
    sqlFile.write(query);
    sqlFile.close();
    return sess.execute_SQL('temporaryQuery.sql')


if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    print(username,password,host)
    sess = Session(username,password, host, db='CENTRAL')
    startDate = '19830000'
    endDate = '19850000'
   
    
    testDf = get_monthly_dwa_data(startDate,endDate, sess, 'A2H056')
    print(testDf)
    pass