__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


from myjobapps.models import *
from django.http import Http404


def loadAgencyOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['agency'] = Agency.objects.get(id=kargs['agency'], User=args[0].user)
		except Agency.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadCompanyOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['company'] = Company.objects.get(id=kargs['company'], User=args[0].user)
		except Company.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadJobOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['job'] = Job.objects.get(id=kargs['job'], User=args[0].user)
		except Job.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadOrphanAppointmentOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['appointment'] = Appointment.objects.get(id=kargs['appointment'], User=args[0].user, Job__isnull=True,  Company__isnull=True,  Agency__isnull=True)
		except Appointment.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f

def loadTaskOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['task'] = Task.objects.get(id=kargs['task'], User=args[0].user)
		except Task.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadNoteOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['note'] = Note.objects.get(id=kargs['note'], User=args[0].user)
		except Note.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadCommunicationOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['communication'] = Communication.objects.get(id=kargs['communication'], User=args[0].user)
		except Communication.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadAppointmentOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['appointment'] = Appointment.objects.get(id=kargs['appointment'], User=args[0].user)
		except Appointment.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f



def loadEmailMessageOr404(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		try:
			kargs['emailmessage'] = EmailMessage.objects.get(id=kargs['emailmessage'], User=args[0].user)
		except EmailMessage.DoesNotExist:
			raise Http404()
		return f(*args,**kargs)
	return new_f


def loadAgencyIfSet(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		if 'agency' in kargs and kargs['agency']:
			try:
				kargs['agency'] = Agency.objects.get(id=kargs['agency'], User=args[0].user)
			except Agency.DoesNotExist:
				raise Http404()
		return f(*args,**kargs)
	return new_f


def loadCompanyIfSet(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		if 'company'  in kargs and kargs['company']:
			try:
				kargs['company'] = Company.objects.get(id=kargs['company'], User=args[0].user)
			except Company.DoesNotExist:
				raise Http404()
		return f(*args,**kargs)
	return new_f


def loadJobIfSet(f):
	def new_f(*args,**kargs):
		if not args[0].user.is_authenticated():
			raise Http404()   # extra layer of security: be really sure we are logged in at this stage
		if 'job' in kargs and kargs['job']:
			try:
				kargs['job'] = Job.objects.get(id=kargs['job'], User=args[0].user)
			except Job.DoesNotExist:
				raise Http404()
		return f(*args,**kargs)
	return new_f

def yearMonthValidIntegerOr404(f):
	def new_f(*args,**kargs):
		kargs['year'], kargs['month'] = int(kargs['year']), int(kargs['month'])
		if kargs['month'] < 1 or kargs['month'] > 12:
			raise Http404()
		if kargs['year'] < 2000 or kargs['year'] > 2100:
			raise Http404()
		return f(*args,**kargs)
	return new_f



