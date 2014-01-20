import urllib2
import urllib

def sendMail(to, subject, body):
	params = {'to' : to, 'subject' : subject, 'body' : body}
	url = "http://jeremycohensoftware.com/email?" + urllib.urlencode(params)
	return urllib2.urlopen(url).read()
    