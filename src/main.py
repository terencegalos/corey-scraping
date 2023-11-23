# from scraping.scraper1_threading import Scraper1 as Scraper
from scraping.scraper1_threading import Scraper4 as Scraper
# from scraping.scraper2 import Scraper2
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
        for batch_results in scraper.scrape_with_refcodes():
            # Store data in the db
            print(batch_results)
            print("Storing batch to database...")
            db_handler.store_data(scraper.table_name,batch_results)
        
        logger.info("Scraping and storing data completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}",exc_info=True)
    finally:
        # Close the db connection
        db_handler.close_connection()
        
if __name__ == "__main__":
    main()