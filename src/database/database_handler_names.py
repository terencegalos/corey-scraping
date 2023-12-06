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
    

    def read_table(self,table_name,column_name):
        select_query = f'SELECT {column_name} FROM {table_name}'
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        result_list = [row[0] for row in rows]
        return result_list


        
    def close_connection(self):
        # Close the db connection
        self.conn.close()