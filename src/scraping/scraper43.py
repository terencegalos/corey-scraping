import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator

class Scraper43:
    def __init__(self):
        self.url = 'https://smallbusinesschoice.com'
        self.validateform = 'https://www.smallbusinesschoice.com/form_handler/validate'
        self.table_name = "scraper43_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.url}")
        
    
    
    
    def scrape_single(self,url,data):
        
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "www.smallbusinesschoice.com",
            "Connection": "keep-alive",
            "Content-Length": "185",
            # "Content-Type": "multipart/form-data; boundary=---------------------------405174275634778339372685771568",
            # "Cookie": "_gcl_au=1.1.2107904941.1701963805; _ga_Z0XG6WNC0N=GS1.1.1703664016.8.1.1703664214.0.0.0; _ga=GA1.1.1165202017.1701963905",
            "Host": "www.smallbusinesschoice.com",
            "Origin": "https://www.smallbusinesschoice.com",
            "Referer": "https://www.smallbusinesschoice.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        }



                
        response = requests.post(url, data=data, allow_redirects=True)
        # raise for failed requests
        # response.raise_for_status()
        
        if response.status_code == 404:
            print("Code invalid.")
            return
        
        # print(response.text)
        # Parse the HTML content with BeautifulSoup
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print(' '.join(soup.get_text().split()))
        
        # Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'primaryOwnerFirstName'}).get_text() if soup.find(attrs={'name':'primaryOwnerFirstName'}) else None
        last_name_el = soup.find(attrs={'name':'primaryOwnerLastName'}).get_text() if soup.find(attrs={'name':'primaryOwnerLastName'}) else None
        business_el = soup.find(attrs={'name':'businessLegalName'}).get_text() if soup.find(attrs={'name':'businessLegalName'}) else None
        email_el = soup.find(attrs={'name':'primaryOwnerEmail'}).get_text() if soup.find(attrs={'name':'primaryOwnerEmail'}) else None
        phone_el = soup.find(attrs={'name':'primaryOwnerMobile'}).get_text() if soup.find(attrs={'name':'primaryOwnerMobile'}) else None
        rev_el = soup.find(attrs={'name':'annualBusinessRevenue'}).get_text() if soup.find(attrs={'name':'annualBusinessRevenue'}) else None
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
    
    
    
    
    def scrape_with_refcodes(self,batch_size=10,num_threads=5):

            
        # refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        pmfid_generator = code_generator.generate_code_gen(2064,200000000,'SC',9,batch_size)
        # print(f"There are {len(pmfid)} pmfid to rotate!")
        # results = []
        
        def scrape_single_thread(pmfid):
            print(f"pmfid : {pmfid}")
            data = {'pmfId':pmfid}
            result = self.scrape_single(self.url,data)
            print(result)
            if result is None:
                print("Skipping 'None' values.")
            return result
            
        while True:
            try:
                codes =  next(pmfid_generator)
                print(codes)
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                    # for i in range(0,len(pmfid),batch_size):
                    batch_results = [result for result in list(executor.map(scrape_single_thread,codes)) if result is not None]
                    yield batch_results
            except StopIteration:
                print("Scraping successful")
                break