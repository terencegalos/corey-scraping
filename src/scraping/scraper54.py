import requests,json,time#, json, re
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from fake_useragent import UserAgent
from string import ascii_uppercase
from config.proxies import proxy_dict
# from config.proxies_1 import proxy_list

class Scraper54:
    def __init__(self):
        
        self.baseurl = 'https://cis.scc.virginia.gov/'
        self.searchurl = 'https://cis.scc.virginia.gov/UCCOnlineSearch/UCCSearch'
        self.table_name = "scraper54_info"
        self.last_interrupt_txt = 'last_char_scraper54.txt'
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
            'DNT': '1',
            'Host': 'cis.scc.virginia.gov',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }


        


        print(f'Extracting info from url: {url}')
        response = requests.get(url,headers=headers,proxies={'https':'47.243.92.199:3128'},allow_redirects=True,verify=False)
        print(f'Status code: {response.status_code}')
        # print(f'Content: {response.text}')



        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)
# 
        # return in no results found
        soup_table = soup.find_all('table')
        if len(soup_table) < 1:
            return

        
        results = [] # store results here

     
    
        # define empty result set 
        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}

        try:
            soup_tr = soup_table[1].find_all('tr')
        except IndexError:
            print(f'Error getting table rows. Table count: {len(soup_table)}')
            return
        
        for tr in soup_tr[1:]:
            debtor_name = " ".join(tr.find_all("td")[0].get_text().split())
            try:
                debtor_address = " ".join(tr.find_all("td")[1].get_text().split())
            except IndexError:
                debtor_address = 'N/A'
            result_dict.update({'debtor_name':debtor_name})
            result_dict.update({'debtor_address':debtor_address})
    
            secured_party_name = " ".join(soup_table[2].find_all("td")[0].get_text().split())
            try:
                secured_party_address = " ".join(soup_table[2].find_all("td")[1].get_text().split())
            except IndexError:
                secured_party_address = 'N/A'
            result_dict.update({'secured_party_name':secured_party_name})
            result_dict.update({'secured_party_address':secured_party_address})
        
            print(result_dict)
            results.append(result_dict)



        # update all results dict
        for result_dict in results:
            result_dict.update({'secured_party_name':secured_party_name})
            result_dict.update({'secured_party_address':secured_party_address})

        return results

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',end_char = 'Z',last_interrupted_page=1,starting_page=1):
        
        def get_page_links(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')
            page_results = list(set([f'{self.baseurl}{tr.find('a')['href']}' for tr in tr_elements[1:] if tr.find('a')]))

            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        
        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0
        end_char_index = ascii_uppercase.index(end_char)


        if last_interrupt_char:
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        # Start of loop
        for char in ascii_uppercase[last_interrupt_char_index:end_char_index]:
            print(f"Extract search results for '{last_interrupt_char}'")

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '471',
                'Content-Type': 'application/json; charset=utf-8',
                # 'Cookie': 'ASP.NET_SessionId=kx1y2czpavpgpeqnjl1lmhzu; nmstat=438e7bf1-1a01-14c2-299a-06b764fb7c58',
                'DNT': '1',
                'Host': 'cis.scc.virginia.gov',
                'Origin': 'https://cis.scc.virginia.gov',
                'Pragma': 'no-cache',
                'Referer': 'https://cis.scc.virginia.gov/UCCOnlineSearch/UCCSearch',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'X-Requested-With': 'XMLHttpRequest',
            }



            num_gen = num_generator(last_interrupted_page)

            last_interrupted_page = 0 # reset 
            
  

            
            while True:
                num = next(num_gen)
                print(f'Current page:{num}')

                data = {
                    "search": {
                        "advancedSearch": {
                            "City": "",
                            "Country": "",
                            "County": "",
                            "FilingDateFrom": "",
                            "FilingDateTo": "",
                            "LapseDateFrom": "",
                            "LapseDateTo": "",
                            "State": "",
                            "Status": "",
                            "StatusID": "",
                            "StreetAddress1": "",
                            "StreetAddress2": "",
                            "Zip4": ""
                        },
                        "IsOnline": True,
                        "quickSearch": {
                            "Contains": 0,
                            "ExactMatch": 0,
                            "FirstName": "",
                            "IsIndividual": True,
                            "LastName": f"{char}",
                            "MiddleName": "",
                            "Name": "zundefined",
                            "OrganizationName": "",
                            "StartsWith": "2",
                            "Suffix": "",
                            "pidx": f"{num}"
                        },
                        "SearchCriteria": "2",
                        "SearchType": "DebtorName"
                    }
                }

                data2 = {
                    "undefined": "",
                    "sortby": "",
                    "stype": "a",
                    "pidx": f"{num}"
                }
                
                current_url = self.searchurl
                print("Sending post requests.")
                response = requests.post(current_url,data=json.dumps(data),headers=headers,proxies={'https':'47.243.92.199:3128'},verify=False)
                # response = requests.post(current_url,data=json.dumps(data),headers=headers,proxies={'https':'32.223.6.94:80'},verify=False)
                
                # print(f'Scraping entries in url: {current_url}')
                # print(response.text)
                print(response.headers)
                print(f'Status code: {response.status_code}')

                # time.sleep(100)

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                

                # Get first page results and store
                if soup:
                    page_links = get_page_links(soup)
                else:
                    print("table for results not visible. check requests")

                if len(page_links) == 0:
                    print("No more pages found. Exiting.")
                    break
                else:
                    for link in page_links:
                        print(f'link result: {link}')
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    for i in range(0,len(page_links),batch_size):
                        batch_results = [item for results in executor.map(self.scrape_single,page_links[i:i+batch_size]) for item in results]
                        yield batch_results
