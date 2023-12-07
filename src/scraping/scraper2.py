import requests, time
from requests.exceptions import ConnectTimeout
from requests.exceptions import SSLError
from requests.exceptions import HTTPError
from requests.cookies import RequestsCookieJar
from itertools import cycle
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
from scraping import code_generator
from config import proxies

proxies = proxies.proxy_dict

class Scraper2:
    def __init__(self):
        self.url = 'https://myonlineloanpro.com/'
        print(f"Scraping: {self.url}")
        self.table_name = 'scraper2_info'
        self.prefix = 'NA'
        self.ua = UserAgent()
        self.session = requests.Session()
        # self.extracted_cookies = 'mailer-sessions=s%3AuB3PbvKyVRwJqFWh-8ZxfOIfxB_RKcGH.kZc8Aau6zKLPy24aDSW%2F63C1eOwm%2FTCs3ghQJOSgmTA; wc_visitor=78875-a3f785a4-f143-dbcd-e9b1-72d2a0c381d2; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-a3f785a4-f143-dbcd-e9b1-72d2a0c381d2+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-a3f785a4-f143-dbcd-e9b1-72d2a0c381d2+..+'
        self.jar = RequestsCookieJar()        
        self.renew_cookies()
        self.last_time_check = time.time()
    

    def str_to_cookies(self,cookie_str):
        cookies = cookie_str.split(';')
        for cookie in cookies:
            name,value = cookie.strip().split("=")
            self.jar.set(name,value)


    def renew_cookies(self):
        print(f'Renewing cookies...')
        response = self.session.get(self.url)
        print(f'Cookies: {response.cookies.items()}')
        for name,value in response.cookies.items():
            self.jar.set(name,value)


    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/css,*/*;q=0.1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': self.extracted_cookies,
            'Host': 'myonlineloanpro.com',
            # 'If-Modified-Since': 'Tue, 12 Sep 2023 23:46:34 GMT',
            # 'If-None-Match': 'W/"f5-18a8bca20f1"',
            'Referer': 'https://myonlineloanpro.com/',
            # 'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            # 'Sec-Ch-Ua-Mobile': '?0',
            # 'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'style',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.ua.random
        }

        def extract_data(response):
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #Extract relevant data from the HTML using BeautifulSoup methods
            first_name_el = soup.select_one("#firstName")['value'] if soup.select_one("#firstName") else None
            last_name_el = soup.select_one("#lastName")['value'] if soup.select_one("#lastName") else None
            address_el = soup.select_one("#address")['value'] if soup.select_one("#address") else None
            city_el = soup.select_one("#city")['value'] if soup.select_one("#city") else None
            state_el = soup.select("#state option[selected]")[1].text if len(soup.select("#state option[selected]")) > 1 else None
            zip_code_el = soup.select_one("#zipCode")['value'] if soup.select_one("#zipCode") else None
        
        
        
            # Check if any value is None, if yes, return None
            if any(value is None for value in [first_name_el, last_name_el, address_el, city_el, state_el, zip_code_el]):
                return None        
            
            
            # Return the scraped data as dictionary        
            return {
                'first_name' : first_name_el,
                'last_name' : last_name_el,
                'address' : address_el,
                'city' : city_el,
                'state' : state_el,
                'zip_code' : zip_code_el
            }

        # self.str_to_cookies(self.extracted_cookies)

        # Check cookies
        # for cookie in self.jar:
        #     if cookie.expires and cookie.expires < time.time():
        #         self.renew_cookies()
        #         break




        # max_attempts = 5

        # for attempt in range(max_attempts):
        #     try:
        #         response = self.session.post(url, headers=headers,cookies=self.jar, data=data, proxies=proxies, allow_redirects=True)
        #         response.raise_for_status() # Raises a HTTPError if the status if 4xx, 5xx
        #         break
        #     except (ConnectTimeout,ConnectionError,SSLError,HTTPError) as e:
        #         print(f'Connecting to {url} failed. Pausing for 20 sec before reconnecting...')
        #         time.sleep(1)
        #         if attempt < max_attempts -1:
        #             continue
        #         else:
        #             raise
        # print(response.text)
        
        response = self.session.post(url, headers=headers,cookies=self.jar, proxies=proxies, data=data, allow_redirects=True)
        print(f'Origin: {response.headers.items()}')

        if response.status_code == 201:
        # Parse the HTML content with BeautifulSoup        
            extracted_data = extract_data(response)
            return extracted_data
            
        elif response.status_code == 429:
            print(f'Headers: {response.headers.items()}')
            retry_after = response.headers.get('Retry-After',0)
            remaining_requests = int(response.headers.get('X-RateLimit-Remaining',0))

            if retry_after:
                sleep_time = max(0,int(retry_after)+1)
                print(f'Rate limit exceeded. Waiting for {sleep_time} seconds.')
                time.sleep(sleep_time)

                response = self.session.post(url, headers=headers,cookies=self.jar, data=data, proxies=proxies, allow_redirects=True)

                if response.status_code == 201:
                    print('Request successful after rate limit reset!')
                    data = extract_data(response)
                    return extracted_data
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")
                
            elif remaining_requests == 0:
                reset_time = response.headers.get('X-RateLimit-Reset',0)
                sleep_time = max(0,reset_time - int(time.time())+1)
                print(f'Rate limit exceeded. Waiting for {sleep_time} seconds.')
                time.sleep(sleep_time)

                response = self.session.post(url, headers=headers,cookies=self.jar, data=data, proxies=proxies, allow_redirects=True)

                if response.status_code == 201:
                    print('Request successful after rate limit reset!')
                    data = extract_data(response)
                    return extracted_data
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")
                
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")

        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def scrape_with_refcodes(self,batch_size=100):
            
        refcodes = code_generator.generate_code(289000,1000000,'NA') #207593
        print(f"There are {len(refcodes)} refcodes to rotate!")
        # results = []
        
        def scrape_single_thread(refcode):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            last_sent_refcode = refcode
            result = self.scrape_single(self.url,data)
            print(result)
            if result is not None:
                return result
            else:
                print("Skipping 'None' values.")
                return
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0,len(refcodes),batch_size):
                now = time.time()
                if now-self.last_time_check > 180:
                    print('Cookies expired.')
                    self.renew_cookies()
                    time.sleep(1)
                batch_results = [result for result in executor.map(scrape_single_thread,refcodes[i:i+batch_size]) if result is not None]
                yield batch_results

    def scrape(self):
        yield self.scrape_with_refcodes()