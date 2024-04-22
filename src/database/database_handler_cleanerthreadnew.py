import mysql.connector,time

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
                                    phone VARCHAR(255),
                                    line_type VARCHAR(255),
                                    company VARCHAR(255),
                                    registration_status VARCHAR(255)
                                )
                                ''')
            
        # Commit
        self.conn.commit()

        
    def store_data(self, table_name, data):

        print(f"Storing to database: {data}")
        
        # Insert data into the database with explicit default values
        self.cursor.execute(f'''
                            INSERT INTO {table_name} (phone, line_type, company, registration_status)
                            VALUES (%s, %s, %s, %s)
                            ''', (data['Phone Number'], data['Line Type'], data['Company Name'], data['Registration Status']))

        # Commit changes
        self.conn.commit()

    def data_exists(self,table_name,data):
        # Create a SQL query that checks if a record exists
        query = f'SELECT * FROM {table_name} WHERE phone = %s'

        # Execute the query
        self.cursor.execute(query,(data['phone'],))

        # Fetch the result 
        result = self.cursor.fetchone()

        # If a record was found, return True. Otherwise, return False.
        return result is not None

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()