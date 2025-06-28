from datetime import datetime
import streamlit as st
import os
from IntenShalla_Scraper import main
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(
    page_title="Scrapper",
    layout='centered'
)
with st.sidebar:
    selection = option_menu(
        menu_title="Menu",                      # Title of the menu
        options=["Home", "Download Previous File", "About Project"],  # Menu options
        icons=["house", "filetype-csv", "file-earmark-person-fill"],  # Optional icons (from FontAwesome)
        menu_icon="list",                      # Main menu icon
        default_index=1,                       # Default selected item
        orientation="vertical",                # Options: "horizontal" or "vertical"
    )
    
if selection=='Home':
    st.title("Intenshalla Internship And Job Scrapper")

    # st.write("Job Name")
    job_name=st.text_input("👔 Job Name",placeholder='Enter the Job You Want To Scrap',icon='💼')
    limit=int(st.number_input("No. Of Pages to Scrape",1,value=1,icon='📄'))
    if st.button("Begin Scraping",type='secondary',icon='🔎'):
        if job_name:
            date = datetime.now().strftime("%d_%m_%Y")
            output_file=f"files/{job_name}_{date}.csv"
            main(job_name,output_file,limit)
            st.success("Scraped the Data Scuccessfully")
            df=pd.read_csv(output_file)
            st.download_button('Dowmload CSV',data=df.to_csv(index=False),mime='text/plain',file_name=output_file)
            with st.expander("View Data"):
                st.write(df)
        else:
            st.warning("Please Enter Job Name")
elif selection=='Download Previous File':
    st.title("Download Previous Scraped Files")
    os.makedirs("files",exist_ok=True)
    
    files_list=os.listdir('files/')
    file = st.selectbox("☰ Select a file to download", files_list)

    df = pd.read_csv(f'files/{file}')
    with st.expander("View Data",icon='👀'):
        st.write(df)
    
    st.download_button('Download CSV',data=df.to_csv(index=False),mime='text/plain',file_name=file,icon='⬇️')
    # czxczx