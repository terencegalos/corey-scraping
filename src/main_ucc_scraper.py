import sys,importlib
import schedule
import time
import asyncio
import telegram_notifier.telegram_notifier as notifier



num_scraper = sys.argv[1]

module_name = f'scraping.scraper{num_scraper}'
Scraper = getattr(importlib.import_module(module_name),f'Scraper{num_scraper}')

from database.database_handler_ucc_scraper import DatabaseHandler
from config.db_config_local import DB_CONFIG
from log.logger_config import configure_logger
import logging





def main():
    
    # Configure logger
    configure_logger()
    logger = logging.getLogger(__name__)
    
    try:
        # Instantiate scraper
        scraper = Scraper()
        scraper_name = scraper.__class__.__name__
        
        # Store data in the database
        db_handler = DatabaseHandler(
            host=DB_CONFIG['DBHOST'],
            user=DB_CONFIG['DBUSER'],
            password=DB_CONFIG['DBPASS'],
            database=DB_CONFIG['DBNAME'],
            table_names = [scraper.table_name]
        )
        
        # Get last interrupt txt file value
        with open(scraper.last_interrupt_txt,'r') as f:
            try:
                last_char,last_page = str(f.read()).split("_")
            except ValueError:
                logging.error(f"txt file not found.")
                # set to default if empty txt file
                last_char,last_page = ['A','1']

        # state = scraper.load_state()

            
        # Scrape data in batches
        for batch_results in scraper.scrape_with_refcodes(last_interrupt_char=last_char,starting_page=last_page):
            # Store data in the db
            logger.info(batch_results)
            
            # db_handlermysqld.store_data(scraper.table_name,batch_results)
            new_results = db_handler.batch_data_exists(scraper.table_name,batch_results)
            if new_results:
                logger.info(f"Storing to results to {scraper.table_name}.")
                # db_handler.store_data(scraper.table_name,[result for result in batch_results if not db_handler.data_exists(scraper.table_name,result)]) # adding db check if result is already in db
                db_handler.store_data_batch(scraper.table_name,new_results)
            else:
                logger.info('Nothing new to save.')
        
        # Reset last interrupt txt file once done
        with open(scraper.last_interrupt_txt,'w') as f:
            f.write('')

        logger.info("Scraping and storing data completed successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}",exc_info=True)
        message = f"⚠️ **Notice:** Scraper {scraper_name} has been interrupted. Check error log for details."
        # asyncio.run(notifier.send_telegram_message(message))
        
    finally:
        # Close the db connection
        db_handler.close_connection()



# schedule.every().day.at("10:30").do(main)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

main()
