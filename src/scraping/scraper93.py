import requests,json
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent
import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Scraper93:


    def __init__(self):
        # https://apps.calbar.ca.gov/attorney/Licensee/Detail/225031
        self.url = f'https://apps.calbar.ca.gov/attorney/Licensee/Detail/'
        self.table_name = "scraper93_info"
        self.db_name = 'database_handler_calbar'
        self.session = requests.Session()
        self.state_json = 'state_scraper93.json'
        self.ua = UserAgent()
        logging.info(f"Scraping: {self.url}")
        self.session.get("https://apps.calbar.ca.gov/attorney/LicenseeSearch/QuickSearch") # get cookies



    def get_headers(self):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': self.ua.random
        }

        return headers

    
    def save_state(self,count):
        with open(self.state_json,'w') as file:
            json.dump({'count':count}, file)


    def load_state(self):
        try:
            with open(self.state_json,'r') as file:
                content = file.read()
                return json.loads(content)
        except FileNotFoundError:
            logging.error("Save state json file not found. Starting count is 1")
            return {'count':1}
        
        
    
    
    
    def scrape_single(self,url,count):
        

        response = self.session.get(f'{url}{count}',headers=self.get_headers())
        logging.info(f'{url}{count}')
        soup = BeautifulSoup(response.text,'html.parser')


        result_dict = {}

        

        if soup:
            result_dict = {
                "name":"",
                "address":"",
                "phone":"",
                "fax":"",
                "email":"",
                "website_url":"",
                "certified_legal_specialty":"",
                "cls_sections":"",
                "self_reported_practice_areas":"",
                "additional_languages_spoken":"",
                "law_school":""           
            }
            
            # detail = soup.select_one('#moduleMemberDetail').contents
            email_obs = soup.select_one('.block > style:nth-child(5)').text
            
            # Split the string by semicolons to get individual rules
            rules = email_obs.split(";")

            # Create a dictionary to store the selectors and their rules
            css_dict = {}
            for rule in rules:
                if "{" in rule:
                    selector, css_rule = rule.split("{")
                    css_dict[selector.strip().replace("}","")] = css_rule.strip("}")
                elif "}" in rule:
                    selector = rule.split("}")[0]
                    css_dict[selector.strip().replace("}","")] = ""

            for item in css_dict:
                if 'inline' in css_dict[item]:
                    email_id = item.strip("#")
                    logging.info(f'Email id : {email_id}')

            


            name = soup.select_one('#moduleMemberDetail > div:nth-child(5) > h3:nth-child(1)').text.strip().splitlines()[0].strip()
            print(name)
                
            try:
                address = soup.select_one("#moduleMemberDetail > div > p:nth-child(1)").text.strip()
            except AttributeError:
                return

            try:
                phone_fax = soup.select_one("#moduleMemberDetail > div > p:nth-child(2)").text
                phone = phone_fax.split("|")[0].split(":")[1].strip()
                fax = phone_fax.split("|")[1].split(":")[1].strip()
            except AttributeError:
                phone = ""
                fax = ""
            except IndexError:
                phone = ""
                fax = ""

            
            try:
                email_url = soup.select_one("#moduleMemberDetail > div > p:nth-child(3)").text
                website_url = email_url.split("|")[1].split(":")[1].strip()
                result_dict.update({"website_url":website_url}) # update dictionary with website
            except AttributeError:
                logging.error(soup.text)
            except IndexError:
                website_url = ""


            try:
                email = soup.find("span",attrs={'id':email_id}).text
            except AttributeError:
                email = ""

            result_dict.update({"name":name,"address":address,"phone":phone,"fax":fax,"email":email})

            # Get more details
            more_fields = ['Certified Legal Specialty','CLA Sections','Self-Reported Practice Areas','Additional Languages Spoken','Law School']

            more_soup = soup.select('#panelMoreDetail-1 > div')
            more_soup.extend(soup.select("#panelMoreDetail-1 > p")) # add div and p elements to more section
            # #panelMoreDetail-1 > div
            for entry_soup in more_soup:
                entry = entry_soup.get_text()
                if ":" in entry:
                    entry_clean = " ".join(entry.split())
                    print(entry_clean)
                    try:
                        key,value = entry_clean.split(":")
                        logging.info({key:value})
                    except ValueError: 
                        # check if there are multiple colons
                        try:
                            key,value1,value2,value3 = entry_clean.split(":")
                            value = ", ".join([value2.split()[0],value3]) # get only the language
                            logging.info({key:(value1,value2.split()[0],value3)})
                        except ValueError:
                            key = entry_clean.split(":")[0]
                            value = entry_clean.split(":")[1]

                    if key.strip() in more_fields:
                        logging.info(f"Field found: {key.strip()}")
                        result_dict.update({"_".join(key.lower().replace("-","_").split()): value.strip()}) # update dictionary if found field

            # save state
            self.save_state(count)
            # print(result_dict)

            return result_dict
            # except AttributeError as e:
            #     return None,e


    
    
    
    def scrape(self,end=999999,batch_size=10,num_threads=20):

        state = self.load_state()
        
        def scrape_single_thread(count):
            logging.info(f"State bar count : {count}")
            results = self.scrape_single(self.url,count)
            logging.info(results)


            if results:
                return results
            return None
        
        # test = scrape_single_thread(state['count'])
        # logging.info(test)
        # raise
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            i = state['count']
        
            while True:
                if i == end: # check count if maximum reached and exit
                    logging.info('Scraper done.')
                    break
                
                batch_results = [sublist for sublist in executor.map(scrape_single_thread, range(i, i+batch_size)) if sublist is not None]# for item in sublist if len(sublist) > 0]
                yield batch_results
                i += batch_size
