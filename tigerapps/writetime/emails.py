import smtplib

def sendMail(to, subject, body):
	gmail_user = 'princetonwritetime@gmail.com'
	gmail_pwd = 'dondero217'
	fromEmail = "Write Time<princetonwritetime@gmail.com>" 
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + fromEmail + '\n' + 'Subject:' + subject + '\n' + 'Content-type: text/html' + '\n'
	msg = header + '\n' + body
	smtpserver.sendmail(gmail_user, to, msg)
	smtpserver.close()

def sendNotifyEmail(appointment, toName, toEmail):
	subject = "Your Writing Center Appointment Has Been Claimed"
	body = """
		<p>Hello %s,</p>
		<p>Your Writing Center appointment has been claimed by %s (%s).  He or she 
		will arrive at the Writing Center at %s in your place.  Thank you for using
		WriteTime!</p>
		<p>Best,</p>
		<p>The WriteTime Team</p>
	""" % (appointment.name, toName, toEmail, appointment.time.strftime("%I:%M %p on %A, %B %d"))
	
	sendMail(appointment.netid + "@princeton.edu", subject, body)

	subject = "Your New Writing Center Appointment!"
	body = """
		<p>Hello %s,</p>
		<p>You have accepted a Writing Center appointment from %s (%s).  You should arrive 
		at the Writing Center at <b>%s</b> in his or her place.  Thank you for using
		WriteTime!</p>
		<p>Best,</p>
		<p>The WriteTime Team</p>
	""" % (toName, appointment.name, appointment.netid + "@princeton.edu", appointment.time.strftime("%I:%M %p on %A, %B %d"))
	
	sendMail(toEmail, subject, body)
	
def sendConfirmEmail(appointment):
	sender = 'Write Time<princetonsectionswap@gmail.com>'
	subject = "Your Writing Center Appointment Has Been Posted"
	body = """
		<p>Hello %s,</p>
		<p>Your Writing Center appointment has been posted.  You will receive an
		email if someone else claims it.  If you change your mind and decide to
		keep the appointment, please remove it from the web site.</p>
		<p>Best,</p>
		<p>The WriteTime Team</p>
	""" % (appointment.name)
	
	sendMail(appointment.netid + "@princeton.edu", subject, body)