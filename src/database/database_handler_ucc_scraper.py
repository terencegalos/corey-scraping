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

    def data_exists(self,table_name,data):
        # Create a SQL query that checks if a record exists
        query = f'SELECT * FROM {table_name} WHERE debtor_name = %s AND debtor_address = %s AND secured_party_name = %s AND secured_party_address = %s'

        # Execute the query
        self.cursor.execute(query,(data['debtor_name'],data['debtor_address'],data['secured_party_name'],data['secured_party_address']))

        # Fetch the result 
        result = self.cursor.fetchone()

        # If a record was found, return True. Otherwise, return False.
        return result is not None

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()