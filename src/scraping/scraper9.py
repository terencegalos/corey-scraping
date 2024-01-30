import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent

from scraping import name_generator_large_file as name_generator
from scraping import get_us_state

class Scraper9:
    def __init__(self):
        
        self.url = 'advdebthelp.com'
        self.table_name = 'scraper9_info'
        
        self.ua = UserAgent()
        print(f"Scraping: {self.url}")
    
    
    def scrape_single(self,url):
        
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            # "Host": "jamessmith.advdebthelp.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua.random
        }


    
        
        try:
            response = requests.get(f"http://{url}", headers=headers, allow_redirects=True)
        except requests.exceptions.ConnectionError as e:
            print(f'Connecting failed to {url}. Error: {e}\nReconnecting in 20 secs...')
            time.sleep(20)
            response = requests.get(f"http://{url}", headers=headers, allow_redirects=True)
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
        address_el = soup.find(attrs={'name':'street'})['value'] if soup.find(attrs={'name':'street'}) else None
        city_el = soup.find(attrs={'name':'city'})['value'] if soup.find(attrs={'name':'city'}) else None
        zip_code_el = soup.find(attrs={'name':'zip'})['value'] if soup.find(attrs={'name':'zip'}) else None
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
        
    
    def scrape_with_names(self,batch_size=10,num_threads=3):
        
        names_generator = name_generator.generate_names('caorran','younts')#'/root/projects/corey/src/scraping/CommonFirstandLast.xlsx','David','DAVIS')
        # print(names)
        # print(f"There {len(names)} names to rotate!")
        results = []
        
        def scrape_single_with_increment(name,num=''):
            base_url = f"{"".join([text.lower() for text in name.split()])}{num if num > 0 else ''}.{self.url}"
            print(f"Base url: {base_url}")
            result = self.scrape_single(base_url)
            return result
        
        def generate_numbers():
            counter = 0
            while True:
                yield counter
                counter += 1
                
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
               
            while True:
                try:
                    for name in next(names_generator):
                        num_generator = generate_numbers()
                        continue_to_next_name = False
                        
                        while True:
                            futures = [executor.submit(scrape_single_with_increment, name.replace("'","").replace("/","").replace(")","").replace("(","").replace("[",""), num) for num in [next(num_generator) for _ in range(3)] ]
                            
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
                except StopIteration:
                    print("Scraping successful.")
                    break
                        
        # Yield any remaining results
        if results:
            yield result