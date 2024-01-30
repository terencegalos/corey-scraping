import requests,time#, json, re
from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from fake_useragent import UserAgent
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper52:
    def __init__(self):
        
        self.baseurl = 'https://apps.ilsos.gov/uccsearch/'
        self.searchurl = 'https://apps.ilsos.gov/uccsearch/'
        self.table_name = "scraper52_info"
        self.last_interrupt_txt = 'last_char_scraper52.txt'
        # self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.baseurl}")
        
    
    
    
    def scrape_single(self,url):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'appas.ilsos.gov',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }






        print(f'Extracting doc links from URL: {url}')
        response = requests.get(url,headers=headers,proxies=proxy_dict,allow_redirects=True)
        # for proxy in proxy_list:
        #     try:
        #         response = requests.get(url,proxies=proxy,allow_redirects=True)
        #         break
        #     except Exception as e:
        #         # print(f'Connecting failed to url {url}. Reconnecting in 20 secs')
        #         # time.sleep(20)
        #         # response = requests.get(url,headers=headers,proxies=proxy_dict)
        #         print(e)
        print(f'Status code: {response.status_code}')
        print(f'Content: {response.text}')



        # raise for failed requests
        # response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)

        # return in no results found
        soup_table = soup.find('table')
        if not soup_table:
            # print(response.text)
            return



        # find all links that contains the info
        info_links = [a.attrs['href'] for a in soup_table.find_all("a") if 'href' in a.attrs and 'selecteddoc' in a.attrs['href'].lower()]

        # print(f'doc links:{info_links}')
        
        results = [] # store results here

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
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }


        for link in info_links:
            print(f"Extracting info. URL: {self.searchurl+link}")
            try:
                response = requests.get(self.searchurl+link,headers=headers,proxies=proxy_dict)
            except requests.exceptions.ConnectionError:
                print(f'Connecting failed to url {self.searchurl+link}. Retrying in 20 secs')
                time.sleep(20)
                response = requests.get(self.searchurl+link,headers=headers,proxies=proxy_dict)
                
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table')
            tr_elements = table.find_all('tr')
            # for tr in tr_elements:
            #     print("***")
            #     print(tr.contents)



    
            for tr in tr_elements[1:]:
                # print(tr.contents)
                # print(tr.find('span').get_text())
                
                # define empty result set 
                result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
                # print(result_dict)
                if 'debtor' in tr.find('span').get_text().lower():

                    # get info
                    # print(tr.contents)
                    # print(tr.find_all('td')[1].get_text())
                    debtor_name = " ".join(tr.find_all("td")[1].get_text().split())
                    try:
                        debtor_address = " ".join(tr.find_all("td")[2].get_text().split())
                    except IndexError:
                        debtor_address = 'N/A'
                    result_dict.update({'debtor_name':debtor_name})
                    result_dict.update({'debtor_address':debtor_address})
                elif 'secured' in tr.find('span').get_text().lower():                
                    secured_party_name = " ".join(tr.find_all('td')[1].get_text().split())
                    try:
                        secured_party_address = " ".join(tr.find_all("td")[2].get_text().split())
                    except IndexError:
                        secured_party_address = 'N/A'
                    result_dict.update({'secured_party_name':secured_party_name})
                    result_dict.update({'secured_party_address':secured_party_address})
                    
                    # update all results dict
                    for result_dict in results:
                        result_dict.update({'secured_party_name':secured_party_name})
                        result_dict.update({'secured_party_address':secured_party_address})
                else:
                    pass


                print(result_dict)

                results.append(result_dict)

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
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements if tr.find('a')]
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        # result = self.scrape_single(self.baseurl)
        # print(f'Sample result: {result}')

        
        # 1 letter search; Loop all uppercase
        last_interrupt_char_index = 0
        end_char_index = ascii_uppercase.index(end_char)


        if last_interrupt_char:
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        # Start of loop
        for current_char in ascii_uppercase[last_interrupt_char_index:end_char_index]:
            print(f"Extract search results for '{last_interrupt_char}'")

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


            num_gen = num_generator(last_interrupted_page)

            last_interrupted_page = 0 # reset 
            
  

            
            while True:
                num = next(num_gen)
                print(f'Current page:{num}')
                data = {
                    'command': 'index',
                    'method': 'index',
                    'page': 'index.jsp',
                    'searchType': 'U',
                    'uccSearch': 'P',
                    'lastName': f'{current_char}',
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
                # response = requests.post(current_url,data=data,headers=headers)
                response = requests.get('https://apps.ilsos.gov/uccsearch/',headers=headers,proxies=proxy_dict)
                print(f'Scraping entries in url: {current_url}')
                print(f'Status code: {response.status_code}')
                print(response.text)

                time.sleep(20)

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                

                # Get first page results and store
                urls = get_page_links(soup)

                if len(urls) == 0:
                    print("No more pages found. Exiting.")
                    break
                else:
                    for url in urls:
                        print(f'result url: {url}')
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    for i in range(0,len(urls),batch_size):
                        batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                        yield batch_results
