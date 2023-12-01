import mysql.connector
from config.db_config import DB_CONFIG


# Establish a connection to the MySQL server
cnx = mysql.connector.connect(user=DB_CONFIG['DBUSER'], password=DB_CONFIG['DBPASS'], host=DB_CONFIG['DBHOST'])

# Create a cursor object
cursor = cnx.cursor()

# Select the database
cursor.execute(f"USE {DB_CONFIG['DBNAME']}")

# Get the list of all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

total_records = 0

# Loop through all tables
for table in tables:
    table_name = table[0]
    
    # Count the records in the current table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    print(f"The table '{table_name}' has {count} records.")
    
    # Add the count to the total
    total_records += count

print(f"The total number of records in all tables is {total_records}.")

# Close the cursor and connection
cursor.close()
cnx.close()
