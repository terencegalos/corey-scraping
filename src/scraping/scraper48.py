import requests,json
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator

class Scraper48:
    def __init__(self):
        # https://bizfileonline.sos.ca.gov/api/FilingDetail/ucc/487504/false
        self.url = f'https://bizfileonline.sos.ca.gov/api/FilingDetail/ucc/'
        self.table_name = "scraper48_info"
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


        response = requests.get(f'{url}{data['code']}/false')
        parsed_data = json.loads(response.text)
        print(parsed_data)

        result_list = []

        current_secured_party = {}

        

        for entry in parsed_data['DRAWER_DETAIL_LIST']:
            label = entry['LABEL']
            value = entry['VALUE']

            if label == 'Debtor Name':
                current_debtor = {'debtor_name' : value}
            elif label == 'Debtor Address':
                current_debtor['debtor_address'] = value
                result_entry = current_debtor.copy()
                result_entry.update(current_secured_party)
                result_list.append(result_entry)
            elif label == 'Secured Party Name':
                current_secured_party = {'secured_party_name': value}
            elif label == 'Secured Party Address':
                current_secured_party['secured_party_address'] = value
                
                # insert secured party info to all results
                for entry in result_list:
                    entry.update(current_secured_party)



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        # Return the scraped data as dictionary        
        # return {
        #     'debtor_name' : name,
        #     'debtor_address' : address,
        #     'secured_party_name' : secured_party_name,
        #     'secured_party_address' : secured_party_address
        # }

        return result_list
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self,batch_size=10,num_threads=3):

            
        # refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        # codes = code_generator.generate_code(1,200000000,'',6)
        codes = 2000000
        # print(f"There are {len(codes)} codes to rotate!")
        # results = []
        
        def scrape_single_thread(code):
            print(f"code : {code}")
            data = {'code':code}
            results = self.scrape_single(self.url,data)
            print(results)
            if results:
                print("Skipping 'None' values.")
            return results
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i in range(1,codes,batch_size):
                # batch_results = [results for results in list(executor.map(scrape_single_thread,list(range(i,i+batch_size)))) if len(results) > 0]
                batch_results = [item for sublist in executor.map(scrape_single_thread, range(i, i+batch_size)) for item in sublist if len(sublist) > 0]
                yield batch_results