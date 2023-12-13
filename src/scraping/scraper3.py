
import requests, time, re
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import concurrent.futures
from fake_useragent import UserAgent
import execjs

from scraping import code_generator

class Scraper3:
    def __init__(self):
<<<<<<< HEAD
        
        self.url = 'xmydebt.com'
        self.url1 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
        self.url2 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?cbqe=QXBwS2V5PWU5YWM4MDAwZDU4MTNiNTc4OWRjNDM1M2FkOGQmanM9dHJ1ZSZjYkVtYkRlcGxveVdpdGg9bmV3X2FzeW5jX2VtYmVkanMmY2JEYXRhcGFnZUFuY2hvcklkPWRwX2FuY2hvcl9pZF84MjIxNDEwMDAwJnBhdGhuYW1lPWh0dHBzOi8vYzBoY2IxNzcuY2FzcGlvLmNvbS9kcC9lOWFjODAwMGQ1ODEzYjU3ODlkYzQzNTNhZDhkJmNiU2NyZWVuV2lkdGg9MTYwMCZjYkVtYlF1ZXJ5U3RyPVJlZkNvZGU9UkQwMDAwMDExJmNiUGFyYW1MaXN0PQ==&cbEmbedTimeStamp=1702325678727'
        # self.bridge = 'https://c0hcb177.caspio.com'
=======
       
        self.url = 'xmydebt.com'
        self.url1 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
        self.url2 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?cbqe=QXBwS2V5PWU5YWM4MDAwZDU4MTNiNTc4OWRjNDM1M2FkOGQmanM9dHJ1ZSZjYkVtYkRlcGxveVdpdGg9bmV3X2FzeW5jX2VtYmVkanMmY2JEYXRhcGFnZUFuY2hvcklkPWRwX2FuY2hvcl9pZF84MjIxNDEwMDAwJnBhdGhuYW1lPWh0dHBzOi8vYzBoY2IxNzcuY2FzcGlvLmNvbS9kcC9lOWFjODAwMGQ1ODEzYjU3ODlkYzQzNTNhZDhkJmNiU2NyZWVuV2lkdGg9MTYwMCZjYkVtYlF1ZXJ5U3RyPVJlZkNvZGU9UkQwMDAwMDExJmNiUGFyYW1MaXN0PQ==&cbEmbedTimeStamp=1702325678727'
>>>>>>> 389b6b38a32bcbcba896cff4de1ac02e38048880
        self.table_name = 'scraper3_info'
        self.session = requests.Session()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        self.extracted_cookie = 'AWSALB=eSL33oCU4aZD0Oj177SUerKd+Up0wKCR1WxPVLHWNyNjE2Leny0CGC5i9pFEl25TjvHcyICE58rL5snqF/j0++w37xDHWl4kF0c+BfPag5rZ33zfgZP/upiGd8RL; AWSALBCORS=eSL33oCU4aZD0Oj177SUerKd+Up0wKCR1WxPVLHWNyNjE2Leny0CGC5i9pFEl25TjvHcyICE58rL5snqF/j0++w37xDHWl4kF0c+BfPag5rZ33zfgZP/upiGd8RL; cbParamList=; cbCookieAccepted=1'

        print(self.url)

    def str_to_cookies(self,cookie_str):
        cookies = cookie_str.split(";")
        for cookie in cookies:
            name,value = cookie.strip().split("=")
            self.jar.set(name,value)

    def renew_cookies(self,response):
        print(f'Renewing cookies...')
        # response = self.session.get(self.url)
        print(f'{response.cookies.items()}')
        for name,value in response.cookies.items():
            self.jar.set(name,value)
   
   
    def scrape_single(self,url,data):

        print(data)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "542",
            "Host": "c0hcb177.caspio.com",
            "Origin": "https://c0hcb177.caspio.com",
            "Referer": f"https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            }
        

        params = {
            'appkey' : 'e9ac8000d5813b5789dc4353ad8d',
            'js' : 'true',
            'cmEmbDeployWith' : 'new_async_embedjs'
        }

       
       

        response = requests.post(f"https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}",params=params,data=data,allow_redirects=True)
        
        print(f'Status code:{response.status_code}')
       

       
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup_content = BeautifulSoup(response.content, 'html.parser')
        soup = soup_content.find('form')


        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find('input',attrs={'name':r'\"EditRecordFirstName\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordFirstName\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordFirstName\"'}).attrs and len(soup.find('input',attrs={'name':r'\"EditRecordFirstName\"'})['value']) > 1  else None
        last_name_el = soup.find('input',attrs={'name':r'\"EditRecordLastName\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordLastName\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordLastName\"'}).attrs  and len(soup.find('input',attrs={'name':r'\"EditRecordLastName\"'})['value']) > 1 else None
        address_el = soup.find('input',attrs={'name':r'\"EditRecordAddress\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordAddress\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordAddress\"'}).attrs and len(soup.find('input',attrs={'name':r'\"EditRecordAddress\"'})['value']) > 1 else None
        city_el = soup.find('input',attrs={'name':r'\"EditRecordCity\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordCity\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordCity\"'}).attrs  and len(soup.find('input',attrs={'name':r'\"EditRecordCity\"'})['value']) > 1 else None
        state_el = soup.find('input',attrs={'name':r'\"EditRecordState\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordState\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordState\"'}).attrs  and len(soup.find('input',attrs={'name':r'\"EditRecordState\"'})['value']) > 1 else None
        zip_code_el = soup.find('input',attrs={'name':r'\"EditRecordZip\"'})['value'].replace('\\','').replace('"','') if soup.find('input',attrs={'name':r'\"EditRecordZip\"'}) and 'value' in soup.find('input',attrs={'name':r'\"EditRecordZip\"'}).attrs and len(soup.find('input',attrs={'name':r'\"EditRecordZip\"'})['value']) > 1 else None

        # print((first_name_el,last_name_el,address_el,city_el,state_el,zip_code_el))
       
       
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el,last_name_el,address_el,city_el,state_el,zip_code_el]):
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
   
    def scrape_with_refcodes(self,batch_size=10):
           
        refcodes = code_generator.generate_code(11,2000000,'RD')
        print(f"There are {len(refcodes)} refcodes to rotate!")
       
        def scrape_single_thread(refcode):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            time.sleep(0.3)
            result = self.scrape_single(self.url,data)
            print(result)
            if result is not None:
                return result
            else:
                print("Skipping 'None' values")
                return
               
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0,len(refcodes),batch_size):
                batch_result = [result for result in executor.map(scrape_single_thread,refcodes[i:i+batch_size]) if result is not None ]
                yield batch_result