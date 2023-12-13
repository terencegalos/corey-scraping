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
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    name VARCHAR(255),
                                    address VARCHAR(255),
                                    secured_party_name VARCHAR(255),
                                    secured_party_address VARCHAR(255),
                                    date_created DATE DEFAULT CURRENT_DATE,
                                    time_created TIME DEFAULT CURRENT_TIME
                                )
                                ''')
            
        # Commit
        self.conn.commit()
        
    def store_data(self,table_name, data_list):
        
        # Insert data into the database
        for data in data_list:
            self.cursor.execute(f'''
                                INSERT INTO {table_name} (name,address,secured_party_name,secure_party_address)
                                VALUES (%s,%s,%s,%s)
                                ''', (data['name'],data['address'], data['secured_party_name'], data['secured_party_address']))

        # Commit changes
        self.conn.commit()
        
    def close_connection(self):
        # Close the db connection
        self.conn.close()