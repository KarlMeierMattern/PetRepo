import os
import random

from flask import Flask, redirect, render_template, request, session, url_for, send_file
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash
import base64
from io import BytesIO

from dotenv import load_dotenv

# Create a flask app
app = Flask(
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)

# This loads the variables from .env
# Now you access the SECRET_KEY like this
load_dotenv()
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

    users = db.get('users', {})
    
    if email not in users:
      return redirect(url_for('signup'))

    if email in users and check_password_hash(users[email]['password'],password):
      session['email'] = email
      return redirect(url_for('profile'))

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
    
    # Store the first and last name in session variables
    session['first_name'] = first_name
    session['last_name'] = last_name
    
    # Initialize 'users' dict in db if it doesn't exist
    if 'users' not in db.keys():
      db['users'] = {}
    # Fetch the current users dictionary from the db
    users = db.get('users', {})
    
    # Check if email already exists
    if email in users:
      print('Email already exists. Please log in or use another email address.')
      return redirect(url_for('login'))
      
    # Store email and hashed password in Replit DB
    users[email] = {
      'first_name': first_name, 
      'last_name': last_name, 
      'password': hashed_password,
      'pet': {}
    }
    
    # Saves records back into the database
    db['users'] = users

    # After successful signup store the user's email in the session
    session['email'] = email
    print("Session Email Set:", session['email']) # debug message

    # Redirects to the profile function
    return redirect(url_for('pet'))
  else:
    print("Rendering signup.html...") # Debug message
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
      age = request.form['age']
      bio = request.form['bio']
      info = request.form['info']
      picture = request.files['picture']

      # Check if the picture was provided
      if not picture:
        raise ValueError("Picture was not uploaded.")

      # Get the users' email of the currently logged in user
      session_email = session.get('email')

      # Base64 is a method for encoding binary data (like images) as a string of ASCII...
      # characters which can be stored and transmitted over text-based protocols such as HTTP.
      picture_bytes = picture.read()
      picture_base64 = base64.b64encode(picture_bytes).decode('utf-8')

      # Fetch the current users dictionary from the db
      users = db['users']
      email = session['email']

      users[email]['pet'] = {
        'name': pet_name,
        'breed': breed,
        'age': age,
        'bio': bio,
        'info': info,
        'picture': picture_base64
      }
      
      # Saves records back into the database
      db['users'] = users

      # sends an HTTP redirect to the client's browser, instructing it to make a new GET
      # request to the URL generated for the 'profile' view. As a result, the browser's 
      # address bar will be updated to reflect the new URL, and refreshing the browser 
      # would not cause form resubmission. This follows the Post/Redirect/Get (PRG) 
      # pattern and is generally a good practice after handling form submissions to 
      # prevent duplicate submissions.
      return redirect(url_for('profile'))

    except Exception as e:
      return f"An error occurred: {e}", 400
      
  else:
    # Display the pet form webpage when /pet is accessed with a GET request
    return render_template('pet.html')

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('login'))
    
  email = session['email']
  users = db['users']
  user = users.get(email, {})

  if not user:
    return 'User not found', 404

  email = session['email']
  
  first_name = user.get('first_name')
  last_name = user.get('last_name')
  pet = user.get('pet')

  # Handle the case where the pet dictionary does not have all keys
  pet_name = pet.get('name', 'No name provided')
  breed = pet.get('breed', 'No breed provided')
  age = pet.get('age', 'No age provided')
  bio = pet.get('bio', 'No bio provided')
  info = pet.get('info', 'No info provided')
  picture_base64 = pet.get('picture', None)
  
  # Handle picture retrieval logic if implemented
  # Render profile with user's and pet's information
  return render_template('profile.html', email=email, first_name=first_name, last_name=last_name, pet_name=pet_name, breed=breed, age=age, bio=bio, info=info, picture_base64=picture_base64)

# end point for serving requests
@app.route('/get_image/<filename>')
def get_image(filename):
  # Filename is the email of the user
  users = db['users']
  user = users.get(filename, None)

  if not user or 'picture' not in user['pet']:
    return 'Image not found', 404
    
  picture_base64 = user['pet']['picture']
  # Since the picture is stored in base64 encoding, it needs to be decoded back...
  # into binary data to be used as an image.
  picture_data = base64.b64decode(picture_base64)

  # This is a simple sniffing that assumes if the first byte is 0x89 it's a PNG
  # If bytes 6-10 are 'JFIF', it's a JPEG
  # Otherwise, it defaults to JPEG
  if picture_data[0] == 0x89:
    mimetype = 'image/png'
  elif b'JFIF' in picture_data[6:11]:
    mimetype = 'image/jpeg'
  else:
    mimetype = 'image/jpeg' # Default mimetype if the above checks don't match
    
  # HTTP response to send the picture data back to the user's browser or requesting client
  return send_file(
    BytesIO(picture_data),
    mimetype=mimetype, # or 'image/png' depending on the type of image you're dealing with
    as_attachment=False,
  )

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
  if request.method == 'POST':
    admin_password = request.form['password']
    if admin_password == os.environ.get('ADMIN_PASSWORD'):
        session['admin'] = True
        return redirect(url_for('admin_users'))
    else:
        return 'Invalid admin password!'

  return render_template('admin_login.html')

@app.route('/admin/users')
def admin_users():
  # Basic check to see if 'admin' is in the session (logged in successfully)
  if 'admin' in session and session['admin']:
    user_details = {}

    users = db.get('users', {})

    for email, details in users.items():
      user_details[email] = {k:v for k,v in details.items() if k != 'password'}
    
    return render_template('admin_users.html', users=user_details)
  else:
      return redirect(url_for('admin_login'))

if __name__ == "__main__":  # Makes sure this is the main process
  app.run( # Starts the site
  host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
  port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
)