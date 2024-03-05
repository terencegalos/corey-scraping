import requests,time#,subprocess,tempfile,os#execjs, json, re
from requests_html import HTMLSession
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from fake_useragent import UserAgent
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper53:
    def __init__(self):
        
        self.baseurl = 'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/'
        self.searchurl = 'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx'
        self.table_name = "scraper53_info"
        self.last_interrupt_txt = 'last_char_scraper53.txt'
        self.session = HTMLSession()
        # self.session = requests.Session()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
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
            'DNT': '1',
            'Host': 'corp.sec.state.ma.us',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
        }

        headers1 = {
            "Host": "corp.sec.state.ma.us",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer":f'{self.baseurl}{url}',
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        







        print(f'Extracting doc links from URL: {url}')

        response = self.session.get(f'{self.baseurl}{url}', headers=headers1)

        print(f'Status code: {response.status_code}')
        # print(f'Content: {response.text}')



    
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)
        print(soup.get_text())


        table = soup.find('table',id_='MainContent_tblFilingHistory')
        debtor_tr = table.find_all('tr')[7]
        secured_party_tr = table.find_all('tr')[7]
        
        '#MainContent_tblFilingHistory > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(1)'
        '#MainContent_tblFilingHistory > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(1)'




        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}

        # get info
        # print(tr.contents)
        # print(tr.find_all('td')[1].get_text())
        debtor_name = debtor_tr.find_all("td")[0].get_text().splitlines()[0]
        try:
            debtor_address = " ".join(debtor_tr.find_all("td")[0].get_text().splitlines()[1:])
        except IndexError:
            debtor_address = 'N/A'

        result_dict.update({'debtor_name':debtor_name})
        result_dict.update({'debtor_address':debtor_address})
    
        secured_party_name = secured_party_tr.find_all('td')[0].get_text().splitlines()[0]
        try:
            secured_party_address = " ".join(secured_party_tr.find_all("td")[0].get_text().splitlines()[1:])
        except IndexError:
            secured_party_address = 'N/A'

        result_dict.update({'secured_party_name':secured_party_name})
        result_dict.update({'secured_party_address':secured_party_address})


        print(result_dict)


        return result_dict

        

    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='X',end_char='Z',last_interrupted_page=1,starting_page=1):
        
        def get_page_links(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')
            page_results = [tr.find('a')['href'] for tr in tr_elements if tr.find('a') and 'UCCSearch.aspx?SearchLapsed=True' not in tr.find('a')['href']]
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        
        # 1 letter search; Loop all uppercase
                
        # Get index of start ascii char
        last_interrupt_char_index = 0
        
        # Get index of end ascii char
        end_char_index = ascii_uppercase.index(end_char)


        if last_interrupt_char:
            print(f'Interruption specified: {last_interrupt_char}\nGetting index..')
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        # Start of loop
        for char in ascii_uppercase[last_interrupt_char_index:end_char_index]:
            for char2 in ascii_uppercase:
                print(f"Extract search results for '{char}{char2}'")

                headers1 = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'DNT': '1',
                    'Host': 'corp.sec.state.ma.us',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'cross-site',
                    'TE': 'trailers',
                    'Upgrade-Insecure-Requests': '1',
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",

                }

                headers2 = {
                    "Host": "corp.sec.state.ma.us",
                    "Content-Length":"999999",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://corp.sec.state.ma.us",
                    "DNT": "1",
                    "Sec-GPC": "1",
                    "Connection": "keep-alive",
                    "Referer": "https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "TE": "trailers"
                }


                headers3 = { 
                    
                    "Accept": "text/html:application/xhtml+xml:application/xml:q=0.9:image/avif:image/webp:*/*:q=0.8",			
                    "Accept-Encoding":"gzip: deflate: br",			
                    "Accept-Language": "en-US:en:q=0.5",			
                    "Connection": "keep-alive",			
                    "Content-Length": "9303", 			
                    "Content-Type": "application/x-www-form-urlencoded",
                    "DNT": "1",			
                    "Host": "corp.sec.state.ma.us",			
                    "Origin": "https://corp.sec.state.ma.us",			
                    "Referer": "https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx",			
                    "Sec-Fetch-Dest": "document",			
                    "Sec-Fetch-Mode": "navigate",			
                    "Sec-Fetch-Site": "same-origin",		
                    "Sec-Fetch-User": "?1",			
                    "Sec-GPC": "1",
                    "Upgrade-Insecure-Requests": "1",			
                    "User-Agent": "Mozilla/5.0 (X11: Ubuntu: Linux x86_64: rv:123.0) Gecko/20100101 Firefox/123.0"
                    }

                





                num_gen = num_generator(last_interrupted_page)

                last_interrupted_page = 0 # reset 
                
    

                
                while True:


                    num = next(num_gen)
                    print(f'Current page:{num}')                  
                    current_url = self.searchurl



                    # Get new cookies and set headers
                    response_ = self.session.get(current_url)
                    response_ = self.session.post(current_url,headers=headers1)

                    soup = BeautifulSoup(response_.text,'html.parser')
                    print(soup.contents)
                    print(response_.status_code)
                    # print("Does it return initial requests?")

                    time.sleep(1)
                    
                    


                    


                    viewstate = soup.find('input',{'name':'__VIEWSTATE'})['value']
                    eventvalidation = soup.find('input',{'name':'__EVENTVALIDATION'})['value']
                    # print({'viewstate':viewstate,'eventvalidation':eventvalidation}.items())

                    data = {
                        "__EVENTTARGET": "ctl00$MainContent$UCCSearchMethodI",
                        "__EVENTARGUMENT": "",
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": f"{viewstate}",
                        "__VIEWSTATEGENERATOR": "CB1FA542",
                        "__EVENTVALIDATION": f"{eventvalidation}",
                        "ctl00$MainContent$UccSearch": "rdoSearchI",
                        "ctl00$MainContent$txtLastName": f"{char.lower()}{char2.lower()}",
                        "ctl00$MainContent$txtFirstName": "",
                        "ctl00$MainContent$txtMiddleName": "",
                        "ctl00$MainContent$txtSuffix": "",
                        "ctl00$MainContent$txtICity": "",
                        "ctl00$MainContent$cboIState": "",
                        "ctl00$MainContent$txtName": "",
                        "ctl00$MainContent$txtOCity": "",
                        "ctl00$MainContent$cboOState": "",
                        "ctl00$MainContent$txtFilingNumber": "",
                        "ctl00$MainContent$UCCSearchMethodI": "B",
                        "ctl00$MainContent$txtStartDate": "",
                        "ctl00$MainContent$chkDebtor": "on",
                        "ctl00$MainContent$UCCSearchMethod": "M",
                        "ctl00$MainContent$ddRecordsPerPage": "100000",
                        "ctl00$MainContent$HiddenSearchOption_SearchLapsed": "False"
                    }
                    data1 = {
                        "__EVENTTARGET": "ctl00$MainContent$UCCSearchMethodI",
                        "__EVENTARGUMENT": "",
                        "__LASTFOCUS": "",
                        "__VIEWSTATE": f"{viewstate}",
                        "__VIEWSTATEGENERATOR": "CB1FA542",
                        "__EVENTVALIDATION": f"{eventvalidation}",
                        "ctl00$MainContent$UccSearch": "rdoSearchI",
                        "ctl00$MainContent$txtLastName": f"{char.lower()}{char2.lower()}",
                        "ctl00$MainContent$txtFirstName": "",
                        "ctl00$MainContent$txtMiddleName": "",
                        "ctl00$MainContent$txtSuffix": "",
                        "ctl00$MainContent$txtICity": "",
                        "ctl00$MainContent$cboIState": "",
                        "ctl00$MainContent$txtName": "",
                        "ctl00$MainContent$txtOCity": "",
                        "ctl00$MainContent$cboOState": "",
                        "ctl00$MainContent$txtFilingNumber": "",
                        "ctl00$MainContent$UCCSearchMethodI": "B",
                        "ctl00$MainContent$txtStartDate": "",
                        "ctl00$MainContent$chkDebtor": "on",
                        "ctl00$MainContent$UCCSearchMethod": "B",
                        "ctl00$MainContent$ddRecordsPerPage": "100000",
                        "ctl00$MainContent$btnSearch": "Search",
                        "ctl00$MainContent$HiddenSearchOption_SearchLapsed": "False"
                    }
                    # time.sleep(3)

                    # self.session.headers.update(headers2)
                    while True:
                        response_ = self.session.post(current_url,data=data1)
                        if 'robots' in response_.text.lower():
                            print(response_.text)
                            print("Bot trap detected. Retrying..")
                            time.sleep(1)
                            continue
                        else:
                            print(response_.text)
                            break



                    


                    # Get page results
                    # Parse the HTML content with BeautifulSoup
                    soup = BeautifulSoup(response_.content,'html.parser')
                    # print(soup.contents)
                    print(soup.get_text())
                    print(f'status_code: {response_.status_code}')
                    print(f"response history:{response_.history}")

                    print("Results displayed?")
                    # time.sleep(100)
                    

                    # Get first page results and store
                    urls = get_page_links(soup)

                    # Break while loop if no more page results
                    if len(urls) == 0:
                        print("No more pages found. Exiting.")
                        break
                    else:
                        for url in urls:
                            print(f'result url: {self.baseurl}{url}')
                    
                    
                    # scrape info using multithread
                    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                        for i in range(0,len(urls),batch_size):
                            batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                            yield batch_results
