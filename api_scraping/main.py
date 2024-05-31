import importlib

from config.db_config import DB_CONFIG
from database.database_handler import DatabaseHandler

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler('scraping.log')
    ]
    )
logger = logging.getLogger(__name__)

# api = sys.argv[1]
api = input("Enter the api: ")
logger.info(f"You entered '{api}'")
route = input("Choose the route: ")
logger.info(f"You chose '{route}'")

module_name = f'scraper.{api.lower()}_scraper'
Scraper = getattr(importlib.import_module(module_name),f'Scrape{route.upper()}')



def main():
    try:

        scraper = Scraper()
        db_handler = DatabaseHandler(
            host = DB_CONFIG['DBHOST'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            database=DB_CONFIG['DBNAME'],
            table=scraper.table_name,
            field_dict=scraper.field_names,
        )

        for result in scraper.run():
            db_handler.store_data(result,scraper.field_names)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        db_handler.close_cursor()
        db_handler.close_connection()


if __name__ == "__main__":
    main()