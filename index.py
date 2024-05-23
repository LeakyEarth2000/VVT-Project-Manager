from flask import Flask, request, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)

correctPasscode = 1234
correctPassword = "maths>english"
redirectURL = 'http://127.0.0.1:5500/ManageUsers/users.html'

@app.route("/")
def hello_world():
    return render_template('Index/index.html')

# User data storage
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the form submission
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return jsonify({"error": "Username already exists"}), 400
        users[username] = password

        # Save users to a JSON file
        with open('users.json', 'w') as f:
            json.dump(users, f)

        return jsonify({"success": "User registered successfully"}), 200
    else:
        # Render the registration form
        return render_template('Register/registerAuthorise.html')

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Handle the form submission
        passcode = request.form['passcode']
        password = request.form['password']
        if int(passcode) == correctPasscode and password == correctPassword:
            return render_template('ManageUsers/users.html')
        elif password == "english>maths":
            return "<h1> No, it's not!!</h1>"
        else:
            return '<h1>Incorrect!</h1>'
    # Render the users management page
    return render_template('ManageUsers/users.html')



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username not in users or users[username] != password:
        return jsonify({"error": "Invalid username or password"}), 400
    return jsonify({"success": "User logged in successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)