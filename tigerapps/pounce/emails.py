import urllib2
import urllib
import smtplib  

def sendMail(to, subject, body):
	passwordFile = open('/srv/tigerapps/pounce/EMAIL_PASSWORD')
	password = passwordFile.read().strip()
	passwordFile.close()

	sender = 'Princeton Pounce<princetonpounce@gmail.com>'

	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, to, subject, body)

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')  
		server.starttls()  
		server.login('princetonpounce',password)  
		server.sendmail(sender, to, message)  
		server.quit()  
	except:
		print "ERROR IN SENDING MAIL"