__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

from django import forms
from myjobapps.widgets import SelectDateTimeWidget
from myjobapps.widgetneworexisting import SelectNewOrExisting
from datetime import datetime, timedelta



class NewJobForm(forms.Form):
	"""NOT used for editing, it has extra special fields"""
	def __init__(self, *args,**kargs):
		self.OldCompanies = kargs['old_companies']
		self.OldAgencies = kargs['old_agencies']
		del kargs['old_companies']
		del kargs['old_agencies']
		super(NewJobForm, self).__init__(*args,**kargs)
		# http://www.djangosnippets.org/snippets/1552/ cottoned me onto this self.fields stuff ........
		self.fields['Company'] = forms.CharField(widget=SelectNewOrExisting(old_data=self.OldCompanies),required=False, )
		self.fields['Agency'] = forms.CharField(widget=SelectNewOrExisting(old_data=self.OldAgencies),required=False, )
	Title = forms.CharField(required=True)
	Note = forms.CharField(widget=forms.Textarea,required=False)
	URL = forms.URLField(required=False, label="From Webpage")

class EditJobForm(forms.Form):
	Title = forms.CharField(required=True)
	Note = forms.CharField(widget=forms.Textarea,required=False)
	URL = forms.URLField(required=False, label="From Webpage", help_text="If you provide the website address of this job, we will attempt to provide more information for you.")

class NewAgencyForm(forms.Form):
	"""also used for editing"""
	Title = forms.CharField(required=True)
	Note = forms.CharField(widget=forms.Textarea,required=False)
	URL = forms.URLField(required=False, label="From Webpage", help_text="If you provide the website address of this agency, we will attempt to provide more information for you.")

class NewCompanyForm(forms.Form):
	"""also used for editing"""
	Title = forms.CharField(required=True)
	Note = forms.CharField(widget=forms.Textarea,required=False)
	URL = forms.URLField(required=False, label="From Webpage", help_text="If you provide the website address of this company, we will attempt to provide more information for you.")

class NewJobQuickForm(forms.Form):
	URL = forms.URLField(required=True, label="From Webpage")

class NewNoteForm(forms.Form):
	"""also used for editing"""
	Note = forms.CharField(widget=forms.Textarea,required=True)

class NewCommunicationForm(forms.Form):
	"""also used for editing"""
	Note = forms.CharField(widget=forms.Textarea,required=True, label="Email or Letter")

class NewToDoForm(forms.Form):
	"""also used for editing"""
	Note = forms.CharField(widget=forms.Textarea,required=True,  label="To Do")
	Start = forms.DateTimeField(widget=SelectDateTimeWidget, required=True, initial=datetime.now(),  label="Do this after", help_text="You will not be prompted to do this task until after this time.")
	End = forms.DateTimeField(widget=SelectDateTimeWidget, required=True, initial=(datetime.now()+timedelta(14)).replace(hour=17,minute=0),  label="Deadline")
	def clean_Start(self):
		"""Check date is sensible."""
		if self.cleaned_data['Start'].year < 2009:
			raise forms.ValidationError("The date can not be before 2009!")
		latest_year = datetime.now().year + 5
		if self.cleaned_data['Start'].year >  latest_year:
			raise forms.ValidationError("The date can not be before %s!" % (latest_year))
		return self.cleaned_data['Start']
	def clean_End(self):
		"""Check End is not before start and is sensible."""
		if self.cleaned_data['End'].year < 2009:
			raise forms.ValidationError("The date can not be after 2009!")
		latest_year = datetime.now().year + 5
		if self.cleaned_data['End'].year >  latest_year:
			raise forms.ValidationError("The date can not be before %s!" % (latest_year))
		if self.cleaned_data['End'] < self.cleaned_data['Start']:
			raise forms.ValidationError("The deaedline can not be before the starting date!")
		return self.cleaned_data['End']

class NewAppointmentForm(forms.Form):
	"""also used for editing"""
	Note = forms.CharField(widget=forms.Textarea,required=True,  label="Appointment")
	Start = forms.DateTimeField(widget=SelectDateTimeWidget, required=True, initial=(datetime.now()+timedelta(1)).replace(hour=9,minute=0))
	End = forms.DateTimeField(widget=SelectDateTimeWidget, required=True, initial=(datetime.now()+timedelta(1)).replace(hour=10,minute=0))
	def clean_Start(self):
		"""Check date is sensible."""
		if self.cleaned_data['Start'].year < 2009:
			raise forms.ValidationError("The date can not be before 2009!")
		latest_year = datetime.now().year + 5
		if self.cleaned_data['Start'].year >  latest_year:
			raise forms.ValidationError("The date can not be after %s!" % (latest_year))
		return self.cleaned_data['Start']
	def clean_End(self):
		"""Check End is not before start and is sensible."""
		if self.cleaned_data['End'].year < 2009:
			raise forms.ValidationError("The date can not be after 2009!")
		latest_year = datetime.now().year + 5
		if self.cleaned_data['End'].year >  latest_year:
			raise forms.ValidationError("The date can not be before %s!" % (latest_year))
		if self.cleaned_data['End'] < self.cleaned_data['Start']:
			raise forms.ValidationError("The end date can not be before the start date!")
		return self.cleaned_data['End']

class EditUserProfile(forms.Form):
	FirstName = forms.CharField(required=False, max_length=30,  label="First Name")
	SecondName = forms.CharField(required=False, max_length=30,   label="Last Name")
	sendReminderEmailsMonday = forms.BooleanField(required=False, label="Send reminder emails on monday")
	sendReminderEmailsTuesday =  forms.BooleanField(required=False, label="Send reminder emails on tuesday")
	sendReminderEmailsWednesday = forms.BooleanField(required=False, label="Send reminder emails on wednesday")
	sendReminderEmailsThursday =  forms.BooleanField(required=False, label="Send reminder emails on thursday")
	sendReminderEmailsFriday =  forms.BooleanField(required=False, label="Send reminder emails on friday")
	sendReminderEmailsSaturday =  forms.BooleanField(required=False, label="Send reminder emails on saturday")
	sendReminderEmailsSunday = 	 forms.BooleanField(required=False, label="Send reminder emails on sunday")
	AppointmentReminderEmailDaysWarnings = forms.IntegerField(required=True, min_value=1, max_value=14, label="Warning for Appointments (in days)")
	TaskReminderEmailDaysWarnings = forms.IntegerField(required=True, min_value=1, max_value=14, label="Warning for Tasks (in days)")
	TaskDefaultDaystoComplete = forms.IntegerField(required=True, min_value=1, max_value=60, label="Default number of days to compelete a Task")




