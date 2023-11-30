import requests, time
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
        self.table_name = 'scraper2_info'
        self.prefix = 'NA'
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3AhmqlDOakqu4qpvvxcMLdpdwfcKRVT33Q.Hd%2Bf0A6xIZ53HHdc54oZ5LuBstAdcH4cVVbkAQzBR1A; wc_visitor=78875-380d3f17-fbaa-1a78-0931-f4889472a8c1; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-380d3f17-fbaa-1a78-0931-f4889472a8c1+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-380d3f17-fbaa-1a78-0931-f4889472a8c1+..+'
        self.jar = RequestsCookieJar()
        print(f"Scraping: {self.url}")
    

    def str_to_cookies(self,cookie_str):
        cookies = cookie_str.split(';')
        for cookie in cookies:
            name,value = cookie.strip().split("=")
            self.jar.set(name,value)


    def renew_cookies(self):
        response = requests.get(self.url)
        for name,value in response.cookies.items:
            self.jar.set(name,value)


    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/css,*/*;q=0.1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': self.extracted_cookies,
            'Host': 'myonlineloanpro.com',
            'If-Modified-Since': 'Tue, 12 Sep 2023 23:46:34 GMT',
            'If-None-Match': 'W/"f5-18a8bca20f1"',
            'Referer': 'https://myonlineloanpro.com/',
            'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'style',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.ua.random
        }

        self.str_to_cookies(self.extracted_cookies)

        # Check cookies
        # for cookie in self.jar:
        #     if cookie.expires and cookie.expires < time.time():
        #         self.renew_cookies()
        #         break




                
        
        response = requests.post(url, headers=headers,cookies=self.jar, data=data, proxies=proxies, allow_redirects=True)
        # print(response.text)
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
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
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    def scrape_with_refcodes(self,batch_size=100):
            
        refcodes = code_generator.generate_code(1,200000,'NA')
        print(f"There are {len(refcodes)} refcodes to rotate!")
        # results = []
        
        def scrape_single_thread(refcode):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            result = self.scrape_single(self.url,data)
            print(result)
            if result is not None:
                return result
            else:
                print("Skipping 'None' values.")
                return
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0,len(refcodes),batch_size):
                batch_results = [result for result in executor.map(scrape_single_thread,refcodes[i:i+batch_size]) if result is not None]
                yield batch_results