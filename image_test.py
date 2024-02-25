import mysql.connector
from PIL import Image
from io import BytesIO
import os

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_NAME']
)

# Execute query to fetch image data
cursor = db_connection.cursor()
cursor.execute("SELECT picture FROM pets WHERE email = %s", ('alexander@gmail.com',))
row = cursor.fetchone()

# Check if data is fetched successfully
if row is not None:
    picture_data = row[0]

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

    # Open image using PIL
    try:
        image = Image.open(BytesIO(picture_data))
        image.show()  # Display image
    except Exception as e:
        print("Error:", e)
else:
    print("No data found for the specified email.")