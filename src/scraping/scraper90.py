import requests,re
import brotli
import pandas as pd
# from requests_html import HTMLSession
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from fake_useragent import UserAgent
# from string import ascii_uppercase
# from config.proxies import proxy_dict

class Scraper90:
    def __init__(self):
        
        self.baseurl = 'https://www.ispot.tv/'
        self.table_name = "scraper90_info"
        self.last_interrupt_txt = 'last_char_scraper90.txt'
        self.session = requests.Session()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.baseurl}")

        response = self.session.get(self.baseurl)
        # self.renew_cookies(response)



    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)
    
    
    
    def scrape_single(self,url):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "www.ispot.tv",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        }







        print(f'Extracting doc links from URL: {url}')
        # response = requests.get(url,headers=headers,cookies=self.jar)
        response = self.session.get(url,headers=headers)#,cookies=self.jar)
        # print(response.text)
        # content = response.content
        # decompressed_content = brotli.decompress(content)
        # print(f'Decompressed content: {decompressed_content}')
        # print(f'Response headers: {response.headers.items()}')
        print(f'Status code: {response.status_code}')
        # print(f'Content: {decompressed_content.decode('utf-8')}')



        # raise for failed requests
        response.raise_for_status()
        
        # if response.status_code == 200:

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content,'html.parser')#,from_encoding='latin-1')
        # print(soup.get_text())

        parag = soup.find('p',class_='lead')

        brand_info_dict = {'brand':'','industry':'','phone':'','competition':'','airing_number':'','air_ranking':'','spend_ranking':'','social_media':''}
        
        

        text = parag.text

        # Extract brand
        # brand_info = re.search(r'campaigns for (.+). In the past', text)
        brand_info = re.search(r'campaigns for (.*?)(\.| In the past)', text)
        brand = brand_info.group(1) if brand_info else 'NA'
        
        phone = re.search(r'phone at ((\d+[-.]\d+[-.]\d+([-.]\d+)?)|(1-800-[A-Z-]+))', text).group(1) if re.search(r'phone at ((\d+[-.]\d+[-.]\d+([-.]\d+)?)|(1-800-[A-Z-]+))', text) else 'NA'

        # Extract competition brands
        competition_start = text.find('Competition for') + len('Competition for') + len(brand) + len(' includes ')
        competition_end = text.find(' and the other brands in the ')
        competition = ", ".join(text[competition_start:competition_end].split(', ')) if competition_start < competition_end else 'NA'
        
        # Extract industry
        industry_start = text.find('brands in the ') + len('brands in the ')
        industry_end = text.find(' industry')
        industry = text[industry_start:industry_end] if industry_start < industry_end else 'NA'

        # Extract airing number, air ranking, and spend ranking
        airing_info = re.search(r'has had (\d+(,\d+)*)? airings and earned an airing rank of #(\d+(,\d+)*)? with a spend ranking of #(\d+(,\d+)*)?', text)

        if airing_info:
            airing_number = airing_info.group(1)
            air_ranking = airing_info.group(2)
            spend_ranking = airing_info.group(3)
        else:
            airing_number = 'NA'
            air_ranking = 'NA'
            spend_ranking = 'NA'

        # Extract social media links
        social_media_info = re.search(r'(.*You can connect with .+ on .+ or by phone.*)', response.text)
        social_media_links = re.findall(r'<a href="(http[^"]+)"', social_media_info.group(1)) if social_media_info else False
        social_media = ", ".join([link for link in social_media_links]) if social_media_links else 'NA'


        

        brand_info_dict['brand'] = brand
        brand_info_dict['industry'] = industry
        brand_info_dict['phone'] = phone
        brand_info_dict['competition'] = competition
        brand_info_dict['airing_number'] = airing_number
        brand_info_dict['air_ranking'] = air_ranking
        brand_info_dict['spend_ranking'] = spend_ranking
        brand_info_dict['social_media'] = social_media

        print(brand_info_dict)


        return [brand_info_dict]
    
    
    def scrape(self, batch_size=10, last_interrupt_url=None):
        
        def get_page_links(path='/root/corey-scraping/src/database/TV Links.xlsx'):

            # print(os.listdir("/home/terence/Desktop/corey"))

            data = pd.read_excel(path)

            return [row.iloc[0] for index,row in data.iterrows()]

        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

                

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "www.ispot.tv",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        }




        # Get urls from an excel sheet
        urls = get_page_links()

        # print("\n".join(urls))

        result = self.scrape_single(urls[0])
        print(result)
        
        
        # scrape info using multithread
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0,len(urls),batch_size):
                batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                yield batch_results
