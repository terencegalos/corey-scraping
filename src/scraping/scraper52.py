import requests,time, json
from bs4 import BeautifulSoup
import concurrent.futures

import scraping.name_generator_large_file as name_generator
from requests_html import HTMLSession
from requests.cookies import RequestsCookieJar
from fake_useragent import UserAgent
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper52:
    def __init__(self):
        
        self.baseurl = 'https://apps.ilsos.gov/uccsearch/'
        self.searchurl = 'https://apps.ilsos.gov/uccsearch/UCCSearch'
        self.table_name = "scraper52_info"
        self.last_interrupt_txt = 'last_char_scraper52.txt'
        self.state_json = 'state_scraper52.json'
        # self.session = requests.Session()
        self.session = HTMLSession()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        self.data_param = {}
        print(f"Scraping: {self.baseurl}")


    def save_state(self,last_name):
        with open(self.state_json,'w') as file:
            json.dump({'last_name':last_name},file)

    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            print("Save state json file not found.")
            return None
        
    
    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)
        
    
    
    
    def scrape_single_row(self,tr_soup):
            
                
        # define empty result set 
        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
        tds = tr_soup.find_all('td')

        debtor_info = tds[2].get_text()

        debtor_name = " ".join(debtor_info.splitlines()[1].split())
        debtor_address = " ".join([" ".join(line.split()) for line in debtor_info.splitlines()[2:-1]])

        result_dict.update({'debtor_name':debtor_name,'debtor_address':debtor_address})
        
        secured_party_info = tds[3].get_text()
        
        secured_party_name = " ".join(secured_party_info.splitlines()[1].split())
        secured_party_address = " ".join([" ".join(line.split()) for line in secured_party_info.splitlines()[2:]])

        result_dict.update({'secured_party_name':secured_party_name,'secured_party_address':secured_party_address})


        # print(result_dict)


        return result_dict
    
    
    
    
    def get_page_rows(self,soup):

        table = soup.find("table")

        if table:
            trs_soup = table.find_all('tr')[1:]
        else:
            return []
        
        try:
            tr_data_soup = table.find_all('tr')[0]
        except IndexError:
            return []
        
        inputs_soup = tr_data_soup.find_all('input')

        # get all data parameters for next post requests
        if inputs_soup:
            self.data_param.update({input.get('name'): input.get('value') for input in inputs_soup})
            self.data_param['command'] = 'uccsearchresults'
            self.data_param['method'] = 'uccsearchresults'
            self.data_param['page'] = 'WEB-INF/pages/uccsearchresults.jsp'
            self.data_param['moreRecords'] = 'Y'
            if "" in self.data_param['history']:
                self.data_param.update({'history':'N'})
            if self.data_param['fileNbr'] == None:
                self.data_param.update({'fileNbr':''})

        print(self.data_param)
        
        print(f'tr length: {len(trs_soup)}')

        
        return trs_soup
    
    def num_generator(self, last_interrupt_page):
        num = last_interrupt_page
        while True:
            yield num
            num += 50


    def scrape_with_refcodes(self, batch_size=10):
        

        last_interrupt_lname_idx = 0
        
        state = self.load_state()
        
        last_names = ['xavier','smith','johnson']
        # last_names = name_generator.get_last_names()

        if state:
            last_interrupt_lname = state['last_name']
            try:
                last_interrupt_lname_idx = last_names.index(last_interrupt_lname)
            except ValueError:
                print(f"{last_interrupt_lname} not in list. Starting at the beginning.")
                last_interrupt_lname_idx = 0
        
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(last_interrupt_lname_idx,len(last_names),batch_size):
                batch_result = [item for result in executor.map(self.scraped_with_last_name,last_names[i:i+batch_size]) for item in result]
                yield batch_result
            





    def scraped_with_last_name(self,lname,last_interrupted_page=0):

        print(f"Extract search results for '{lname}'")

        self.save_state(lname)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'apps.ilsos.gov',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        }


        num_gen = self.num_generator(last_interrupted_page) # page number generator

        last_interrupted_page = 0 # reset         



        results = []
        
        # walk pagination
        while True:
            num = next(num_gen)
            print(f'Current page:{num} , last name: {lname}')
            data = {
                'command': 'index',
                'method': 'index',
                'page': 'index.jsp',
                'searchType': 'U',
                'uccSearch': 'P',
                'lastName': f'{lname}',
                'firstName': '',
                'middleName': '',
                'orgName': '',
                'searchWord': '',
                'fileNum': '',
                'lienNumber': '',
                'lienName': '',
                'submitIt': ['Submit', 'Submit']
            }
            

            
            current_url = self.baseurl


            try:
                response = self.session.get(current_url,headers=headers)
            except requests.exceptions.ConnectionError:
                print("Retrying in 20 secs.")
                time.sleep(20)
                response = self.session.get(current_url,headers=headers)

            headers1 = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Connection": "keep-alive",
                    "Content-Length": "189",
                    "Content-Type": "application/x-www-form-urlencoded",
                    # "Cookie": "JSESSIONID=00015qDVLDaS8xGxIlbpDLCAquP:1dmjj1u30; _abck=DEF228224E8BC59E6D1E5E8E76F3AAF3~0~YAAQ509DF1U6MoqNAQAAG/DkogvpPc5b4AB2oZg3DuY0tQfG2AUMOtm+lbH5pdBwVJPY8498O32BuuPKz6N3kcrIU0JPE+7BhGxf7HCpWAF1owm52HPA8dGp89J+SV7H8tj+56yxcrJaNxTOjwuqsjVTq2I4WXCmKnGP93IS7Ja4lXRbuC7EUHH0lTmFWre/+cFp6pozv8K0FHmUATR2ot68rcNSSBazVb9qGYEhT/b92MGUJwFvWD4f4He4CoOOGZO6fPbO6rE5lOYtQqCIQ0q3E/2evJDOK860LR7d968VdwAbzDcttDuVm09K3wBg+wRVV7zuDlS4o6bvU0aKU6wfQivxyZibNpKfACQN5gYuYFRv4aO787nL70XpgJZJHuim15G8T90+ukZ8vDAB+jyAlihEWg8=~-1~-…2ahQBK2RsBoWGolOB6SE6Mg3rLWkCInj4Mz0XkD+0ld/nL/RP3w1PHNhbaj1SJY0WabbJmDpZKhxlkpZ9cZfYyO9KxqdrupN9LoKos9W3qLe5lDYKuxCLAXh0M9obotrRHcdilHMlN2RLHpWZF4MLspfncH18kAbQUbpVl8kz33X+DIf8kDXGl1RNE92/btKFQ==~3618628~3556146; bm_sv=679D0A24FA7AE5FCA91122A1DADFCBE6~YAAQ509DF4FAMoqNAQAA1PTmohbWKVIPZdJQ9UNLMYg7fTpDxxVimbw+awWYqXy0Oyu/wEVNSvUQ9HsK3eTgQlc8LwQSJ32lsTB5fjaUL/leVLwU7C/Gym7y7yiTtXEhxQJr4phSnkPwNGixzQMkXasw4r9EjlMXbQSDd+/gnW+htR7UbbvXks4m69YEecs1XTiqB9bzqnh9FYo1KEcUn+Qau8cJLU0LGkCEXiB9c25gv/cTY/xtwNrj2I3ctlI=~1",
                    "DNT": "1",
                    "Host": "apps.ilsos.gov",
                    "Origin": "https://apps.ilsos.gov",
                    "Referer": "https://apps.ilsos.gov/uccsearch/",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Sec-GPC": "1",
                    "TE": "trailers",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
                }
            
            

            
            


            try:
                response = self.session.post(self.searchurl,data=(data if num == 0 else self.data_param),headers=headers1,allow_redirects=True)
            except requests.exceptions.ConnectionError:
                print("Retrying in 20 secs.")
                response = self.session.post(self.searchurl,data=(data if num == 0 else self.data_param),headers=headers1,allow_redirects=True)
            print(f"Status code: {response.status_code}")

            # Get page results using Beautifulsoup
            soup = BeautifulSoup(response.content,'html.parser')
            print(f'Scraping entries in url: {current_url}')
            

            # Get first page results and store
            trs_soup = self.get_page_rows(soup)

            if len(trs_soup) == 0:
                print("No more pages found. Exiting.")
                break

            page_result = [self.scrape_single_row(row) for row in trs_soup]

            print(f"Page result: {page_result}")

            results.extend(page_result)
            
            
        return results
    

            # scrape info using multithread
            # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            #     for i in range(0,len(trs_soup),batch_size):
            #         batch_results = [results for results in executor.map(self.scrape_single_row,trs_soup[i:i+batch_size])]# for item in results]
            #         yield batch_results
            
            # continue
