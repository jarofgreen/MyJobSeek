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
from myjobapps.models import EmailMessage

import email

logging.basicConfig(filename=settings.EMAIL_IMPORT_LOG,level=logging.DEBUG,)
logging.debug('File Email Process Started')

# get string from standard io
emailID = int(sys.argv[1])
logging.debug('Trying to file email id='+str(emailID))

try:
	email = EmailMessage.objects.get(id=emailID)
except EmailMessage.DoesNotExist:
	logging.debug('Could not load requested email for filing: '+str(emailID))
	print "NOLOAD"
	sys.exit(1)

if email.Job or email.Company or email.Agency:
	logging.debug('This Email already seems to be filled! id='+str(emailID))
	print "ALREADY FILED"
	sys.exit(1)

jobs = []
companies = []
agencies = []

# ATTEMPT 1: load all addresses mentioned, and take out our own
#addresses = email.To.split(",")
#addresses.extend(email.From.split(","))
#addresses = [i for i in addresses if i.find(email.User.email) == -1 and  i.find(email.User.username+"@"+settings.USER_EMAIL_DOMAIN) == -1]
# so this isn't really going till work until we sort out the forwarding email thing

#ATTEMPT 2: subject?
for data in EmailMessage.objects.filter(Subject__contains=email.getSubjectFreeOfPrefixes()):
	#print data
	if data.Job and not data.Job in jobs:
		jobs.append(data.Job)
	if data.Company and not data.Company in companies:
		companies.append(data.Company)
	if data.Agency and not data.Agency in agencies:
		agencies.append(data.Agency)


#Finish
found = False

#print jobs
#print companies
#print agencies

if len(jobs) == 1:
	email.Job = jobs[0]
	found = True
if len(companies) == 1:
	email.Company = companies[0]
	found = True
if len(agencies) == 1:
	email.Agency = agencies[0]
	found = True

if found:
	print "OK"
	email.save()
	#pass


