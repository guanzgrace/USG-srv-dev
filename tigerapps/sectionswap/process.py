from swap.models import SwapRequest
from django.core.mail import EmailMessage

# Don't let a user submit identical have/want request

def process(input_req):
    input_req.save()
    cycle = input_req.find_cycle()
    if cycle != None:
        req_strs = []
        for req in cycle:
            req_strs.append(unicode(req))
        for req in cycle:
            email(req, req_strs)
            delete_all(req)
        return req_strs
    return None

def delete_all(input_req):
    for req in input_req.have.had_by_set.all():
        if req.user == input_req.user:
            req.delete()

def email(req, req_strs):
    email_body = """
    	<p>Hey there, %s!</p>
    	<p>We've identified a potential swap for <b>%s</b> from <b>%s</b> into <b>%s</b>.</p>
    	<p>You'll swap with the following people:</p>
    	<p>%s</p>
    	<p>Cheers!</p>
    	<p>The Section Swap Team</p>
    	""" % (str(req.user.netid), str(req.have.course), str(req.have.name), str(req.want.name), "</p><p>".join(req_strs))

    msg = EmailMessage('Successful swap into ' + str(req.want), email_body, 'Section Swap<princetonsectionswap@gmail.com>', [req.user.netid + '@princeton.edu'])
    msg.content_subtype = "html"
    msg.send()
