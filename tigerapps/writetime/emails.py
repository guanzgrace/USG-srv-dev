from django.core.mail import EmailMessage

def sendEmail(appointment, toName, toEmail):
	sender = 'Write Time<princetonsectionswap@gmail.com>'
	subject = "Your Writing Center Appointment Has Been Claimed"
	body = """
		<p>Hello %s,</p>
		<p>Your Writing Center appointment has been claimed by %s (%s).  He or she 
		will arrive at the Writing Center at %s in your place.  Thank you for using
		WriteTime!</p>
		<p>Best,</p>
		<p>The WriteTime Team</p>
	""" % (appointment.name, toName, toEmail, appointment.time.strftime("%I:%M %p on %A, %B %d"))
	
	msg = EmailMessage(subject, body, sender, [appointment.netid + "@princeton.edu"])
	msg.content_subtype = 'html'
	msg.send()
	
	subject = "Your New Writing Center Appointment!"
	body = """
		<p>Hello %s,</p>
		<p>You have accepted a Writing Center appointment from %s (%s).  You should arrive 
		at the Writing Center at <b>%s</b> in his or her place.  Thank you for using
		WriteTime!</p>
		<p>Best,</p>
		<p>The WriteTime Team</p>
	""" % (toName, appointment.name, appointment.email, appointment.time.strftime("%I:%M %p on %A, %B %d"))
	
	msg = EmailMessage(subject, body, sender, [toEmail])
	msg.content_subtype = 'html'
	msg.send()
	
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
	
	msg = EmailMessage(subject, body, sender, [appointment.netid + "@princeton.edu"])
	msg.content_subtype = 'html'
	msg.send()