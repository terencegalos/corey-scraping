import requests,time, json, re
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
        # https://arc-sos.state.al.us/cgi/uccdetail.mbr/detail?ucc=20-7799272&page=name
        # https://arc-sos.state.al.us/cgi/uccname.mbr/input
        # self.baseurl = 'https://arc-sos.state.al.us/'
        self.baseurl = 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-nonstand/portal.aspx'
        self.table_name = "scraper50_info"
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





        print(f'Extracting info. URL: {url}')
        response = requests.get(url)
        # print(f'Content: {response.text}')
        print(f'Status code: {response.status_code}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)


        # Extract debtor info from a table tag
        table = soup.find('table')

        # Loop td tags to get the required data
        tds = table.find_all('td')
        result_set = tds[6]
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

        # print(result_dict)
        
        # index = 11
        # # try:

        print(result_dict)

        return result_dict

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A', last_interrupt_debtor=None):
        
        def get_page_links(soup):
            tr_elements = soup.find_all("tr")
            print(f'tr length: {len(tr_elements)}')
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements[1:-1] if tr.find('a') and 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=' in tr.find('a')['href']]
            return page_results
                

        # result = self.scrape_single("https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=be5c804e-19b5-4a5f-bdd4-0065cf431c9e")
        # print(f'Sample result: {result}')

        
        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0


        if last_interrupt_char:
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        for char in ascii_uppercase[last_interrupt_char_index:]:
            print(f"Extract search results for '{char}'")

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
            
            
            data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": "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",
                "__VIEWSTATEGENERATOR": "DE76B829",
                "__VIEWSTATEENCRYPTED": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl14$hiddenUserResponse": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MatchType": "MatchStartingWithRadioButton",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchBy": "OrganizationRadioButton",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput": f"{char}",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MailingAddressInput": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$CityInput": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$StateInput": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$ZipInput": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$LastNameTextBox": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$FirstNameTextBox": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MiddleNameTextBox": "",
                "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchButton": "Search"
            }
            
            # while True:
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
            
            last_interrupt_debtor_index = urls.index(last_interrupt_debtor) if last_interrupt_debtor is not None else 0
            # scrape info using multithread
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for i in range(last_interrupt_debtor_index,len(urls),batch_size):
                    batch_results = [results for results in executor.map(self.scrape_single,urls[i:i+batch_size])]
                    yield batch_results