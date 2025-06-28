from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.chrome.options import Options
import random
import time
from bs4 import BeautifulSoup
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import logging
import pickle
from concurrent.futures import ThreadPoolExecutor
#creating logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@dataclass
class IntenshallaAgentConfig():
    cookies_folder_path = os.path.join(os.getcwd(),'cookies')

    
class IntenshallaAgent():
    
    def __init__(self,driver:webdriver.Chrome):
        self.config = IntenshallaAgentConfig()
        self.driver = driver
        
    def _add_cookies(self):
        """This function is used to add custoum cookies to the driver so that it can autofill username and password and help to bypass the login page in website"""
        
        cookies_list = [cookie for cookie in os.listdir(self.config.cookies_folder_path) if cookie.endswith('.pkl')]

        #using random module to randomly select cookies 
        cookies = random.choice(cookies_list) 
        with open(cookie,'rb') as file:
            cookies = pickle.load(file)
            
        for cookie in cookies:
            if cookie['value']:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    print(cookie)
                    pass
        
    def get_job_cards(self,soup):
        
        all_jobs_cards =  all_job_cards = soup.find('div',{'id':'internship_list_container'}).find_all('div',{'class':'internship_meta duration_meta'})
        
        return all_job_cards
    
    def get_job_data(self,job_card):
        job_title = job_card.find('a',class_='job-title-href').text
        company_name = job_card.find('p', class_='company-name').text.strip()
        job_details = job_card.find('div',{'class':"individual_internship_details"}).find('div',class_='detail-row-1')
        location= job_details.div.span.a.text
        duration = job_details.select('div[class="row-1-item"] span ')[0].text
        stipend =  job_details.select('div[class="row-1-item"] span ')[1].text.split('/')[0]

        return [job_title,company_name,location,duration,stipend]
    
    def close_pop(self):
        #closing pop migth appear
        try:
            self.driver.find_element(By.ID,'close_popup').click()
        except:
            pass
        
    
    def create_dataframe(self,data_list):
        df = pd.DataFrame(data_list,columns=['Title',"Company's Name","Location",'Duration',"Stipend"])
        return df
    def job_agent(self,job_name,output_file,limit):
        
        self.driver.get('https://internshala.com/')
        time.sleep(2)
        
        #not using cookie right now 
        # self._add_cookies()
        # time.sleep(1)
        
        #find search box and entering job_name 
        search_box = self.driver.find_element(By.CLASS_NAME,'search-cta')
        search_box.click()
        time.sleep(2)
        search = self.driver.find_element(By.CSS_SELECTOR, '.form-field.dropdown-field.multi-select-chip-field.input-field.search-field')
        search = search.find_element(By.CSS_SELECTOR,'.input-container.with-search')
        search = search.find_element(By.TAG_NAME,'input')
        search.click()
        search.clear()
        search.send_keys(job_name)
        time.sleep(1)
        search.send_keys(Keys.RETURN)
        time.sleep(1)
        
        url = self.driver.current_url.split("?utm")[0]
        print(url)
        
        #getting total pages
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        total_page=soup.find('span',id='total_pages').text

        # print(total_page)
        total_page=int(total_page)
        if limit>total_page:
            limit=total_page
            print(f"There are only {total_page} pages")
        
       
        job_data = []
        
        try:
            for idx in range(limit):
                page_url = f"{url}page-{idx+1}/"
                self.close_pop()
                self.driver.get(page_url)
                
                #creating soup object
                soup = BeautifulSoup(self.driver.page_source,'html.parser')
                all_jobs_cards = self.get_job_cards(soup)
                
                #using thread to increase the efficiency of scrapper
                with ThreadPoolExecutor(max_workers=5) as executor:
                    data = list(executor.map(self.get_job_data,all_jobs_cards))
                    
                # print(data)
                # print(len(data))
                job_data.extend(data)
            print(len(job_data))   
            df = self.create_dataframe(job_data)
            df.to_csv(output_file,index=False)            
                
                
        except:
            print("All Pages are Loaded")
        self.driver.save_screenshot('4.png')
        
        
            
        
        
        
def main(job_name,output_file,limit=1):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver (Ensure you have the correct WebDriver installed)
    driver = webdriver.Chrome(options=options)
    obj = IntenshallaAgent(driver)
    obj.job_agent(job_name,output_file,limit)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True, help="InternShalla search role")
    parser.add_argument('--output', type=str, required=True, help="Output CSV file path")
    parser.add_argument('--limit', type=int, default=1, help="Number of pages to scrape")

    args = parser.parse_args()
    main(args.name, args.output, args.limit)
