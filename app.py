# Import necessary modules
from seek_copy import *
from baytnew import *
from wwr import *
from found_it import *
from flask import Flask, render_template, request
from threading import Thread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import sys
import os
import logging
from datetime import date
import glob

# Set up Flask application
app = Flask(__name__)
app.secret_key = "imp"

# Configure logging to write to a log file
logging.basicConfig(
    filename='scraping_log.log',  # Specify the log file name
    level=logging.INFO,           # Set the logging level (INFO or DEBUG)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize the log format
)

# Redirect stdout and stderr to the log file
sys.stdout = sys.stderr = open('scraping_log.log', 'a')

# Function to send main email with attachment
def main_email(f, email):
    try:
        # Email body
        body = '''<p>Dear User,</p>
        <p>Please find the attached file to this email. The data in this file represents information collected 
        over the last 30 days.</p>
        <p>Thank you for your attention, and have a 
        great day!</p>
        <p>Best regards,<br> DA Pune</p>
        '''
        
        # Email credentials
        senders_email = "linkdinscrrapping@gmail.com"
        sender_password = "exwroxsmvoxtadmn"
        reveiver_email = email
        
        # MIME Setup
        message = MIMEMultipart()
        message['From'] = senders_email
        message['To'] = reveiver_email
        message['Subject'] = 'Extracted CSV'
        
        time.sleep(5)
        
        # Attach file(s) to the email
        if type(f) == str:
            with open(f, "rb") as attached_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attached_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{f}"')
                message.attach(part)
        elif type(f) == list:
            for file_path in f:
                with open(file_path, 'rb') as file:
                    part = MIMEApplication(file.read(), Name=file.name)
                    part['Content-Disposition'] = f'attachment; filename="{file.name}"'
                    message.attach(part)
        
        # Attach email body
        message.attach(MIMEText(body, 'html'))
        
        # Establish SMTP connection
        session = smtplib.SMTP('smtp.gmail.com', 587)  # Use gmail with port
        session.starttls()  # Enable security
        session.login(senders_email, sender_password)  # Login with mail_id and password
        text = message.as_string()
        
        # Send email
        session.sendmail(senders_email, reveiver_email, text)
        time.sleep(10)
        session.quit()
        print("Email sent successfully!")
        
    except Exception as e:
        return e

# Function to check and create folder for extracted CSV files
def folder_exist():
    cwd = ''
    cwd = os.getcwd()
    os.chdir(cwd)
    os.makedirs(cwd+'\\Extracted_CSV', exist_ok=True)
    
    os.chdir(cwd+'\\Extracted_CSV')
    today = date.today()
    all_filenames = [file for file in glob.glob(f'*{today}.csv')]
   
    return all_filenames

# Function to remove files after sending email
def remove_files(file):
    cwd = os.getcwd()
    for filename in file:
        if filename.endswith('.csv'):
            file_path = os.path.join(cwd, filename)
            os.remove(file_path)
    os.chdir('..')
    print('Files are removed')

# Route for the homepage
@app.route('/')
def index():
    return render_template('job.html')   

# Route for handling form submission and sending emails
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST' and 'skills' in request.form and 'location' in request.form and 'email' in request.form and 'website'in request.form:
        skills = request.form['skills'] 
        location = request.form['location']
        website = request.form['website']
        email = request.form['email']
        
        # Check selected website and perform scraping accordingly
        if website == 'seek':
            try:
                main_seek(skills,location)
                file = folder_exist()
                main_email(file,email)
                msg = 'Email was sent successfully!'
            except Exception as e:
                print(e)
                msg = "Error in Seek scraping or email sending."
        elif website=='bayt':
            try:
                scrape_bayt(skills,location)
                file = folder_exist()
                main_email(file,email)
                msg = 'Email was sent successfully!'
            except Exception as e:
                print(e)
                msg = "Error in Bayt scraping or email sending."
        elif website=='weworkremotely':
            try:
                main_wwr()
                file = folder_exist()
                main_email(file,email)
                msg = 'Email was sent successfully!'
            except Exception as e:
                print(e)
                msg =  "Error in wwr scraping or email sending."
        elif website=='foundit':
            try:
                main_foundit(skills,location)
                file = folder_exist()
                main_email(file,email)
                msg = 'Email was sent successfully!'
            except Exception as e:
                print(e)
                msg = "Error in found_it.py scraping or email sending." 
        elif website == 'AllSites':
            try:
                try:
                    main_foundit(skills,location)
                except Exception as e: 
                    print(e)
                    print("error in foundit")
                try:    
                    main_wwr()
                except Exception as e: 
                    print(e)
                    print("error in wwr")
                try:    
                    scrape_bayt(skills,location)
                except Exception as e: 
                    print(e)
                    print("error in bayt") 
                try:    
                    main_seek(skills,location)
                except Exception as e: 
                    print(e)
                    print("error in seek")    
                file = folder_exist()
                main_email(file,email)
                msg = 'Email was sent successfully!'
            except Exception as e:
                print(e)
                msg = "Error in allsite scraping or email sending." 
        remove_files(file)
    return render_template('email_sent_msg.html',message=msg)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)

    