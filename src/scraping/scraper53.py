import requests,time,subprocess,tempfile,os#execjs, json, re
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
import concurrent.futures
# from scraping import code_generator
from fake_useragent import UserAgent
from string import ascii_uppercase
from config.proxies import proxy_dict

class Scraper53:
    def __init__(self):
        
        self.baseurl = 'https://corp.sec.state.ma.us/'
        self.searchurl = 'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx'
        self.table_name = "scraper53_info"
        # self.session = requests.Session()
        self.jar = RequestsCookieJar()
        self.ua = UserAgent()
        self.extracted_cookies = 'mailer-sessions=s%3A-xmOYnkEUpr5_faMgi-HKzN7AhNZNnUc.fgKPMZ%2B3eKVo%2Br4%2FUUYO%2FyVxUHLjk5Z43CnLjxXq5PU; wc_visitor=78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5; wc_client=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+; wc_client_current=direct+..+none+..++..++..++..++..+https%3A%2F%2Fmobilendloan.com%2F+..+78875-73be57c6-bcd2-cd6c-b8d7-445b47bba2c5+..+'
        print(f"Scraping: {self.baseurl}")



    def renew_cookies(self,response):
        print('Renewing cookies...')
        print(response.cookies.items())
        for name,value in response.cookies.items():
            self.jar.set(name,value)
    
    
    
    def scrape_single(self,url):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'corp.sec.state.ma.us',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        }







        print(f'Extracting doc links from URL: {url}')
        response = requests.get(url,headers=headers, allow_redirects=True)
        print(f'Status code: {response.status_code}')
        print(f'Content: {response.text}')



        # raise for failed requests
        # response.raise_for_status()
        
        # if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(response.content,'html.parser')
        # print(soup.contents)

        # return in no results found
        soup_table = soup.find('table')
        if not soup_table:
            # print(response.text)
            return



        # find all links that contains the info
        info_links = [a.attrs['href'] for a in soup_table.find_all("a") if 'href' in a.attrs and 'selecteddoc' in a.attrs['href'].lower()]

        # print(f'doc links:{info_links}')
        
        results = [] # store results here

        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            # "Cookie": "TS017bf281=0102f3c98045bf1a8fdcb62af56beaf558a84e0a0b599344109ff95baadb34f0ad419e1faf9737cb9024a0540a5eef294ff7a1f42b",
            "Host": "dnr.alaska.gov",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.ua.random
        }

        for link in info_links:
            print(f"Extracting info. URL: {self.searchurl+link}")
            try:
                response = requests.get(self.searchurl+link,headers=header)
            except requests.exceptions.ConnectionError:
                print(f'Connecting failed to url {self.searchurl+link}. Retrying in 20 secs')
                time.sleep(20)
                response = requests.get(self.searchurl+link,headers=header)
                
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table')
            tr_elements = table.find_all('tr')
            # for tr in tr_elements:
            #     print("***")
            #     print(tr.contents)



    
            for tr in tr_elements[1:]:
                # print(tr.contents)
                # print(tr.find('span').get_text())
                
                # define empty result set 
                result_dict = {'debtor_name':'','debtor_address':'','secured_party_name':'','secured_party_address':''}
                # print(result_dict)
                if 'debtor' in tr.find('span').get_text().lower():

                    # get info
                    # print(tr.contents)
                    # print(tr.find_all('td')[1].get_text())
                    debtor_name = " ".join(tr.find_all("td")[1].get_text().split())
                    try:
                        debtor_address = " ".join(tr.find_all("td")[2].get_text().split())
                    except IndexError:
                        debtor_address = 'N/A'
                    result_dict.update({'debtor_name':debtor_name})
                    result_dict.update({'debtor_address':debtor_address})
                elif 'secured' in tr.find('span').get_text().lower():                
                    secured_party_name = " ".join(tr.find_all('td')[1].get_text().split())
                    try:
                        secured_party_address = " ".join(tr.find_all("td")[2].get_text().split())
                    except IndexError:
                        secured_party_address = 'N/A'
                    result_dict.update({'secured_party_name':secured_party_name})
                    result_dict.update({'secured_party_address':secured_party_address})
                    
                    # update all results dict
                    for result_dict in results:
                        result_dict.update({'secured_party_name':secured_party_name})
                        result_dict.update({'secured_party_address':secured_party_address})
                else:
                    pass


                print(result_dict)

                results.append(result_dict)

        return results

        
        
        # Check if any value is None, if yes, return None
        # if any(value is None for value in [name, address, secured_party_name, secured_party_address]):
        #     return None        
            
            
        
            
        # else :
        #     raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    
    
    
    def scrape_with_refcodes(self, batch_size=10, last_interrupt_char='Y',end_char='Z',last_interrupted_page=1):
        
        def get_page_links(soup):
            table = soup.find("table")
            tr_elements = table.find_all('tr')
            
            print(f'tr length: {len(tr_elements)}')
            page_results = [f'{tr.find('a')['href']}' for tr in tr_elements if tr.find('a')]
            return page_results
        
        def num_generator(last_interrupt_page):
            num = last_interrupt_page
            while True:
                yield num
                num += 1
                

        # result = self.scrape_single(self.baseurl)
        # print(f'Sample result: {result}')

        
        # 1 letter search; Loop all uppercase
                
        # Get index of start ascii char
        last_interrupt_char_index = 0
        
        # Get index of end ascii char
        end_char_index = ascii_uppercase.index(end_char)


        if last_interrupt_char:
            print(f'Interruption specified: {last_interrupt_char}\nGetting index..')
            last_interrupt_char_index = ascii_uppercase.index(last_interrupt_char)

        # Start of loop
        for char in ascii_uppercase[last_interrupt_char_index:end_char_index]:
            print(f"Extract search results for '{last_interrupt_char}'")

            headers1 = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'DNT': '1',
                'Host': 'corp.sec.state.ma.us',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Sec-GPC': '1',
                'TE': 'trailers',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            }

            headers2 = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Content-Length': '9183',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'corp.sec.state.ma.us',
                'Origin': 'https://corp.sec.state.ma.us',
                'Referer': 'https://corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            }




            num_gen = num_generator(last_interrupted_page)

            last_interrupted_page = 0 # reset 
            
  

            
            while True:
                num = next(num_gen)
                print(f'Current page:{num}')
                data = {
                        "__LASTFOCUS": "",
                        "__EVENTTARGET": "ctl00$MainContent$UCCSearchMethodI",
                        "__EVENTARGUMENT": "",
                        "__VIEWSTATE": "/wEPDwULLTE0MTkxODA2NTYPZBYCZg9kFgICBg9kFgICAQ9kFhYCAQ9kFgJmD2QWAgIBDw8WAh4EVGV4dAUTVUNDIFB1YmxpYyBTZWFyY2ggIGRkAgMPDxYEHwBlHgdWaXNpYmxlaGRkAgUPZBYCAgEPZBYEAgEPDxYCHwAFakZpbmFuY2luZyBzdGF0ZW1lbnRzIHJlbWFpbiBpbiB0aGlzIFVDQyBpbmZvcm1hdGlvbiBtYW5hZ2VtZW50IHN5c3RlbSB1bnRpbCBhdCBsZWFzdCBvbmUgeWVhciBhZnRlciBsYXBzZS5kZAIFDw8WBB8ABUYgVGhpcyBFeGFjdCBNYXRjaCBTZWFyY2ggaXMgcHJvdmlkZWQgZm9yIGluZm9ybWF0aW9uYWwgcHVycG9zZXMgb25seS4gHwFoZGQCBg8QDxYCHgdDaGVja2VkZ2RkZGQCCQ8WAh4Fc3R5bGUFPndpZHRoOjEwMCU7YmFja2dyb3VuZC1jb2xvcjp3aGl0ZTtib3JkZXItdG9wOjFwdCBzb2xpZCBzaWx2ZXI7FgQCAQ9kFgQCAQ9kFgICAQ8PZBYCHg1hcmlhLXJlcXVpcmVkBQR0cnVlZAICD2QWAgIBDw8WBB4MRXJyb3JNZXNzYWdlBRxSZXF1aXJlZDogZW50ZXIgYSBsYXN0IG5hbWUuHgdFbmFibGVkZ2RkAgIPZBYCAgMPZBYCAgEPEA8WBh4NRGF0YVRleHRGaWVsZAUJU3RhdGVOYW1lHg5EYXRhVmFsdWVGaWVsZAUJU3RhdGVDb2RlHgtfIURhdGFCb3VuZGdkEBU0CkFsbCBTdGF0ZXMHQWxhYmFtYQZBbGFza2EHQXJpem9uYQhBcmthbnNhcwpDYWxpZm9ybmlhCENvbG9yYWRvC0Nvbm5lY3RpY3V0CERlbGF3YXJlFERpc3RyaWN0IG9mIENvbHVtYmlhB0Zsb3JpZGEHR2VvcmdpYQZIYXdhaWkFSWRhaG8ISWxsaW5vaXMHSW5kaWFuYQRJb3dhBkthbnNhcwhLZW50dWNreQlMb3Vpc2lhbmEFTWFpbmUITWFyeWxhbmQNTWFzc2FjaHVzZXR0cwhNaWNoaWdhbglNaW5uZXNvdGELTWlzc2lzc2lwcGkITWlzc291cmkHTW9udGFuYQhOZWJyYXNrYQZOZXZhZGENTmV3IEhhbXBzaGlyZQpOZXcgSmVyc2V5Ck5ldyBNZXhpY28ITmV3IFlvcmsOTm9ydGggQ2Fyb2xpbmEMTm9ydGggRGFrb3RhBE9oaW8IT2tsYWhvbWEGT3JlZ29uDFBlbm5zeWx2YW5pYQxSaG9kZSBJc2xhbmQOU291dGggQ2Fyb2xpbmEMU291dGggRGFrb3RhCVRlbm5lc3NlZQVUZXhhcwRVdGFoB1Zlcm1vbnQIVmlyZ2luaWEKV2FzaGluZ3Rvbg1XZXN0IFZpcmdpbmlhCVdpc2NvbnNpbgdXeW9taW5nFTQAAkFMAkFLAkFaAkFSAkNBAkNPAkNUAkRFAkRDAkZMAkdBAkhJAklEAklMAklOAklBAktTAktZAkxBAk1FAk1EAk1BAk1JAk1OAk1TAk1PAk1UAk5FAk5WAk5IAk5KAk5NAk5ZAk5DAk5EAk9IAk9LAk9SAlBBAlJJAlNDAlNEAlROAlRYAlVUAlZUAlZBAldBAldWAldJAldZFCsDNGdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIKDxYCHwMFS3dpZHRoOjEwMCU7YmFja2dyb3VuZC1jb2xvcjp3aGl0ZTtib3JkZXItdG9wOjFwdCBzb2xpZCBzaWx2ZXI7ZGlzcGxheTpub25lOxYEAgEPZBYCAgIPZBYCAgEPDxYCHwUFJVJlcXVpcmVkOiBlbnRlciBhbiBvcmdhbml6YXRpb24gbmFtZS5kZAICD2QWAgIDD2QWAgIBDxAPFgYfBwUJU3RhdGVOYW1lHwgFCVN0YXRlQ29kZR8JZ2QQFTQKQWxsIFN0YXRlcwdBbGFiYW1hBkFsYXNrYQdBcml6b25hCEFya2Fuc2FzCkNhbGlmb3JuaWEIQ29sb3JhZG8LQ29ubmVjdGljdXQIRGVsYXdhcmUURGlzdHJpY3Qgb2YgQ29sdW1iaWEHRmxvcmlkYQdHZW9yZ2lhBkhhd2FpaQVJZGFobwhJbGxpbm9pcwdJbmRpYW5hBElvd2EGS2Fuc2FzCEtlbnR1Y2t5CUxvdWlzaWFuYQVNYWluZQhNYXJ5bGFuZA1NYXNzYWNodXNldHRzCE1pY2hpZ2FuCU1pbm5lc290YQtNaXNzaXNzaXBwaQhNaXNzb3VyaQdNb250YW5hCE5lYnJhc2thBk5ldmFkYQ1OZXcgSGFtcHNoaXJlCk5ldyBKZXJzZXkKTmV3IE1leGljbwhOZXcgWW9yaw5Ob3J0aCBDYXJvbGluYQxOb3J0aCBEYWtvdGEET2hpbwhPa2xhaG9tYQZPcmVnb24MUGVubnN5bHZhbmlhDFJob2RlIElzbGFuZA5Tb3V0aCBDYXJvbGluYQxTb3V0aCBEYWtvdGEJVGVubmVzc2VlBVRleGFzBFV0YWgHVmVybW9udAhWaXJnaW5pYQpXYXNoaW5ndG9uDVdlc3QgVmlyZ2luaWEJV2lzY29uc2luB1d5b21pbmcVNAACQUwCQUsCQVoCQVICQ0ECQ08CQ1QCREUCREMCRkwCR0ECSEkCSUQCSUwCSU4CSUECS1MCS1kCTEECTUUCTUQCTUECTUkCTU4CTVMCTU8CTVQCTkUCTlYCTkgCTkoCTk0CTlkCTkMCTkQCT0gCT0sCT1ICUEECUkkCU0MCU0QCVE4CVFgCVVQCVlQCVkECV0ECV1YCV0kCV1kUKwM0Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgsPFgIfAwVLd2lkdGg6MTAwJTtiYWNrZ3JvdW5kLWNvbG9yOndoaXRlO2JvcmRlci10b3A6MXB0IHNvbGlkIHNpbHZlcjtkaXNwbGF5Om5vbmU7FgJmD2QWAgICD2QWBAIBDw8WAh8FBSBSZXF1aXJlZDogZW50ZXIgYSBmaWxpbmcgbnVtYmVyLmRkAgMPDxYCHwUFfUZpbGUgTnVtYmVyIG11c3QgYmUgOCBvciAxMiBjaGFyYWN0ZXJzIGxvbmc6ICBleDogOTkxMjM0NTYgZm9yIHByZSBhcnRpY2xlIDkgZmlsaW5ncywgMjAwMDEyMzQ1NjAxIGZvciBwb3N0IEFydGljbGUgOSBmaWxpbmdzZGQCDA8WAh8DBT53aWR0aDoxMDAlO2JhY2tncm91bmQtY29sb3I6d2hpdGU7Ym9yZGVyLXRvcDoxcHQgc29saWQgc2lsdmVyOxYGAgEPZBYCAgEPZBYEAgEPEA8WAh8BaBYCHwMFDWRpc3BsYXk6bm9uZTtkFgFmZAIDDxAPFgIfAWcWAh8DBQ9kaXNwbGF5OmlubGluZTtkFgFmZAICD2QWAgICD2QWAgIBDw8WAh8FBT9JbnZhbGlkIGRhdGUgZm9ybWF0ISAgTm90ZTogdGhlIHZhbGlkIGZvcm1hdCBpcyBpbiBNTS9ERC9ZWVlZLiBkZAIDD2QWAgIBD2QWCgIBDw8WBB8FBTVDaGVjayBhdCBsZWFzdCBvbmUgbmFtZSB0eXBlIHRvIGluY2x1ZGU6IGUuZy46IERlYnRvch8GaGRkAgMPDxYCHwUFNUNoZWNrIGF0IGxlYXN0IG9uZSBuYW1lIHR5cGUgdG8gaW5jbHVkZTogZS5nLjogRGVidG9yZGQCBQ8QDxYEHwJnHwZoZGRkZAIHDxAPFgQfAmgfBmhkZGRkAgkPEA8WBB8CaB8GaGRkZGQCDg8QZGQWAWZkAhIPDxYCHwAFzwIgV2UgaGF2ZSBjaGFuZ2VkIG91ciBkZWZhdWx0IHNlYXJjaCB0byBhbiBBcnRpY2xlIDkgc2VhcmNoLiBBbiBBcnRpY2xlIDkgc2VhcmNoIGlzIGRvbmUgaW4gYWNjb3JkYW5jZSB3aXRoIG91ciBSdWxlcyBhbmQgUmVndWxhdGlvbnMsIDk1MCBDTVIgMTQwLjAwLiBQbGVhc2UgY2xpY2sgYmVsb3cgdG8gcmV2aWV3IHRoZSByZWd1bGF0aW9ucy4gSWYgeW91IGFyZSB1bnN1cmUgb2YgeW91ciBkZWJ0b3IncyBjb3JyZWN0IGxlZ2FsIG5hbWUsIHlvdSBtYXkgYmUgYmVzdCBzZXJ2ZWQgdG8gcnVuIGEgJ2JlZ2lucyB3aXRoJyBzZWFyY2ggZmlyc3QgdG8gaWRlbnRpZnkgeW91ciBkZWJ0b3IuIGRkAhMPDxYCHwAFtAMgU2VjcmV0YXJ5IEdhbHZpbidzIFVDQyBEaXZpc2lvbiBoYXMgYWRkZWQgYSBuZXcgc2VhcmNoIGZ1bmN0aW9uLCBmb3IgaW5mb3JtYXRpb25hbCBwdXJwb3Nlcy4gVGhlIGluZm9ybWF0aW9uYWwgRXhhY3QgTWF0Y2ggU2VhcmNoIGFsbG93cyBzZWFyY2hlcnMgdG8gc2VhcmNoIGFuIG9yZ2FuaXphdGlvbmFsIG5hbWUgZXhhY3RseSwgaW5jbHVkaW5nIGl0cyBjb3Jwb3JhdGUgZW5kaW5nLiBOb2lzZSB3b3JkcyAoc3VjaCBhcyAnQ29ycG9yYXRpb24nLCAnQ29ycC4nLCAnTGltaXRlZCBMaWFiaWxpdHkgQ29tcGFueScsIG9yICdMTEMnKSBhcmUgbm90IGlnbm9yZWQgYnkgdGhlIEV4YWN0IE1hdGNoIHNlYXJjaCBsb2dpYywgaXQgYXBwbGllcyB0aGUgbG9naWMgZGVmaW5lZCBpbiA5NTAgQ01SIDE0MC40OSwgd2l0aCB0aGUgZXhjZXB0aW9uIG9mIDE0MC40OSg1KS4gZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgUFHGN0bDAwJE1haW5Db250ZW50JHJkb1NlYXJjaEkFHGN0bDAwJE1haW5Db250ZW50JHJkb1NlYXJjaE8FHGN0bDAwJE1haW5Db250ZW50JHJkb1NlYXJjaE8FHGN0bDAwJE1haW5Db250ZW50JHJkb1NlYXJjaEYFHGN0bDAwJE1haW5Db250ZW50JHJkb1NlYXJjaEZz95OoUMJH+oxwIMOxbPkF5+kmmUd5nb1JvJZ0ki/ZAA==",
                        "__VIEWSTATEGENERATOR": "CB1FA542",
                        "__SCROLLPOSITIONX": "0",
                        "__SCROLLPOSITIONY": "204",
                        "__EVENTVALIDATION": "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",
                        "ctl00$MainContent$UccSearch": "rdoSearchI",
                        "ctl00$MainContent$txtLastName": f"{char}",
                        "ctl00$MainContent$txtFirstName": "",
                        "ctl00$MainContent$txtMiddleName": "",
                        "ctl00$MainContent$txtSuffix": "",
                        "ctl00$MainContent$txtICity": "",
                        "ctl00$MainContent$cboIState": "",
                        "ctl00$MainContent$txtName": "",
                        "ctl00$MainContent$txtOCity": "",
                        "ctl00$MainContent$cboOState": "",
                        "ctl00$MainContent$txtFilingNumber": "",
                        "ctl00$MainContent$UCCSearchMethodI": "B",
                        "ctl00$MainContent$txtStartDate": "",
                        "ctl00$MainContent$UCCSearchMethod": "M",
                        "ctl00$MainContent$ddRecordsPerPage": "100000",
                        "ctl00$MainContent$HiddenSearchOption_SearchLapsed": "False"
                    }

                current_url = self.searchurl

                # Get new cookies
                response = requests.get(current_url,headers=headers1,proxies=proxy_dict,allow_redirects=True)
                self.renew_cookies(response)


                response = requests.post(f'{current_url}',data=data,headers=headers1,cookies=self.jar,allow_redirects=True)

                # response = requests.get(f'{current_url}sysvalue=ORIhMVYRub09EF9n4TWp2YHrUO62ErYNEY2LWxdD8P4',headers=headers1,cookies=self.jar)
                print(response.text)
                print(f'status code: {response.status_code}')
                print(response.headers)

                # self.renew_cookies(response)

                # response = requests.post(current_url,headers=headers1,data=data)
                # print(response.headers)
                # print(response.text)


                # soup = BeautifulSoup(response.content,'html.parser')
                # soup_js = soup.find('script')
                # print(soup_js['src'])
                # response = requests.get(self.baseurl+soup_js['src'])

                # js_code = response.text

                # with tempfile.NamedTemporaryFile(mode='w',delete=False) as temp_file:
                #     temp_file.write(js_code)
                #     temp_file_path = temp_file.name

                # try:
                #     with subprocess.Popen(["node","-e", temp_file_path], stdout=subprocess.PIPE,  text=True) as process:
                #         result, _ = process.communicate()

                #     print(f'result:{result}')
                # finally:
                #     os.remove(temp_file_path)

                time.sleep(100)
                self.renew_cookies(response)

                response = requests.post(current_url,data=data,cookies=self.jar,headers=headers)

                print(f'Scraping entries in url: {current_url}')
                print(f'Status code: {response.status_code}')
                print(response.text)

                time.sleep(100)

                # Get page results
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content,'html.parser')
                

                # Get first page results and store
                urls = get_page_links(soup)

                if len(urls) == 0:
                    print("No more pages found. Exiting.")
                    break
                else:
                    for url in urls:
                        print(f'result url: {url}')
                
                
                # scrape info using multithread
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    for i in range(0,len(urls),batch_size):
                        batch_results = [item for results in executor.map(self.scrape_single,urls[i:i+batch_size]) for item in results]
                        yield batch_results
