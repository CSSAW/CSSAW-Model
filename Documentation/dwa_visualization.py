import pydeck
from geojson import Feature, Point, FeatureCollection
from cssaw_central.Session import Session
# Some c
def create_geo_json(date, sess):

    tableName = '`dwa-primary`'
    query = "SELECT * from Test." + tableName \
         + " WHERE `DATE` > " + (str)(date) \
         + " AND `DATE` <= " + (str)(date + 31) 
         
    dataFrame = sess.execute_query(query, pandas=True)
    dataFrame = dataFrame.drop("TIME", axis='columns')
    dataFrame = dataFrame.drop("QUA", axis='columns')
    dataFrame = dataFrame.drop("QUA.1", axis='columns')
    dataFrame = dataFrame.drop("id", axis='columns')
    sess.conn.close()

    # dataFrame = dataFrame.drop("date", axis='columns')
    # The line below gets rid of the Day portion of the Date column,
    # it is used in the groupby to return monthly data. 
    # dataFrame["DATE"] = dataFrame["DATE"].apply(lambda x: (int)(x / 100))
    print(dataFrame.head())

    dataFrame = dataFrame.groupby("station").mean()
    print(dataFrame.head())
    
    geoJsonList = []
    for index,row in dataFrame.iterrows():
        feature = Feature(geometry=Point((row['long'], row['lat'])), properties={"elevation":row["COR.LEVEL"]*50000})
        geoJsonList.append(feature)

    featureCollection = FeatureCollection(geoJsonList)
    print(featureCollection)
    return featureCollection

if __name__ == "__main__":
    credentials = open('../credentials.txt', 'r')
    username = credentials.readline().replace('\n','')
    password = credentials.readline().replace('\n','')
    host = credentials.readline().replace('\n','')
    mapbox_api_key = credentials.readline().replace('\n','')
    credentials.close()
    
    sess = Session(username,password, host, db='Test')
    # DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
    data = create_geo_json(19050100,sess)
    
    LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]

    INITIAL_VIEW_STATE = pydeck.ViewState(latitude=-24.654950, longitude=29.3906515, zoom=7, max_zoom=16, pitch=45, bearing=0)

    # polygon = pydeck.Layer(
    #     "PolygonLayer",
    #     LAND_COVER,
    #     stroked=False,
    #     # processes the data as a flat longitude-latitude pair
    #     get_polygon="-",
    #     get_fill_color=[255, 0, 0, 20],
    # )

    geojson = pydeck.Layer(
        "GeoJsonLayer",
        data = data,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        # get_elevation='properties.corlevel * 20',
         elevation_range=[0, 3000],
         elevation_scale=50,
        get_radius=1000, 
        get_fill_color=[255, 0, 10, 255], 
        get_line_color=[255, 255, 255],
    )

    r = pydeck.Deck(layers=[ geojson], initial_view_state=INITIAL_VIEW_STATE)

    r.to_html("geojson_layer.html")
