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
                                    brand VARCHAR(255),
                                    industry VARCHAR(255),
                                    phone VARCHAR(20),
                                    competition VARCHAR(255),
                                    airing_number VARCHAR(20),
                                    air_ranking VARCHAR(20),
                                    spend_ranking VARCHAR(20),
                                    social_media VARCHAR(255)
                                )
                                ''')
            
        # Commit
        self.conn.commit()
        
    def store_data(self,table_name, data_list):
        
        # Insert data into the database
        for data in data_list:
            print(data)
            self.cursor.execute(f'''
                                INSERT INTO {table_name} (brand,industry,phone,competition,airing_number,air_ranking,spend_ranking,social_media)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                                ''', (data['brand'],data['industry'], data['phone'], data['competition'], data['airing_number'], data['air_ranking'], data['spend_ranking'], data['social_media']))

        # Commit changes
        self.conn.commit()

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()