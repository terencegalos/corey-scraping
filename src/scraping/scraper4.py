import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent

from scraping import name_generator

class Scraper4:
    def __init__(self):
        
        # https://johnsmith1.moneyladdernow.com
        self.url = 'moneyladdernow.com'
        self.table_name = 'scraper4_info'
        self.ua = UserAgent()
        print(f"Scraping: {self.url}")
    
    
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

    
        
        response = requests.get(f"https://{url}", headers=headers, allow_redirects=True)
        # print(response.text)
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'first_name'})['value'] if soup.find(attrs={'name':'first_name'}) else None
        last_name_el = soup.find(attrs={'name':'last_name'})['value'] if soup.find(attrs={'name':'last_name'}) else None
        address_el = soup.find(attrs={'name':'address'})['value'] if soup.find(attrs={'name':'address'}) else None
        city_el = soup.find(attrs={'name':'city'})['value'] if soup.find(attrs={'name':'city'}) else None
        state_el = soup.select("#state option")[1].text if soup.select("#state") else 'NA'
        zip_code_el = soup.find(attrs={'name':'zip_code'})['value'] if soup.find(attrs={'name':'zip_code'}) else None
        
        
    
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
        
    
    def scrape_with_names(self,batch_size=100,num_threads=3):
        
        names = name_generator.generate_names()
        print(f"There {len(names)} names to rotate!")
        results = []
        
        def scrape_single_with_increment(name,num):
            base_url = f"{"".join([text.lower() for text in name.split()])}{num if num > 0 else ''}.{self.url}"
            print(base_url)
            result = self.scrape_single(base_url)
            return result
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(scrape_single_with_increment,name,count,self.url) for name in names for count in range(3)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                print(result)
                if result is not None:
                    results.append(result)
                    
                    # Yield results in batches
                    if len(results) % batch_size == 0:
                        yield results
                        results = [] # clear results list after yielding
                        
        # Yield any remaining results
        if results:
            yield result
                    
            