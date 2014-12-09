import os
import smtplib
from email.mime.text import MIMEText
from EMAIL_SETTINGS import user, password 

# This will not work on the development server
# but it does work in production
# because EMAIL_SETTINGS does exist on the server

def sendMail(to, subject, body):
    smtp = smtplib.SMTP_SSL("smtp.sendgrid.net")
    smtp.login(user, password)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "Princeton Pounce"
    msg['To'] = to
    response = smtp.sendmail("jmcohen@princeton.edu", [to], msg.as_string())
    smtp.quit() 
    return response
