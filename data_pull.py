"""
Pull all data from cloud to local

The function will create and return a dataframe. The script 
saves that dataframe to a csv.
"""

from data.dwa_getter import *
from data.dam_getter import *
from data.grace_gracefo_getter import *
from data.saws_getter import *

def cloud_to_df():
    """[summary]

    Args:
        conn (Session): CSSAW-Central connection to use
    """
    # Open credentials
    try:
        credentials = open('credentials.txt', 'r')
    except (FileNotFoundError) as e:
        print("No credentials found, add credentials.txt to CSSAW-Model directory with the following format:")
        print("<USERNAME>\n<PASSWORD>\n<HOST>")
        return
    username = credentials.readline().replace('\n', '')
    password = credentials.readline().replace('\n', '')
    host = credentials.readline().replace('\n', '')
    credentials.close()

    sess = Session(username, password, host, db='CENTRAL')

    startDate = '19800000'
    endDate = '20200000'
    SAWS_startDate = '20120100'
    SAWS_endDate = '20120200'

    # get all data
    dwa_df = get_monthly_dwa_data(startDate,endDate, sess, 'A2H056')
    # GRACE seems to be empty currently, gives warning: truncated incorrect double value: 'Date'
    dam_df = get_dam_levels(startDate, endDate, sess)
    #saw_df = get_monthly_saws_data(SAWS_startDate, SAWS_endDate, sess)
    print("DWA:")
    print(dwa_df.head())
    print("Dam:")
    print(dam_df.head())
    for col in dam_df.columns:
        print(col)
    print(dam_df['FSC'])
    print("SAWS:")
    #print(saw_df.head())
    #for col in saw_df.columns:
    #    print(col)


if __name__ == "__main__":
    cloud_to_df()