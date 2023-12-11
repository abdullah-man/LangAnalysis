import pandas as pd
import os
from excel_loader import load_excel
from pandas_agnt import create_agent, ask_agent

import streamlit as st
from langchain.llms import OpenAI
from key import save_api_key, read_api_key

# OpenAPI Key
OPENAI_API_KEY = "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"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY 

# KEY_SET = False

# ------ WORK ------
# 1 Test the refactored code from excel-loader and pandas-agent                                 DONE
# 2 Integrate this code into streamlit and test                                                 
# 3 Refactor the streamlit code into functions and implement key persistance for the session
# 4 Build creation using PyInstaller 
# 5 Build creation on windows platform
# ------------------

# 1 
excel_folder_path = "excel_data"
exel_files = [os.path.join(excel_folder_path, fn) for fn in os.listdir(excel_folder_path)]
print(exel_files)

ALL_DF = list()
ALL_ERROR = dict()

for file in exel_files:
    loaded_dict = load_excel(file)
    dataframes = loaded_dict['dataframes']
    ALL_DF = ALL_DF + dataframes

    error_sheets = loaded_dict['error_sheets']
    ALL_ERROR[file] = error_sheets

for key in ALL_ERROR.keys():
    print(key,'\n',ALL_ERROR[key])

for df in ALL_DF:
    print(df.info())

# No Error - ALL Excel Files Loaded, Successfully Tested

# agent creation and QA
OPENAI_API_KEY = "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"
pd_agent = create_agent(dataframes_list=ALL_DF, API_KEY=OPENAI_API_KEY, hallucination=0.0)


while True:
    query = input("Enter Query: ")
    if query=='q':
        break
    else:
        response = ask_agent(agent=pd_agent, query=query)
        print(response)



# No Error - Agent Working