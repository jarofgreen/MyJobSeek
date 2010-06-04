#!/usr/bin/env python
__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

import sys, os
import logging
from datetime import datetime

sys.path.append('/usr/share/python-support/python-django/django/')
sys.path.append(os.path.dirname(__file__))

from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.contrib.auth.models import User
from myjobapps.models import EmailMessage, getUserProfile

import email

logging.basicConfig(filename=settings.EMAIL_IMPORT_LOG,level=logging.DEBUG,)

# get string from standard io
myString = sys.stdin.readlines()

# turn it into a email message
msg = email.message_from_string("".join(myString))
logging.debug('Headers: '+str(msg.items()))
emailto_bits =  msg['X-Original-To'].split('@')
if emailto_bits[1] != settings.USER_EMAIL_DOMAIN:
	logging.error('Could not find to email address! '+emailto_bits[1]+" is not "+settings.USER_EMAIL_DOMAIN)
	sys.exit(1)
username = emailto_bits[0]
logging.debug('Found username: '+username)


	
# check user exists and is valid, error if not
try:
	user = User.objects.get(is_active=True, username=username)
except User.DoesNotExist:
	print "NO USER "+username+" COULD BE FOUND ON MY JOB SEEK"
	logging.debug('Cant load user: '+username)
	sys.exit(1)
	
# check user is allowed emails
up = getUserProfile(user)
if not up.can_accept_emails():
	print "USER "+username+" CAN NOT CURRENTLY ACCEPT EMAILS; PLEASE TRY AGAIN SOON!"
	logging.debug('user not accepting emails: '+username)
	sys.exit(1)

# finally write into Database
body = False
if msg.is_multipart():
	for part in msg.walk():
		if part.get_content_type() == 'text/plain' and not body:
			body = part.get_payload(decode=True)
else:
	body = msg.get_payload(decode=True)

m = EmailMessage(User=user)
m.Subject = msg['Subject']
m.MessageID = msg['Message-Id']
m.From = msg['From']
m.To = msg['To']
m.Body = body
m.EmailDate = datetime.now()
m.Headers = str(msg.items())
m.save()
print "OK"

# now spawn child process to file email. don't wait for results; we want the email
# program to get a message back as soon as possible and the filing may take time
cmd = os.path.join(os.getcwd(), 'fileemail.py')
args = [cmd,  str(m.id)]
pid = os.spawnvpe(os.P_NOWAIT, cmd, args, os.environ)
logging.debug('Spawned Filing Process: '+cmd+' ID is: '+ str(pid))






