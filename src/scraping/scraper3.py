import requests, time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraping import code_generator

class Scraper3:
    def __init__(self):
        print("***Scraping xmydebt.com")
        self.url = 'https://xmydebt.com/'
        self.br = self.get_browser()
        # self.url = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
    
    
    def scrape_single(self,url,data):
        
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Cookie": "_ga_BVE2LD5W7L=GS1.1.1700129947.1.0.1700129947.0.0.0; _ga=GA1.1.1067707445.1700129947; _wpfuj={\"1700129947\":\"https%3A%2F%2Fxmydebt.com%2F%7C%23%7CX%20My%20Debt%7C%23%7C4291\"}; _wpfuuid=fdf05fe9-ff91-484c-85da-57187b32940c",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }


                
        
        # response = requests.post(url, headers=headers, data=data, allow_redirects=True)
        # print(response.text)
        
        # Go to url using selenium browser automation
        self.br.get(url)
        time.sleep(0.5)
        
        # Enter code
        self.br.find_element(By.NAME,"wpforms[fields][1]").send_keys(data['refCode'])
        self.br.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
        time.sleep(0.5)
        
        # print(self.br.page_source)
        
        # Wait for the page with info to load
        WebDriverWait(self.br,5).until(EC.visibility_of_element_located((By.NAME,"wpforms[fields][1][first]")))
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        
        soup = BeautifulSoup(self.br.page_source, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'wpforms[fields][1][first]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][first]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][first]'}).attrs  else None
        last_name_el = soup.find(attrs={'name':'wpforms[fields][1][last]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][last]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][last]'}).attrs else None
        address_el = soup.find(attrs={'name':'wpforms[fields][4][address1]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][address1]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][address1]'}).attrs else None
        city_el = soup.find(attrs={'name':'wpforms[fields][4][city]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][city]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][city]'}).attrs else None
        state_el = soup.select('select[name="wpforms[fields][4][state]"] option[selected]')[1].text if len(soup.select('select[name="wpforms[fields][4][state]"] option[selected]')) > 1 else None
        zip_code_el = soup.find(attrs={"name":"wpforms[fields][4][postal]"})['value'] if 'value' in soup.find(attrs={"name":"wpforms[fields][4][postal]"}).attrs else None
        
        # if first_name_el is not None:
        #     first_name = first_name_el
        # else:
        #     first_name = 'NA'
            
        # if last_name_el is not None:
        #     last_name = last_name_el
        # else:
        #     last_name = 'NA'
        
        # if address_el is not None:
        #     address = address_el
        # else:
        #     address = 'NA'
            
        # if city_el is not None:
        #     city = city_el
        # else:
        #     city = 'NA'
            
        # if state_el is not None:
        #     state = state_el
        # else:
        #     state = 'NA'
        
        # if zip_code_el is not None:
        #     zip_code = zip_code_el
        # else:
        #     zip_code = 'NA'
        
        
        
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el,last_name_el,address_el,city_el,state_el,zip_code_el]):
            return None
        
        
        # Return the scraped data as dictionary        
        return {
            'first_name' : first_name_el,
            'last_name' : last_name_el,
            'address' : address_el,
            'city' : city_el,
            'state' : state_el,
            'zip_code' : zip_code_el
        }
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    def scrape_with_refcodes(self,batch_size=100):
        # with open(refcodes_file,'r') as file:
        #     refcodes = [line.strip() for line in file]
            
        refcodes = self.generate_code(8,20000)
        print(f"There are {len(refcodes)} refcodes to rotate!")
        results = []
        
        for i,refcode in enumerate(refcodes,start=1):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            time.sleep(0.3)
            result = self.scrape_single(self.url,data)
            print(result)
            if result is not None:
                results.append(result)
            else:
                print("Skipping 'None' values")
                
            # Yield results in batches
            if i % batch_size == 0:
                yield results
                results = [] # clear the results list after yielding
            
        # Yield any remaining results
        if result:
            yield results
    
    
    # Use selenium browser automation
    def get_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,924")
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"')

        browser = webdriver.Chrome(options=chrome_options)
        return browser