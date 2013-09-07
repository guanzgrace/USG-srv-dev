import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from EMAIL_SETTINGS import username, password, sender

# Note: to get this to work, I had to generate an "application-specific" password from Gmail.
# Note again: *sigh* that didn't get through either.  I think the email needs to be send from an @princeton.edu-affiliated account.

def sendEmail(to, subject, body):
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, to, subject, body)

	try:
		message = MIMEMultipart('alternative')
		message['subject'] = subject
		message['To'] = to
		message['From'] = sender
		html = MIMEText(body, 'html')
		plain = MIMEText("This is the plaintext version of this email.", 'plain')
		message.attach(plain)
		message.attach(html)

		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login(username,password)  
		server.sendmail(sender, to, message.as_string())  
		server.quit()  
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return 0

	return 1
	