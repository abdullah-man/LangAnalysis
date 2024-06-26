from excel_loader import load_excel
from pandas_agnt import create_agent, ask_agent

import streamlit as st

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

# Main content
st.title(selected_section)

# Setting API_KEY_SET as session variables to be accessed and set globally in streamlit application 
if ('API_KEY_SET' and 'API_BOOL' and 'Uploaded' and 'ALL_DF' and 'Erro_SHT') not in st.session_state: 
    st.session_state['API_KEY_SET'] = ""
    st.session_state['API_BOOL'] = False
    st.session_state['Uploaded'] = False
    st.session_state['ALL_DF'] = list()
    st.session_state['Erro_SHT'] = list()


# --------------------- SECTION : Set API Key ---------------------

if (selected_section == "Set API Key"):
    
    # Case : if API key already set
    if st.session_state['API_BOOL']:
        st.success(f"API Key set successfully as {st.session_state['API_KEY_SET']}")
    
    api_key = st.text_input("Enter API Key:", type="password")
    # Case : if API key not already set
    if st.button("Submit"):
        # if a value is entered as API key and it starts with sk- then:
        if api_key:
            if api_key.startswith('sk-'): 
                st.session_state['API_KEY_SET'] = api_key
                st.session_state['API_BOOL'] = True
                st.success(f"API Key set successfully as {st.session_state['API_KEY_SET']}")
        
        # if it is empty or does not start with sk- then:
        else:
            st.error("Please enter a valid API Key.")
            st.error(f"Please try again. You entered: {api_key}")
    
    
# --------------------- SECTION : Upload Files ---------------------

# if API Key already set then open this section
if (selected_section == "Upload Files") and (st.session_state['API_BOOL'] is True):     
    uploaded_files = st.file_uploader("Select multiple files:", type=["xlsx"], accept_multiple_files=True)
    
    if uploaded_files: # if uploaded_files contain any file then
        st.write("Selected Files:")
        for file in uploaded_files:
            st.write(file.name)

        
        if st.button("Upload"): # if Upload button is clicked
            with st.spinner("Uploading files..."):
                uploaded_files_names = [file.name for file in uploaded_files]
                # uploaded_files_paths = [file.getvalue() for file in uploaded_files]
                
            # --- Loading Excel files as Pandas dataframe objects ---

            for file in uploaded_files: 
                
                load_response = load_excel(excel_file=file)

                # case 1 : successfull file load
                if isinstance(load_response, dict):
                    sheets = load_response['dataframes']
                    st.session_state['ALL_DF'] = st.session_state['ALL_DF'] + sheets

                    # Handling Error Sheets
                    # error_sheets = load_response['error_sheets']
                    # if len(error_sheets)>0: # if error_sheets list contains info
                    #     st.session_state['Erro_SHT'].append({file.name : error_sheets})
                    
                    st.success(f"File {file.name} successfully opened.")
                
                # case 2 : failed to load the entire file
                if load_response is None:
                    st.error(f"File {file.name} could not be opened.")


    # Displaying list of error sheets
    # if len(st.session_state['Erro_SHT']) > 0:
    #     st.write("These sheets in files have problem opening:")
    #     st.write(str(st.session_state['Erro_SHT']))

    # Setting Uploaded to True if any dataframe was added to st.session_state['ALL_DF'] varibale
    # This means now we can perform queries on this dataframe
    if len(st.session_state['ALL_DF']) > 0: # if this list contain any dataframe then:
        st.session_state['Uploaded'] = True
        st.success("Files Uploaded and Opened Successfully!")
    
        # displaying data for checking
        for df in st.session_state['ALL_DF']:
            st.dataframe(df, use_container_width=True)


# --------------------- SECTION : Ask Queries / Chat ---------------------

# if Files already uploaded then open this section
if (selected_section == "Ask Query") and (st.session_state['Uploaded'] is True): 
    
    def clear_text():
        """
        Inner function to reset the text appearing in the input_text field
        """
        st.session_state["input"] = ""

    # Chat Agent Creation
    pd_agent = create_agent(dataframes_list=st.session_state['ALL_DF'], API_KEY=st.session_state['API_KEY_SET'], hallucination=0.0)    
    
    # Ask questions / chat
    input_text = st.text_area("Enter the query", key='input')
    
    col_1, col_2, col_3, col_4 = st.columns(4) # making additional 2 columns to make the two buttons appear close to each other

    if col_1.button("Ask from data"):
        if input_text:
            st.info("Your Query: "+ input_text)

            # asking agent
            with st.spinner('Thinking ...'):
                response = ask_agent(agent=pd_agent, query=input_text)
                st.success(response)
    
    if col_2.button("Clear Text", on_click=clear_text):
        pass
