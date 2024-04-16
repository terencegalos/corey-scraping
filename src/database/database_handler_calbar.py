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
                                    name VARCHAR(510),
                                    address VARCHAR(510),
                                    phone VARCHAR(510),
                                    fax VARCHAR(510),
                                    email VARCHAR(510),
                                    website_url VARCHAR(510),
                                    certified_legal_specialty VARCHAR(510),
                                    cls_sections VARCHAR(510),
                                    self_reported_practice_areas VARCHAR(510),
                                    additional_languages_spoken VARCHAR(510),
                                    law_school VARCHAR(510)
                                )
                                ''')
            
        # Commit
        self.conn.commit()
        
    def store_data(self, table_name, data_list):
        print(f"Storing results to database.")
        
        # Insert data into the database with explicit default values
        for data in data_list:
            print(data)
            self.cursor.execute(f'''
                                INSERT INTO {table_name} (name, address, phone, fax, email, website_url, certified_legal_specialty, cls_sections, self_reported_practice_areas, additional_languages_spoken, law_school)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ''', (data['name'], data['address'], data['phone'], data['fax'], data['email'], data['website_url'],data['certified_legal_specialty'],data['cls_sections'], data['self_reported_practice_areas'], data['additional_languages_spoken'], data['law_school']))

        # Commit changes
        self.conn.commit()


    def data_exists(self,table_name,data):
        # Create a SQL query that checks if a record exists
        query = f'SELECT * FROM {table_name} WHERE name = %s AND address = %s AND phone = %s AND email = %s AND website_url = %s'

        # Execute the query
        self.cursor.execute(query,(data['name'],data['address'],data['phone'],data['fax'],data['email'],data['website_url']))

        # Fetch the result 
        result = self.cursor.fetchone()

        # If a record was found, return True. Otherwise, return False.
        return result is not None

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()