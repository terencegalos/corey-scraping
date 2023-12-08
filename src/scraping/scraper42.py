import requests, time
import concurrent.futures
from urllib.parse import quote
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from scraping import name_generator_large_file
# from scraping import name_generator
from scraping import get_us_state

class Scraper42:
    def __init__(self):
        
        self.url = 'bhgelite.com/ApplicationA.html?SessionGuid=b1dd4eec-9fd1-44f4-b8f0-1a093e95e2bc'
        self.table_name = 'scraper42_info'
        
        self.ua = UserAgent()
        print(f"Scraping: {self.url}")
    
    
    def scrape_single(self,url):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            # 'Host': 'neemafarhang2.bhgelite.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        }

    
        
        try:
            response = requests.get(f"http://{url}", headers=headers, allow_redirects=True)
            print(f'status code:{response.status_code}')
        except requests.exceptions.RequestException as e:
            if isinstance(e,requests.exceptions.ConnectionError):
                print(f'Connecting failed to {url}. Error: {e}')
                return None
            elif isinstance(e,requests.exceptions.HTTPError):
                print(f'Connecting failed to {url}. Error: {e}\nReconnecting in 20 secs...')
                time.sleep(20)
                response = requests.get(f"http://{url}", headers=headers, allow_redirects=True)
            else:
                print(f'An error occurred:{e}')
                return None

        # print(response.text)
        # print(f'response headers: {response.headers}')
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'firstname'})['value'] if soup.find(attrs={'name':'firstname'}) else None
        middle_name_el = soup.find(attrs={'name':'middlename'})['value'] if soup.find(attrs={'name':'middlename'}) else None
        last_name_el = soup.find(attrs={'name':'lastname'})['value'] if soup.find(attrs={'name':'lastname'}) else None
        email_el = soup.find(attrs={'name':'email'})['value'] if soup.find(attrs={'name':'email'}) else None
        phone_el = soup.find(attrs={'name':'phone'})['value'] if soup.find(attrs={'name':'phone'}) else None
        address_el = soup.find(attrs={'name':'address1'})['value'] if soup.find(attrs={'name':'address1'}) else None
        city_el = soup.find(attrs={'name':'city'})['value'] if soup.find(attrs={'name':'city'}) else None
        zip_code_el = soup.find(attrs={'name':'zip'})['value'] if soup.find(attrs={'name':'zip'}) else None
        print(f'ZIP:{zip_code_el}')
        state = get_us_state.get_state(str(zip_code_el.split("-")[0] if zip_code_el is not None else 'NA'))
        # print(state)
        # state_el = soup.select("#state option[selected]")[1].text if len(soup.select("#state")) > 1 else (state if state else 'NA')
        
        
    
        # Check if any value is None, if yes, return None
        if any(value is None for value in [first_name_el,middle_name_el, last_name_el,email_el, phone_el, address_el, city_el, zip_code_el]):
            return None        
        
        
        # Return the scraped data as dictionary        
        return {
            'first_name' : first_name_el,
            'middle_name' : middle_name_el,
            'last_name' : last_name_el,
            'email' : email_el,
            'phone' : phone_el,
            'address' : address_el,
            'city' : city_el,
            'state' : state,
            'zip_code' : zip_code_el
        }
        
    
    def scrape_with_names(self,batch_size=100,num_threads=3):
        
        names_generator = name_generator_large_file.generate_names()

        # names = name_generator.generate_names()
        # print(f"There {len(names)} names to rotate!")
        results = []
        
        def scrape_single_with_increment(name,num=''):
            base_url = f"{"".join([text.lower().replace("'","") for text in name.split()])}{num if num > 0 else ''}.{self.url}"
            print(f"Base url: {base_url}")
            result = self.scrape_single(base_url)
            return result
        
        def generate_numbers():
            counter = 0
            while True:
                yield counter
                counter += 1
                
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # names = []
            while True:
                try:
                    for name in next(names_generator):
                        # names.append(name)
                        print(name)
                except StopIteration:
                    break
               
            for name in names:
                num_generator = generate_numbers()
                continue_to_next_name = False
                
                while True:
                    futures = [executor.submit(scrape_single_with_increment, name, num) for num in [next(num_generator) for _ in range(3)] ]
                    
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        if result is not None:
                            print(result)
                            results.append(result)

                            # Yield results in batches
                            if len(results) % batch_size == 0:
                                yield results
                                results = []  # Clear the results list after yielding
                        else:
                            print(f'Not available. Stopping...')
                            continue_to_next_name = True
                            break
                        
                    if continue_to_next_name:
                    # if next(num_generator) > 100:
                        break
                        
        # Yield any remaining results
        if results:
            yield result

    def scrape(self):
        yield self.scrape_with_names()