from scraping.scraper1 import Scraper1
from database.database_handler import DatabaseHandler
from config.db_config import DB_CONFIG
from log.logger_config import configure_logger
import logging


def main():
    
    # Configure logger
    configure_logger()
    logger = logging.getLogger(__name__)
    
    try:
        # Instantiate scraper
        scraper1 = Scraper1()        
        
        # Store data in the database
        db_handler = DatabaseHandler(
            host=DB_CONFIG['DBHOST'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            database=DB_CONFIG['DBNAME']
        )
        
        # Scrape data in batches
        for batch_results in scraper1.scrape_with_refcodes():
            # Store data in the db
            print(batch_results)
            print("Storing batch to database...")
            db_handler.store_data(batch_results)
        
        logger.info("Scraping and storing data completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}",exc_info=True)
    finally:
        # Close the db connection
        db_handler.close_connection()
        
if __name__ == "__main__":
    main()