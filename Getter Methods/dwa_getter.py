import pandas as pd
from cssaw_central.Session import Session

# Returns a pandas df with monthly data
# Dates are integers in the YYYYMMDD format 
# session is an instance of cssaw-central
# station is a string 
def get_dwa_data(startDate, endDate, session ,station):
    

    return None


if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline()[:-1]
    password = credentials.readline()[:-1]
    host = credentials.readline()[:]
    print(username,password,host)
    sess = Session(username,password, host, db='CENTRAL')
    startDate = 19830000
    endDate = 19850000

    
    testDf = get_dwa_data()

    pass