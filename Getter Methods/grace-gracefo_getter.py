import pandas as pd
from cssaw_central.Session import Session


def get_lwe_byRange(startDate, endDate, session, bbox = None):
  '''
  @param startDate (YYYYMMDD)
  @param endDate (YYYYMMDD)
  @param session (cssaw_central.Session)
  @param bbox (A list of coordinates to bound regional date [lat_max, lon_max, lat_min, lon_min])
  Returns a pandas dataframe with land water equivalent thickness data
  within the specified range
  '''

  table = "lwe_data"
  query = "SELECT * FROM CENTRAL." + table \
          + " WHERE 'Date' >= " + startDate \
          + " AND 'Date' <= " + endDate
  if bbox != None and len(bbox) == 4:
    query += " AND 'Latitude' >= " + bbox[2] \
           + " AND 'Latitude' <= " + bbox[0] \
           + " AND 'Longitude' >= " + bbox[3] \
           + " AND 'Longitude' <= " + bbox[1]
  print(query)
  return session.execute_query(query, pandas = True)


if __name__ == "__main__":
  credential = open("credentials.txt", "r").readlines()
  print(credential)
  userName = credential[0].replace("\n", "")
  passWord = credential[1].replace("\n", "")
  host = credential[2].replace("\n", "")
  print(userName, passWord, host)
  try:
    session = Session(userName, passWord, host, db = "CENTRAL")
    print("Database connection successful")
  except:
    print("Connection error")
  
  bbox = ['-25.5', '25.5', '-30.5', '30.5']
  data = get_lwe_byRange("20020101", "20030101", session)
  date_2 = get_lwe_byRange("20020101", "20030101", session, bbox)
