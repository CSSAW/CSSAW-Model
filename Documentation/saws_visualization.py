import pydeck
from geojson import Feature, Point, FeatureCollection, Polygon
from cssaw_central.Session import Session

from sklearn import preprocessing
import pandas as pd
import numpy as np
import streamlit as st

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

    # make sure that the start date and end date are not within the same month and year
    if startMonth != endMonth or startYear != endYear:
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

        # handle the end month, year here
        currentDate = "{}-1-{}".format(currentMonth, currentYear)
        query = "SELECT * from CENTRAL.saws_precipitation" + " WHERE `Date` LIKE '" + currentDate + "'"
        # get data by date from the database and append to the dataframe
        dataFrame = dataFrame.append(pd.DataFrame(sess.execute_query(query, pandas=True)), ignore_index=True)

    # The line below gets rid of the Day portion of the Date column
    dataFrame["Date"] = dataFrame["Date"].apply(reformatDate) 

    return dataFrame

# creates and returns a geo json out of Limpopo region and the precipiatation data 
def create_geo_json(date, sess):
    dataFrame = get_monthly_saws_data(date, date, sess)
    sess.conn.close()

    print(dataFrame.head())
    # normalized_df=(normalized_df-normalized_df.min())/(normalized_df.max()-normalized_df.min())
    polygonSize = 0.02/2
    geoJsonList = []
    # print(normalized_df.head())
    for index,row in dataFrame.iterrows():
        # feature = Feature(geometry=Point((row['long'], row['Latitude'])), properties={"elevation":row["Rainfall (mm)"]})
       # Polygon()

        #Polygon([[[row['Longitude']-polygonSize, row['Latitude']-polygonSize],[row['Longitude']-polygonSize, row['Latitude']+polygonSize],[row['Longitude']+polygonSize, row['Latitude']+polygonSize],[row['Longitude']+polygonSize, row['Latitude']-polygonSize], [row['Longitude']-polygonSize, row['Latitude']-polygonSize]]])

        feature = Feature(geometry=Polygon([[ [29.39, 24.65], [29.59, 24.85], [29.79, 25.05], [29.99, 25.25], [29.39, 24.65] ]]), 
        properties={"elevation": row["Rainfall (mm)"], "normalizedElevation": row["Rainfall (mm)"]
        })
        geoJsonList.append(feature)

    featureCollection = FeatureCollection(geoJsonList)
    return featureCollection

if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    mapbox_api_key = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username, password, host, db='CENTRAL')
    data = create_geo_json("20120101", sess)
    
    INITIAL_VIEW_STATE = pydeck.ViewState(Latitude=-24.654950, Longitude=29.3906515, zoom=7, max_zoom=16, pitch=45, bearing=0)

    geojson = pydeck.Layer(
        "GeoJsonLayer",
        data = data,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="elevation*1500000",
        get_radius=1000, 
        get_fill_color="[255 ,100, normalizedElevation * 255, 255]", 
        get_line_color=[255, 255, 255],
    )


    r = pydeck.Deck(mapbox_key=mapbox_api_key, layers=[ geojson], initial_view_state=INITIAL_VIEW_STATE)

    r.to_html("saws_geojson_layer.html")

