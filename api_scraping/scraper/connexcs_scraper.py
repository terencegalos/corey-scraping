import requests
import base64
from config import secrets

class ScrapeDID:
    def __init__(self):
        self.api_url = 'https://app.connexcs.com/api/cp/did'
        self.method = 'get'
        self.field_names = {
            "id": "INT",
            "did": "VARCHAR(20)",
            "destination": "VARCHAR(255)",
            "destination_type": "VARCHAR(10)",
            "destination2": "VARCHAR(255)",
            "destination2_type": "VARCHAR(10)",
            "destination3": "VARCHAR(255)",
            "destination3_type": "VARCHAR(10)",
            "customer": "VARCHAR(50)",
            "customer_id": "INT",
            "provider": "VARCHAR(50)",
            "provider_id": "INT",
            "customer_card_id": "INT",
            "customer_card": "VARCHAR(50)",
            "provider_card_id": "INT",
            "provider_card": "VARCHAR(50)",
            "cost": "DECIMAL(10, 2)",
            "cost_currency": "VARCHAR(3)",
            "retail": "DECIMAL(10, 2)",
            "retail_currency": "VARCHAR(3)",
            "tags": "TEXT",  # TEXT is used for storing JSON-like arrays
            "max_duration": "INT",
            "rtp_mode": "VARCHAR(10)",
            "rtp_proxy": "INT",
            "timeout": "TEXT",  # TEXT is used for storing JSON-like arrays
            "package_id": "INT",
            "ftc_reported": "INT",
            "spam_score": "INT",
            "flags": "TEXT",  # TEXT is used for storing JSON-like arrays
            "rtp_codec": "TEXT"  # TEXT is used for storing JSON-like objects
        }
        self.table_name = 'connexcs_did'
        


    def run(self):
        print(f'Scraping {self.api_url}')
        session = requests.Session()
        session.auth = (secrets.username,secrets.password)
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
            # "Authorization": "Basic cmVwb3J0QHZ1bHRpay5jb206a2E4M1VzdGEh",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            # "Postman-Token": "4fe992e3-f201-4d32-8ae5-3485ab0ca3c8",
            "Host": "app.connexcs.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        response = session.get(self.api_url,headers=headers)
        for result in response.json():
            yield result