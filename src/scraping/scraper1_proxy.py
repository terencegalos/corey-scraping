import requests
from bs4 import BeautifulSoup
from scraping import code_generator

class Scraper1:
    def __init__(self):
        self.url = 'https://mobilendloan.com/'
        self.table_name = "scraped_info"
        self.proxies = self.get_proxies()
        self.current_proxy_index = 0
        print(f"Scraping: {self.url}")
        
        
        
    def get_proxies(self):
        # Fetch a list of free proxies from the API
        response= requests.get('https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.json')
        # print(type(response.json()))
        proxies = response.json()
        return [{'http': f'http://{proxy["ip"]}:{proxy["port"]}', 'https': f'https://{proxy["ip"]}:{proxy["port"]}'} for proxy in proxies]
    
    
    
    
    def rotate_proxy(self):
        self.current_proxy_index = (self.current_proxy_index + 1 ) % len(self.proxies)
    
    
    
    
    def scrape_single_with_proxy(self,data):
        proxy = self.proxies[self.current_proxy_index]
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'wc_visitor=78875-8e58ea76-7881-1226-5972-32e0d616e201; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2FSimonYarandiN1+..+78875-8e58ea76-7881-1226-5972-32e0d616e201+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-8e58ea76-7881-1226-5972-32e0d616e201+..+; mailer-sessions=s%3AWFN7pGvX0P106a0mApRed3q3ZalflDV7.rVW67jNjXPTtdy2NT%2BZmoxLKquugeSJAnjdDqDcdFD0',
            'Host': 'mobilendloan.com',
            'Origin': 'https://mobilendloan.com',
            'Referer': 'https://mobilendloan.com/',
            'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }




        try:
            response = requests.post(self.url, headers=headers, data=data, proxies=proxy)
            response.raise_for_status()
            
            # print(response.text)
            # Parse the HTML content with BeautifulSoup
        
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract relevant data from the HTML using BeautifulSoup methods
            first_name_el = soup.select_one("#firstName")['value'] if soup.select_one("#firstName") else None
            last_name_el = soup.select_one("#lastName")['value'] if soup.select_one("#lastName") else None
            address_el = soup.select_one("#address")['value'] if soup.select_one("#address")['value'] else None
            city_el = soup.select_one("#city")['value'] if soup.select_one("#city")['value'] else None
            try:
                state_el = soup.select("#state option[selected]")[1].text
            except IndexError:
                state_el = None
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
        except requests.exceptions.RequestException as e:
            print(f"Error to rotate proxy :{proxy}: {e}")
            self.rotate_proxy()
            
            
            
    
    def scrape_with_refcodes(self,batch_size=100):            
        # refcodes = code_generator.invite_codes_with_prefix # last code before error JO0000013
        refcodes = code_generator.generate_code(53674,222000,'HA')
        print(f"There are {len(refcodes)} refcodes to rotate!")
        results = []
        
        for i, refcode in enumerate(refcodes,start=1):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            # time.sleep(0.3)
            result = self.scrape_single_with_proxy(data)
            print(result)
            if result is not None:
                results.append(result)
                
            else:
                print("Skipping 'None' values.")
            
            # Yield results in batches
            if i % batch_size == 0:
                yield results
                results = [] # clear the results list after yielding

        # Yield any remaining results
        if results:
            yield results
    
    