import pandas as pd
from cssaw_central.Session import Session

def get_dam_levels(startDate, endDate, session, province, river):
    # lookup table of provinces
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
    if provinces.get(province) == None and province not in provinces.values():
        raise ValueError("Invalid province argument")

    # changes the province to its full name if it is not already
    if provinces.get(province) != None:
        province = provinces[province]

    # makes sure that the river ends with river
    if not river.endswith(" River"):
        river = river + " River"

    table = "Norm" + province + "Dams"

    query = "SELECT * FROM CENTRAL." + table + " WHERE River = '" + river + "' AND Date >= " + startDate + " AND Date <= " + endDate

    return session.execute_query(query, pandas=True) 
