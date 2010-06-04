__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

class Company(models.Model):
	Title = models.CharField(max_length=255)
	Note = models.TextField(blank=True)
	URL = models.URLField(verify_exists=False,blank=True,null=True)
	IsInteresting = models.BooleanField(default=True)
	User = models.ForeignKey(User, related_name="companyuser")
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		return '/company/' + str(self.id) + '/'
	def get_jobs(self):
		return Job.objects.filter(Company=self, User=self.User).order_by('Title')
	def get_interesting_jobs(self):
		return Job.objects.filter(Company=self, User=self.User, IsInteresting=True).order_by('Title')
	def get_boring_jobs(self):
		return Job.objects.filter(Company=self, User=self.User, IsInteresting=False).order_by('Title')
	def get_childdata(self):
		cd = list(Note.objects.filter(Q(Company=self) | Q(Job__Company=self), User=self.User).order_by('Created'))
		cd.extend(Task.objects.filter(Q(Company=self) | Q(Job__Company=self), User=self.User).order_by('Created'))
		cd.extend(Appointment.objects.filter(Q(Company=self) | Q(Job__Company=self), User=self.User).order_by('Created'))
		cd.extend(Communication.objects.filter(Q(Company=self) | Q(Job__Company=self), User=self.User).order_by('Created'))
		cd.extend(EmailMessage.objects.filter(Q(Company=self) | Q(Job__Company=self), IsDeleted=False,IsSpam=False,User=self.User).order_by('Created'))
		def compare_created(a, b):
			return cmp(a.Created, b.Created)
		return sorted(cd, compare_created)
	def has_action_points(self):
		if Task.objects.filter(Company=self, IsCompleted=False, User=self.User ).count() > 0:
			return True
		if Appointment.objects.filter(Company=self, End__gt=datetime.now(), User=self.User ).count() > 0:
			return True
		return False
	def needs_action_point(self):
		if not self.IsInteresting:
			return False
		else:
			return not self.has_action_points()

class Agency(models.Model):
	Title = models.CharField(max_length=255)
	Note = models.TextField(blank=True)
	URL = models.URLField(verify_exists=False,blank=True,null=True)
	IsInteresting = models.BooleanField(default=True)
	User = models.ForeignKey(User, related_name="agencyuser")
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		return '/agency/' + str(self.id) + '/'
	def get_jobs(self):
		return Job.objects.filter(Agency=self, User=self.User).order_by('Title')
	def get_interesting_jobs(self):
		return Job.objects.filter(Agency=self, User=self.User, IsInteresting=True).order_by('Title')
	def get_boring_jobs(self):
		return Job.objects.filter(Agency=self, User=self.User, IsInteresting=False).order_by('Title')
	def get_childdata(self):
		cd = list(Note.objects.filter(Q(Agency=self) | Q(Job__Agency=self), User=self.User).order_by('Created'))
		cd.extend(Task.objects.filter(Q(Agency=self) | Q(Job__Agency=self), User=self.User).order_by('Created'))
		cd.extend(Appointment.objects.filter(Q(Agency=self) | Q(Job__Agency=self), User=self.User).order_by('Created'))
		cd.extend(Communication.objects.filter(Q(Agency=self) | Q(Job__Agency=self), User=self.User).order_by('Created'))
		cd.extend(EmailMessage.objects.filter(Q(Agency=self) | Q(Job__Agency=self), IsDeleted=False,IsSpam=False,User=self.User).order_by('Created'))
		def compare_created(a, b):
			return cmp(a.Created, b.Created)
		return sorted(cd, compare_created)
	def has_action_points(self):
		if Task.objects.filter(Agency=self, IsCompleted=False, User=self.User ).count() > 0:
			return True
		if Appointment.objects.filter(Agency=self, End__gt=datetime.now(), User=self.User ).count() > 0:
			return True
		return False
	def needs_action_point(self):
		if not self.IsInteresting:
			return False
		else:
			return not self.has_action_points()
	def can_lose_intrest(self):
		if Job.objects.filter(IsInteresting=True, Agency=self):
			return False
		else:
			return True

class Job(models.Model):
	Title = models.CharField(max_length=255)
	Note = models.TextField(blank=True)
	URL = models.URLField(verify_exists=False,blank=True,null=True)
	IsInteresting = models.BooleanField(default=True)
	User = models.ForeignKey(User, related_name="jobuser")
	Agency = models.ForeignKey(Agency, related_name="jobagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="jobcompany", blank=True, null=True )
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		return '/job/' + str(self.id) + '/'
	def get_childdata(self):
		cd = list(Note.objects.filter(Job=self, User=self.User).order_by('Created'))
		cd.extend(Task.objects.filter(Job=self, User=self.User).order_by('Created'))
		cd.extend(Appointment.objects.filter(Job=self, User=self.User).order_by('Created'))
		cd.extend(Communication.objects.filter(Job=self, User=self.User).order_by('Created'))
		cd.extend(EmailMessage.objects.filter(Job=self, IsDeleted=False,IsSpam=False,User=self.User).order_by('Created'))
		def compare_created(a, b):
			return cmp(a.Created, b.Created)
		return sorted(cd, compare_created)
	def has_action_points(self):
		if Task.objects.filter(Job=self, IsCompleted=False, User=self.User ).count() > 0:
			return True
		if Appointment.objects.filter(Job=self, End__gt=datetime.now(), User=self.User ).count() > 0:
			return True
		return False
	def needs_action_point(self):
		if not self.IsInteresting:
			return False
		else:
			return not self.has_action_points()
	def can_lose_intrest(self):
		if Job.objects.filter(IsInteresting=True, Company=self):
			return False
		else:
			return True

class Note(models.Model):
	Note = models.TextField()
	User = models.ForeignKey(User, related_name="noteuser")
	Agency = models.ForeignKey(Agency, related_name="noteagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="notecompany", blank=True, null=True )
	Job = models.ForeignKey(Job, related_name="notejob", blank=True, null=True )
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		if self.Job:
			return '/job/' + str(self.Job.id) + '/#n' + str(self.id)
		elif self.Agency:
			return '/agency/' + str(self.Agency.id) + '/#n' + str(self.id)
		elif self.Company:
			return '/company/' + str(self.Company.id) + '/#n' + str(self.id)
	def isLinkedToIntrestingThing(self):
		if self.Job:
			return self.Job.IsInteresting
		elif self.Agency:
			return self.Agency.IsInteresting
		elif self.Company:
			return self.Company.IsInteresting
		else:
			raise Exception("THIS NOTE DATA IS NOT LINKED TO ANYTHING!")

class Communication(models.Model):
	Note = models.TextField()
	User = models.ForeignKey(User, related_name="communicationuser")
	Agency = models.ForeignKey(Agency, related_name="communicationagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="communicationcompany", blank=True, null=True )
	Job = models.ForeignKey(Job, related_name="communicationjob", blank=True, null=True )
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		if self.Job:
			return '/job/' + str(self.Job.id) + '/#c' + str(self.id)
		elif self.Agency:
			return '/agency/' + str(self.Agency.id) + '/#c' + str(self.id)
		elif self.Company:
			return '/company/' + str(self.Company.id) + '/#c' + str(self.id)
	def getCompany(self):
		if self.Company:
			return self.Company
		elif self.Job:
			return self.Job.Company
	def getAgency(self):
		if self.Agency:
			return self.Agency
		elif self.Job:
			return self.Job.Agency
	def isLinkedToIntrestingThing(self):
		if self.Job:
			return self.Job.IsInteresting
		elif self.Agency:
			return self.Agency.IsInteresting
		elif self.Company:
			return self.Company.IsInteresting
		else:
			raise Exception("THIS COMMUNICATION DATA IS NOT LINKED TO ANYTHING!")

class Task(models.Model):
	Note = models.TextField()
	Start = models.DateTimeField()
	End = models.DateTimeField()
	IsCompleted = models.BooleanField(default=False)
	User = models.ForeignKey(User, related_name="taskuser")
	Agency = models.ForeignKey(Agency, related_name="taskagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="taskcompany", blank=True, null=True )
	Job = models.ForeignKey(Job, related_name="taskjob", blank=True, null=True )
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		if self.Job:
			return '/job/' + str(self.Job.id) + '/#t' + str(self.id)
		elif self.Agency:
			return '/agency/' + str(self.Agency.id) + '/#t' + str(self.id)
		elif self.Company:
			return '/company/' + str(self.Company.id) + '/#t' + str(self.id)
	def isLinkedToIntrestingThing(self):
		if self.Job:
			return self.Job.IsInteresting
		elif self.Agency:
			return self.Agency.IsInteresting
		elif self.Company:
			return self.Company.IsInteresting
		else:
			raise Exception("THIS TASK DATA IS NOT LINKED TO ANYTHING!")
	def hasStarted(self):
		return datetime.now() > self.Start
	def isLate(self):
		return datetime.now() > self.End
	def getCompany(self):
		if self.Company:
			return self.Company
		elif self.Job:
			return self.Job.Company
	def getAgency(self):
		if self.Agency:
			return self.Agency
		elif self.Job:
			return self.Job.Agency


class Appointment(models.Model):
	Note = models.TextField()
	Start = models.DateTimeField()
	End = models.DateTimeField()
	User = models.ForeignKey(User, related_name="appointmentuser")
	Agency = models.ForeignKey(Agency, related_name="appointmentagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="appointmentcompany", blank=True, null=True )
	Job = models.ForeignKey(Job, related_name="appointmentjob", blank=True, null=True )
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		if self.Job:
			return '/job/' + str(self.Job.id) + '/#a' + str(self.id)
		elif self.Agency:
			return '/agency/' + str(self.Agency.id) + '/#a' + str(self.id)
		elif self.Company:
			return '/company/' + str(self.Company.id) + '/#a' + str(self.id)
		else:
			return '/calendar/view/'+str(self.id) +'/'
	def isLinkedToIntrestingThing(self):
		if self.Job:
			return self.Job.IsInteresting
		elif self.Agency:
			return self.Agency.IsInteresting
		elif self.Company:
			return self.Company.IsInteresting
		else:
			return True   # appointmens are a special case, they can be linked to nothing
	def get_calendar_url(self):
		return '/calendar/'+str(self.Start.year)+'/'+str(self.Start.month)+'/'
	def getCompany(self):
		if self.Company:
			return self.Company
		elif self.Job:
			return self.Job.Company
	def getAgency(self):
		if self.Agency:
			return self.Agency
		elif self.Job:
			return self.Job.Agency

class EmailMessage(models.Model):
	# for linking to data in apps
	User = models.ForeignKey(User, related_name="emailmsguser")
	Agency = models.ForeignKey(Agency, related_name="emailmessageagency", blank=True, null=True )
	Company = models.ForeignKey(Company, related_name="emailmessagecompany", blank=True, null=True )
	Job = models.ForeignKey(Job, related_name="emailmessagejob", blank=True, null=True )
	# email details
	Subject = models.CharField(max_length=255)
	From = models.CharField(max_length=255)
	To = models.CharField(max_length=255)
	Headers =  models.TextField(blank=True)
	Body =  models.TextField(blank=True)
	MessageID = models.CharField(max_length=255)
	EmailDate = models.DateTimeField(null=True, blank=True)
	# what user did with it
	IsRead = models.BooleanField(default=False)
	IsDeleted = models.BooleanField(default=False)
	DeletedDate = models.DateTimeField(null=True, blank=True)
	IsSpam = models.BooleanField(default=False)
	MarkedAsSpamDate = models.DateTimeField(null=True, blank=True)
	# meta-info on this
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def get_absolute_url(self):
		if self.Job:
			return '/job/' + str(self.Job.id) + '/#e' + str(self.id)
		elif self.Agency:
			return '/agency/' + str(self.Agency.id) + '/#e' + str(self.id)
		elif self.Company:
			return '/company/' + str(self.Company.id) + '/#e' + str(self.id)
		else:
			return '/email/' + str(self.id) + '/'
	def getCompany(self):
		if self.Company:
			return self.Company
		elif self.Job:
			return self.Job.Company
	def getAgency(self):
		if self.Agency:
			return self.Agency
		elif self.Job:
			return self.Job.Agency
	def mark_as_spam(self):
		"""If we can, mark message as spam and save. Returns whether we did or not"""
		if not self.IsSpam:
			self.IsSpam = True
			self.MarkedAsSpamDate = datetime.now()
			self.save()
			return True
		return False
	def mark_as_not_spam(self):
		"""If we can, mark message as not spam and save. Returns whether we did or not"""
		if self.IsSpam:
			self.IsSpam = False
			self.save()
			return True
		return False
	def isLinkedToIntrestingThing(self):
		if self.Job:
			return self.Job.IsInteresting
		elif self.Agency:
			return self.Agency.IsInteresting
		elif self.Company:
			return self.Company.IsInteresting
		else:
			return True   # emails are a special case, they can be linked to nothing if they haven't been filed yet
	def getSubjectFreeOfPrefixes(self):
		subject = self.Subject.strip()
		while subject.lower().startswith(('re:','fw:','fwd:')) or ( subject[0] == '[' and subject[-1] == ']' ) :
			if subject[0] == '[' and subject[-1] == ']':
				subject = subject[1:-1].strip()
			if subject.lower().startswith(('re:','fw:')):
				subject = subject[3:].strip()
			if subject.lower().startswith(('fwd:')):
				subject = subject[4:].strip()
		return subject

				




class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True )
	sendReminderEmailsMonday = models.BooleanField(default=True)
	sendReminderEmailsTuesday = models.BooleanField(default=True)
	sendReminderEmailsWednesday = models.BooleanField(default=True)
	sendReminderEmailsThursday = models.BooleanField(default=True)
	sendReminderEmailsFriday = models.BooleanField(default=True)
	sendReminderEmailsSaturday = models.BooleanField(default=True)
	sendReminderEmailsSunday = models.BooleanField(default=True)
	AppointmentReminderEmailDaysWarnings = models.PositiveIntegerField(default=4)
	TaskReminderEmailDaysWarnings = models.PositiveIntegerField(default=3)
	TaskDefaultDaystoComplete = models.PositiveIntegerField(default=7)
	sendSiteNews = models.BooleanField(default=True)
	Created = models.DateTimeField(auto_now_add=True, editable=False)
	LastEdited = models.DateTimeField(auto_now=True, editable=False)
	def reminder_emails_string(self):
		if self.sendReminderEmailsMonday and self.sendReminderEmailsTuesday and self.sendReminderEmailsWednesday and self.sendReminderEmailsThursday and self.sendReminderEmailsFriday and self.sendReminderEmailsSaturday and self.sendReminderEmailsSunday:
			return "Every day of the week"
		elif self.sendReminderEmailsMonday and self.sendReminderEmailsTuesday and self.sendReminderEmailsWednesday and self.sendReminderEmailsThursday and self.sendReminderEmailsFriday and not self.sendReminderEmailsSaturday and not self.sendReminderEmailsSunday:
			return "Every week day"
		elif not self.sendReminderEmailsMonday and not self.sendReminderEmailsTuesday and not self.sendReminderEmailsWednesday and not self.sendReminderEmailsThursday and not self.sendReminderEmailsFriday and self.sendReminderEmailsSaturday and self.sendReminderEmailsSunday:
			return "Weekends"
		else:
			out = []
			if self.sendReminderEmailsMonday:
				out.append('Monday')
			if self.sendReminderEmailsTuesday:
				out.append('Tuesday')
			if self.sendReminderEmailsWednesday:
				out.append('Wednesday')
			if self.sendReminderEmailsThursday:
				out.append('Thursday')
			if self.sendReminderEmailsFriday:
				out.append('Friday')
			if self.sendReminderEmailsSaturday:
				out.append('Saturday')
			if self.sendReminderEmailsSunday:
				out.append('Sunday')
			return ", ".join(out)
	def send_Reminder_Email(self):
		if datetime.now().date().weekday() == 0 and self.sendReminderEmailsMonday:
			return True
		elif datetime.now().date().weekday() == 1 and self.sendReminderEmailsTuesday:
			return True
		elif datetime.now().date().weekday() == 2 and self.sendReminderEmailsWednesday:
			return True
		elif datetime.now().date().weekday() == 3 and self.sendReminderEmailsThursday:
			return True
		elif datetime.now().date().weekday() == 4 and self.sendReminderEmailsFriday:
			return True
		elif datetime.now().date().weekday() == 5 and self.sendReminderEmailsSaturday:
			return True
		elif datetime.now().date().weekday() == 6 and self.sendReminderEmailsSunday:
			return True
		return False
	def can_accept_emails(self):
		"""Return Bolean"""
		## Reason: To protect against floods, user can only have a certain number of fresh emails waiting for them!
		if len(EmailMessage.objects.filter(User=self.user, IsRead=False, IsSpam=False, IsDeleted=False)) > 200:    # TODO DJANGO1.1: USE COUNT!
			return False
		return True



def getUserProfile(user):
	"""We use this, not user.get_profile() cos that doesn't create new ones if they don't exist.
	http://docs.djangoproject.com/en/1.0/topics/auth/#storing-additional-information-about-users """
	try:
		return UserProfile.objects.get(user=user)
	except UserProfile.DoesNotExist:
		return UserProfile(user=user)




class UserMessage(models.Model):
	User = models.ForeignKey(User, unique=False )
	Message = models.CharField(max_length=255)
	UndoURL = models.CharField(max_length=255)
	isRead = models.BooleanField(default=False)
	Created = models.DateTimeField(auto_now_add=True, editable=False)

def createUserMessage(user, message, undoURL=False):
	um = UserMessage(User=user, Message=message)
	if undoURL:
		um.UndoURL = undoURL
	um.save()




	
