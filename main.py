import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_custom_model
import pandas as pd

samples={
        'https://www.scrapethissite.com/pages/simple/':'Get the name of Country,Capital,Population and area',
        'https://quotes.toscrape.com/':'Get all the quotes,tags and author names',
        'https://books.toscrape.com/':'Get the book title,price and is available in stock or not',
        'https://webscraper.io/test-sites/e-commerce/allinone':'Get the product name,price and description',
        }

# Streamlit UI
st.set_page_config(page_title="AI Web Scraper", page_icon=":mag_right:")
st.title("AI Web Scraper")

selection=''
if st.toggle('Get Sample'):
    selection = int(st.selectbox('Select a sample website to scrape', list(f"Sample {i}" for i in range(1, len(samples)+1)), format_func=lambda x: f"Sample {x.split()[-1]}").split(' ')[-1])

# print(list(samples.keys())[selection-1])
url = st.text_input("Enter Website URL",value=list(samples.keys())[selection-1] if selection else '', placeholder="https://example.com")


# Step 1: Scrape the Website
scrape=st.button("Scrape Website")
if scrape:
    if url:
        # st.write("Scraping the website...")
        with st.spinner("Scraping in progress..."):
            page_source = scrape_website(url)
            body_content = extract_body_content(page_source) 
            clean_content = clean_body_content(body_content)
            
            st.session_state.dom_content = clean_content
        if page_source:
            st.success("Website scraped successfully!")
            with st.expander("View Screenshot"):
                st.image('screenshot.png', caption='Screenshot of the website')
            with st.expander("View Cleaned Content"):
                st.text_area("Cleaned Content", value=clean_content, height=300)
        else:
            st.error("Failed to scrape the website. Please check the URL or your internet connection.")
    else:
        st.error("Please enter a valid URL.")       
        
if 'dom_content' in st.session_state:
    
    parse_desription = st.text_area("Describe what you want to extract from the content",value=list(samples.values())[selection-1] if selection else "") +"\n get data in csv format"
    
    if st.button("Parse Content"):
        if parse_desription:
            with st.spinner("Parsing in progress..."):
                
                dom_chunks = split_dom_content(st.session_state.dom_content)
                
                parse_with_custom_model(dom_chunks, parse_desription)
                df = pd.read_csv('parsed_output.csv',sep=';:;', engine='python')
                st.dataframe(df)
                st.download_button(
                    label="Download Parsed CSV",
                    data=df.to_csv(sep=';:;', index=False).encode('utf-8'),
                    file_name='parsed_output.csv',
                    mime='text/csv',
                )
                
                
                
        