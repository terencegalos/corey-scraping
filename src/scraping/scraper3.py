import requests, time, re
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# from requests_html import HTMLSession
import concurrent.futures
from fake_useragent import UserAgent
import execjs

from scraping import code_generator

class Scraper3:
    def __init__(self):
        
        self.url = 'xmydebt.com'
        self.url1 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
        self.url2 = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?cbqe=QXBwS2V5PWU5YWM4MDAwZDU4MTNiNTc4OWRjNDM1M2FkOGQmanM9dHJ1ZSZjYkVtYkRlcGxveVdpdGg9bmV3X2FzeW5jX2VtYmVkanMmY2JEYXRhcGFnZUFuY2hvcklkPWRwX2FuY2hvcl9pZF84MjIxNDEwMDAwJnBhdGhuYW1lPWh0dHBzOi8vYzBoY2IxNzcuY2FzcGlvLmNvbS9kcC9lOWFjODAwMGQ1ODEzYjU3ODlkYzQzNTNhZDhkJmNiU2NyZWVuV2lkdGg9MTYwMCZjYkVtYlF1ZXJ5U3RyPVJlZkNvZGU9UkQwMDAwMDExJmNiUGFyYW1MaXN0PQ==&cbEmbedTimeStamp=1702325678727'
        # self.bridge = 'https://c0hcb177.caspio.com'
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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "xmydebt.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        }

        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Host": "c0hcb177.caspio.com",
            "Referer": "https://xmydebt.com/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1"
        }

        headers2 = {
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

        
        

        
        # response = self.session.get(f'https://{url}', headers=headers)
        # cookies = response.cookies
        # print(f"get0: {response.status_code}")

        # response = self.session.get(f'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}', headers=headers2)
        # print(f"get1: {response.status_code}")
        # print(response.headers)
        # cookies = response.cookies
        # print(response.text)
        # print(response.headers)

        # response = self.session.post(f'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}', params=params, data=data,headers=headers2,allow_redirects=True)
        # print(f"get2: {response.status_code}")
        # print(response.headers)
        # print(response.text)

        response = requests.get(f"https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d")#?RefCode={data['refCode']}")
        cookies = response.cookies
        response = requests.post(f"https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}",params=params,data=data,cookies=cookies,allow_redirects=True)
        # print(response.text)
        print(f'Status code:{response.status_code}')
        

        # soup = BeautifulSoup(response.text,'html.parser')
        # article_el = soup.find('article')
        # if article_el:
        #     article_content = article_el.get_text()
        #     print(article_content)
        

        
        # soup = BeautifulSoup(response.text,'html.parser')
        # script_src = soup.find('script').get('src')
        # response = requests.post(script_src,headers=headers2,cookies=cookies,data=data,params=params,allow_redirects=True)
        # print(response.headers)


        # cookies = response.cookies

        # response = self.session.post(f'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d',data=data,cookies=cookies,params=params,headers=headers2,allow_redirects=True)
        # print(f"post:0 {response.status_code}")
        # print(response.headers)
        # print(response.text)

        # print(response.text)
        # soup = BeautifulSoup(response.text,'html.parser')

        # script = soup.find("script")
        # script_src = script.get('src')
        # print(f'src: {script_src}')

        # response = self.session.post(script_src,data=data)
        # print(f'post1: {response.status_code}')
        # print(response.text)

        # context = execjs.compile(response.text)
        # result = context.eval(response.text)
        # print(f'Result: {result}')

        # self.renew_cookies(response)
        # self.session.get(f"https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode={data['refCode']}")
        
        # print(f'{url}?RefCode={data['refCode']}')
        # response = requests.post(f'{url}?RefCode={data['refCode']}',allow_redirects=True)
        # print(response.text)
        # print(response.headers)
        
        # soup = BeautifulSoup(response.content,'html.parser')
        # script_tag = soup.find('script')
        # source_value = script_tag.get('src')
        # print(source_value)
        # response = session.get(source_value)
        # print(response.text)
        
        
        # pattern = r"new requestDataPage\('(.*?)', '(.*?)'"
        
        # match = re.search(pattern,response.text)
        
        # if match:
        #     print("Match!")
        #     subdomain = match.group(1)
        #     app_key = match.group(2)
            
        #     url = f"https://{subdomain}/dp/{app_key}?RefCode={data['refCode']}"
        #     print(url)
        #     response = self.session.post(url,headers=headers,allow_redirects=True)
        #     print(response.text)
        
        # Extract infomation using regular expressions
        first_name_el = re.search(r'id="EditRecordFirstName" name="EditRecordFirstName" value="(.*?)"', response.text)
        last_name_el = re.search(r'id="EditRecordLastName" name="EditRecordLastName" value="(.*?)"', response.text)
        address_el = re.search(r'id="EditRecordAddress" name="EditRecordAddress" value="(.*?)"', response.text)
        city_el = re.search(r'id="EditRecordCity" name="EditRecordCity" value="(.*?)"', response.text)
        state_el = re.search(r'id="EditRecordState" name="EditRecordState" value="(.*?)"', response.text)
        zip_code_el = re.search(r'id="EditRecordZip" name="EditRecordZip" value="(.*?)"', response.text)
        
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        # first_name_el = soup.find(attrs={'name':'wpforms[fields][1][first]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][first]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][first]'}).attrs  else None
        # last_name_el = soup.find(attrs={'name':'wpforms[fields][1][last]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][last]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][last]'}).attrs else None
        # address_el = soup.find(attrs={'name':'wpforms[fields][4][address1]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][address1]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][address1]'}).attrs else None
        # city_el = soup.find(attrs={'name':'wpforms[fields][4][city]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][city]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][city]'}).attrs else None
        # state_el = soup.select('select[name="wpforms[fields][4][state]"] option[selected]')[1].text if len(soup.select('select[name="wpforms[fields][4][state]"] option[selected]')) > 1 else None
        # zip_code_el = soup.find(attrs={"name":"wpforms[fields][4][postal]"})['value'] if 'value' in soup.find(attrs={"name":"wpforms[fields][4][postal]"}).attrs else None
        
        
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
    
    def scrape_with_refcodes(self,batch_size=100):
            
        refcodes = code_generator.generate_code(11,20000,'RD')
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
                
        for code in refcodes:
            scrape_single_thread(code)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     for i in range(0,len(refcodes),batch_size):
        #         batch_results = [result for result in executor.map(scrape_single_thread,refcodes[i:i+batch_size]) if result is not None ]
        #         yield batch_results