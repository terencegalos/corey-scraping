import requests,time, json, re
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper49:
    def __init__(self):
        # https://arc-sos.state.al.us/cgi/uccdetail.mbr/detail?ucc=20-7799272&page=name
        # https://arc-sos.state.al.us/cgi/uccname.mbr/input
        # self.baseurl = 'https://arc-sos.state.al.us/'
        self.baseurl = 'https://arc-sos.state.al.us/cgi/uccname.mbr/'
        self.url = 'https://arc-sos.state.al.us'
        self.table_name = "scraper49_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.url}")
        
    
    
    
    def scrape_single(self,url):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'arc-sos.state.al.us',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }



        print(f'Extracting info. URL: {url}')
        try:
            response = requests.get(f"{url}", headers=headers,proxies=proxy_dict)
        except requests.exceptions.ConnectionError:
            print(f'Connecting failed to {url}.\nReconnecting in 20 secs...')
            time.sleep(20)
            response = requests.get(f"{url}", headers=headers,proxies=proxy_dict)
        except requests.exceptions.InvalidURL:
            print("Invalid url")
            return None

        print(f'Status code: {response.status_code}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')

        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}

        # Extract debtor info
        # print(f'Content: {soup.get_text()}')
        result_set = soup.find_all('td',class_='aiSosDetailValue')
        if result_set:
            debtor_info = result_set[7:8]
        else:
            print('Elements not found.')
            return

        # for d in debtor_info:
        #     print(f'info: {d.get_text(separator='\n').split('\n')}')

        if debtor_info:
            debtor = debtor_info[0].get_text(separator='\n')
            debtor_name = debtor.split("\n")[0]
            debtor_address = ' '.join(debtor.split("\n")[1:])
            result_dict.update({'debtor_name':debtor_name})
            result_dict.update({'debtor_address':debtor_address})

        print(result_dict)
        # Extract secured party info
        secured_party_info = soup.find_all('td',class_='aiSosDetailValue')[8:9]
        print(f'len: {len(secured_party_info)}')
        secured_party = secured_party_info[0].get_text(separator='\n')
        if secured_party_info:
            secured_party_name = secured_party.split("\n")[0]
            secured_party_address = ' '.join(secured_party.split("\n")[1:])
            result_dict.update({'secured_party_name':secured_party_name})
            result_dict.update({'secured_party_address':secured_party_address})

        print(result_dict)

        return result_dict

        
        
        # Check if any value is None, if yes, return None
        if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
            return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='F',starting_page=951):
        
        def get_page_links(soup):
            tr_elements = soup.find_all("tr")
            page_results = [f'{self.url}{tr.find('a')['href']}' for tr in tr_elements[1:-1]]
            return page_results
                


        # 1 letter search; Loop all uppercase
        last_interrupt_index = ascii_uppercase.index(last_interrupt_char)
        for char in ascii_uppercase[last_interrupt_index:]:
            print(f"Extract search results for '{char}' and starting page in {starting_page}")
            starting_page = starting_page

            current_page = starting_page
            
            while True:
                current_url = f'{self.baseurl}output?s={current_page}&search={char}&type=ALL&status=&order=default&hld=&dir=&page=Y'
                response = requests.get(current_url)
                print(f'Scraping entries in url: {current_url}')
                print(f'Status code: {response.status_code}')

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                
                # urls = [] # Page results here

                # Get first page results and store
                urls = get_page_links(soup)
                print("\n".join(urls))
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    batch_results = [results for results in executor.map(self.scrape_single,urls)]
                    yield batch_results

                # for url in urls:
                #     result = self.scrape_single(url)
                #     print(result)
                #     yield result
                
                # add 25 to current_page to get next page
                current_page += 25
                next_page_link = re.search(r'>>',requests.get(current_url).text)

                if not next_page_link:
                    print('No more pages. Exiting.')
                    break






    # def scrape_with_refcodes(self,batch_size=10,num_threads=3):

            
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
        # data = {"search":"a","type":"ALL"}

        # self.scrape_pages(batch_size)

        # self.scrape_single(self.url,data)