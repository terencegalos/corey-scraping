import csv
# import cloudscraper
from requests_html import HTMLSession
import cfscrape
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import random
import logging

from database_handler import DatabaseHandler
from db_config_local import DB_CONFIG

table_name = 'youmail'


# Setting up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# User Agents list for random header generation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    # Add more user agents as needed
]

def get_random_headers():
    return {

        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "75",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "www.youmail.com",
        "Origin": "https://www.youmail.com",
        "Referer": "https://www.youmail.com/home/signup?utm_source=web&utm_medium=button&utm_campaign=header",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers",

        "User-Agent": random.choice(USER_AGENTS),
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",

        
    }


def get_proxies():
    proxies = [
        ("proxy.proxy-cheap.com", "31112", "ursnmj9j", "adIdbZdbAXvr3lwR_country-UnitedStates"),
        ("proxy.proxy-cheap.com", "31112", "yvz44lfj", "f3BDMZJHPgNYntFw_country-UnitedStates"),
        ("24.199.75.16", "31112", "yvz44lfj", "f3BDMZJHPgNYntFw_country-UnitedStates"),
        ("24.199.78.244", "31112", "ursnmj9j", "adIdbZdbAXvr3lwR_country-UnitedStates"),
        
        
        
        
    ]
    return cycle([
        {'http': f"http://{user}:{password}@{ip}:{port}",
         'https': f"http://{user}:{password}@{ip}:{port}"}
        for ip, port, user, password in proxies
    ])

def load_completed_phones(completed_csv):
    try:
        with open(completed_csv, 'r') as file:
            completed = {line.strip().split(',')[0] for line in file}
            logging.info(f"Loaded completed phones, count: {len(completed)}")
            return completed
    except FileNotFoundError:
        logging.info("No completed file found, starting fresh.")
        return set()

def save_completed_phone(completed_csv, phone_number):
    with open(completed_csv, 'a') as file:
        file.write(f"{phone_number},WIRELESS,VERIZON WIRELESS\n")
        file.flush()
    logging.info(f"Saved completed phone number: {phone_number}")


def post_data(phone_number, proxy):
    api_url = "https://www.youmail.com/home/api/signup/signupVerify"
    headers = get_random_headers()
    # Correctly format the phone number to ensure it's a 10-digit string
    formatted_phone_number = f"{int(float(phone_number))}"[-10:]
    json_data = {"accountVerification": {"phoneNumber": formatted_phone_number, "countryCode": "US"}}
    
    # Create a session and scrape Cloudflare-protected website
    session = HTMLSession()
    session.proxies = proxy
    scraper = cfscrape.create_scraper(sess=session)

    # scraper = cloudscraper.create_scraper()
    # scraper.proxies.update(proxy)

    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.youmail.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
    }



    # response_ = scraper.get('https://www.youmail.com/home/signup?utm_source=web&utm_medium=button&utm_campaign=header',headers=headers_1)
    # for cookie in response_.cookies.items():
    #     print(cookie)
    
    try:
        response = scraper.post(api_url, json=json_data, headers=headers, timeout=10)
        logging.debug(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"Response data: {data}")
            reg_status = data['accountVerificationResults'][0]['registrationStatus']
            return reg_status, None
        elif response.status_code in [429, 403]:
            # data = response.text
            # logging.debug(f"Response data: {data}")
            logging.warning("Need to rotate proxy")
            return None, "Rotate proxy and retry."
        else:
            logging.error(f"HTTP error: {response.status_code}, {response.reason}")
            return None, f"HTTP error {response.status_code}, reason: {response.reason}"
    except cloudscraper.exceptions.CloudflareChallengeError as e:
        logging.error(f"Cloudflare challenge error: {e}")
        return None, f"Cloudflare challenge error: {e}"
    except Exception as e:
        logging.error(f"General exception: {e}")
        return None, f"Request exception {e}"

def process_requests(rows, proxy_cycle):
    with ThreadPoolExecutor(max_workers=8) as executor: #40
        future_to_phone = {executor.submit(post_data, row['Phone Number'], next(proxy_cycle)): row for row in rows}
        
        for future in tqdm(as_completed(future_to_phone), total=len(future_to_phone), desc="Processing Requests"):
            row = future_to_phone[future]
            result, error = future.result()
            if result:
                row['Registration Status'] = result
                yield row, None
            else:
                logging.debug(f"Error processing phone {row['Phone Number']}: {error}")
                yield None, error

def write_results(writer, outfile, completed_csv, processed_results,db_handler,table_name):
    for result, error in processed_results:
        if result:
            writer.writerow(result)
            outfile.flush()
            db_handler.store_data(table_name,result)
            save_completed_phone(completed_csv, result['Phone Number'])
        elif error:
            logging.info(error)  # Detailed error log

def process_phone_numbers(input_csv, output_csv, completed_csv, chunk_size=32):#100000
    proxy_cycle = get_proxies()
    
    database_handler = DatabaseHandler(
        host = DB_CONFIG['DBHOST'],
        user = DB_CONFIG['DBUSER'],
        password = DB_CONFIG['DBPASS'],
        database = DB_CONFIG['DBNAME'],
        table_names = [table_name]
    )

    with open(input_csv, mode='r', newline='') as file, open(output_csv, mode='a', newline='') as outfile:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['Registration Status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if outfile.tell() == 0:
            writer.writeheader()

        completed_phones = load_completed_phones(completed_csv)
        batch_number = 0

        while True:
            rows = [row for row, _ in zip(reader, range(chunk_size)) if row['Phone Number'] not in completed_phones]
            if not rows:
                print("Phone numbers already processed.")
                break

            batch_number += 1
            logging.info(f"Starting batch #{batch_number}")
            processed_results = process_requests(rows, proxy_cycle)
            write_results(writer, outfile, completed_csv, processed_results,database_handler,table_name)

        logging.info("Completed processing all batches.")

if __name__ == "__main__":
    logging.info("Script started")
    input_csv = 'output_clean.csv'
    output_csv = 'checked.csv'
    completed_csv = 'completed_phones.csv'
    process_phone_numbers(input_csv, output_csv, completed_csv)
    logging.info("Script finished")
