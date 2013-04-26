import urllib2

def sendMail(to, subject, body):
	url = "http://princetonpounce.com/email?" + "to=" + to + "&subject=" + subject + "&body=" + body
	return url
#	return urllib2.urlopen(url).read()