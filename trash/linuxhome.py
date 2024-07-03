from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/')
def home():
    if 'authenticated' in session:
        # Render the page with full Raspberry Pi access.
        return render_template('full_access.html')
    else:
        # Render the login page.
        return render_template('linuxlogin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check if the credentials are correct.
    if username == 'admin' and password == 'adminjb':
        session['authenticated'] = True
        # Redirect to a special URL that grants access to the full GUI.
        return redirect(url_for('grant_access'))
    else:
        # Incorrect credentials, display an error message.
        return render_template('home.html', error='Invalid credentials')

@app.route('/grant_access')
def grant_access():
    if 'authenticated' in session:
        try:
            # Start the Raspberry Pi Desktop with a 5-second delay.
            subprocess.Popen('sleep 5 && startx', shell=True)
            
            # Provide a message indicating successful access to the GUI.
            return "Access granted to the full Raspberry Pi GUI. Please wait..."
        except Exception as e:
            # Handle any errors that may occur when starting the GUI.
            return f"Error: {str(e)}"
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
