import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

def scrape_website(website_url):
    # service= Service(executable_path='chromedriver')  
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--window-size=1920,1080')  # Set a default window size
    options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
    options.add_argument('--allow-running-insecure-content')  # Allow insecure content
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(website_url)
        driver.save_screenshot('screenshot.png')  
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()   
        
def extract_body_content(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):   
        script_or_style.decompose()
    clean_content = soup.get_text(separator='\n', strip=True).splitlines()
    # print("Cleaned content length:", len(clean_content))
    clean_content='\n'.join(content.strip() for content in clean_content if content.strip())
    return clean_content

def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]