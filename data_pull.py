"""
Pull all data from cloud to local

The function will create and return a dataframe. The script 
saves that dataframe to a csv.
"""

from data.dwa_getter import *
from data.dam_getter import get_dam_levels
from data.grace_gracefo_getter import get_lwe_byRange
from data.saws_getter import get_monthly_saws_data

def cloud_to_df():
    """[summary]

    Args:
        conn (Session): CSSAW-Central connection to use
    """
    # Collect data using getters
    dwa_df = runDWA()
    print(dwa_df)