import mysql.connector
from .PropertyUtil import load_db_properties

def get_connection():
    """Create and return a new database connection."""
    props = load_db_properties()
    conn = mysql.connector.connect(
        host=props['host'], 
        user=props['user'], 
        password=props['password'], 
        database=props['database']
    )
    return conn

