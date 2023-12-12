import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator

class Scraper47:
    def __init__(self):
        self.url = 'https://fundingpronto.com'
        self.table_name = "scraper47_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
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
        first_name_el = soup.find(attrs={'name':'primaryOwnerFirstName'})['value'] if soup.find(attrs={'name':'primaryOwnerFirstName'}) else None
        last_name_el = soup.find(attrs={'name':'primaryOwnerLastName'})['value'] if soup.find(attrs={'name':'primaryOwnerLastName'}) else None
        business_el = soup.find(attrs={'name':'businessLegalName'})['value'] if soup.find(attrs={'name':'businessLegalName'}) else None
        email_el = soup.find(attrs={'name':'primaryOwnerEmail'})['value'] if soup.find(attrs={'name':'primaryOwnerEmail'}) else None
        phone_el = soup.find(attrs={'name':'primaryOwnerMobile'})['value'] if soup.find(attrs={'name':'primaryOwnerMobile'}) else None
        rev_el = soup.find(attrs={'name':'annualBusinessRevenue'})['value'] if soup.find(attrs={'name':'annualBusinessRevenue'}) else None
        # try:
        #     state_el = soup.select("#state option[selected]")[1].text
        # except IndexError:
        #     state_el = None
        # zip_code_el = soup.select_one("#zipCode")['value'] if soup.select_one("#zipCode") else None
        
    
        
        
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el, last_name_el, business_el, email_el, phone_el, rev_el]):
            return None        
            
            
        # Return the scraped data as dictionary        
        return {
            'first_name' : first_name_el,
            'last_name' : last_name_el,
            'business' : business_el,
            'email' : email_el,
            'phone' : phone_el,
            'rev' : rev_el
        }
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self,batch_size=10,num_threads=3):

            
        # refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        pmfid = code_generator.generate_code(1,200000000,'FP',9)
        print(f"There are {len(pmfid)} pmfid to rotate!")
        # results = []
        
        def scrape_single_thread(pmfid):
            print(f"pmfid : {pmfid}")
            data = {'pmfid':pmfid}
            result = self.scrape_single(self.url,data)
            print(result)
            if result is None:
                print("Skipping 'None' values.")
            return result
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i in range(0,len(pmfid),batch_size):
                batch_results = [result for result in list(executor.map(scrape_single_thread,pmfid[i:i+batch_size])) if result is not None]
                yield batch_results