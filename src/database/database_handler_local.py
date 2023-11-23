import mysql.connector

class DatabaseHandler:
    def __init__(self,host,user,password,database):
        # Connection to the database
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # Create a cursor to interact with the db
        self.cursor = self.conn.cursor()
        
        # Create a table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS scraped_info_1 (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                first_name VARCHAR(255),
                                last_name VARCHAR(255),
                                address VARCHAR(255),
                                city VARCHAR(255),
                                state VARCHAR(255),
                                zip_code VARCHAR(20)
                            )
                            ''')
        
        # Commit
        self.conn.commit()
        
    def store_data(self,table_name="scraped_info_1",data_list=[]):
        
        # Insert data into the database
        for data in data_list:
            self.cursor.execute(f'''
                                INSERT INTO scraped_info_1 (first_name,last_name,address,city,state,zip_code)
                                VALUES (%s,%s,%s,%s,%s,%s)
                                ''', (data['first_name'], data['last_name'], data['address'], data['city'], data['state'], data['zip_code']))

        # Commit changes
        self.conn.commit()
        
    def close_connection(self):
        # Close the db connection
        self.conn.close()