import requests,time, json, re
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper50:
    def __init__(self):
        # ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput
        # https://arc-sos.state.al.us/cgi/uccdetail.mbr/detail?ucc=20-7799272&page=name
        # https://arc-sos.state.al.us/cgi/uccname.mbr/input
        # self.baseurl = 'https://arc-sos.state.al.us/'
        self.baseurl = 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-nonstand/portal.aspx'
        self.url = 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-stand/portal.aspx'
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
        response = requests.get(url,headers=headers,proxies=proxy_dict)
        print(f'Status code: {response.status_code}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')

        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}

        # Extract debtor info
        print(f'Content: {soup.get_text()}')
        result_set = soup.find('.uccFilingRepeater > div:nth-child(1) > div:nth-child(4) > div:nth-child(9)')
        # if result_set:
        #     debtor_info = result_set.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl01_NameLabel')
        # else:
        #     print('Elements not found.')

        # for d in debtor_info:
        #     print(f'info: {d.get_text(separatr='\n').split('\n')}')

        if result_set:
            # debtor = result_set.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl01_NameLabel')
            debtor_name = result_set.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl01_NameLabel')
            debtor_address = result_set.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl01_mailAddressLabel')
            result_dict.update({'debtor_name':debtor_name})
            result_dict.update({'debtor_address':debtor_address})

        print(result_dict)
        # Extract secured party info
        secured_party_info = soup.find('.uccFilingRepeater > div:nth-child(1) > div:nth-child(4) > div:nth-child(9) > div:nth-child(3) > div:nth-child(3)')
        # print(f'len: {len(secured_party_info)}')
        if secured_party_info:
            secured_party_name = secured_party_info.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl02_NameLabel')
            secured_party_address = secured_party_info.find(id='ctl00_ContentPlaceHolder1_PortalPageControl1_ctl22_uccFilingRepeater_ctl01_uccNamesRepeater_ctl02_mailAddressLabel')
            result_dict.update({'secured_party_name':secured_party_name})
            result_dict.update({'secured_party_address':secured_party_address})

        print(result_dict)

        return result_dict

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char=None):
        
        def get_page_links(soup):
            tr_elements = soup.find_all("tr")
            print(f'tr length: {len(tr_elements)}')
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements[1:-1] if tr.find('a') and 'https://business.sos.ms.gov/star/portal/ucc/page/uccSearch-filingchain/portal.aspx?Id=' in tr.find('a')['href']]
            return page_results
                


        # 1 letter search; Loop all uppercase
        for char in ascii_uppercase[last_interrupt_char:]:
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
            # data = {'ctl00$ContentPlaceHolder1$PortalPageControl1$ctl24$OrganizationNameInput':f'{char}'}
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
            # starting_page = 1

            # current_page = starting_page
            
            # while True:
            current_url = self.baseurl#f'{self.baseurl}output?s={current_page}&search={char}&type=ALL&status=&order=default&hld=&dir=&page=Y'
            response = requests.post(current_url,data=data,headers=headers)
            print(f'Scraping entries in url: {current_url}')
            print(f'Status code: {response.status_code}')
            # print(response.text)

            # Get page results
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content,'html.parser')
            
            # urls = [] # Page results here

            # Get first page results and store
            urls = get_page_links(soup)
            # print("\n".join(urls))
            
            
            # scrape info using multithread
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                batch_results = [results for results in executor.map(self.scrape_single,urls)]
                yield batch_results

            # # for url in urls:
            # #     result = self.scrape_single(url)
            # #     print(result)
            # #     yield result
            
            # # add 25 to current_page to get next page
            # current_page += 25
            # next_page_link = re.search(r'>>',requests.get(current_url).text)

            # if not next_page_link:
            #     print('No more pages. Exiting.')
            #     break







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