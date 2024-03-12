import requests, json, time, re
from bs4 import BeautifulSoup
import concurrent.futures
from fake_useragent import UserAgent

# from scraper92_data import data

class Scraper92:




    def __init__(self):
        
        
        # url for index
        self.page_url = 'https://fccprod.servicenowservices.com/rmd?id=rmd_listings'

        # url for api
        self.item_url = 'https://fccprod.servicenowservices.com/api/now/sp/widget/2ba6f55c1b72a89089df9796bc4bcb10?id=rmd_listings'

        self.table_name = 'scraper92_info'        
        self.ua = UserAgent()
        self.session = requests.Session()
        print(f"Scraping: {self.page_url}")
    


   



    
    def scrape(self,batch_size=8,num_threads=3):

        max_length = 1024


        def extract_token(url):

            headers01 = {
                "Host": "fccprod.servicenowservices.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            }

            response_ = self.session.get(url,headers=headers01)
            soup = BeautifulSoup(response_.content,'html.parser')
            head_tag = soup.find('head')
            head_tag_text = head_tag.find_all('script')[3].get_text()
            
            match = re.search(r"g_ck\s*=\s*'([^']*)'", head_tag_text)
            extracted_token = match.group(1)
            
            # print(extracted_token)

            addtl_header = {"X-UserToken" : extracted_token}

            return addtl_header
        




        # Loop url and extract data
        def scrape_single(url):

            token = extract_token(url['url1']) # use url 1 to generate token
            


            headers03 = {
                "Host": "fccprod.servicenowservices.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "x-portal": "ac2856301b92681048c6ed7bbc4bcb27",
                "X-Requested-With": "XMLHttpRequest",
                "X-Transaction-Source": "Interface=Service-Portal,Interface-Type=rmd,Interface-SysID=ac2856301b92681048c6ed7bbc4bcb27",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            }

            self.session.headers.update(token)
            self.session.headers.update(headers03)
            response = self.session.get(url['url2']) # use url 2 with token to extract item data
            # print(response.text)
            result_dict = json.loads(response.text)
            fields_dict = result_dict['result']['containers'][1]['rows'][0]['columns'][0]['widgets'][1]['widget']['data']['f']['_fields']

            # item_dict = {}

            entry_dict = {
                'has_had_investigation': '',
                'country': '',
                'contact_telephone_number': '',
                'business_address': '',
                'voice_role_in_call_path': '',
                'sys_updated_on': '',
                'contact_phone_extension': '',
                'intermediate_provider_role_in_call_path': '',
                'number': '',
                'no_suppress': '',
                'sys_updated_by': '',
                'sys_created_on': '',
                'contact_department': '',
                'intermediate_provider_complete_stir_shaken': '',
                'ocn': '',
                'sys_created_by': '',
                'contact_business_address': '',
                'intermediate_provider_exemption_rule': '',
                'business_name': '',
                'foreign_voice_provider': '',
                'frn': '',
                'e_signature': '',
                'gateway_complete_stir_shaken': '',
                'declaration_date': '',
                'other_dba_names': '',
                'complete_stir_shaken': '',
                'contact_title': '',
                'gateway_provider_exemption_rule': '',
                'gateway_partial_stir_shaken': '',
                'partial_stir_shaken': '',
                'no_stir_shaken': '',
                'voice_service_provider': '',
                'gateway_no_stir_shaken': '',
                'contact_email': '',
                'gateway_role_in_call_path': '',
                'intermediate_provider_partial_stir_shaken': '',
                'intermediate_provider': '',
                'principals_affiliates_subsidiaries': '',
                'voice_service_provider_exemption_rule': '',
                'implementation': '',
                'no_flag': '',
                'robocall_mitigation_contact_name': '',
                'declaration': '',
                'gateway_provider': '',
                'investigation_description': '',
                'previous_dba_names': '',
                'other_frns': '',
                'contact_country': '',
                'intermediate_provider_no_stir_shaken': ''
            }


            for key in fields_dict.keys():

                try:
                    if len(fields_dict[key]['displayValue']) <= max_length:
                        entry_dict.update({key:fields_dict[key]['displayValue']})
                    else:
                        entry_dict.update({key:fields_dict[key]['displayValue'][:max_length]})
                    
                except KeyError:
                    entry_dict.update({key:"N/A"})



            print(entry_dict)
            return entry_dict

        



        # Rotate pages

        for page_num in range(1,1099):

            print(f"Scrape attempt page number: {page_num}")

            urls = []
        

            headers02 = {
                "Host": "fccprod.servicenowservices.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://fccprod.servicenowservices.com/rmd?id=rmd_listings",
                # "x-portal": "ac2856301b92681048c6ed7bbc4bcb27",
                # "X-UserToken": "e989a5dd1bfcc250ce3364a8624bcbf2276159ed51aa3b2b355b23c8f8a989b331c4616e",
                "Content-Type": "application/json;charset=utf-8",
                "X-Transaction-Source": "Interface=Service-Portal,Interface-Type=rmd,Interface-SysID=ac2856301b92681048c6ed7bbc4bcb27",
                "Content-Length": "29208",
                "Origin": "https://fccprod.servicenowservices.com",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                # "Cookie": "JSESSIONID=F40F2CFCADD4A0A33EBE0A61A254D28B; glide_user_route=glide.0aeff4dcc8ad083866dce26782183331; BIGipServerpool_fccprod=528658442.35390.0000"
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }

            data = {
                "active": False,
                "allow_link": "True",
                "color": "default",
                "color_dv": "Default",
                "css": "\n#x61108f231be6649089df9796bc4bcb22 .panel {\n\tpadding: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .panel-title {\n\tfont-size: 32px;\n\tfont-weight: 300;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .table > thead:first-child > tr:first-child > th {\n\tborder-left: 0;\n}\n\n#x61108f231be6649089df9796bc4bcb22 .panel-heading .dropdown-toggle {\n\tdisplay: none;\n}",
                "d": "desc",
                "display_field": "business_address",
                "enable_filter": "False",
                "fields": "",
                "filter": "status=Published^EQ",
                "headerTitle": "Robocall Mitigation Database",
                "hide_header": False,
                "maximum_entries": 8,
                "o": "sys_updated_on",
                "order": -1,
                "order_by": "sys_updated_on",
                "order_direction": "desc",
                "order_direction_dv": "Descending",
                "roles": "public",
                "sessionRotationTrigger": True,
                "show_attachment_link": "True",
                "show_breadcrumbs": False,
                "show_keywords": "True",
                "size": "md",
                "size_dv": "Medium",
                "sp_column": "a9f394611b566c1048c6ed7bbc4bcba2",
                "sp_column_dv": "",
                "sp_page": "rmd_form",
                "sp_page_dv": "rmd_form",
                "sp_widget": "75af76231be6649089df9796bc4bcbdd",
                "sp_widget_dv": "",
                "sys_class_name": "sp_instance_table",
                "sys_class_name_dv": "Instance with Table",
                "sys_name": "Robocall Mitigation Database",
                "sys_tags": "",
                "table": "x_g_fmc_rmd_robocall_mitigation_database",
                "title": "Robocall Mitigation Database",
                "view": "service_portal",
                "widget_parameters": "{\n\t\"show_keywords\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"allow_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"view\": {\n\t\t\"value\": \"service_portal\",\n\t\t\"displayValue\": \"service_portal\"\n\t},\n\t\"show_attachment_link\": {\n\t\t\"value\": \"True\",\n\t\t\"displayValue\": \"True\"\n\t},\n\t\"show_breadcrumbs\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t},\n\t\"hide_header\": {\n\t\t\"value\": False,\n\t\t\"displayValue\": False\n\t}\n}",
                "window_size": "8",
                "p":page_num
            }

    
            


            
                    
            # Extract user token from head tag
            token_header = extract_token(self.page_url)



            # Update headers adding user token
            self.session.headers.update(token_header)



            # Send post requests with data
            response = self.session.post(self.item_url,json=data,headers=headers02)



            # Extract json and convert into dictionary
            result_dict = json.loads(response.content)
            results_list = result_dict['result']['data']['list']
            
            


            # Extract sys id and targetTable to make a url
            for result in results_list:
                
                sys_id = result['sys_id']
                target_table = result['targetTable']

                url_temp1 = f'https://fccprod.servicenowservices.com/rmd?id=rmd_form&table={target_table}&sys_id={sys_id}&view=sp'

                request_param = {
                    'host':'fccprod.servicenowservices.com',
                    'filename': '/api/now/sp/page',
                    'id': 'rmd_form',
                    "table" : f'{target_table}',
                    'sys_id': f'{sys_id}',
                    'view': 'sp',
                    'portal_id': 'ac2856301b92681048c6ed7bbc4bcb27',
                    'request_uri': f'/rmd?id=rmd_form&table={target_table}&sys_id={sys_id}&view=sp'
                }

                'https://fccprod.servicenowservices.com/api/now/sp/page?id=rmd_form&table=x_g_fmc_rmd_robocall_mitigation_database&sys_id=a854c0c51bf6f010544a404fe54bcb08&view=sp&time=1709752285185&portal_id=ac2856301b92681048c6ed7bbc4bcb27&request_uri=%2Frmd%3Fid%3Drmd_form%26table%3Dx_g_fmc_rmd_robocall_mitigation_database%26sys_id%3Da854c0c51bf6f010544a404fe54bcb08%26view%3Dsp'
                url_temp2 = f"https://{request_param['host']}{request_param['filename']}?id={request_param['id']}&table={request_param['table']}&sys_id={request_param['sys_id']}&view={request_param['view']}&portal_id={request_param['portal_id']}&request_uri={request_param['request_uri']}"

                url_dict = {'url1':url_temp1,'url2':url_temp2}
                # print(url_dict)
                urls.append(url_dict)

                # print(urls)








            # scrape_single(urls[1])



            
                    
            
            # scrape info using multithread
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                results = list(executor.map(scrape_single,urls))
                yield results