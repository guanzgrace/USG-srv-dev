import os
import smtplib
from email.mime.text import MIMEText
def sendMail(to, subject, body):
    smtp = smtplib.SMTP_SSL("smtp.princeton.edu")
    # POUNCE_EMAIL_USER and POUNCE_EMAIL_PASS should be environment
    # variables containing the netid and the password for the email sender
    user = os.environ["POUNCE_EMAIL_USER"]
    password = os.environ["POUNCE_EMAIL_PASS"] 
    smtp.login(user, password)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "Princeton Pounce"
    msg['To'] = to
    response = smtp.sendmail(user + "@princeton.edu", [to], msg.as_string())
    smtp.quit() 
    return response
