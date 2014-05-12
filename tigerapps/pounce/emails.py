#import os
#import smtplib
#from email.mime.text import MIMEText
#from EMAIL_SETTINGS import user, password 
def sendMail(to, subject, body):
    raise Exception("Jeremy Cohen, you suck.  This doesn't work.")
    smtp = smtplib.SMTP_SSL("smtp.princeton.edu")
    smtp.login(user, password)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "Princeton Pounce"
    msg['To'] = to
    response = smtp.sendmail(user + "@princeton.edu", [to], msg.as_string())
    smtp.quit() 
    return response
