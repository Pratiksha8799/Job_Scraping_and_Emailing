# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 15:13:18 2023

@author: user
"""
from fastapi import FastAPI, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time
from seek_copy import*
from baytnew import*
from wwr import*
from found_it import*
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
from email.mime.application import MIMEApplication

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class JobSearchRequest(BaseModel):
    skills: str
    location: str
    email: str
    website: str


def main_email(f, email):
    # ... (Your email sending logic remains the same as in your Flask app)
    body = '''<p>Hi, Please check attached CSV.<br/><br/><br/>
    
    Thank you<br/>
    <br/>
    </p>
    
    '''
    # config = configparser.RawConfigParser()
    # config.read('config.ini')
    
    senders_email = "supriyashindearess63@gmail.com"
    sender_password = "uhxtruqdctbknpgh"
    reveiver_email = email
    
    # MIME Setup
    message = MIMEMultipart()
    message['From'] = senders_email
    message['To'] = reveiver_email
    message['Subject'] = 'Extracted CSV'
    
    time.sleep(5)
    
   # f = 'bayt_data.csv'
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
    
    message.attach(MIMEText(body, 'html'))
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Use gmail with port
    session.starttls()  # Enable security
    session.login(senders_email, sender_password)  # Login with mail_id and password
    text = message.as_string()
    
    session.sendmail(senders_email, reveiver_email, text)
    time.sleep(10)
    session.quit()
    print("Email sent successfully!")


@app.get("/", response_class=HTMLResponse)
async def index(request):
    return templates.TemplateResponse("job.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search(job_request: JobSearchRequest):
    skills = job_request.skills
    location = job_request.location
    website = job_request.website
    email = job_request.email
    print('Working')
    print(website)

    if website == 'seek':
        try:
            print("inside seek")
            file = 'seek_data.csv'
            main_seek(skills, location)
            main_email(file, email)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error in Seek scraping or email sending.")

    elif website == 'bayt':
        try:
            print('inside bayt')
            file = 'bayt_data.csv'
            scrape_bayt(skills, location)
            main_email(file, email)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error in Bayt scraping or email sending.")

    elif website == 'weworkremotely':
        try:
            print('inside weworkremotely')
            file = 'wwr_data.csv'
            main_wwr()
            main_email(file, email)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error in wwr scraping or email sending.")

    elif website == 'foundit':
        try:
            print('inside foundit')
            file = 'foundit_data.csv'
            main_foundit(skills, location)
            main_email(file, email)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error in found_it.py scraping or email sending.")

    elif website == 'AllSites':
        try:
            print('inside All site')
            file = ['foundit_data.csv', 'seek_data.csv', 'bayt_data.csv', 'wwr_data.csv']
            try:
                main_foundit(skills, location)
            except Exception as e:
                print(e)
                print("error in foundit")
            try:
                main_wwr()
            except Exception as e:
                print(e)
                print("error in wwr")
            try:
                scrape_bayt(skills, location)
            except Exception as e:
                print(e)
                print("error in bayt")
            try:
                main_seek(skills, location)
            except Exception as e:
                print(e)
                print("error in seek")
            main_email(file, email)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error in allsite scraping or email sending.")

    return templates.TemplateResponse("email_sent_msg.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
