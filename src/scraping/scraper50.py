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
        self.baseurl = 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-nonstand/portal.aspx'
        self.table_name = "scraper50_info"
        self.last_interrupt_txt = 'last_char_scraper50.txt'
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
        # response.raise_for_status()
        
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

        print(result_dict)

        return result_dict

        
        
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A', last_interrupt_debtor=None,searchby_start=0,starting_page=1): # starting page is a dummy and is always 1
        
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


            # Save last char to txt file
            with open(self.last_interrupt_txt,'w') as f:
                f.write(str(char)+"_"+str(1))


            search_by = ['OrganizationRadioButton','IndividualRadioButton']

            # Loop by organization AND individual
            for searchby in search_by[searchby_start:]:

                print(f"Extract search results for '{char}', search by {searchby}")

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
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchBy": f"{searchby}",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput": f"{char if searchby == search_by[0] else ''}",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MailingAddressInput": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$CityInput": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$StateInput": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$ZipInput": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$LastNameTextBox": f"{char if searchby == search_by[1] else ''}",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$FirstNameTextBox": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$MiddleNameTextBox": "",
                    "ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$SearchButton": "Search"
                }
                

                # print(data)

                
                
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