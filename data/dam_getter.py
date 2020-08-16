import pandas as pd
from cssaw_central.Session import Session

def get_dam_levels_river(startDate, endDate, session, river):
    query = "SELECT * FROM CENTRAL.NormAllDams WHERE River = '" + river
    query = query + "' AND Date >= " + str(startDate) + " AND Date <= " + str(endDate)

    return session.execute_query(query, pandas=True) 

def get_dam_levels_coords(startDate, endDate, session, lat1, lat2, lon1, lon2):
    # return dam levels such that each entry's location is lat1 <= x <= lat2 and lon1 <= x <= lon2
    query = "SELECT * FROM CENTRAL.NormAllDams WHERE Date >= " + str(startDate) + " AND Date <= " + str(endDate)
    query = query + " AND Latitude >= " + str(lat1) + " AND Latitude <= " + str(lat2) + " AND Longitude >= " + str(lon1) + " AND Longitude <= " + str(lon2)

    return session.execute_query(query, pandas=True) 
