from database.database_handler_names import DatabaseHandler
from config.db_config import DB_CONFIG
import pandas as pd
from itertools import product

def generate_names(last_interrupted_first=None,last_interrupted_last=None):
        
        db_handler = DatabaseHandler(
             host=DB_CONFIG['DBHOST'],
             user=DB_CONFIG['DBUSER'],
             password=DB_CONFIG['DBPASS'],
             database=DB_CONFIG['DBNAME']
        )

        try:
            first_names = db_handler.read_table('first_names','first_name')
            last_names = db_handler.read_table('last_names','last_name')
            db_handler.close_connection()
        except Exception as e:
            print(f"Reading table failed. (Error): {e}")
            return []
        
        
        start_index = 0
        start_index_last = 0
        if last_interrupted_first:
            try:
                start_index = first_names.index(last_interrupted_first)
                start_index_last = last_names.index(last_interrupted_last)
            except ValueError:
                print(f"Last interrupted name '{last_interrupted_first} {last_interrupted_last}' not found. Starting from the beginning.")
        
        all_name_combinations = [''.join(pair).lower() for pair in list(product(first_names[start_index:],last_names[start_index_last:]))]
        print(f'There are {len(all_name_combinations)} names to loop (plus increments in each).')
        
        return all_name_combinations