import smtplib

def sendEmail(to, subject, body):
	gmail_user = 'princetonwritetime@gmail.com'
	gmail_pwd = 'dondero217'
	from = "Write Time<princetonwritetime@gmail.com>" 
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + from + '\n' + 'Subject:testing \n'
	msg = header + '\n' + body
	smtpserver.sendmail(gmail_user, to, msg)
	smtpserver.close()