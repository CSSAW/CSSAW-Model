import pandas as pd
from cssaw_central.Session import Session

import sys
sys.path.append('Getter Methods/')
# Enables importing files in getter methods

from dwa_getter import get_monthly_dwa_data
from grace_gracefo_getter import get_lwe_by_range
from saws_getter import get_monthly_saws_data


def get_all_data(startDate, endDate, sess,  station):
    """ Returns a pandas df with monthly data
        args:
            startDate ---- a string in the YYYYMMDD format for the start of the desired data
            endDate ---- a string in the YYYYMMDD format for the end of the desired data
            sess ---- a cssaw-central session used to query the database
            station ---- a string representing the desired station. ex: 'A2H056'
    """
    dwa_df = get_monthly_dwa_data(startDate,endDate,sess,station)
    lat = dwa_df["lat"].iloc[0]
    long = dwa_df["long"].iloc[0]
    print(lat,long)
    print(dwa_df.head())
    lwe_df = get_lwe_by_range(startDate,endDate,sess, bbox=[str(lat-1),str(long-1),str(lat+1),str(long+1)] )
    print(lwe_df.head())
    return "Not implemented"

if __name__ == "__main__":
    credentials = open('credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username,password, host, db='CENTRAL')
    print(get_all_data("20030100","20040100",sess,"A9H029"))