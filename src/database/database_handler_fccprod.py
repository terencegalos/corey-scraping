import mysql.connector

class DatabaseHandler:

    def __init__(self, host, user, password, database, table_names):
        # Connection to the database
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # Create a cursor to interact with the db
        self.cursor = self.conn.cursor()

        # Set the session wait_timeout
        self.cursor.execute("SET SESSION wait_timeout = 28800000")

        # Set the session interactive_timeout
        self.cursor.execute("SET SESSION interactive_timeout = 28800000")

        for table in table_names:        
            # Create a table
            self.cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS {table} (
                                    has_had_investigation VARCHAR(255),
                                    country VARCHAR(255),
                                    contact_telephone_number VARCHAR(255),
                                    business_address VARCHAR(255),
                                    voice_role_in_call_path VARCHAR(255),
                                    sys_updated_on VARCHAR(255),
                                    contact_phone_extension VARCHAR(255),
                                    intermediate_provider_role_in_call_path VARCHAR(255),
                                    number VARCHAR(255),
                                    no_suppress VARCHAR(255),
                                    sys_updated_by VARCHAR(255),
                                    sys_created_on VARCHAR(255),
                                    contact_department VARCHAR(255),
                                    intermediate_provider_complete_stir_shaken VARCHAR(1024),
                                    ocn VARCHAR(255),
                                    sys_created_by VARCHAR(255),
                                    contact_business_address VARCHAR(255),
                                    intermediate_provider_exemption_rule VARCHAR(1024),
                                    business_name VARCHAR(255),
                                    foreign_voice_provider VARCHAR(255),
                                    frn VARCHAR(255),
                                    e_signature VARCHAR(255),
                                    gateway_complete_stir_shaken VARCHAR(255),
                                    declaration_date VARCHAR(255),
                                    other_dba_names VARCHAR(255),
                                    complete_stir_shaken VARCHAR(255),
                                    contact_title VARCHAR(255),
                                    gateway_provider_exemption_rule VARCHAR(255),
                                    gateway_partial_stir_shaken VARCHAR(255),
                                    partial_stir_shaken VARCHAR(255),
                                    no_stir_shaken VARCHAR(255),
                                    voice_service_provider VARCHAR(255),
                                    gateway_no_stir_shaken VARCHAR(255),
                                    contact_email VARCHAR(255),
                                    gateway_role_in_call_path VARCHAR(255),
                                    intermediate_provider_partial_stir_shaken VARCHAR(255),
                                    intermediate_provider VARCHAR(255),
                                    principals_affiliates_subsidiaries VARCHAR(1024),
                                    voice_service_provider_exemption_rule VARCHAR(1024),
                                    implementation VARCHAR(255),
                                    no_flag VARCHAR(255),
                                    robocall_mitigation_contact_name VARCHAR(255),
                                    declaration VARCHAR(255),
                                    gateway_provider VARCHAR(255),
                                    investigation_description VARCHAR(1024),
                                    previous_dba_names VARCHAR(255),
                                    other_frns VARCHAR(255),
                                    contact_country VARCHAR(255),
                                    intermediate_provider_no_stir_shaken VARCHAR(255)
                                )
                            ''')

            
        # Commit
        self.conn.commit()
        
    def store_data(self, table_name, data_list):
        # Insert data into the database
        for data in data_list:
            print(f'key count:{len(data.keys())}')
            self.cursor.execute(f'''
                INSERT INTO {table_name} (has_had_investigation, country, contact_telephone_number, business_address, 
                                        voice_role_in_call_path, sys_updated_on, contact_phone_extension, 
                                        intermediate_provider_role_in_call_path, number, no_suppress, sys_updated_by, 
                                        sys_created_on, contact_department, intermediate_provider_complete_stir_shaken, 
                                        ocn, sys_created_by, contact_business_address, intermediate_provider_exemption_rule, 
                                        business_name, foreign_voice_provider, frn, e_signature, gateway_complete_stir_shaken, 
                                        declaration_date, other_dba_names, complete_stir_shaken, contact_title, 
                                        gateway_provider_exemption_rule, gateway_partial_stir_shaken, partial_stir_shaken, 
                                        no_stir_shaken, voice_service_provider, gateway_no_stir_shaken, contact_email, 
                                        gateway_role_in_call_path, intermediate_provider_partial_stir_shaken, 
                                        intermediate_provider, principals_affiliates_subsidiaries, 
                                        voice_service_provider_exemption_rule, implementation, no_flag, 
                                        robocall_mitigation_contact_name, declaration, gateway_provider, 
                                        investigation_description, previous_dba_names, other_frns, contact_country, 
                                        intermediate_provider_no_stir_shaken)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', (data['has_had_investigation'], data['country'], data['contact_telephone_number'], data['business_address'], 
                    data['voice_role_in_call_path'], data['sys_updated_on'], data['contact_phone_extension'], 
                    data['intermediate_provider_role_in_call_path'], data['number'], data['no_suppress'], data['sys_updated_by'], 
                    data['sys_created_on'], data['contact_department'], data['intermediate_provider_complete_stir_shaken'], 
                    data['ocn'], data['sys_created_by'], data['contact_business_address'], data['intermediate_provider_exemption_rule'], 
                    data['business_name'], data['foreign_voice_provider'], data['frn'], data['e_signature'], data['gateway_complete_stir_shaken'], 
                    data['declaration_date'], data['other_dba_names'], data['complete_stir_shaken'], data['contact_title'], 
                    data['gateway_provider_exemption_rule'], data['gateway_partial_stir_shaken'], data['partial_stir_shaken'], 
                    data['no_stir_shaken'], data['voice_service_provider'], data['gateway_no_stir_shaken'], data['contact_email'], 
                    data['gateway_role_in_call_path'], data['intermediate_provider_partial_stir_shaken'], 
                    data['intermediate_provider'], data['principals_affiliates_subsidiaries'], 
                    data['voice_service_provider_exemption_rule'], data['implementation'], data['no_flag'], 
                    data['robocall_mitigation_contact_name'], data['declaration'], data['gateway_provider'], 
                    data['investigation_description'], data['previous_dba_names'], data['other_frns'], data['contact_country'], 
                    data['intermediate_provider_no_stir_shaken']))

        # Commit changes
        self.conn.commit()

    def data_exists(self, table_name, data):
        # Create a SQL query that checks if a record exists
        query = f'''
                SELECT * FROM {table_name} 
                WHERE number = %s 
                '''

        # Execute the query
        self.cursor.execute(query, (
            (data['number'],)
        ))

        # Fetch the result 
        result = self.cursor.fetchone()

        # If a record was found, return True. Otherwise, return False.
        return result is not None
        
    def close_connection(self):
        # Close the db connection
        self.conn.close()
