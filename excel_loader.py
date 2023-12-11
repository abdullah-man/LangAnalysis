"""
This file contains code to load excel files and save them as csv files
"""

from typing import List
import pandas as pd


def load_excel(excel_file) -> dict | None:
    """
    Loads excel sheet by sheet in dataframes and return the list of dataframes
    params:
        excel_file : Excel file
    returns:
        Dictionary : Contains lists of dataframes and sheet names that could not be opened
        None : If Excel file could not be opened.               
    """
    dataframes = list()
    error_sheets = list()
    try:
        loaded_excel = pd.read_excel(excel_file, sheet_name=None)
        sheet_names = list(loaded_excel.keys())
        # loading each sheet one by one as pandas Dataframe
        for sheet in sheet_names:
            try:
                dataframes.append(pd.read_excel(excel_file, sheet_name=sheet))
            except Exception as e:
                error_sheets.append(sheet)
                continue
        return {'dataframes' : dataframes, 'error_sheets' : error_sheets}
    
    except Exception as e:
        return None
        
