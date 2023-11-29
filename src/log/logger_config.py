import logging

def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler('~/projects/corey-scraping/src/log/scraping.log')
        logging.FileHandler('scraping.log')
        ]
    )