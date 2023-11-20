import requests, time
from bs4 import BeautifulSoup
from scraping import code_generator

class Scraper2:
    def __init__(self):
        self.url = 'https://myonlineloanpro.com/'
    
    
    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'wc_visitor=78875-0c5aaef4-6080-ce03-fcef-8a4a88356818; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-0c5aaef4-6080-ce03-fcef-8a4a88356818+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-0c5aaef4-6080-ce03-fcef-8a4a88356818+..+; mailer-sessions=s%3AbCTKFIchsG52c_WfT3_SKFfI74T8jZ9s.m1PoGbhsYYhogSwm92gi5X6QjuYzdY%2Bu76S8iWQpLOs',
            'Host': 'myonlineloanpro.com',
            'Origin': 'https://myonlineloanpro.com',
            'Referer': 'https://myonlineloanpro.com/',
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




                
        
        response = requests.post(url, headers=headers, data=data, allow_redirects=True)
        # print(response.text)
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.select_one("#firstName")['value'] if soup.select_one("#firstName") else None
        last_name_el = soup.select_one("#lastName")['value'] if soup.select_one("#lastName") else None
        address_el = soup.select_one("#address")['value'] if soup.select_one("#address") else None
        city_el = soup.select_one("#city")['value'] if soup.select_one("#city") else None
        state_el = soup.select("#state option[selected]")[1].text if len(soup.select("#state option[selected]")) > 1 else None
        zip_code_el = soup.select_one("#zipCode")['value'] if soup.select_one("#zipCode") else None
        
        # if first_name_el is not None:
        #     first_name = first_name_el
        # else:
        #     first_name = 'NA'
            
        # if last_name_el is not None:
        #     last_name = last_name_el
        # else:
        #     last_name = 'NA'
        
        # if address_el is not None:
        #     address = address_el
        # else:
        #     address = 'NA'
            
        # if city_el is not None:
        #     city = city_el
        # else:
        #     city = 'NA'
            
        # if state_el is not None:
        #     state = state_el
        # else:
        #     state = 'NA'
        
        # if zip_code_el is not None:
        #     zip_code = zip_code_el
        # else:
        #     zip_code = 'NA'
        
        
        
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
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    def scrape_with_refcodes(self,batch_size=100):
        # with open(refcodes_file,'r') as file:
        #     refcodes = [line.strip() for line in file]
            
        refcodes = self.generate_code(6723,30000)
        print(f"There are {len(refcodes)} refcodes to rotate!")
        results = []
        
        for i, refcode in enumerate(refcodes,start=1):
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            time.sleep(0.5)
            result = self.scrape_single(self.url,data)
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