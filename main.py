from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import UnstructuredCSVLoader

from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import OpenAI

import pandas as pd
import os


# OpenAPI Key
OPENAI_API_KEY = "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"
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY 

# Data Path
csv_folder_path = f'data/'
files = os.listdir(csv_folder_path)

# CSV Loader
# loaders = [UnstructuredCSVLoader(os.path.join(csv_folder_path, fn)) for fn in os.listdir(csv_folder_path)]
# print(loaders)
# from langchain.vectorstores.utils import filter_complex_metadata

# # Vector Store Creation
# index = VectorstoreIndexCreator().from_loaders(loaders)

# # Query
# answer = index.query("How many records have Pais value Honduras?")
# print("Answer from Excel File: \n", answer)


# pandas agent
csv_files = [os.path.join(csv_folder_path, fn) for fn in os.listdir(csv_folder_path)]
# print(csv_files)

csv_dataframes = []
for csv in csv_files:
    csv_dataframes.append(pd.read_csv(csv))

agent = create_pandas_dataframe_agent(OpenAI(temperature=0), csv_dataframes, verbose=True)
agent.run("how many times El Salvador appears in Pais column in all the data?")

