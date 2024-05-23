from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

correctPasscode = 1234
correctPassword = "maths>english"

# Configure path to user data file
user_data_file = 'users.json'

def load_users():
  """Loads user data from JSON file (creates file if it doesn't exist)"""
  try:
    with open(user_data_file, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    with open(user_data_file, 'w') as f:
      json.dump({}, f, indent=4)  # Create an empty JSON file if not found
    return {}

def save_users(users):
  """Saves user data to JSON file"""
  with open(user_data_file, 'w') as f:
    json.dump(users, f, indent=4)

users = load_users()  # Load existing users on startup

@app.route("/")
def hello_world():
  return render_template('Index/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if username in users:
      print("Existing username has already been created!")
      return render_template('ManageUsers/users.html')
    users[username] = password
    save_users(users)
    return render_template('Index/index.html')
  else:
    return render_template('Register/registerAuthorise.html')

@app.route('/manageusers', methods=['GET', 'POST'])
def manageusers():
  if request.method == 'POST':
    passcode = request.form['passcode']
    password = request.form['password']
    if int(passcode) == correctPasscode and password == correctPassword:
        return render_template('ManageUsers/users.html')
    elif password == "english>maths":
        return "<h1> No, it's not!!</h1>"
    else:
        return '<h1>Incorrect!</h1>'
  return render_template('Register/registerAuthorise.html')

@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  if username not in users or users[username] != password:
    print("Invalid username or password")
    return render_template('Index/index.html') # maybe a pop up error, or a modified version of index.html that will say an error? i think its easier to modify the website so that it will show an error instead of a pop up??
  else:
    print("Logged in")
    return render_template('Index/index.html') # must change to a different website
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=6969)
