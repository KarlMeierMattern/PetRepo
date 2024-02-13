import os
import random

from flask import Flask, redirect, render_template, request, session, url_for, send_file
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash
import base64
from io import BytesIO

import mysql.connector

from flask import jsonify

# MySQL Connection Parameters
# Always create a specific user with limited privileges in MySQL workbench
db_config = {
   'host': os.environ['DB_HOST'],
   'user': os.environ['DB_USER'],
   'password': os.environ['DB_PASSWORD'],
   'database': os.environ['DB_NAME']
}

# Establish a database connection
db_connection = mysql.connector.connect(**db_config)

# Create a flask app
app = Flask(
   __name__,
   template_folder='templates',  # Name of html file folder
   static_folder='static'  # Name of directory for static files
)

# This loads the variables from .env
# Now you access the SECRET_KEY like this
app.secret_key = os.getenv('SECRET_KEY')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
   return render_template('index.html')

# Tells Flask that when it receives a GET request to /login, it should call the login()...
# ...function and return the rendered login.html template.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       
        # SQL query to fetch the user with the provided email
        # Means "get me the records where the email column matches the specific email address I will provide later.
        query = "SELECT email, password FROM users WHERE email = %s"


        # Check if the existing global database connection is open
        if not db_connection.is_connected():
            # Reconnect if the connection has been closed
            db_connection.reconnect()

        # Initialize cursor to execute the query
        # Cursor acts as an intermediary for executing database commands
        cursor = db_connection.cursor(dictionary=True)
    
        try:
            # Execute the query
            # Cursor is a Python object that enables you to communicate with the database and...
            # ...execute queries like selecting, inserting, updating data
            # email replaces the placeholder %s
            cursor.execute(query, (email,))
      
            # After executing a SELECT query that retrieves data from the database, this method...
            # is used to get one row from the query result. Think of it as asking the cursor to...
            # bring back one record from the data it has fetched from the database.
            user_record = cursor.fetchone()
      
            if user_record:
                # Verifying the provided password with the stored hashed password
                if check_password_hash(user_record['password'], password):
                    session['email'] = user_record['email']
                    return redirect(url_for('profile'))
      
            # Either user not found or wrong password provided
            return redirect(url_for('signup'))
        
        except mysql.connector.Error as e:
            # Handle any SQL errors
            return f"An error occurred: {e}", 500
        
        finally:
            cursor.close()
    
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        # Get data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password for security
        hashed_password = generate_password_hash(password)
        
        # Prepare the SQL statement
        insert_statement = (
        "INSERT INTO users (email, first_name, last_name, password) "
        "VALUES (%s, %s, %s, %s)"
        )
    
        # Check if the existing global database connection is open
        if not db_connection.is_connected():
            # Reconnect if the connection has been closed
            db_connection.reconnect()

        # Connect to the database
        cursor = db_connection.cursor()

        try:
            # Execute the query
            cursor.execute(insert_statement, (email, first_name, last_name, hashed_password))
            
            # Commit the changes to the database
            db_connection.commit()

            # Store the email in session after signup
            session['email'] = email

            # Redirect to the pet profile page
            return redirect(url_for('pet'))

        except mysql.connector.IntegrityError as e:
        # Handle the integrity error (e.g., email already exists)
            return f"An error occurred: {e}", 400
        except mysql.connector.Error as e:
        # Handle other possible MySQL errors
            return f"An error occurred: {e}", 500
        finally:
            cursor.close()
    else:
        # Render signup page if the request method is 'GET'
        return render_template('signup.html')


@app.route('/pet', methods=['GET','POST'])
def pet():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Get data from the form
            pet_name = request.form['pet_name']
            breed = request.form['breed']
            weight = request.form['weight']
            sex = request.form['sex']
            age = request.form['age']
            bio = request.form['bio']
            health = request.form['health']
            behaviour = request.form['behaviour']
            picture = request.files['picture']
            address = request.form['address']

            # Check if the picture was provided
            if not picture:
                raise ValueError("Picture was not uploaded.")

            # Get the users' email of the currently logged in user
            session_email = session.get('email')

            # Base64 encode the picture
            picture_bytes = picture.read()
            picture_base64 = base64.b64encode(picture_bytes).decode('utf-8')

            # SQL statement to insert pet data
            insert_pet = (
                "INSERT INTO pets (email, pet_name, breed, weight, sex, age, bio, health, behaviour, picture, address) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE "
                "pet_name=%s, breed=%s, weight=%s, sex=%s, age=%s, bio=%s, health=%s, behaviour=%s, picture=%s, address=%s"
            )

            # Connect to the database and insert/update pet information
            cursor = db_connection.cursor()
            cursor.execute(insert_pet, (
                session_email, pet_name, breed, weight, sex, age, bio, health, behaviour, picture_base64, address,
                pet_name, breed, weight, sex, age, bio, health, behaviour, picture_base64, address
            ))
            db_connection.commit()

            # Redirect to the profile page
            return redirect(url_for('profile'))

        except Exception as e:
            return f"An error occurred: {e}", 400
      
    else:
        # Return the form for inputting pet data
        return render_template('pet.html')


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']

    # Provide query and initialise cursor
    query = "SELECT first_name, last_name, pet_name, breed, weight, sex, age, bio, health, behaviour, picture, address FROM users LEFT JOIN pets ON users.email = pets.email WHERE users.email = %s"
    cursor = db_connection.cursor(dictionary=True)

    try:
        # SQL query to fetch user and pet data by email
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        if not user_data:
            return 'User not found', 404
        
        # Use the data fetched from the database
        first_name = user_data.get('first_name', 'No first name provided')
        last_name = user_data.get('last_name', 'No last name provided')
        pet_name = user_data.get('pet_name', 'No pet name provided')
        breed = user_data.get('breed', 'No breed provided')
        age = user_data.get('age', 'No age provided')
        bio = user_data.get('bio', 'No bio provided')
        info = user_data.get('info', 'No info provided')
        picture_base64 = user_data.get('picture', None)
    
    except mysql.connector.Error as e:
        # Optionally, handle database errors here
        return f"An error occurred: {e.msg}", 500
  
    # Render profile with user's and pet's information
    return render_template(
        'profile.html',
        email=email,
        first_name=first_name,
        last_name=last_name,
        pet_name=pet_name,
        breed=breed,
        age=age,
        bio=bio,
        info=info,
        picture_base64=picture_base64
    )


# end point for serving requests
@app.route('/get_image/<filename>')
def get_image(filename):
    # Filename is the email of the user

    query = "SELECT picture FROM pets WHERE email = %s"
    cursor = db_connection.cursor(dictionary=True)

    try:
        # Query to select the picture from the pet data of the specified user profile
        cursor.execute(query, (filename,))
        pet_data = cursor.fetchone()
        
        # No pet data found for user
        if not pet_data or 'picture' not in pet_data:
            return 'Image not found', 404
        
        # Fetch the picture data from the query result
        picture_base64 = pet_data['picture']
        picture_data = base64.b64decode(picture_base64)
        
        # Close the cursor and the connection
        cursor.close()
        db_connection.close()
        
        # Sniff image type and assign MIME type accordingly
        if picture_data[0] == 0x89:
            mimetype = 'image/png'
        
        elif b'JFIF' in picture_data[6:11]:
            mimetype = 'image/jpeg'
        
        else:
            mimetype = 'image/jpeg'  # Default mimetype if the above checks don't match
        
        return send_file(
            BytesIO(picture_data),
            mimetype=mimetype,
            as_attachment=False,
        )
    
    except mysql.connector.Error as e:
        print(f"Error fetching image from database: {e}")
        return f"An error occurred: {e}", 500

@app.route('/get_health_textbox')
def get_health_textbox():
    html_content = '<textarea class="user_info" id="healthTextBox" name="health" rows="3" cols="30" placeholder="{{ health }}"></textarea>'
    return jsonify({'html_content': html_content})

if __name__ == "__main__":  # Makes sure this is the main process
  app.run( # Starts the site
  host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
  port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
  debug=True
)


# http://127.0.0.1:2395