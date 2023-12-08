"""
This file contains code to load excel files and save them as csv files
"""
from typing import List
import pandas as pd


def load_excel(excel_file) -> List:
    """
    Loads excel sheet by sheet in dataframes and return the list of dataframes
    params:
        excel_file : Excel file
    returns:
        List of pandas dataframe objects
    """
    dataframes = list()
    try:
        loaded_excel = pd.read_excel(excel_file, sheet_name=None)
        sheet_names = list(loaded_excel.keys())
        # loading each sheet one by one as pandas Dataframe
        for sheet in sheet_names:
            try:
                dataframes.append(pd.read_excel(excel_file, sheet_name=sheet))
            except Exception as e:
                print(f"Sheet name {sheet} could not be opened")
                continue
        return dataframes
     
    except Exception as e:
        print(f"Excel file {excel_file} could not be opened.")
        return None
