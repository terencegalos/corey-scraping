import requests, time, re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# from requests_html import HTMLSession
import concurrent.futures
from fake_useragent import UserAgent

from scraping import code_generator

class Scraper3:
    def __init__(self):
        
        self.url = 'https://xmydebt.com/'
        # self.url = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d?RefCode=RD0000011'
        # self.url = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
        self.table_name = 'scraper3_info'
        self.session = requests.Session()
        self.ua = UserAgent()
        self.extracted_cookie = 'AWSALB=2m8HZWBCTk7XvHr+D4oAg84MSY0oruJ3KXSoFGSUTovL8rhmyAw2u6fO7Iyj9JZRDNNtvDSd42d9w0+95tyT1eTgifCfffcZuV9HjGZsuAElnnTR+jwtvsRsvy2M; AWSALBCORS=2m8HZWBCTk7XvHr+D4oAg84MSY0oruJ3KXSoFGSUTovL8rhmyAw2u6fO7Iyj9JZRDNNtvDSd42d9w0+95tyT1eTgifCfffcZuV9HjGZsuAElnnTR+jwtvsRsvy2M; cbParamList=90T6662Z4CVGSY58JMQOX2MPRU80PX8WHT8ZZEH8W1354A4FH95V2XU4JR8DF5H62Q7F0S7D591F8S6I370YXTBDQ029O63YQL024Z6446O2S2DW875XN366IHM79073; cbCookieAccepted=1'
        self.ua = UserAgent()

        print(self.url)
        
    
    
    def scrape_single(self,url,data):
        
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "c0hcb177.caspio.com",
            "Referer": "https://xmydebt.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua.random
        }





        # session = HTMLSession()
        response = self.session.get(f'{url}?RefCode={data['refCode']}',headers=headers,allow_redirects=True)
        print(response.headers)
        print("***")
        print(response.text)
        
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
        
        
        
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'wpforms[fields][1][first]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][first]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][first]'}).attrs  else None
        last_name_el = soup.find(attrs={'name':'wpforms[fields][1][last]'})['value'] if soup.find(attrs={'name':'wpforms[fields][1][last]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][1][last]'}).attrs else None
        address_el = soup.find(attrs={'name':'wpforms[fields][4][address1]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][address1]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][address1]'}).attrs else None
        city_el = soup.find(attrs={'name':'wpforms[fields][4][city]'})['value'] if soup.find(attrs={'name':'wpforms[fields][4][city]'}) and 'value' in soup.find(attrs={'name':'wpforms[fields][4][city]'}).attrs else None
        state_el = soup.select('select[name="wpforms[fields][4][state]"] option[selected]')[1].text if len(soup.select('select[name="wpforms[fields][4][state]"] option[selected]')) > 1 else None
        zip_code_el = soup.find(attrs={"name":"wpforms[fields][4][postal]"})['value'] if 'value' in soup.find(attrs={"name":"wpforms[fields][4][postal]"}).attrs else None
        
        
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