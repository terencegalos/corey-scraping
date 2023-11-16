# Web Scraping Project

This project involves web scraping data from a website using Python and BeautifulSoup. The main goal is to retrieve information from the website using different reference codes.

## Project Structure

The project is organized into the following structure:

project_name/
|-- src/
    |-- config/
    |-- database/
        |-- init.py
        |-- database_handler.py
    |-- log/
        |-- init.py
        |-- logger_config.py
    |-- scraping/
        |-- init.py
        |-- scraper1.py
    |-- main.py
    |-- refcodes.txt
    |-- requirements.txt
    |-- README.md


## Components

### 1. Scraper1

`scraper1.py` contains the first web scraper class (`Scraper1`) that is designed to extract information from a specific website (`https://mobilendloan.com/`). It includes methods to scrape data using reference codes and handle cases where information is not found.

### 2. Scraper2

`scraper2.py` introduces the second web scraper class (`Scraper2`) for the website `https://myonlineloanpro.com/`. Similar to Scraper1, it includes methods to scrape data using reference codes and handles cases where information is not found. The HTML parsing logic is adjusted to match the structure of the new website.

### 3. Scraper3

`scraper3.py` includes the third web scraper class (`Scraper3`) for the website `https://xmydebt.com/`. This class follows a similar structure to Scraper1 and Scraper2, with methods to scrape data using reference codes and handle cases where information is not found.

### 4. DatabaseHandler

`database_handler.py` includes the `DatabaseHandler` class responsible for handling the database interactions. It supports storing a list of dictionaries into a MySQL database. The database configuration can be customized.

### 5. Logging

`logger_config.py` configures the logging for the project.

### 6. Main Script

`main.py` is the main script that orchestrates the web scraping process. It instantiates the scraper, performs the scraping, and stores the data in the database.

## How to Use

1. Set up your MySQL database and configure the `db_config` in `main.py`.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the `main.py` script to start the web scraping process.

Feel free to customize the project structure and code according to your specific needs.

## Additional Notes

- Adjust the scraping logic and database handling to fit the requirements of other websites.

Happy coding!