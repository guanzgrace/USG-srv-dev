################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#		   Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  dsml.py
# Info :  DSML lookup utilities
################################################################

import urllib2
import ldap
from xml.dom.minidom import parseString

#Code adapted from:	http://github.com/benadida/auth-django-app/blob/master/auth_systems/cas.py#
#Robustness added by Michael Yaroshefsky
def gdi(netid):
	""" Get Directory Info (gdi) returns a dictionary of information from the LDAP for a user """
	attributes = ['cn', 'displayName', 'emailbox', 'emailrewrite', 'gecos',
				  'gidnumber', 'givenName', 'homedirectory', 'loginshell',
				  'mail', 'mailalternateaddress', 'mailquota', 'sn',
				  'universityid', 'ou', 'pustatus', 'puclassyear',
				  'puacademiclevel', 'purescollege', 'universityidref',
				  'puhomedepartmentnumber', 'street', 'telephone']

	l = ldap.initialize('ldap://ldap.princeton.edu')
	search_result = l.search_s('uid=%s,o=Princeton University,c=US' % netid, ldap.SCOPE_SUBTREE, '(sn=*)', attributes)

	user_info = {}
	
	# for each attribute, store the attribute-value pair in user_info
	if len(search_result) > 0:
		# search_result: list of tuples (dn, attrs) where attrs is a dict
		for attribute, data in search_result[0][1].iteritems():
			# attribute: string with name of attribute
			# data: list containing attribute values
			user_info[attribute] = data[0]

	return user_info

def namelookup(input):
	""" Conduct an advanced search based on multiple input strings """

	url = 'http://dsml.princeton.edu/'
	headers = {'SOAPAction': "#searchRequest", 'Content-Type': 'text/xml'}
	
	query = ""
	
	terms = input.split(' ')
	
	for term in terms:
		query = query + "<any>%s</any>" % (term)
	
	request_body = """<?xml version='1.0' encoding='UTF-8'?>
	<soap-env:Envelope
		xmlns:xsd='http://www.w3.org/2001/XMLSchema'
		xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
		xmlns:soap-env='http://schemas.xmlsoap.org/soap/envelope/'>
		<soap-env:Body>
			<batchRequest xmlns='urn:oasis:names:tc:DSML:2:0:core'
			requestID='searching'>
				<searchRequest
				dn='o=Princeton University, c=US'
				scope='wholeSubtree'
				derefAliases='neverDerefAliases'
				sizeLimit='10'>
					<filter>
						<or>
							<substrings name='uid'>
								<any>%s</any>
							</substrings>	
							<substrings name='displayName'>
								%s
							</substrings>					
						</or>
					</filter>
					<attributes>
						<attribute name="displayName"/>
						<attribute name="mail"/>
						<attribute name="uid"/>
					</attributes>
				</searchRequest>
			</batchRequest>
		</soap-env:Body>
	</soap-env:Envelope>
	""" % (input,query)
	
	req = urllib2.Request(url, request_body, headers)
	response = urllib2.urlopen(req).read()
	
	# parse the result
	response_doc = parseString(response)
	
	return_list = []
	
	result_people = response_doc.getElementsByTagName('searchResultEntry')
	
	for person in result_people:
		# get all returned attributes
		search_result = person.getElementsByTagName('attr')
		
		user_info = {}
		
		# for each attribute, store the attribute-value pair in user_info
		for attribute in search_result:
			for element in attribute.getElementsByTagName('value'):
				user_info[attribute.getAttribute('name')] = element.firstChild.data
		
		return_list.append(user_info)

	return return_list	
	
	