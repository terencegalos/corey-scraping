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
        # https://arc-sos.state.al.us/cgi/uccname.mbr/output?s=1&search=A&type=ALL&status=&order=default&hld=&dir=&page=Y
        self.baseurl = 'https://arc-sos.state.al.us/cgi/uccname.mbr/'
        self.url = 'https://arc-sos.state.al.us'
        self.table_name = "scraper49_info"
        self.last_interrupt_txt = 'last_char_scraper49.txt'
        self.state_json = 'state_scraper49.json'
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.url}")



    def save_state(self,last_char,last_char2,last_page):
        with open(self.state_json,'w') as file:
            json.dump({"char":last_char,"char2":last_char2,"page":last_page},file)



    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            return None
        
    
    
    
    def scrape_single(self,url):

        

        def get_response():

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
                response = requests.get(f"{url}", headers=headers)
            except requests.exceptions.ConnectionError:
                print(f'Connecting failed to {url}.\nReconnecting in 20 secs...')
                time.sleep(20)
                response = requests.get(f"{url}", headers=headers)
            except (requests.exceptions.InvalidURL,requests.exceptions.ConnectionError):
                print("Invalid url")
                return None

            return response


        while True:
            try:

                response = get_response()
                

                # raise for failed requests
                response.raise_for_status()
                
                
                
                
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                # print(soup.get_text())
                print(response.headers.items())
                print(f'status code:{response.status_code}')

                
                
                result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}




                # Extract debtor info

                result_set = soup.find_all('td',class_='aiSosDetailValue')




                debtor_info = result_set[7:8]

                if debtor_info:
                    debtor = debtor_info[0].get_text(separator='\n')
                    debtor_name = debtor.split("\n")[0]
                    debtor_address = ' '.join(debtor.split("\n")[1:])
                    result_dict.update({'debtor_name':debtor_name})
                    result_dict.update({'debtor_address':debtor_address})

                
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
            

            except Exception as e:
                print(f"Error: {e}. Retrying in 60 secs..")
                time.sleep(60)
                continue

        
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',last_interrupt_debtor=None,starting_page=1):
        
        def get_page_links(soup):
            tr_elements = soup.find_all("tr")
            page_results = [f'{self.url}{tr.find('a')['href']}' for tr in tr_elements[1:-1]]
            return page_results
        

        state = self.load_state()
                


        # 1 letter search; Loop all uppercase
        last_interrupt_index = ascii_uppercase.index(state['char'])
        last_interrupt2_index = ascii_uppercase.index(state['char2'])
        for char in ascii_uppercase[last_interrupt_index:]:
            for char2 in ascii_uppercase[last_interrupt2_index:]:
                last_interrupt2_index = 0 # reset
                print(f"Extract search results for '{char}{char2}' and starting page in {starting_page}")


                current_page = int(starting_page)
                
                while True:
                    current_url = f'{self.baseurl}output?s={current_page}&search={char}{char2}&type=ALL&status=&order=default&hld=&dir=&page=Y'
                    try:
                        response = requests.get(current_url)
                    except requests.exceptions.ConnectionError:
                        print("Connection failed. Retrying after 20 secs.")
                        time.sleep(20)
                        response = requests.get(current_url)

                    print(f'Scraping entries in url: {current_url}')
                    print(f'Status code: {response.status_code}')
                    print(response.headers)

                    # store current char to txt file
                    # with open(self.last_interrupt_txt,'w') as f:
                    #     f.write(str(char+"_"+str(current_page)))
                    self.save_state(str(char),str(char2),str(current_page))


                    # Get page results
                    # Parse the HTML content with BeautifulSoup
                    soup = BeautifulSoup(response.content,'html.parser')
                    
                    # urls = [] # Page results here

                    # Get first page results and store
                    urls = get_page_links(soup)
                    print("\n".join(urls))
                    
                    
                    # scrape info using multithread
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        batch_results = [results for results in executor.map(self.scrape_single,urls) if results is not None]
                        yield batch_results

                    
                    # add 25 to current_page to get next page
                    current_page += 25
                    next_page_link = re.search(r'>>',requests.get(current_url).text)

                    if not next_page_link:
                        print('No more pages. Exiting.')
                        break
        self.save_state('A','A','1') # reset state

