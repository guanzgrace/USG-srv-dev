from models import SwapRequest
from emails import sendEmail

# Don't let a user submit identical have/want request

def process(input_req):
    input_req.save()
    cycle = input_req.find_cycle()
    if cycle != None:
        req_strs = []
        for req in cycle:
            req_strs.append(unicode(req))
        for req in cycle:
            email(req, cycle)
            delete_all(req)
        return req_strs
    return None

def delete_all(input_req):
    for req in input_req.have.had_by_set.all():
        if req.netid == input_req.netid:
            req.delete()

def email(req, cycle):
    req_strs = ''.join(['<p><b>%s</b> will swap from %s into %s.</p>' % (swap.netid, swap.have.name, swap.want.name) for swap in cycle])
    body = """
    	<p>Hey there, %s!</p>
    	<p>We've identified a potential swap for <b>%s</b> from <b>%s</b> into <b>%s</b>.</p>
    	<p>Here's how it'll go down:</p>
    	%s
    	<p>Cheers!</p>
    	<p>The Section Swap Team</p>
    	""" % (str(req.netid), str(req.have.course), str(req.have.name), str(req.want.name), req_strs)

    subject = 'Successful swap into ' + str(req.want)
    to = req.netid + '@princeton.edu'
    sendEmail(to, subject, body)
