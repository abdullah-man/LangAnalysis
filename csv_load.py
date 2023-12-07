
# from langchain.document_loaders import UnstructuredExcelLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import UnstructuredCSVLoader


import os

# OpenAPI Key
os.environ['OPENAI_API_KEY'] = "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"

# Data Path
csv_folder_path = f'data/'
files = os.listdir(csv_folder_path)

# Excel Loader
loaders = [UnstructuredCSVLoader(os.path.join(csv_folder_path, fn)) for fn in os.listdir(csv_folder_path)]
print(loaders)
from langchain.vectorstores.utils import filter_complex_metadata

# Vector Store Creation
index = VectorstoreIndexCreator().from_loaders(loaders)

# Query
answer = index.query("How many records have Pais value Honduras?")
print("Answer from Excel File: \n", answer)

