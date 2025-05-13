from datetime import datetime
import streamlit as st
from IntenShalla_Scraper import main
import pandas as pd
st.set_page_config(
    page_title="Scrapper",
    layout='centered'
)
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