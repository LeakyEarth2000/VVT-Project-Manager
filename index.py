from flask import Flask, request, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)

correctPasscode = 1234
correctPassword = "maths>english"
redirectURL = 'http://127.0.0.1:5500/ManageUsers/users.html'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['POST'])
def validate_passcode():
    userPasscode = int(request.form['passcode'])
    userPassword = str(request.form['password'])

    if userPasscode == correctPasscode and userPassword == correctPassword:
        return redirect(redirectURL)
    elif userPasscode != correctPasscode:
        return '<h1>Incorrect!</h1>'
    elif userPassword == "english>maths":
        return "<h1> No, it's not!!</h1>"
    else:
        return '<h1>Incorrect!</h1>'

# User data storage
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    users[username] = password

    # Save users to a JSON file
    with open('users.json', 'w') as f:
        json.dump(users, f)

    return jsonify({"success": "User registered successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username not in users or users[username] != password:
        return jsonify({"error": "Invalid username or password"}), 400
    return jsonify({"success": "User logged in successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)