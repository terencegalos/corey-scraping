import sys,importlib

num_scraper = sys.argv[1]
module_name = f'scraping.scraper{num_scraper}'
Scraper = getattr(importlib.import_module(module_name),f'Scraper{num_scraper}')


# from database.database_handler_local import DatabaseHandler
from database.database_handler_bhgelite import DatabaseHandler
from config.db_config_local import DB_CONFIG
# from config.db_config import DB_CONFIG
from log.logger_config import configure_logger
import logging


def main():
    
    # Configure logger
    configure_logger()
    logger = logging.getLogger(__name__)

    last_sent_refcode = None
    
    try:
        # Instantiate scraper
        scraper = Scraper()
        
        # Store data in the database
        db_handler = DatabaseHandler(
            host=DB_CONFIG['DBHOST'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            database=DB_CONFIG['DBNAME'],
            table_names = [scraper.table_name]
        )
        
        # Scrape data in batches
        # for batch_results in scraper.scrape_with_refcodes():
        for batch_results in scraper.scrape_with_names():
        # for batch_results in scraper.scrape():
            # Store data in the db
            print(batch_results,scraper.table_name)
            print("Storing batch to database...")
            if len(batch_results) == 0:
                print("Empty batch results. Skipping...")
                continue
            db_handler.store_data(scraper.table_name,batch_results)
        
        logger.info("Scraping and storing data completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}",exc_info=True)
        print(f'Last sent refcode before the error: {last_sent_refcode}')
    finally:
        # Close the db connection
        db_handler.close_connection()
        
if __name__ == "__main__":
    main()