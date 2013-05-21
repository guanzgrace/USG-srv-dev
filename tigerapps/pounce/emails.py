import urllib2
import urllib
import smtplib  

def sendMail(to, subject, body):
	params = {'to' : to, 'subject' : subject, 'body' : body}
	url = "http://princetonpounce.com/email?" + urllib.urlencode(params)
	return urllib2.urlopen(url).read()

def sendEmail(to, subject, body):
	passwordFile = open('EMAIL_PASSWORD')
	password = passwordFile.read().strip()
	passwordFile.close()

	server = smtplib.SMTP('smtp.gmail.com:587')  
	server.starttls()  
	server.login('princetonpounce',password)  
	server.sendmail('Princeton Pounce<princetonpounce@gmail.com', to, body)  
	server.quit()  