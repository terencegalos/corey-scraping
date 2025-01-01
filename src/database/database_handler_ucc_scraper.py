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
        
        
        
        
    def store_data_batch(self,table_name,data_list):
        if not data_list:
            return
        
        print(f"Preparing to store {len(data_list)} records in {table_name}")
        
        # Prepare the SQL string for bulk insert
        placeholders = ','.join(['(%s,%s,%s,%s,DEFAULT)' for _ in data_list])
        
        sql = f"""
        INSERT INTO {table_name} (debtor_name,debtor_address,secured_party_name,secured_party_address,date_time_created)
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
        except mysql.connector.Error as err:
            print(f"Failed to insert data into {table_name}: {err}")
            self.conn.rollback() # Rollback in case of error
        
        
        
        

    def data_exists(self,table_name,data):
        # Create a SQL query that checks if a record exists
        query = f'SELECT 1 FROM {table_name} WHERE debtor_name = %s AND debtor_address = %s AND secured_party_name = %s AND secured_party_address = %s limit 1'

        # Execute the query
        self.cursor.execute(query,(data['debtor_name'],data['debtor_address'],data['secured_party_name'],data['secured_party_address']))

        # Fetch the result 
        result = self.cursor.fetchone()

        # If a record was found, return True. Otherwise, return False.
        return result is not None
    
    
    
    def batch_data_exists(self, table_name,data_list):
        """usage: new_results = db_handler.batch_data_exists(scraper.table_name,batch_results)"""
        if not data_list:
            return 
        
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
        
        # Check which items exist
        return [data for data in data_list if tuple([data[field] for field in ['debtor_name','debtor_address','secured_party_name','secured_party_address']]) not in existing_set]

        
        
    def close_connection(self):
        # Close the db connection
        self.conn.close()