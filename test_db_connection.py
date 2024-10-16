import mysql.connector
from mysql.connector import Error

def test_connection(host, user, password, database):
    try:
        # Create a connection
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Check if connection is successful
        if db_connection.is_connected():
            print("Connection to MySQL DB successful")
            db_info = db_connection.get_server_info()
            print(f"Server version: {db_info}")

            # Optional: Select a database to check access
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM  posts;")
            current_database = cursor.fetchone()
            print(f"Current database: {current_database[0]}")

            # Close the cursor
            cursor.close()
        else:
            print("Connection failed.")
    
    except Error as e:
        print(f"Error: '{e}' occurred")

    finally:
        # Ensure the connection is closed
        if (db_connection.is_connected()):
            db_connection.close()
            print("MySQL connection closed.")


test_connection('127.0.0.1', 'root', 'ikkDUD56*', 'retail_sales')
