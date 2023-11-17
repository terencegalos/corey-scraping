import requests, time
from bs4 import BeautifulSoup

class Scraper3:
    def __init__(self):
        print("***Scraping xmydebt.com")
        self.url = 'https://xmydebt.com/'
        # self.url = 'https://c0hcb177.caspio.com/dp/e9ac8000d5813b5789dc4353ad8d'
    
    
    def scrape_single(self,url,data):
        
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Cookie": "_ga_BVE2LD5W7L=GS1.1.1700129947.1.0.1700129947.0.0.0; _ga=GA1.1.1067707445.1700129947; _wpfuj={\"1700129947\":\"https%3A%2F%2Fxmydebt.com%2F%7C%23%7CX%20My%20Debt%7C%23%7C4291\"}; _wpfuuid=fdf05fe9-ff91-484c-85da-57187b32940c",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }


                
        
        # session = HTMLSession()
        # response = session.get(url)
        # response.html.render()
        
        # form_el = response.html.find('#wpforms-form-4251', first=True)
        # inputs = form_el.inputs
        # inputs['wpforms[fields][1]'] = data['refCode']
        
        # response = form_el.submit()
        response = requests.post(url, headers=headers, data=data, allow_redirects=True)
        # print(response.headers)
        # response = requests.post(redirect_url)
        print(response.text)
        
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Extract relevant data from the HTML using BeautifulSoup methods
        first_name_el = soup.find(attrs={'name':'wpforms[fields][1][first]'})['value']
        last_name_el = soup.find(attrs={'name':'wpforms[fields][1][last]'})['value']
        address_el = soup.find(attrs={'name':'wpforms[fields][4][address1]'})['value']
        city_el = soup.find(attrs={'name':'wpforms[fields][4][city]'})['value']
        try:
            state_el = soup.select('select[name="wpforms[fields][4][state]"] option[selected]')[1].text
        except:
            state_el = 'not indicated'
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