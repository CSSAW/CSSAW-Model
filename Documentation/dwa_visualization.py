import pydeck
from geojson import Feature, Point, FeatureCollection, Polygon
from cssaw_central.Session import Session

from sklearn import preprocessing
import pandas as pd
# Some c
def create_geo_json(date, sess):

    tableName = '`dwa_primary`'
    query = "SELECT * from CENTRAL." + tableName \
         + " WHERE `DATE` > " + (str)(date) \
         + " AND `DATE` <= " + (str)(date + 31) 
         
    dataFrame = sess.execute_query(query, pandas=True)
    dataFrame = dataFrame.drop("TIME", axis='columns')
    dataFrame = dataFrame.drop("QUA", axis='columns')
    dataFrame = dataFrame.drop("QUA.1", axis='columns')

    sess.conn.close()

    # dataFrame = dataFrame.drop("date", axis='columns')
    # The line below gets rid of the Day portion of the Date column,
    # it is used in the groupby to return monthly data. 
    # dataFrame["DATE"] = dataFrame["DATE"].apply(lambda x: (int)(x / 100))

    dataFrame = dataFrame.groupby("station").mean()
    normalized_data = dataFrame["COR.LEVEL"]
    # print(normalized_df.head())

    # min_max_scaler = preprocessing.MinMaxScaler()
    # normalized_data = min_max_scaler.fit_transform(normalized_data.reshape())
    print(pd.DataFrame(dataFrame["COR.LEVEL"]).max() - pd.DataFrame(dataFrame["COR.LEVEL"]).min() )
    dataFrame["normalizedCor"] = pd.DataFrame(dataFrame["COR.LEVEL"]).apply(lambda x: (x-x.min())/(x.max()-x.min()))

    print(dataFrame.head())
    # normalized_df=(normalized_df-normalized_df.min())/(normalized_df.max()-normalized_df.min())
    polygonSize = 0.02/2
    geoJsonList = []
    # print(normalized_df.head())
    for index,row in dataFrame.iterrows():
        # feature = Feature(geometry=Point((row['long'], row['lat'])), properties={"elevation":row["COR.LEVEL"]})
        feature = Feature(geometry=Polygon([[[row['long']-polygonSize, row['lat']-polygonSize],[row['long']-polygonSize, row['lat']+polygonSize],[row['long']+polygonSize, row['lat']+polygonSize],[row['long']+polygonSize, row['lat']-polygonSize]]]), 
        properties={"elevation": row["COR.LEVEL"], "normalizedElevation": row["normalizedCor"]
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
    
    sess = Session(username,password, host, db='CENTRAL')
    data = create_geo_json(19900100,sess)
    
    INITIAL_VIEW_STATE = pydeck.ViewState(latitude=-24.654950, longitude=29.3906515, zoom=7, max_zoom=16, pitch=45, bearing=0)

    geojson = pydeck.Layer(
        "GeoJsonLayer",
        data = data,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="elevation*150000",
        get_radius=1000, 
        get_fill_color="[255 ,100, normalizedElevation * 255, 255]", 
        get_line_color=[255, 255, 255],
    )


    r = pydeck.Deck(mapbox_key=mapbox_api_key, layers=[ geojson], initial_view_state=INITIAL_VIEW_STATE)

    r.to_html("geojson_layer.html")