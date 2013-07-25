import smtplib
import sys

# Note: to get this to work, I had to generate an "application-specific" password from Gmail.

def sendEmail(to, subject, body):
	username = "princetonsectionswap"
	password = "ufytzbdhqwyimiif"

	sender = 'Section Swap<princetonsectionswap@gmail.com>'

	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, to, subject, body)

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login(username,password)  
		server.sendmail(sender, to, message)  
		server.quit()  
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return 0

	return 1
