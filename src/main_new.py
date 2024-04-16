import sys,importlib
import schedule
import time

num_scraper = sys.argv[1]

module_name = f'scraping.scraper{num_scraper}'
Scraper = getattr(importlib.import_module(module_name),f'Scraper{num_scraper}')

# from database.database_handler_calbar import DatabaseHandler
from config.db_config_local import DB_CONFIG
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
        DatabaseHandler = getattr(importlib.import_module(f'database.{scraper.db_name}'),'DatabaseHandler') # dynamically import db handler
        
        # Store data in the database
        db_handler = DatabaseHandler(
            host=DB_CONFIG['DBHOST'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            database=DB_CONFIG['DBNAME'],
            table_names = [scraper.table_name]
        )
        
        # Scrape data in batches
        for batch_results in scraper.scrape():
            # Store data in the db
            print("Storing to database......")
            time.sleep(3)
            # print(f'batch results: {batch_results}')
            db_handler.store_data(scraper.table_name,batch_results) # adding db check if result is already in db

        logger.info("Scraping and storing data completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}",exc_info=True)
    finally:
        # Close the db connection
        db_handler.close_connection()
        
# Schedule the job every day
# schedule.every().day.at("00:44").do(main)


# while True:
#     # Run pending tasks
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    main()