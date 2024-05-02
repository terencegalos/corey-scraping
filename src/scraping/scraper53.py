import json, requests, time
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
        self.state_json = 'state_scraper53.json'
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

    def save_state(self,last_char,last_char2,last_char3,search):
        with open(self.state_json,'w') as file:
            json.dump({"char":last_char,"char2":last_char2,"char3":last_char3,"search":search},file)



    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            return None
    
    
    
    def scrape_single(self,url):

        headers1 = {
            "Host": "corp.sec.state.ma.us",
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": 'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearchResults.aspx?sysvalue=ORIhMVYRub09EF9n4TWp2YHrUO62ErYNEY2LWxdD8P4-',
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
        time.sleep(3) # pause to avoid rate limit

        for item in self.session.cookies.items():
            print(item)
            
        self.session.headers.update(headers1)
        # self.session.headers.update({"Referer":'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearchResults.aspx?sysvalue=ORIhMVYRub09EF9n4TWp2YHrUO62ErYNEY2LWxdD8P4-'})
        
        # send get requests; if status code 403 retry until it is 200
        while True:
            try:
                response = self.session.get(f'{self.baseurl}{url}')
            except requests.exceptions.ConnectionError:
                print("Connection failed. Retrying in 20 secs..")
                time.sleep(20)
                response = self.session.get(f'{self.baseurl}{url}')
            except:
                # Return None and discard current url
                print('Invalid url. Skipping..')
                return


            if response.status_code == 403:
                print(f"Forbidden GET request for {self.baseurl}{url}. Skipping...")
                # time.sleep(120)
                return
            elif response.status_code == 503:
                print(f"Service unavailable for GET request: {self.baseurl}{url}. Retrying in 120 secs")
                time.sleep(120)
                continue
            elif response.status_code == 200 or response.status_code == 302:
                break
            else:
                raise requests.HTTPError(f"Error: status code {response.status_code}")



    
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        print(soup.get_text())


        table = soup.select_one('table table:nth-child(4)')
        
        '#MainContent_tblFilingHistory > tbody:nth-child(1) > tr > td:nth-child(1)'

        # Loop tr tags
        try:
            tr_soup = table.find_all('tr')
        except AttributeError:
            print("Table rows not available. Skipping..")
            return


        count = 0 # check if row is odd or even (odd is debtor info even is secured party info)
        result_dict_list = [] # store dictionaries here if multiple
        result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}

        for tr in tr_soup[1:]:


            # check if tr has 2 td children and no more
            if tr.select_one('td:nth-child(2)') and not tr.select_one('td:nth-child(3)'):

                count += 1
                if count % 2 == 0: 
                    # secured party
                    secured_party_info = tr.select_one('td:nth-child(1)').get_text(separator='\n')
                    # print(secured_party_info.splitlines())
                    result_dict.update({'secured_party_name':secured_party_info.splitlines()[0]})
                    result_dict.update({'secured_party_address':' '.join(secured_party_info.splitlines()[1:])})
                    
                    result_dict_list.append(result_dict)
                    result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''} # reset
                else: 
                    # debtor
                    debtor_info = tr.select_one('td:nth-child(1)').get_text(separator='\n')
                    result_dict.update({'debtor_name':debtor_info.splitlines()[0]})
                    result_dict.update({'debtor_address':' '.join(debtor_info.splitlines()[1:])})

                





        # get info
                    


        print(result_dict_list)


        return result_dict_list

        

    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='A',end_char='Z',last_interrupted_page=1,starting_page=1):



        state = self.load_state()
        

        def get_page_links(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')
            page_results = [tr.find('a')['href'] for tr in tr_elements if tr.find('a') and 'UCCSearch.aspx?SearchLapsed=True' not in tr.find('a')['href'] and ".pdf" not in tr.find('a')['href']]
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1

        def get_viewstate(soup):
            viewstate = soup.find('input',{'name':'__VIEWSTATE'})
            return viewstate['value'] if viewstate else None
                
        def get_eventvalidation(soup):
            eventvalidation = soup.find('input',{'name':'__EVENTVALIDATION'})
            return eventvalidation['value'] if eventvalidation else None
                








        
        # 1 letter search; Loop all uppercase

        print(f"Searching character: {state['char']}{state['char2']}, search:{state['search']}")
                
        # Get index of start ascii char
        last_interrupt_char_index = ascii_uppercase.index(state['char'])
        last_interrupt_char2_index = ascii_uppercase.index(state['char2'])
        last_interrupt_char3_index = ascii_uppercase.index(state['char3'])
        
        # Get index of end ascii char
        # end_char_index = ascii_uppercase.index(end_char)







        # Start of loop
        search = ['I']
        search_index = search.index(state['search'])
        
        for uccsearch in search[search_index:]:
            for char in ascii_uppercase[last_interrupt_char_index:]:
                for char2 in ascii_uppercase[last_interrupt_char2_index:]:
                    for char3 in ascii_uppercase:

                        print(f"Extract search results for '{char}{char2}{char3} search:{uccsearch}'")
                

                        last_interrupt_char_index = 0 # reset 

                        self.save_state(char,char2,char3,uccsearch)                        


                        # set url
                        current_url = self.searchurl


                        # Get new cookies and set headers

                        while True:
                            
                            
                            response_ = self.session.get(current_url)
                            time.sleep(3)
                            
                                                
                            # Get VIEWSTATE AND EVENT VALIDATION
                            soup = BeautifulSoup(response_.text,'html.parser')
                            print(soup.get_text())
                            print(response_.status_code)
                            # time.sleep(100)


                            viewstate = get_viewstate(soup)
                            eventvalidation = get_eventvalidation(soup)
                            if viewstate and eventvalidation:
                                # print({'viewstate':viewstate,'eventvalidation':eventvalidation}.items())
                                break
                            else:
                                print("viewstate/eventvalidation extraction failed. Retrying in 120 secs.")
                                print(f"viewstate:{viewstate}, eventvalidation:{eventvalidation}")
                                time.sleep(120)
                                continue




                        
                        data1 = {
                            "__EVENTTARGET": f"ctl00$MainContent$UCCSearchMethod{uccsearch}",
                            "__EVENTARGUMENT": "",
                            "__LASTFOCUS": "",
                            "__VIEWSTATE": f"{viewstate}",
                            "__VIEWSTATEGENERATOR": "CB1FA542",
                            "__EVENTVALIDATION": f"{eventvalidation}",
                            "ctl00$MainContent$UccSearch": f"rdoSearch{uccsearch}",
                            "ctl00$MainContent$txtLastName": f"{char.lower()}{char2.lower()}{char3.lower()}" if "I" in uccsearch else "",
                            "ctl00$MainContent$txtFirstName": "",
                            "ctl00$MainContent$txtMiddleName": "",
                            "ctl00$MainContent$txtSuffix": "",
                            f"ctl00$MainContent$txt{uccsearch}City": "",
                            f"ctl00$MainContent$cbo{uccsearch}State": "",
                            "ctl00$MainContent$txtName": f"{char.lower()}{char2.lower()}{char3.lower()}" if "O" in uccsearch else "",
                            "ctl00$MainContent$txtFilingNumber": "",
                            f"ctl00$MainContent$UCCSearchMethod{uccsearch}": "B",
                            "ctl00$MainContent$txtStartDate": "",
                            "ctl00$MainContent$chkDebtor": "on",
                            "ctl00$MainContent$UCCSearchMethod": "B",
                            "ctl00$MainContent$ddRecordsPerPage": "100000",
                            "ctl00$MainContent$btnSearch": "Search",
                            "ctl00$MainContent$HiddenSearchOption_SearchLapsed": "False"
                        }

                        # Send post requests with data param
                        try:

                            while True:
                                response_ = self.session.post(current_url,data=data1)
                                print(response_.status_code)

                                soup = BeautifulSoup(response_.content,'html.parser')
                                # Check status code. Retry if it return 403
                                result_text = soup.get_text()
                                if response_.status_code == 200 or response_.status_code == 302:
                                    print(result_text)

                                    # Retry if captcha or table not found
                                    if 'requests unsuccessful' in result_text.lower() or not soup.find('table'):
                                        continue
                                        
                                    break
                                    
                                else:
                                    print(result_text)
                                    raise Exception("Forbidden.")
                                    
                        except requests.exceptions.ConnectionError:
                            print("Connection failed. Retrying in 20 secs.")
                            time.sleep(20)
                            response_ = self.session.post(current_url,data=data1)
                        except Exception as e:         
                            print(f'Search failed: {e}. Chars: {char}{char2}{char3} search: {uccsearch}. Skipping..')
                            continue

              

                        # Get page results and store
                        if soup:
                            urls = get_page_links(soup)
                        else:
                            # Skip if soup return None
                            print("page soup returns None. Skipping")
                            continue

                        for url in urls:
                            print(f'result url: {self.baseurl}{url}')
                        
                        
                        # scrape info using multithread
                        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                            for i in range(0,len(urls),batch_size):
                                batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                                yield batch_results

        self.save_state('A','A','A','I')
