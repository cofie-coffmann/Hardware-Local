from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/')
def login():
    # Initialize the 'msg' variable to an empty string (no message initially)
    msg = ""
    return render_template('home.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
