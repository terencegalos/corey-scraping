from database.database_handler_names import DatabaseHandler
from config.db_config import DB_CONFIG
import pandas as pd
from itertools import product,islice


db_handler = DatabaseHandler(
    host=DB_CONFIG['DBHOST'],
    user=DB_CONFIG['DBUSER'],
    password=DB_CONFIG['DBPASS'],
    database=DB_CONFIG['DBNAME']
)
     


def get_first_names():

    try:
        first_names = db_handler.read_table('first_names','first_name')
        return first_names
    except Exception as e:
        print(f"Reading table failed. (Error): {e}")
        return []
    

def get_last_names():

    try:
        last_names = db_handler.read_table('last_names','last_name')
        return last_names
    except Exception as e:
        print(f"Reading table failed. (Error): {e}")
        return []
    


def generate_names(chunk_size=100):
        
        
        
        first_names = get_first_names()    
        last_names = get_last_names()        
        
        print(f'Generating all name combinations. Please wait...')

        all_name_combinations = []
        # Break up first names into chunks
        for chunk_start in range(0,len(first_names),chunk_size):
            chunk_end = min(chunk_start+chunk_size,len(first_names))
            current_chunk_first_names = first_names[chunk_start:chunk_end]
            
            # Generate batches for the current chunk
            for batch in generate_batches(current_chunk_first_names,last_names):
                name_combinations = [''.join(pair).lower() for pair in batch]
                print(f'{'\n'.join(name_combinations)}')
                all_name_combinations.extend(name_combinations)
            
        print(f'There are {len(all_name_combinations)} names to loop (plus increments in each).')
        
        return all_name_combinations




def generate_batches(first_names,last_names,batch_size=1000,last_interrupted_first=None,last_interrupted_last=None):
    # get index of last interrupted names
    start_index_first = 0
    start_index_last = 0
    if last_interrupted_first:
        try:
            start_index_first = first_names.index(last_interrupted_first)
            start_index_last = last_names.index(last_interrupted_last)
        except ValueError:
            print(f"Last interrupted name '{last_interrupted_first} {last_interrupted_last}' not found. Starting from the beginning.")

    # get names by batch_size until exhausted
    # for chunk in iter(lambda :list(islice(product(first_names[start_index_first:],last_names[start_index_last:]),batch_size)),[]):
    #     yield chunk

    it = iter(product(first_names[start_index_first:],last_names[start_index_last:]))
    while True:
        chunk = list(islice(it,batch_size))
        if not chunk:
            break
        yield chunk