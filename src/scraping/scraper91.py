import requests, json
import csv
from requests.cookies import RequestsCookieJar


api_url = 'https://offervault.com/api/offers/search'
baseurl = 'https://offervault.com/'
jar = RequestsCookieJar()
result_dicts_all = []




def num_generator(last_page = 1):
    num = int(last_page)
    while True:
        yield num
        num += 1

def renew_cookies(response):
    print('Renewing cookies...')
    # print(response.cookies.items())
    for name,value in response.cookies.items():
        jar.set(name,value)






##########################
        




page_num_gen = num_generator()


session = requests.Session()



for _ in range(170):
    page_num = next(page_num_gen)

    print("*********************\n")
    print("Scrape attempt for page: ",page_num)
    

    headers0 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "offervault.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
}


    
    headers1 = {
        "Host": "offervault.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "site-identifier": "offervault",
        "Content-Type": "application/json;charset=utf-8",
        "Content-Length": "133",
        "Origin": "https://offervault.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://offervault.com/?selectedTab=topOffers&search=sweepstakes&page=1",
        # "Cookie": "auth.strategy=local; _ga_CQWXR5GZCV=GS1.1.1709624407.1.1.1709625420.60.0.0; _ga=GA1.1.1165994593.1709624408; _redisSessionStore=s%3AA6MzMSJCyOquQgO-AAQt_43-_s3IObky.zNct9nWUQZeg%2BqAkOCDCzbzQeIlmNDpzsDbH%2FU1di%2Bo",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }


    data = {"query":"sweepstakes","page":page_num,"sortBy":"","sortDesc":False,"networks":[],"countries":[],"categories":[],"ppc":False,"mobile":False}

    cookies = {
        "_ga": "GA1.1.1165994593.1709624408",
        "_ga_CQWXR5GZCV": "GS1.1.1709624407.1.0.1709624407.60.0.0",
        "_redisSessionStore": "s:A6MzMSJCyOquQgO-AAQt_43-_s3IObky.zNct9nWUQZeg+qAkOCDCzbzQeIlmNDpzsDbH/U1di+o",
        "auth.strategy": "local"
    }


    response_ = session.get(f"https://offervault.com/?selectedTab=topOffers&search=sweepstakes&page=1",headers=headers0)
    renew_cookies(response_)
    

    response = session.post(api_url,json=data,cookies=jar,headers=headers1)
    
    result_dict = json.loads(response.text)
    if 'offers' not in result_dict:
        print("No offers scraped. Saving results to csv...")
        break

    for entry_dict in result_dict['offers']:
        print(entry_dict)
        result_dicts_all.append(entry_dict)










# Specify CSV file name
csvfile = 'offervault_scraper_results.csv'

textfile = 'skipped_results.txt'
skipped_data = []

# Write to CSV file
with open(csvfile,'w',newline='') as file:
    writer = csv.DictWriter(file,fieldnames=result_dicts_all[0].keys())
    writer.writeheader()
    for data in result_dicts_all:
        try:
            writer.writerow(data)
        except:
            skipped_data.append(data)

print("Data has been saved to",csvfile)


if len(skipped_data) > 0:
    with open(textfile,'w') as file:
        for data in skipped_data:
            json_data = json.dumps(data)

    print("Skipped data has been saved to",textfile)

    # if page_num >= 1:
    #     print("breaking...")
    #     break

