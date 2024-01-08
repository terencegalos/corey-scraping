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
        self.cursor = self.conn.cursor()
        
        for table in table_names:        
            # Create a table
            self.cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS {table} (
                                    name VARCHAR(255),
                                    address VARCHAR(255),
                                    phone VARCHAR(255),
                                    miles VARCHAR(255),
                                    discipline VARCHAR(255),
                                    specialty VARCHAR(255),
                                    zip_code VARCHAR(255)
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
                                INSERT INTO {table_name} (name, address, phone, miles, discipline, specialty, zip_code)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ''', (data['name'], data['address'], data['phone'], data['miles'],data['discipline'],data['specialty'],data['zip_code']))


        # Commit changes
        self.conn.commit()

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()