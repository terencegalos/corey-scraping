import requests, time
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent


# from scraping import name_generator
# from scraping import name_generator_large_file as name_generator
from config.db_config import DB_CONFIG
from scraping import get_us_state
from database.database_handler_california_zip_codes import DatabaseHandler
from database.md_specialty import specialties_dict

class Scraper57:
    def __init__(self):
        
        self.baseurl = 'https://www.dir.ca.gov/databases/dwc/qmestartnew.asp'
        self.searchurl = 'https://www.dir.ca.gov/databases/dwc/qmeN.asp'
        self.table_name = 'scraper57_info'
        
        self.ua = UserAgent()
        print(f"Scraping: {self.baseurl}")
    
    
    def scrape_single(self,url):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }

    
        
        try:
            response = requests.get(f"https://{url}", headers=headers, allow_redirects=True)
        except requests.exceptions.ConnectionError as e:
            print(f'Connecting failed to {url}. Error: {e}\nReconnecting in 20 secs...')
            time.sleep(20)
            response = requests.get(f"https://{url}", headers=headers, allow_redirects=True)
        except requests.exceptions.InvalidURL:
            print("Invalid url")
            return

        # print(response.text)
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'first_name'})['value'] if soup.find(attrs={'name':'first_name'}) else None
        last_name_el = soup.find(attrs={'name':'last_name'})['value'] if soup.find(attrs={'name':'last_name'}) else None
        address_el = soup.find(attrs={'name':'address'})['value'] if soup.find(attrs={'name':'address'}) else None
        city_el = soup.find(attrs={'name':'city'})['value'] if soup.find(attrs={'name':'city'}) else None
        zip_code_el = soup.find(attrs={'name':'zip_code'})['value'] if soup.find(attrs={'name':'zip_code'}) else None
        state = get_us_state.get_state(str(zip_code_el))
        print(state)
        # state_el = soup.select("#state option[selected]")[1].text if len(soup.select("#state")) > 1 else (state if state else 'NA')
        
        
    
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el, last_name_el, address_el, city_el, zip_code_el]):
            return None        
        
        
        # Return the scraped data as dictionary        
        return {
            'first_name' : first_name_el,
            'last_name' : last_name_el,
            'address' : address_el,
            'city' : city_el,
            'state' : state,
            'zip_code' : zip_code_el
        }
        
    
    def scrape_with_zipcodes(self,last_interrupt_zipcode=None,last_interrupt_specialty=None,batch_size=10,num_threads=3):

        db_handler = DatabaseHandler(
                    host=DB_CONFIG['DBHOST'],
                    user=DB_CONFIG['DBUSER'],
                    password=DB_CONFIG['DBPASS'],
                    database=DB_CONFIG['DBNAME'],
                    table_names = ['california_zip_codes']
        )

        zip_codes = db_handler.get_all_codes('california_zip_codes')
        db_handler.close_connection()
        
        results = []
        
        
        def generate_numbers():
            counter = 0
            while True:
                yield counter
                counter += 1
                


        def get_page_results(sp,code,specialty):

            results = [] # store result dictionaries here

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Length": "31",
                "Content-Type": "application/x-www-form-urlencoded",
                # "Cookie": "_ga_69TD0KNT0F=GS1.1.1704731783.1.1.1704733797.0.0.0; _ga=GA1.2.1344870777.1704731783; _ga_9C30LB4KFJ=GS1.1.1704731783.1.1.1704733800.0.0.0; _gid=GA1.2.1457700408.1704731784; _ga_75V2BNQ3DR=GS1.1.1704732099.1.1.1704733752.0.0.0; _gat_gtag_UA_3419582_30=1; _gat_gtag_UA_3419582_2=1; _gat_gtag_UA_5092920_1=1",
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
            }

            data = {
                "scode": f"{sp}",
                "radius": "9999",
                "zip": f"{code}"
            }

            # send post requests
            response  = requests.post(self.searchurl,headers=headers,data=data)

            print(f'status code: {response.status_code}')

            # use beautifulsoup to parse html
            soup = BeautifulSoup(response.text,'html.parser')

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
                print(tr.contents)

                row_result.update({'name':" ".join(row_tds[0].get_text().split())})
                row_result.update({'address':" ".join(row_tds[1].get_text().split())})
                row_result.update({'phone':" ".join(row_tds[2].get_text().split())})
                try:
                    row_result.update({'miles':" ".join(row_tds[3].get_text().split())})
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
        last_interrupt_zip_index = zip_codes.index(last_interrupt_zipcode)
        last_interrrupt_sp_index = sp_keys.index(last_interrupt_specialty)

        for code in zip_codes[last_interrupt_zip_index:]: # loop zip codes
            print(f'Current zip: {code}')

            # for sp in sp_keys[last_interrrupt_sp_index:]: # loop specialties
            #     specialty = specialties_dict[sp] # extract value using dictionary key
            #     print(f'Specialty: {specialty}')
            #     batch_results = get_page_results(sp,code,specialty)
            #     yield batch_results

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                args = [(sp,code,specialties_dict[sp]) for sp in list(specialties_dict.keys())[last_interrrupt_sp_index:]]
                futures = [executor.submit(get_page_results,*arg) for arg in args]

                for future in concurrent.futures.as_completed(futures):
                    page_result = future.result()
                    yield page_result

            last_interrrupt_sp_index = 0 # reset sp key index