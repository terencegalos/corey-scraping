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
        self.last_interrupt_txt = 'last_code_scraper48.txt'
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.url}")
        
    
    
    
    def scrape_single(self,url,data):
        

        response = requests.get(f'{url}{data['code']}/false')
        print(f'{url}{data['code']}/false')
        parsed_data = json.loads(response.text)
        # print(parsed_data)

        result_list = []

        current_secured_party = {}

        

        try:
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
        except KeyError as e:
            print(f'KeyError: {e}')
            return KeyError



        # raise for failed requests
        response.raise_for_status()

        # Save current code to txt file
        with open(self.last_interrupt_txt,'w') as f:
            f.write(str(data['code']))
    

        return result_list
            
    
    
    
    def scrape_with_refcodes(self,start=1,batch_size=10,num_threads=3):

            
        # refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        # codes = code_generator.generate_code(1,200000000,'',6)
        # code_gen = code_generator.num_generator()
        # print(f"There are {len(codes)} codes to rotate!")
        # results = []
        
        def scrape_single_thread(code):
            print(f"code : {code}")
            data = {'code':code}
            results = self.scrape_single(self.url,data)
            print(results)


            if results:
                return results
            return None
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            i = start
            # stop = 0
            while True:
                batch_results = [item for sublist in executor.map(scrape_single_thread, range(i, i+batch_size)) if sublist is not None for item in sublist if len(sublist) > 0]
                if len(batch_results) < 1:
                    break
                yield batch_results
                i += batch_size
                # stop += 1
                # if stop > 3:
                #     raise ValueError('Simulated error raised')
