from flask import Flask, render_template, request, redirect, url_for, session, send_file
import subprocess
import shutil
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define a User class for flask-login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader callback for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    if 'authenticated' in session:
        # Render the page with full Raspberry Pi access.
        return render_template('index.html')
    else:
        # Render the login page.
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the credentials are correct.
        if username == 'admin' and password == 'adminjb':
            user = User(id='admin')
            login_user(user)
            session['authenticated'] = True
            # Redirect to a special URL that grants access to the full GUI.
            return redirect(url_for('grant_access'))
        elif username == 'jbuser' and password == '12345678':
            user = User(id='jbuser')
            login_user(user)
            session['authenticated'] = True
            # Redirect to a special URL that grants access to the full GUI.
            return render_template('home.html')
        elif username == 'viewer' and password == '12345':
            user = User(id='viewer')
            login_user(user)
            session['authenticated'] = True
            # Redirect to a special URL that grants access to the full GUI.
            return render_template('home.html')
        else:
            # Incorrect credentials, display an error message.
            return render_template('index.html', error='Invalid credentials')
    else:
        return render_template('index.html')

@app.route('/grant_access')
@login_required
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

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/login')

@app.route('/download_log')
@login_required
def download_log():
    try:
        source = '/home/pi/Desktop/desk.csv'
        destination = '/media/pi/USB_DRIVE/output/desk.csv'  # Adjust this path based on your actual USB drive path

        # Ensure the output folder exists
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Copy the file
        shutil.copy(source, destination)

        return "File has been copied to the USB drive."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/update_frequency', methods=['POST'])
@login_required
def update_frequency():
    try:
        data = request.get_json()
        frequency = int(data.get('frequency'))

        if frequency < 1:
            return "Frequency cannot be less than 1 minute."

        # Update the crontab with the new frequency
        cron_job = f"*/{frequency} * * * * /path/to/your/command\n"  # Adjust the command path as needed

        with open("/tmp/crontab.txt", "w") as f:
            f.write(cron_job)

        subprocess.run(["crontab", "/tmp/crontab.txt"])

        return "Frequency has been updated in the crontab."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
