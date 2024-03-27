import csv
import sys
import mysql.connector
from datetime import datetime,timedelta

from config.db_config import DB_CONFIG


def fetch_data(date):

    # Connect to the MYSQL database

    db = mysql.connector.connect(

        host = DB_CONFIG['DBHOST'],
        user = DB_CONFIG['DBUSER'],
        password = DB_CONFIG['DBPASS'],
        database = DB_CONFIG['DBNAME']

    )

    cursor = db.cursor(dictionary=True)

    results = []




    # Fetch data from each table

    for i in range(48,55):
        table = f"scraper{i}_info"
        query = f"SELECT DISTINCT debtor_name, debtor_address, secured_party_name, secured_party_address, datetime_created FROM {table} WHERE DATE(datetime_created) = %s"
        cursor.execute(query, (date,))
        table_results = cursor.fetchall()

        # Add the source table to each result

        for result in table_results:
            result['source_table'] = table


        results.extend(table_results)

    return results







def write_to_csv(results,filename):
    fieldnames = ['debtor_name', 'debtor_address', 'secured_party_name', 'secured_party_address', 'datetime_created', 'source_table']

    with open(filename,'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f'UCC results saved to csv file {filename}!')
    





# Get yesterday's date

# yesterday = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')

# Get the date from the command-line arguments
date_param = sys.argv[1]



# Generate the filename with the date

filename = f'ucc_results/ucc_scrape_results_{date_param}.csv'

results = fetch_data(date_param)
write_to_csv(results,filename)