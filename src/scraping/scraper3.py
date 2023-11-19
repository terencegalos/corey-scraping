import requests, time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.br.find_element(By.NAME,"wpforms[fields][1]").send_keys(Keys.ENTER)
        time.sleep(0.5)
        
        # Wait for the page with info to load
        WebDriverWait(self.br,5).until(EC.presence_of_element_located((By.NAME,"wpforms[fields][1][first]")))
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        
        soup = BeautifulSoup(self.br.page_source, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'wpforms[fields][1][first]'})['value']
        last_name_el = soup.find(attrs={'name':'wpforms[fields][1][last]'})['value']
        address_el = soup.find(attrs={'name':'wpforms[fields][4][address1]'})['value']
        city_el = soup.find(attrs={'name':'wpforms[fields][4][city]'})['value']
        try:
            state_el = soup.select('select[name="wpforms[fields][4][state]"] option[selected]')[1].text
        except:
            state_el = 'not indicated'
        zip_code_el = soup.select_one("#zipCode")['value']
        
        if first_name_el is not None:
            first_name = first_name_el
        else:
            first_name = 'NA'
            
        if last_name_el is not None:
            last_name = last_name_el
        else:
            last_name = 'NA'
        
        if address_el is not None:
            address = address_el
        else:
            address = 'NA'
            
        if city_el is not None:
            city = city_el
        else:
            city = 'NA'
            
        if state_el is not None:
            state = state_el
        else:
            state = 'NA'
        
        if zip_code_el is not None:
            zip_code = zip_code_el
        else:
            zip_code = 'NA'
        
        
        
        # Return the scraped data as dictionary
        
        return {
            'first_name' : first_name,
            'last_name' : last_name,
            'address' : address,
            'city' : city,
            'state' : state,
            'zip_code' : zip_code
        }
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    def scrape_with_refcodes(self,batch_size=100):
        # with open(refcodes_file,'r') as file:
        #     refcodes = [line.strip() for line in file]
            
        refcodes = self.generate_code(1,20000)
        print(f"There are {len(refcodes)} refcodes to rotate!")
        results = []
        
        for i,refcode in enumerate(refcodes,start=1):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            time.sleep(0.5)
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
    
    # Generate code
    def generate_code(self,start,end):
        codes = []
        
        for num in range(start, end+1):
            # Generate zero-padded numeric component
            numeric_component = f"{num:07d}"
            
            # Create the invite code by combining the prefix "HA" and the numeric component
            invite_code = f"RD{numeric_component}"
            
            codes.append(invite_code)
            
        return codes
    
    
    # Use selenium browser automation
    def get_browser(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

        browser = webdriver.Chrome(options=chrome_options)
        return browser