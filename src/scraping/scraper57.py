import requests, time
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent


# from scraping import name_generator
# from scraping import name_generator_large_file as name_generator
from config.db_config import DB_CONFIG
from config.proxies import proxy_dict
from scraping import get_us_state
from database.database_handler_california_zip_codes import DatabaseHandler
from database.md_specialty import specialties_dict

class Scraper57:
    def __init__(self):
        
        self.baseurl = 'https://www.dir.ca.gov/databases/dwc/qmestartnew.asp'
        self.searchurl_1 = 'https://www.dir.ca.gov/databases/dwc/qmeCRIT.asp'
        self.searchurl = 'https://www.dir.ca.gov/databases/dwc/qmeN.asp'
        self.table_name = 'scraper57_info'
        
        self.ua = UserAgent()
        print(f"Scraping: {self.baseurl}")
    
    
    
    def scrape_with_zipcodes(self,last_interrupt_zipcode=90001,last_interrupt_specialty='ACA',search_by_other=False,batch_size=10,num_threads=3):

        if search_by_other:
            print("Scrape by other criteria.")

        db_handler = DatabaseHandler(
                    host=DB_CONFIG['DBHOST'],
                    user=DB_CONFIG['DBUSER'],
                    password=DB_CONFIG['DBPASS'],
                    database=DB_CONFIG['DBNAME'],
                    table_names = ['california_zip_codes']
        )

        zip_codes = db_handler.get_all_codes('california_zip_codes')
        # print(zip_codes)
        db_handler.close_connection()
        
        results = []
        
        
        def generate_numbers():
            counter = 0
            while True:
                yield counter
                counter += 1
                


        def get_page_results(sp,code,specialty,searchby_other):

            results = [] # store result dictionaries here

            headers_1 = [{
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Length": "31",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "www.dir.ca.gov",
                "Origin": "https://www.dir.ca.gov",
                "Referer": "https://www.dir.ca.gov/databases/dwc/qmestartnew.asp",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "TE": "trailers",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },{
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Length": "38",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "www.dir.ca.gov",
                "Origin": "https://www.dir.ca.gov",
                "Referer": "https://www.dir.ca.gov/databases/dwc/qmestartnew.asp",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
            }]



            data_1 = [{
                "scode": f"{sp}",
                "radius": "9999",
                "zip": f"{code}"
            },{
                "first": "",
                "last": "",
                "city": "",
                "zip": f"{code}",
                "scode": f"{sp}"
            }]

            data_arg = data_1[1] if search_by_other else data_1[0]
            header_arg = headers_1[0] if search_by_other else headers_1[0]
            url_arg = self.searchurl_1 if search_by_other else self.searchurl

            # send post requests
            response  = requests.post(url_arg,headers=header_arg,data=data_arg,proxies=proxy_dict)

            print(f'status code: {response.status_code}')

            # use beautifulsoup to parse html
            soup = BeautifulSoup(response.text,'html.parser')
            print(soup.get_text())
            time.sleep(1)

            # find table to extract results
            table = soup.find('table')
            tr_soup = table.find_all('tr')

            # loop all rows and extract info one by one
            for tr in tr_soup[1:]:


                # store extracted info in this dictionary
                row_result = {
                    'name':'',
                    'address':'',
                    'phone':'',
                    'miles':'',
                    'discipline':'',
                    'specialty':specialty,
                    'zip_code':code
                    }
                
                # print(tr.contents)
                row_tds = tr.find_all('td')
                
                # if searchby_other is used check for empty phone value and return (means empty results)
                if searchby_other:
                    try:
                        row_tds[3].get_text()
                    except IndexError:
                        print("Empty result found. Skipping")
                        continue
                
                print(tr.contents)

                row_result.update({'name':" ".join(row_tds[0].get_text().split())})
                row_result.update({'address':" ".join(row_tds[1].get_text().split()) if not searchby_other else " ".join(row_tds[2].get_text().split())})
                row_result.update({'phone':" ".join(row_tds[2].get_text().split()) if not searchby_other else " ".join(row_tds[3].get_text().split())})
                try:
                    row_result.update({'miles':" ".join(row_tds[3].get_text().split()) if not searchby_other else ""})
                except IndexError:
                    print('Miles value missing. Keep empty value.')
                try:
                    row_result.update({'discipline':" ".join(row_tds[4].get_text().split())})
                except IndexError:
                    print('Discipline value missing. Keep empty value.')

                print(row_result)
                results.append(row_result)

            return results
                

        sp_keys = list(specialties_dict.keys())
        last_interrupt_zip_index = zip_codes.index(str(last_interrupt_zipcode))
        last_interrrupt_sp_index = sp_keys.index(last_interrupt_specialty)

        for code in zip_codes[last_interrupt_zip_index:]: # loop zip codes
            print(f'Current zip: {code}')

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                args = [(sp,code,specialties_dict[sp]) for sp in list(specialties_dict.keys())[last_interrrupt_sp_index:]]
                futures = [executor.submit(get_page_results,*arg+(search_by_other,)) for arg in args]

                for future in concurrent.futures.as_completed(futures):
                    page_result = future.result()
                    yield page_result

            last_interrrupt_sp_index = 0 # reset sp key index