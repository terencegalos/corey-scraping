import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator

class Scraper1:
    def __init__(self):
        self.url = 'https://mobilendloan.com/'
        self.table_name = "scraped_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'wc_visitor=78875-0d7b6431-042c-e488-c1aa-48cb92e0d053; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-0d7b6431-042c-e488-c1aa-48cb92e0d053+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-0d7b6431-042c-e488-c1aa-48cb92e0d053+..+; mailer-sessions=s%3AuP5KD1GHwy-tFfXJEr-eKCMABYK9B4WN.6wd4DsxqmiRz9FnQMfmYw4H2Cf7Awupx3LpA0W%2BhIrs'
        print(f"Scraping: {self.url}")
        
    
    
    
    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Languffage': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.extracted_cookies,
            'Host': 'mobilendloan.com',
            'Origin': 'https://mobilendloan.com',
            'Referer': 'https://mobilendloan.com/',
            'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }


                
        response = self.session.post(url, headers=headers, data=data, allow_redirects=True)
        # print(response.text)
        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.select_one("#firstName")['value'] if soup.select_one("#firstName") else None
        last_name_el = soup.select_one("#lastName")['value'] if soup.select_one("#lastName") else None
        address_el = soup.select_one("#address")['value'] if soup.select_one("#address")['value'] else None
        city_el = soup.select_one("#city")['value'] if soup.select_one("#city")['value'] else None
        try:
            state_el = soup.select("#state option[selected]")[1].text
        except IndexError:
            state_el = None
        zip_code_el = soup.select_one("#zipCode")['value'] if soup.select_one("#zipCode") else None
        
    
        
        
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el, last_name_el, address_el, city_el, state_el, zip_code_el]):
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
    
    
    
    
    def scrape_with_refcodes(self,batch_size=100,num_threads=3):

            
        refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        # refcodes = code_generator.generate_code(728110,900000,'HA')
        print(f"There are {len(refcodes)} refcodes to rotate!")
        # results = []
        
        def scrape_single_thread(refcode):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            result = self.scrape_single(self.url,data)
            print(result)
            if result is None:
                print("Skipping 'None' values.")
            return result
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i in range(0,len(refcodes),batch_size):
                batch_results = [result for result in list(executor.map(scrape_single_thread,refcodes[i:i+batch_size])) if result is not None]
                yield batch_results