import pandas as pd
from cssaw_central.Session import Session

def get_dam_levels(startDate, endDate, session, river, province=None):
    # lookup table of provinces
    # NOTE: it is not recommended to get specific province data since each province's data is not normalized across all provinces
    # this is only here for legacy purposes
    provinces = {"EC":"EasternCape",
                "FS":"FreeState",
                "G":"Gauteng",
                "KN":"KwaZuluNatal",
                "LP":"Limpopo",
                "M":"Mpumalanga",
                "NC":"NorthernCape",
                "NW":"NorthWest",
                "WC":"WesternCape"}

    # check that the province exists in the dictionary
    if province != None and provinces.get(province) == None and province not in provinces.values():
        raise ValueError("Invalid province argument")

    # changes the province to its full name if it is not already
    if province != None and provinces.get(province) != None:
        province = provinces[province]

    # makes sure that the river ends with river
    if not river.endswith(" River"):
        river = river + " River"

    query = "SELECT Date, Dam, River, FSC, This_Week, Last_Week, Last_Year FROM CENTRAL."

    if province != None:
        table = "Norm" + province + "Dams"

        query = query + table + " WHERE River = '" + river + "' AND Date >= " + startDate + " AND Date <= " + endDate
    else:
        query = query + "NormAllDams WHERE River = '" + river + "' AND Date >= " + startDate + " AND Date <= " + endDate

    return session.execute_query(query, pandas=True) 
