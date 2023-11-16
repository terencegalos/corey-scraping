import requests, time
from bs4 import BeautifulSoup

class Scraper2:
    def __init__(self):
        self.url = 'https://myonlineloanpro.com/'
    
    
    def scrape_single(self,url,data):
        
        headers_1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'mailer-sessions=s%3AefuWHjIcm2344H7VL4PHIQDnP8c8szBH.lScB50CKlSjlZyJFA38E5daKRqY4R4pHsHUI%2BQOgEX8; wc_visitor=78875-0b1f75c7-ab18-5ba1-3d5d-f2e141b81294; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-0b1f75c7-ab18-5ba1-3d5d-f2e141b81294+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmyonlineloanpro.com%2F+..+78875-0b1f75c7-ab18-5ba1-3d5d-f2e141b81294+..+',
            'Origin': 'https://myonlineloanpro.com',
            'Referer': 'https://myonlineloanpro.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        
        response = requests.post(url,headers=headers_1, data=data)
        
        
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            
            print(response.content)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #Extract relevant data from the HTML using BeautifulSoup methods
            # first_name_el = soup.find('div',{'class':'first-name'})
            # last_name_el = soup.find('div',{'class':'last-name'})
            # address_el = soup.find('div',{'class':'address'})
            # city_el = soup.find('div',{'class':'city'})
            # state_el = soup.find('div',{'class':'state'})
            # zip_code_el = soup.find('div',{'class':'zip-code'})
            first_name_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            last_name_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            address_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            city_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            state_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            zip_code_el = soup.select("body > section > div.position-relative > div > div > div > div > div.pt-5.fs-3.text-dark > a")[0]
            
            if first_name_el is not None:
                first_name = first_name_el.text.strip()
            else:
                first_name = 'NA'
                
            if last_name_el is not None:
                last_name = last_name_el.text.strip()
            else:
                last_name = 'NA'
            
            if address_el is not None:
                address = address_el.text.strip()
            else:
                address = 'NA'
                
            if city_el is not None:
                city = city_el.text.strip()
            else:
                city = 'NA'
                
            if state_el is not None:
                state = state_el.text.strip()
            else:
                state = 'NA'
            
            if zip_code_el is not None:
                zip_code = zip_code_el.text.strip()
            else:
                zip_code = 'NA'
            
            
            
            # Return the scraped data as dictionary
            
            return {
                'first_name' : first_name,
                'last_name' : last_name,
                'address' : address,
                'city' : city,
                'state' : state,
                'zip_code' : zip_code
            }
            
        else :
            raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    def scrape_with_refcodes(self,refcodes_file):
        with open(refcodes_file,'r') as file:
            refcodes = [line.strip() for line in file]
            
        results = []
        
        for refcode in refcodes:
            print(f"Refcode : {refcode}")
            data = {'refCode':refcode}
            time.sleep(0.5)
            result = self.scrape_single(self.url,data)
            results.append(result)
            
        return results