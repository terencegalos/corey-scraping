import requests,time, json, re
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper50:
    def __init__(self):
        # https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=1521a398-e075-402c-a94b-005ec6badfc2
        # ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput
        self.baseurl = 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-nonstand/portal.aspx'
        self.table_name = "scraper50_info"
        self.last_interrupt_txt = 'last_char_scraper50.txt'
        self.state_json = 'state_scraper50.json'
        self.session = requests.Session()
        self.ua = UserAgent()
        self.jar = RequestsCookieJar()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.baseurl}")


    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)

    def save_state(self,last_char,last_char2,last_page,search_mode):
        with open(self.state_json,'w') as file:
            json.dump({"char":last_char,"char2":last_char2,"page":last_page,"mode":search_mode},file)

    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            return None
        
    
    
    
    def scrape_single(self,url):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': '4098',
            'Content-Type': 'application/x-www-form-urlencoded',
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


        print(f'Extracting info. URL: {url}')
        response = requests.get(url)
        # print(f'Content: {response.text}')
        print(f'Status code: {response.status_code}')


        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)


        # Extract debtor info from a table tag
        table = soup.find('table')
        if not table:
            print("No table found. Skipping")
            return

        # Loop td tags to get the required data
        tds = table.find_all('td')

        try:
            result_set = tds[6]
        except IndexError:
            print("Index error getting tds[6]. Skipping")
            return

        divs = result_set.find_all('div', class_='itemRepeater')
        
        # define empty result set
        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
        print(result_dict)

        # get info
        print(f'URL: {url}')
        try:
            debtor_name = divs[8].find_all('span')[0].get_text()
        except:
            debtor_name = 'n/a'
        try:
            debtor_address = divs[8].find_all('span')[1].get_text()
        except IndexError:
            debtor_address = 'n/a'
        try:
            secured_party_name = divs[11].find_all('span')[0].get_text()
        except IndexError:
            secured_party_name = 'n/a'
        try:
            secured_party_address = divs[11].find_all('span')[1].get_text()
        except IndexError:
            secured_party_address = 'n/a'

        # Update result set dict
        result_dict.update({'debtor_name':debtor_name})
        result_dict.update({'debtor_address':debtor_address})
        result_dict.update({'secured_party_name':secured_party_name})
        result_dict.update({'secured_party_address':secured_party_address})

        print(result_dict)

        return result_dict

        
        
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',last_interrupt_char2 ='A', last_interrupt_debtor=None,searchby_start=0,starting_page=1): # starting page is a dummy and is always 1
        
        def get_page_links(soup):
            tr_elements = soup.find_all("tr")
            print(f'tr length: {len(tr_elements)}')
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements[1:-1] if tr.find('a') and 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=' in tr.find('a')['href']]
            return page_results
            

        





        # load state
        state = self.load_state()
        # print(state)
        # time.sleep(100)

        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0 # set initial char index to 0
        last_interrupt_char2_index = 0


        # get starting char index
        if last_interrupt_char:
            last_interrupt_char_index = ascii_uppercase.index(state['char'])

        if last_interrupt_char2:
            last_interrupt_char2_index = ascii_uppercase.index(state['char2'])

        search_by = ['OrganizationRadioButton','IndividualRadioButton']





        # start loop from searchby organization
        for searchby in search_by[search_by.index(state['mode']):]:

            for char in ascii_uppercase[last_interrupt_char_index:]:
                for char2 in ascii_uppercase[last_interrupt_char2_index:]: # use 2 char to narrow down search

                    # Save last char to txt file
                    self.save_state(str(char),str(char2),str(1),searchby)
                    # with open(self.last_interrupt_txt,'w') as f:
                    #     f.write(str(char)+"_"+str(1))



                    # Loop by organization AND individual

                    print(f"Extract search results for '{char}{char2}', search by {searchby}")

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                        'Content-Length': '4098',
                        'Content-Type': 'application/x-www-form-urlencoded',
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
                    
                    
                    data = {
                        "__EVENTTARGET": "",
                        "__EVENTARGUMENT": "",
                        "__VIEWSTATE": "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",
                        "__VIEWSTATEGENERATOR": "DE76B829",
                        "__VIEWSTATEENCRYPTED": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl14$hiddenUserResponse": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MatchType": "MatchStartingWithRadioButton",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchBy": "OrganizationRadioButton",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput": f"{char.lower()}{char2.lower()}",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MailingAddressInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$CityInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$StateInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$ZipInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$LastNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$FirstNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MiddleNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchButton": "Search"
                    }

                    data_1 = {
                        "__EVENTTARGET": "",
                        "__EVENTARGUMENT": "",
                        "__VIEWSTATE": "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",
                        "__VIEWSTATEGENERATOR": "DE76B829",
                        "__VIEWSTATEENCRYPTED": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl14$hiddenUserResponse": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MatchType": "MatchStartingWithRadioButton",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchBy": "IndividualRadioButton",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MailingAddressInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$CityInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$StateInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$ZipInput": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$LastNameTextBox": f"{char.lower()}{char2.lower()}",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$FirstNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MiddleNameTextBox": "",
                        "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchButton": "Search"
                    }
                

                    # print((data if searchby in search_by[0] else data_1))

                    
                    
                    current_url = self.baseurl

                    # Renew cookies
                    resp_ = self.session.post(current_url)
                    print(self.session.cookies.items())
                    
                    response = self.session.post(current_url,data=(data if searchby in search_by[0] else data_1),headers=headers)
                    print(f'Scraping entries in url: {current_url}')
                    print(f'Status code: {response.status_code}')
                    # print(response.text)

                    # Get page results
                    # Parse the HTML content with BeautifulSoup
                    soup = BeautifulSoup(response.content,'html.parser')
                    

                    # Get first page results and store
                    urls = get_page_links(soup)
                    
                    last_interrupt_debtor_index = urls.index(last_interrupt_debtor) if last_interrupt_debtor is not None else 0
                    # scrape info using multithread
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        for i in range(last_interrupt_debtor_index,len(urls),batch_size):
                            batch_results = [results for results in executor.map(self.scrape_single,urls[i:i+batch_size])]
                            yield batch_results
                            
                    last_interrupt_debtor = None # reset debtor

            last_interrupt_char_index = 0 # reset char index to 0
        
        self.save_state('A','A','1','OrganizationRadioButton') # reset state
