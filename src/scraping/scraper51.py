import requests,time, json, re
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper51:
    def __init__(self):
        
        self.baseurl = 'https://dnr.alaska.gov/ssd/recoff/ucc/search/Name'
        self.searchurl = 'https://dnr.alaska.gov/ssd/recoff/ucc/search/'
        self.table_name = "scraper51_info"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.baseurl}")
        
    
    
    
    def scrape_single(self,url):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': '4098',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=fong0xk10z1uhuu0irxwkdl1',
            'DNT': '1',
            'Host': 'business.sos.ms.gov',
            'Origin': 'https://business.sos.ms.gov',
            'Referer': 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-nonstand/portal.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }





        print(f'Extracting info. URL: {self.searchurl+url}')
        response = requests.get(self.searchurl+url)
        # print(f'Content: {response.text}')
        print(f'Status code: {response.status_code}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)

        # find all links that contains the info
        info_links = soup.find_all("tr.table-default > td:nth-child(1) > a:nth-child(2)")

        results = [] # store results here
        for link in info_links:
            print(f"Extracting info. URL: {self.searchurl+link}")
            response = requests.get(self.searchurl+link)
            tbody = soup.find("#PartiesTable > tbody")
            tr_elements = tbody.find_all('tr')

        
            # define empty result set
            result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
            print(result_dict)

            # get info
            print(f'URL: {url}')
            debtor_name = soup.find("div.form-group:nth-child(4) > div:nth-child(2) > input:nth-child(1)").attrs['value']
            debtor_address = 'n/a'
            
            secured_party_name = soup.find('tr.table-default:nth-child(5) > td:nth-child(1)').get_text()
            secured_party_address = 'n/a'

            # Update result set dict
            result_dict.update({'debtor_name':debtor_name})
            result_dict.update({'debtor_address':debtor_address})
            result_dict.update({'secured_party_name':secured_party_name})
            result_dict.update({'secured_party_address':secured_party_address})


            print(result_dict)

            results.append(result_dict)

        return result_dict

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',last_interrupted_page=1):
        
        def get_page_links(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            # for tr in tr_elements:
            #     print(tr.contents)
            print(f'tr length: {len(tr_elements)}')
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements if tr.find('a')]
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        # result = self.scrape_single("https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=be5c804e-19b5-4a5f-bdd4-0065cf431c9e")
        # print(f'Sample result: {result}')

        
        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0


        if last_interrupt_char:
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        for char_index in ascii_uppercase[last_interrupt_char_index:]:
            print(f"Extract search results for '{last_interrupt_char}'")

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-us,en;q=0.5',
                'connection': 'keep-alive',
                'content-length': '67',
                'content-type': 'application/x-www-form-urlencoded',
                # 'cookie': 'ts017bf281=0102f3c9809678bdef7ab014e3b4192411c77bbe220ac8b927584449534b4418cecbbecd22400fc040b26cd04712586475d08e77ea',
                'dnt': '1',
                'host': 'dnr.alaska.gov',
                'origin': 'https://dnr.alaska.gov',
                'referer': 'https://dnr.alaska.gov/ssd/recoff/ucc/search/namemenu',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': self.ua.random
            }

            num_gen = num_generator(last_interrupted_page)
            
  

            
            while True:
                num = next(num_gen)
                print(f'Current page:{num}')
                data = {
                    "District": "500",
                    "page_num": f"{num}",
                    "starting_name": f"{char_index}",
                    "sort_desc": "true",
                    "Name+Search": ""
                }
                current_url = self.baseurl
                response = requests.post(current_url,data=data,headers=headers)
                print(f'Scraping entries in url: {current_url}')
                print(f'Status code: {response.status_code}')
                # print(response.text)

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                

                # Get first page results and store
                urls = get_page_links(soup)
                # print(urls)

                if len(urls) == 0:
                    print("No more pages found. Exiting.")
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    for i in range(0,len(urls),batch_size):
                        batch_results = [results for results in executor.map(self.scrape_single,urls[i:i+batch_size])]
                        yield batch_results
