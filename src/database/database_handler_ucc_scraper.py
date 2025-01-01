import mysql.connector


class DatabaseHandler:
    def __init__(self,host,user,password,database,table_names):
        # Connection to the database
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # Create a cursor to interact with the db
        self.cursor = self.conn.cursor(buffered=True)
        
        # Initialize cache for each table
        self.cache = {table:set() for table in table_names}
        
        for table in table_names:        
            # Create a table
            self.cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS {table} (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    debtor_name VARCHAR(255),
                                    debtor_address VARCHAR(255),
                                    secured_party_name VARCHAR(255),
                                    secured_party_address VARCHAR(255),
                                    datetime_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                                ''')
            
        # Commit
        self.conn.commit()
        
        
        
        
    def store_data(self, table_name, data_list):
        for data in data_list:
            print(data)
        
        # Insert data into the database with explicit default values
        for data in data_list:
            self.cursor.execute(f'''
                                INSERT INTO {table_name} (debtor_name, debtor_address, secured_party_name, secured_party_address, datetime_created)
                                VALUES (%s, %s, %s, %s, DEFAULT)
                                ''', (data['debtor_name'], data['debtor_address'], data['secured_party_name'], data['secured_party_address']))

        # Commit changes
        self.conn.commit()
        
        # Update cache after storing data
        for data in data_list:
            self.cache[table_name].add(tuple(data.values()))
        
        
        
        
    def store_data_batch(self,table_name,data_list):
        if not data_list:
            return
        
        print(f"Preparing to store {len(data_list)} records in {table_name}")
        
        # Prepare the SQL string for bulk insert
        placeholders = '(%s,%s,%s,%s,DEFAULT)'
        
        sql = f"""
        INSERT INTO {table_name} (debtor_name, debtor_address, secured_party_name, secured_party_address, datetime_created)
        VALUES {placeholders}
        """
        
        # Flatten the list of dicts to a list of tuples for the query
        flat_data = [(d['debtor_name'],d['debtor_address'],d['secured_party_name'],d['secured_party_address']) for d in data_list]
        
        try:
            # Execute bulk insert
            self.cursor.executemany(sql,flat_data)
            
            # Commit changes - commit in batches if data_list is very large
            self.conn.commit()
            print(f"Successfully inserted {len(data_list)} records into {table_name}")
            
            # Update cache after storing data
            for data in data_list:
                self.cache[table_name].add(tuple(data.values()))
        except mysql.connector.Error as err:
            print(f"Failed to insert data into {table_name}: {err}")
            self.conn.rollback() # Rollback in case of error

        
        
        
        

    def data_exists(self,table_name,data):
        # Check cache first
        data_tuple = tuple(data.values())
        if data_tuple in self.cache[table_name]:
            return True
        
        # If not in cache, check database
        query = f'SELECT 1 FROM {table_name} WHERE debtor_name = %s AND debtor_address = %s AND secured_party_name = %s AND secured_party_address = %s limit 1'

        self.cursor.execute(query,(data['debtor_name'],data['debtor_address'],data['secured_party_name'],data['secured_party_address']))

        result = self.cursor.fetchone()
        
        # Update cache if found in DB
        if result:
            self.cache[table_name].add(data_tuple)

        # If a record was found, return True. Otherwise, return False.
        return result is not None
    
    
    
    def batch_data_exists(self, table_name,data_list):
        """usage: new_results = db_handler.batch_data_exists(scraper.table_name,batch_results)"""
        if not data_list:
            return 
        
        # Check cache first
        new_data = []
        for data in data_list:
            data_tuple = tuple(data.values())
            if data_tuple not in self.cache[table_name]:
                new_data.append(data)
            else:
                self.cache[table_name].add(data_tuple) # Ensure it's in cache if already there in DB
                
        # If all items are in cache, return empty list
        if not new_data:
            return []
        
        # Prepare placeholders for SQL IN clause
        placeholders = ','.join(['(%s,%s,%s,%s)' for _ in data_list])
        
        query = f'''
        SELECT debtor_name, debtor_address,secured_party_name, secured_party_address
        FROM {table_name}
        WHERE (debtor_name, debtor_address, secured_party_name, secured_party_address) IN ({placeholders})
        '''
         
        # Flatten the list of dicts into a list of tuples for the query
        flat_data = [(d['debtor_name'],d['debtor_address'],d['secured_party_name'],d['secured_party_address']) for d in data_list]
        
        self.cursor.execute(query,[item for sublist in flat_data for item in sublist])
        existing = self.cursor.fetchall()
        
        # Convert query results to a set for fast lookup
        existing_set = set(map(tuple, existing))
        
        # Check with items exist and update cache
        new_results = []
        for data in new_data:
            data_tuple = tuple(data.values())
            if data_tuple not in existing_set:
                new_results.append(data)
            else:
                self.cache[table_name].add(data_tuple) # Add to cache if it was in DB but not in our cache initially
        
        # Check which items exist
        # return [data for data in data_list if tuple([data[field] for field in ['debtor_name','debtor_address','secured_party_name','secured_party_address']]) not in existing_set]
        return new_results

        
        
    def close_connection(self):
        # Close the db connection
        self.conn.close()