import requests,json
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from string import ascii_uppercase

class Scraper49:
    def __init__(self):
        # https://arc-sos.state.al.us/cgi/uccdetail.mbr/detail?ucc=20-7799272&page=name
        # https://arc-sos.state.al.us/cgi/uccname.mbr/input
        self.baseurl = 'https://arc-sos.state.al.us/'
        self.url = 'https://arc-sos.state.al.us/cgi/uccname.mbr/output'
        self.table_name = "scraper49_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.url}")
        
    
    
    
    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'arc-sos.state.al.us',
            'Origin': 'https://arc-sos.state.al.us',
            'Referer': 'https://arc-sos.state.al.us/cgi/uccname.mbr/input',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
        }


        response = requests.get("https://arc-sos.state.al.us/cgi/uccname.mbr/input")
        cookies = response.cookies
        response = requests.post(self.url,headers=headers, cookies=cookies, data=data)
        print(f'{url}')

        # print(response.text)
        print(f'Status code: {response.status_code}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        
        urls = []
        tr_elements = soup.find_all("tr")
        for tr in tr_elements:
            url = f'{self.baseurl}{tr.find('a')['href']}'
            print(f'Url: {url}')
            urls.append(url)

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_pages(self,last_interrupt_char):

        def get_nextpage_url(soup):
            next_button = soup.find(text='Next >>')
            if next_button:
                next_url = next_button.find_parent('a')['href']
                return self.baseurl+next_url
            
            return None


        for char in ascii_uppercase[last_interrupt_char:]:
            data = {"search":f"{char}","type":"ALL"}

            response = requests.get("https://arc-sos.state.al.us/cgi/uccname.mbr/input")
            cookies = response.cookies
            response = requests.post(self.url, cookies=cookies, data=data)
            print(f'{url}')

            # print(response.text)
            print(f'Status code: {response.status_code}')

            # raise for failed requests
            # response.raise_for_status()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content,'html.parser')
            
            urls = []
            tr_elements = soup.find_all("tr")
            for tr in tr_elements:
                url = f'{self.baseurl}{tr.find('a')['href']}'
                print(f'Url: {url}')
                urls.append(url)
            
            yield urls






    def scrape_with_refcodes(self,batch_size=10,num_threads=3):

            
        # results = []
        
        # def scrape_single_thread(code):
        #     print(f"code : {code}")
        #     data = {'code':code}
        #     results = self.scrape_single(self.url,data)
        #     print(results)
        #     if results:
        #         print("Skipping 'None' values.")
        #     return results
            
        # with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        #     for i in range(1,codes,batch_size):
        #         # batch_results = [results for results in list(executor.map(scrape_single_thread,list(range(i,i+batch_size)))) if len(results) > 0]
        #         batch_results = [item for sublist in executor.map(scrape_single_thread, range(725, i+batch_size)) if sublist is not None for item in sublist if len(sublist) > 0]
        #         yield batch_results

        # for char in ascii_uppercase:
        data = {"search":"a","type":"ALL"}

        self.scrape_single(self.url,data)