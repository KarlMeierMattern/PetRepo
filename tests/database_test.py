import mysql.connector
import os

# MySQL Connection Parameters
# Always create a specific user with limited privileges in MySQL workbench
db_config = {
  'host': os.environ['DB_HOST'],
  'user': os.environ['DB_USER'],
  'password': os.environ['DB_PASSWORD'],
  'database': os.environ['DB_NAME']
}

def test_db_connection():
  try:
      # Establish a database connection using the provided db_config
      connection = mysql.connector.connect(**db_config)

      # If the connection was successful, no exception will be raised
      cursor = connection.cursor()

      # Execute a simple query just to test the connection (e.g., SELECT version())
      cursor.execute("SELECT VERSION()")

      # Fetch one result
      version = cursor.fetchone()

      # Print the version for verification
      print("Database connection successful. MySQL version:", version[0])

      # Close the cursor and connection
      cursor.close()
      connection.close()

  except mysql.connector.Error as e:
      # Handle any errors that occurred during the connection attempt
      print(f"Error connecting to MySQL: {e.msg}")

# Call the function to test the connection when the script runs
if __name__ == "__main__":
  # Test the database connection
  test_db_connection()