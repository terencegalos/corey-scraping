import requests, time
from bs4 import BeautifulSoup

class Scraper1:
    def __init__(self):
        self.url = 'https://mobilendloan.com/'
    
    
    def scrape_single(self,url,data):
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'wc_visitor=78875-8e58ea76-7881-1226-5972-32e0d616e201; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2FSimonYarandiN1+..+78875-8e58ea76-7881-1226-5972-32e0d616e201+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2FSimonYarandiN1+..+78875-8e58ea76-7881-1226-5972-32e0d616e201+..+; mailer-sessions=s%3AaUQteowl9eoH7Ok3vIyxECYhEUSSRVB7.Q7rtDDvCDx3dwDxTqKWF4gliNz7ZAKK1axnTl14sD8A',
            'Host': 'mobilendloan.com',
            'Origin': 'https://mobilendloan.com',
            'Referer': 'https://mobilendloan.com/SimonYarandiN1',
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
        first_name_el = soup.select_one("#firstName")['value']
        last_name_el = soup.select_one("#lastName")['value']
        address_el = soup.select_one("#address")['value']
        city_el = soup.select_one("#city")['value']
        state_el = soup.select("#state option[selected]")[1].text
        zip_code_el = soup.select_one("#zipCode")['value']
        
        if first_name_el is not None:
            first_name = first_name_el
        else:
            first_name = 'NA'
            
        if last_name_el is not None:
            last_name = last_name_el
        else:
            last_name = 'NA'
        
        if address_el is not None:
            address = address_el
        else:
            address = 'NA'
            
        if city_el is not None:
            city = city_el
        else:
            city = 'NA'
            
        if state_el is not None:
            state = state_el
        else:
            state = 'NA'
        
        if zip_code_el is not None:
            zip_code = zip_code_el
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
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
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