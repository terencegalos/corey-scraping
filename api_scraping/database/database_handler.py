import mariadb,json

class DatabaseHandler:
    def __init__(self,host,user,password,database,table,field_dict):
        self.conn = mariadb.connect(
            host=host,
            user=user,
            password=password,
            database=database  
        )
        self.table = table
        self.cursor = self.conn.cursor()
        
        field_definitions = ", ".join([f"{name} {data_type}" for name, data_type in field_dict.items()])

        self.cursor.execute(f'''
                            CREATE TABLE IF NOT EXISTS {table} ({field_definitions})
        ''')

    def store_data(self,data,field_dict):
        # Serialize list fields to JSON strings
        print("Saving to database...")
        data['tags'] = json.dumps(data['tags'])
        data['timeout'] = json.dumps(data['timeout'])
        data['flags'] = json.dumps(data['flags'])
        data['rtp_codec'] = json.dumps(data['rtp_codec'])
        # print(data)

        field_names = ", ".join([key for key in field_dict.keys()])
        placeholders = ", ".join(['%s'] * len(field_dict))
        values = [data.get(key) for key in field_dict.keys()]
        
        query = f"INSERT INTO {self.table} ({field_names}) VALUES ({placeholders})"
        self.cursor.execute(query,values)
        self.conn.commit()

    def close_cursor(self):
        self.cursor.close()

    def close_connection(self):
        self.conn.close()

