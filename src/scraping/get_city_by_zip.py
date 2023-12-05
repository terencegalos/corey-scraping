import mysql.connector

def getdb(host,user,password,database,table):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        table=table
    )

    return conn

def get_city_by_zip():
