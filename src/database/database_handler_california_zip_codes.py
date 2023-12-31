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
    


    def get_all_codes(self,table_name):
        self.cursor.execute(f'''
                            SELECT zip_codes from {table_name}
                            ''')
        rows = self.cursor.fetchall()
        result_list = [row[0] for row in rows if row[0] is not None]
        return result_list

        
    def close_connection(self):
        # Close the db connection
        self.conn.close()