import pandas as pd
from itertools import product

def generate_names(file_path='/root/projects/corey/src/scraping/CommonFirstandLast.xlsx',last_interrupted=None):
        try:
            df_first_names = pd.read_excel(file_path,sheet_name=0,header=None)
            df_last_names = pd.read_excel(file_path,sheet_name=1,header=None)
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        # Extract names from dataframes
        first_names = df_first_names[0].tolist()
        last_names = df_last_names[0].tolist()
        
        start_index = 0
        if last_interrupted:
            try:
                start_index = first_names.index(last_interrupted) + 1
            except ValueError:
                print(f"Last interrupted name '{last_interrupted}' not found. Starting from the beginning.")
        
        all_name_combinations = [''.join(pair).lower() for pair in list(product(first_names[start_index:],last_names))]
        print(f'There are {len(all_name_combinations)} names to loop (plus increments in each).')
        
        return all_name_combinations