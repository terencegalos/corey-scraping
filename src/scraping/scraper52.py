import requests,time#, json, re
import urllib.parse
from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
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
        # self.session = requests.Session()
        self.session = HTMLSession()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        print(f"Scraping: {self.baseurl}")
    
    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)
        
    
    
    
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
        response = requests.get(url,headers=headers,allow_redirects=True)
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
                response = requests.get(self.searchurl+link,headers=headers)
            except requests.exceptions.ConnectionError:
                print(f'Connecting failed to url {self.searchurl+link}. Retrying in 20 secs')
                time.sleep(20)
                response = requests.get(self.searchurl+link,headers=headers)
                
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
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',end_char = 'Z',last_interrupted_page=1,starting_page=1):
        
        def get_page_rows(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')

            row_tds = [f'{tr.find_all('td')}' for tr in tr_elements]
            {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
            debtor_info = row_tds[2].get_text()
            debtor_name = debtor_info.splitlines()[0]
            debtor_address = "/n".join(debtor_info.splitlines()[1:])
            
            secured_party_info = row_tds[3].get_text()
            secured_party_name = secured_party_info.splitlines()[0]
            secured_party_address = "/n".join(secured_party_info.splitlines()[1:])
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        # result = self.scrape_single(self.baseurl)
        # print(f'Sample result: {result}')
                
        last_names = ['xavier','smith']

        # Start of loop
        for lname in last_names:
            print(f"Extract search results for '{lname}'")

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


                response = self.session.get(current_url,headers=headers)
                # self.renew_cookies(response)
                # time.sleep(1)

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

                
                


                response = self.session.post(self.searchurl,data=data,headers=headers1,allow_redirects=True)
                # response.html.render()
                # print(response.html.raw_html)

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                # print(f'Scraping entries in url: {current_url}')
                # print(soup.get_text())
                # print(f'Status code: {response.status_code}')
                # print(f'History: {response.history}')
                # print(f'Headers: {response.headers.items()}')
                

                # Get first page results and store
                rows_soup = get_page_rows(soup)

                if len(rows_soup) == 0:
                    print("No more pages found. Exiting.")
                    break
                else:
                    for row in rows_soup:
                        print(f'result url: {url}')
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    for i in range(0,len(urls),batch_size):
                        batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                        yield batch_results
