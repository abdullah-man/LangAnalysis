# from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.indexes import VectorstoreIndexCreator

import os


# OpenAPI Key
os.environ['OPENAI_API_KEY'] = "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"

# Data Path
excel_folder_path = f'data/'
files = os.listdir(excel_folder_path)

# Excel Loader
loaders = [UnstructuredExcelLoader(os.path.join(excel_folder_path, fn), mode='elements') for fn in os.listdir(excel_folder_path)]
print(loaders)

# Vector Store Creation
index = VectorstoreIndexCreator().from_loaders(loaders)

# Query
answer = index.query("How many records have Pais value Honduras?")
print("Answer from Excel File: \n", answer)

