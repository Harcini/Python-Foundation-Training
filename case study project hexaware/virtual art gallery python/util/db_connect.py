import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",              
        password="Harcini@1810", 
        database="virtualArtgalleryy"
    )
    return conn
