import requests,json,time#, json, re
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from requests.cookies import RequestsCookieJar
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
        self.state_json = 'state_scraper54.json'
        self.jar = RequestsCookieJar()
        self.session = requests.Session()
        self.ua = UserAgent()
        print(f"Scraping: {self.baseurl}")
        # response = requests.get(self.searchurl)
        # self.renew_cookies(response)
        self.soup = ''

    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)

    def save_state(self,char,char2,page):
        with open(self.state_json,'w') as file:
            json.dump({'char':char,'char2':char2,'page':page},file)

    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            print("Save state json file not found.")
            return None
        
    
    
    
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
        response = requests.get(url,headers=headers,verify=False)
        print(f'Status code: {response.status_code}')
        # print(f'Content: {response.text}')



        # Parse the HTML content with BeautifulSoup
        self.soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)
# 
        # return in no results found
        soup_table = self.soup.find_all('table')
        if len(soup_table) < 1:
            return []

        
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
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10,last_interrupt_char='A',starting_page=1):

        def get_page_rows(soup):
            table = soup.find("table")

            if not table:
                print("Table not found. Skipping")
                return []
            
            tr_elements = table.find_all('tr')
            print(f'tr length: {len(tr_elements)}')
            page_results = [{'debtor_name':tr.find_all('td')[3].get_text(),'debtor_address':tr.find_all('td')[4].get_text()} for tr in tr_elements[1:]]

            return page_results
        
        def get_page_links(soup):
            table = soup.find("table")
            if not table:
                print("Table not found. Skipping")
                return []
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')
            page_results = list(set([f'{self.baseurl}{tr.find('a')['href']}' for tr in tr_elements[1:] if tr.find('a')]))

            return page_results
        
        def num_generator(starting_page):
            num = int(starting_page)
            while True:
                yield num
                num += 1

        state = self.load_state()
        print(state)
                

        
        
        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0
        # end_char_index = ascii_uppercase.index(end_char)



        last_interrupt_char_index = ascii_uppercase.index(state['char'])
        last_interrupt_char2_index = ascii_uppercase.index(state['char2'])



        # Start of loop
        for char in ascii_uppercase[last_interrupt_char_index:]:
            for char2 in ascii_uppercase[last_interrupt_char2_index:]:
                
                print(f"Extract search results for '{char}{char2}'")

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
                    'User-Agent': self.ua.random,#'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'X-Requested-With': 'XMLHttpRequest',
                }



                num_gen = num_generator(state['page'])

                state['page'] = 1 # reset page           

                
                # Rotate pages
                while True:
                    num = next(num_gen)
                    print(f'Current page:{num}')
                    self.save_state(char,char2,num)
                    # self.session.close()

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
                                "LastName": f"{char}{char2}",
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

                    data_org = {
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
                                "IsIndividual": False,
                                "LastName": "",
                                "MiddleName": "",
                                "Name": "ab",
                                "OrganizationName": f"{char}{char2}",
                                "StartsWith": "2",
                                "Suffix": ""
                            },
                            "SearchCriteria": "2",
                            "SearchType": "DebtorName"
                        }
                    }
                    

                    current_url = self.searchurl
                    print("Sending post requests.")



                    param = data_org if num < 2 else data2
                    print(param)
                    response = requests.post(current_url,headers=headers,data=json.dumps(param),verify=False)
                    # self.renew_cookies(response)
                    


                    print(response.headers)
                    print(f'Status code: {response.status_code}')



                    # Get page results

                    # Parse the HTML content with BeautifulSoup
                    self.soup = BeautifulSoup(response.content,'html.parser')
                    print(self.soup.get_text())

                    page_links = []
                    current_page = 0
                    total_page = 0






                    # Get pages info
                    while True:
                        try:
                            page_info_soup = self.soup.find(class_='pageinfo')
                            page_info = page_info_soup.get_text().split(",")[0]
                            print("Success getting page info.")
                            time.sleep(5)

                            current_page = int(page_info.split()[1])
                            total_page = int(page_info.split()[3])

                            # Get first page links
                            if self.soup:
                                page_links.extend(get_page_links(self.soup))

                            break

                        except:
                            if num < 2:
                                print("Page 1 no results. Breaking...")
                                break
                            print("Page info not found. Retrying")
                            time.sleep(1)
                            # self.session.close()
                            response_ = requests.get(self.searchurl)
                            self.renew_cookies(response_)

                            response = requests.post(current_url,headers=headers,cookies=self.jar,data=json.dumps(data),verify=False)
                            self.renew_cookies(response)

                            response = requests.post(current_url,headers=headers,cookies=self.jar,data=json.dumps(param),verify=False)

                            self.soup = BeautifulSoup(response.content,'html.parser')
                            # print(f"Updated content: {self.soup.contents[0]}")

                            # Check if response returns a json instead of html
                            try:
                                response_status_json = json.loads(self.soup.contents[0])

                                if not response_status_json['success']:
                                    print("No more results. Breaking")
                                    break
                            except json.decoder.JSONDecodeError:
                                pass # ignore if not json
                            # print(response.status_code)

                            continue
                    

                    # current_page = int(page_info.split()[1])
                    # total_page = int(page_info.split()[3])


                    # scrape info using multithread
                    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                        for i in range(0,len(page_links),batch_size):
                            results = executor.map(self.scrape_single,page_links[i:i+batch_size])
                            if results is not None:
                                batch_results = [item for results in results for item in results if item is not None]
                                yield batch_results
                            else:
                                print("thread results: None")


                    if current_page >= total_page:
                        print("No more pages found. Next search..")
                        # self.session.close()
                        break
        
        self.save_state('A','A',"1") # reset state once done



