from database.database_handler_names import DatabaseHandler
from config.db_config import DB_CONFIG
from itertools import product,islice


db_handler = DatabaseHandler(
    host=DB_CONFIG['DBHOST'],
    user=DB_CONFIG['DBUSER'],
    password=DB_CONFIG['DBPASS'],
    database=DB_CONFIG['DBNAME']
)
     


def get_first_names(table_name='first_names',col_name='first_name'):

    try:
        first_names = db_handler.read_table(table_name,col_name)
        return first_names
    except Exception as e:
        print(f"Reading table failed. (Error): {e}")
        return []
    




def get_last_names(table_name='last_names',col_name='last_name'):

    try:
        last_names = db_handler.read_table(table_name,col_name)
        return last_names
    except Exception as e:
        print(f"Reading table failed. (Error): {e}")
        return []




def generate_names(last_interrupted_first=None,last_interrupted_last=None):

    print('Getting first names to exclude.')
    old_first_names = get_first_names('first_names_old')
    print('Getting last names to exclude')
    old_last_names = get_last_names('last_names_old')


    # generate names that are not in common names
    first_names = [fname for fname in get_first_names() if fname not in old_first_names]
    last_names = [lname for lname in get_last_names() if lname not in old_last_names]

    # get index of last interrupted names
    start_index_first = 0
    start_index_last = 0
    if last_interrupted_first:
        try:
            start_index_first = first_names.index(last_interrupted_first)
            start_index_last = last_names.index(last_interrupted_last) if last_interrupted_last else 0
        except ValueError:
            print(f"Last interrupted name '{last_interrupted_first} {last_interrupted_last}' not found. Starting from the beginning.")

    # Generate all name combination from first names and last names
    # To manage system resources we loop every first name not everything at once
    for idx in range(start_index_first,len(first_names)):
        batch = [" ".join(name) for name in list(iter(product([first_names[idx]],last_names[start_index_last:])))]
        yield batch