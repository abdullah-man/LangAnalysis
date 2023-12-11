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

# setting streamlit app configurations for title and icon
st.set_page_config(
    page_title="ExcelGPT",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Hide streamlit 3dot menu, footer and Deploy link
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Sidebar Sections
# st.sidebar.title("Sections")
selected_section = st.sidebar.radio("Section Selection", ("Set API Key", "Upload Files", "Ask Query"))

# # Main content
st.title(selected_section)

# Data 
all_data_frames = list()
error_sheet_info = dict()

# Setting API_KEY_SET as session variables to be accessed and set globally in streamlit application 
if ('API_KEY_SET' and 'API_BOOL') not in st.session_state: 
    st.session_state['API_KEY_SET'] = ""
    st.session_state['API_BOOL'] = False


# --------------------- SECTION : Set API Key --------------------- 
if (selected_section == "Set API Key"):
    
    # Case : if API key already set
    if st.session_state['API_BOOL']:
        st.success(f"API Key set successfully as {st.session_state['API_KEY_SET']}")
    
    api_key = st.text_input("Enter API Key:")
    # Case : if API key not already set
    if st.button("Submit"):
        # if a value is entered as API key and it starts with sk- then:
        if (api_key) and api_key.startswith('sk-'): 
            st.session_state['API_KEY_SET'] = api_key
            st.session_state['API_BOOL'] = True
            st.success(f"API Key set successfully as {st.session_state['API_KEY_SET']}")
        
        # if it is empty or does not start with sk- then:
        else:
            st.error("Please enter a valid API Key.")
            st.error(f"Please try again. You entered: {api_key}")
    
    
# --------------------- SECTION : Upload Files ---------------------
if selected_section == "Upload Files":
    # st.header("Upload Files")
    uploaded_files = st.file_uploader("Select multiple files:", type=["xlsx"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write("Selected Files:")
        for file in uploaded_files:
            st.write(file.name)

        if st.button("Upload"):
            with st.spinner("Uploading files..."):
                # Simulate file upload process (replace this with actual file processing logic)
                uploaded_files_names = [file.name for file in uploaded_files]
                uploaded_files_paths = [file.getvalue() for file in uploaded_files]
                
                # Loading Excel files as Pandas dataframe objects
                for file in uploaded_files_paths:
                    load_response = load_excel(excel_file=file)
                    # case 1 : successfull file load
                    if isinstance(load_response, dict):
                        sheets = load_response['dataframes']
                        all_data_frames = all_data_frames + sheets

                        # error_sheets = load_response['error_sheets']
                        # error_sheet_info[file] = error_sheets
                    
                    # case 2 : failed file load
                    if load_response is None:
                        st.write(f"File {file} could not be opened.")

        st.write("Selected Files:")
        for file in uploaded_files:
            st.write(file.name)

        if st.button("Upload"):
            with st.spinner("Uploading files..."):
                # Simulate file upload process (replace this with actual file processing logic)
                uploaded_files_names = [file.name for file in uploaded_files]
                uploaded_files_paths = [file.getvalue() for file in uploaded_files]
                
                # Loading Excel files as Pandas dataframe objects
                for file in uploaded_files_paths:
                    load_response = load_excel(excel_file=file)
                    # case 1 : successfull file load
                    if isinstance(load_response, dict):
                        sheets = load_response['dataframes']
                        all_data_frames = all_data_frames + sheets

                        # error_sheets = load_response['error_sheets']
                        # error_sheet_info[file] = error_sheets
                    
                    # case 2 : failed file load
                    if load_response is None:
                        st.write(f"File {file} could not be opened.")

                # st.write(f"These files have these problamatic sheets.")
                # st.write(list(error_sheet_info.items()))
    

            st.success("Files uploaded successfully!")
            st.write("Successfully uploaded files:")
            st.write(uploaded_files_names)


# --------------------- SECTION : Ask Queries / Chat ---------------------
if selected_section == "Ask":
    # st.header("Chat Section")
    user_input = st.text_input("Type your message:")
    chat_messages = st.empty()  # Create an empty container for chat messages

    if st.button("Submit"):
        if user_input:
            # Process user input and generate a response (replace with your logic)
            response = "You said: " + user_input

            # Append user's message and response to chat_messages
            chat_messages.text(f"You: {user_input}")
            chat_messages.text(f"Bot: {response}")
        else:
            st.warning("Please enter a message before submitting.")



# To Run:
# streamlit run main.py --server.maxUploadSize 1000