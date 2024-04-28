from flask import Flask, request

app = Flask(__name__)

correctPasscode = 1234

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['POST'])
def validate_passcode():
    userPasscode = int(request.form['passcode']) # from the post, gets the passcode form

    if userPasscode == correctPasscode:
        return '<h1>Correct Passcode!</h1>'
    else:
        return '<h1>Incorrect Passcode!</h1>'

# for flask to run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
