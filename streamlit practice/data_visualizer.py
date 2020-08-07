import streamlit as st
import numpy as np
import pandas as pd
from cssaw_central.Session import Session
import time
import sys

# get credentials via reading a text file
credentials = open('../credentials.txt', 'r')
username = credentials.readline().replace('\n','')
password = credentials.readline().replace('\n','')
host = credentials.readline().replace('\n','')
credentials.close()
# use credentials to start a session
#sess = Session(username,password, host, db='CENTRAL')

# method that takes a date in as an argument and reformats it to remove the day
def reformatDate(date):
    month = date[0:date.index("-")]
    year = date[-4:]
    if len(month) == 1:
        month = "0{}".format(month)
    
    return "{}{}".format(year, month)

# @st.cache
# def get_monthly_saws_data(startDate, endDate):
#     """ Returns a pandas df with monthly saws data
#         args:
#             startDate ---- a string in the YYYYMMDD format for the start of the desired data
#             endDate ---- a string in the YYYYMMDD format for the end of the desired data
#             sess ---- a cssaw-central session used to query the database
#             station ---- a string representing the desired station. ex: 'A2H056'
#     """
#     startMonth, startDay, startYear = startDate[4:6], startDate[-2:], startDate[0:4]
#     endMonth, endDay, endYear = endDate[4:6], endDate[-2:], endDate[0:4]

#     # remove leading 0s from month and day entries to match the dates in the database
#     if startDay[0] == '0':
#         startDay = startDay[1:]
#     if startMonth[0] == '0':
#         startMonth = startMonth[1:]
#     if endDay[0] == '0':
#         endDay = endDay[1:]
#     if endMonth[0] == '0':
#         endMonth = endMonth[1:]

#     # parse the current month and year to be the starting month and year as integers
#     currentMonth = int(startMonth)
#     currentYear = int(startYear)

#     # get the dataframe for the starting month and year
#     currentDate = "{}-1-{}".format(currentMonth, currentYear)
#     query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
#     # get data by date from the database through a query and set dataframe = to the results
#     dataFrame = sess.execute_query(query, pandas=True)

#     # increment currentMonth and make sure it stays in range of 12 months, incrementing the year after 12 months
#     currentMonth += 1
#     if currentMonth > 12:
#         currentMonth = 1
#         currentYear += 1

#     # make sure that the start date and end date are not within the same month and year
#     if startMonth != endMonth or startYear != endYear:
#         # loop through all the months and years until you reach the end month and year
#         while currentMonth != int(endMonth) and currentYear != endYear:
#             currentDate = "{}-1-{}".format(currentMonth, currentYear)
#             query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"

#             # increment currentMonth and make sure it stays in range of 12 months, incrementing the year after 12 months
#             currentMonth += 1
#             if currentMonth > 12:
#                 currentMonth = 1
#                 currentYear += 1

#             # get data by date from the database through a query and append results to the dataframe
#             dataFrame = dataFrame.append(sess.execute_query(query, pandas=True), ignore_index=True)

#         # handle the end month, year here
#         currentDate = "{}-1-{}".format(currentMonth, currentYear)
#         query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
#         # get data by date from the database and append to the dataframe
#         dataFrame = dataFrame.append(pd.DataFrame(sess.execute_query(query, pandas=True)), ignore_index=True)

#     # The line below gets rid of the Day portion of the Date column
#     dataFrame["Date"] = dataFrame["Date"].apply(reformatDate) 


    return dataFrame


if __name__ == "__main__":
    st.title('Data Visualization')

    st.write("Use the side bar to select different dates")

    # months is used to convert any month name or number to correct formatting
    monthConvert = {
        "January": "01",
        "Febrauary": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
        "1": "01",
        "2": "02",
        "3": "03",
        "4": "04",
        "5": "05",
        "6": "06",
        "7": "07",
        "8": "08",
        "9": "09",
        "10": "10",
        "11": "11",
        "12": "12",
    }
    monthOptions = [
        "January",
        "Febrauary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    years = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]

    startMonth = st.sidebar.selectbox("Pick a startMonth", monthOptions)
    startYear = st.sidebar.selectbox("Pick a year:", years)

    numMonths = st.sidebar.slider("Specify the number of months of data to look at", 1, 5, 1, 1)

    "You selected: ", startMonth, startYear, numMonths

    startDate = "{}{}01".format(startYear, monthConvert[startMonth])
    
    # use 1 month for testing
    endDate = startDate
    currentMonth = int(monthConvert[startMonth])
    currentYear = int(startYear)

    for i in range(numMonths - 1):
        currentMonth += 1
        if currentMonth == 13:
            currentYear += 1
            currentMonth = 1
            
        if currentYear == 2020 and currentMonth <= 7:
            endDate = "{}{}01".format(currentYear, monthConvert[str(currentMonth)])
        elif currentYear <= 2019:
            endDate = "{}{}01".format(currentYear, monthConvert[str(currentMonth)])

    st.write(endDate)

    # use getter method to get data from database for selected date
    #df = get_monthly_saws_data(startDate, endDate)
    
    #st.write(df.head())
