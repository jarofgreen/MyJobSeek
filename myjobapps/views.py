__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

import decorators
import forms

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import auth
from django.template import RequestContext
import myjobapps.decorators as decorators
import myjobapps.forms as forms
from myjobapps.models import *
from datetime import datetime,timedelta
from myjobapps.appointmentscalendar import appointmentscalendar
from django.core.mail import send_mail
import settings
from django.core.paginator import Paginator, EmptyPage
import fetchjobdetails


def homepageView(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.NewJobQuickForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				request.session['new_job_url'] = cd['URL']
				return HttpResponseRedirect('/newjob/')
		else:
			form = forms.NewJobQuickForm( )
		# emails
		emails = EmailMessage.objects.filter(User=request.user, IsDeleted=False, IsSpam=False, IsRead=False)
		unfiledemails = EmailMessage.objects.filter(User=request.user, IsDeleted=False, IsSpam=False, IsRead=True, Company=None, Job=None, Agency=None)
		# other data
		todos = [ i for i in Task.objects.filter(User=request.user, Start__lt=datetime.now(), IsCompleted=False).order_by('End') if i.isLinkedToIntrestingThing()]
		appointments =  [ i for i in Appointment.objects.filter(User=request.user, End__gt=datetime.now()).order_by('Start') if i.isLinkedToIntrestingThing()]
		# return
		return render_to_response('frontpageloggedin.html',{ "todos":todos, "appointments":appointments, 'form': form,'emails':emails,'unfiledemails':unfiledemails, 'userprofile':getUserProfile(request.user)}, context_instance=RequestContext(request))
	else:
		return render_to_response('frontpage.html',{ }, context_instance=RequestContext(request))




def viewPublicStaticPage(request, templatename):
    return render_to_response(templatename, {},  context_instance=RequestContext(request))


@login_required
def viewMyProfile(request):
	return render_to_response('myprofile.html',{'profile':getUserProfile(request.user) }, context_instance=RequestContext(request))

@login_required
def editMyProfile(request):
	initial = { 'FirstName':request.user.first_name, 'SecondName':request.user.last_name}
	profile = getUserProfile(request.user)
	initial['sendReminderEmailsMonday'] = profile.sendReminderEmailsMonday
	initial['sendReminderEmailsTuesday'] = profile.sendReminderEmailsTuesday
	initial['sendReminderEmailsWednesday'] = profile.sendReminderEmailsWednesday
	initial['sendReminderEmailsThursday'] = profile.sendReminderEmailsThursday
	initial['sendReminderEmailsFriday'] = profile.sendReminderEmailsFriday
	initial['sendReminderEmailsSaturday'] = profile.sendReminderEmailsSaturday
	initial['sendReminderEmailsSunday'] = profile.sendReminderEmailsSunday
	initial['AppointmentReminderEmailDaysWarnings'] = profile.AppointmentReminderEmailDaysWarnings
	initial['TaskReminderEmailDaysWarnings'] = profile.TaskReminderEmailDaysWarnings
	initial['TaskDefaultDaystoComplete'] = profile.TaskDefaultDaystoComplete
	if request.method == 'POST':
		form = forms.EditUserProfile(request.POST, initial=initial)
		if form.is_valid():
			cd = form.cleaned_data
			request.user.first_name, request.user.last_name = cd['FirstName'], cd['SecondName']
			request.user.save()
			profile.sendReminderEmailsMonday = cd['sendReminderEmailsMonday']
			profile.sendReminderEmailsTuesday = cd['sendReminderEmailsTuesday']
			profile.sendReminderEmailsWednesday=cd['sendReminderEmailsWednesday']
			profile.sendReminderEmailsThursday=cd['sendReminderEmailsThursday']
			profile.sendReminderEmailsFriday=cd['sendReminderEmailsFriday']
			profile.sendReminderEmailsSaturday=cd['sendReminderEmailsSaturday']
			profile.sendReminderEmailsSunday=cd['sendReminderEmailsSunday']
			profile.AppointmentReminderEmailDaysWarnings=cd['AppointmentReminderEmailDaysWarnings']
			profile.TaskReminderEmailDaysWarnings=cd['TaskReminderEmailDaysWarnings']
			profile.TaskDefaultDaystoComplete = cd['TaskDefaultDaystoComplete']
			profile.save()
			return HttpResponseRedirect('/myprofile/')
	else:
		form = forms.EditUserProfile(  initial=initial)
	return render_to_response('editprofile.html',{'form':form, 'profile':getUserProfile(request.user) }, context_instance=RequestContext(request))

@login_required
@decorators.yearMonthValidIntegerOr404
def viewCalendar(request,year,month):
	d = { 'year': year, 'month':month, 'today': datetime.now().date() }
	d.update(appointmentscalendar(request, year, month,))
	if month == 1:
		d['prevlink'] = "/calendar/"+str(year-1)+"/12/"
	else:
		d['prevlink'] = "/calendar/"+str(year)+"/"+str(month-1)+"/"
	if month == 12:
		d['nextlink'] = "/calendar/"+str(year+1)+"/1/"
	else:
		d['nextlink'] = "/calendar/"+str(year)+"/"+str(month+1)+"/"
	now = datetime.now()
	if now.month != month or now.year != year:
		d['todaylink'] = "/calendar/"
		# next 2 lines could be a really simple template tag
	monthnames = ['January','February','March','April','May','June','July','August','September','October','November','December']
	d['monthname'] = monthnames[month-1]
	return render_to_response('calendar.html',d, context_instance=RequestContext(request))


@login_required
@decorators.loadOrphanAppointmentOr404
def viewOrphanAppointment(request, appointment):
	return render_to_response('orphanappointment.html',{ 'appointment':appointment, }, context_instance=RequestContext(request))

@login_required
@decorators.loadCompanyOr404
def viewCompany(request, company):
	return render_to_response('company.html',{ 'company':company, }, context_instance=RequestContext(request))


@login_required
@decorators.loadJobOr404
def viewJob(request,job):
	return render_to_response('job.html',{ 'job':job, }, context_instance=RequestContext(request))


@login_required
@decorators.loadAgencyOr404
def viewAgency(request,agency):
	return render_to_response('agency.html',{ 'agency':agency,}, context_instance=RequestContext(request))

@login_required
@decorators.loadJobOr404
def viewJobAddCompany(request,job):
	if request.method == 'POST':
		form = forms.NewCompanyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			c = Company(User=request.user, Title=cd['Title'], Note=cd['Note'], URL=cd['URL'])
			c.save()
			job.Company = c
			job.save()
			return HttpResponseRedirect(job.get_absolute_url())
	else:
		form = forms.NewCompanyForm( )
	companies = Company.objects.filter(User=request.user).order_by('Title')
	return render_to_response('jobaddcompany.html',{ 'job':job, 'form': form, 'companies':companies}, context_instance=RequestContext(request))

@login_required
@decorators.loadJobOr404
@decorators.loadCompanyOr404
def viewJobAddExistingCompany(request, job, company):
	job.Company = company
	job.save()
	return HttpResponseRedirect(job.get_absolute_url())

@login_required
@decorators.loadJobOr404
def viewJobAddAgency(request,job):
	if request.method == 'POST':
		form = forms.NewAgencyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			a = Agency(User=request.user, Title=cd['Title'], Note=cd['Note'], URL=cd['URL'])
			a.save()
			job.Agency = a
			job.save()
			return HttpResponseRedirect(job.get_absolute_url())
	else:
		form = forms.NewAgencyForm( )
	agencies = Agency.objects.filter(User=request.user).order_by('Title')
	return render_to_response('jobaddagent.html',{ 'job':job, 'form': form, 'agencies':agencies}, context_instance=RequestContext(request))

@login_required
@decorators.loadJobOr404
@decorators.loadAgencyOr404
def viewJobAddExistingAgency(request, job, agency):
	job.Agency = agency
	job.save()
	return HttpResponseRedirect(job.get_absolute_url())

@login_required
def addNewJob(request):
	if request.method == 'POST':
		form = forms.NewJobForm(request.POST, old_companies=Company.objects.filter(User=request.user), old_agencies=Agency.objects.filter(User=request.user) )
		if form.is_valid():
			cd = form.cleaned_data
			# job
			j = Job(User=request.user, Title=cd['Title'], Note=cd['Note'], URL=cd['URL'])
			# company
			if cd['Company'][0:4] == "NEW:":
				newTitle = cd['Company'][4:]
				if newTitle:
					c = Company(User=request.user, Title=newTitle)
					c.save()
					j.Company=c
			else:
				try:
					j.Company = Company.objects.get(id=int(cd['Company']), User=request.user)
				except Company.DoesNotExist:
					print "COULD NOT LOAD COMPANY: "+cd['Company']
			# agency
			if cd['Agency'][0:4] == "NEW:":
				newTitle = cd['Agency'][4:]
				if newTitle:
					c = Agency(User=request.user, Title=newTitle)
					c.save()
					j.Agency=c
			else:
				try:
					j.Agency = Agency.objects.get(id=int(cd['Agency']), User=request.user)
				except Agency.DoesNotExist:
					print "COULD NOT LOAD AGENCY: "+cd['Agency']
			# all done
			j.save()
			up = getUserProfile(request.user)
			t = Task(User=request.user, Job=j, Note="Apply for this job.", Start=datetime.now(), End=(datetime.now()+timedelta(up.TaskDefaultDaystoComplete)).replace(hour=17,minute=0))
			t.save()
			return HttpResponseRedirect(j.get_absolute_url())
	else:
		initial = {}
		if 'new_job_url' in request.session:
			initial['URL'] = request.session['new_job_url']
			initial['Title'], initial['Note'] = fetchjobdetails.fetch(initial['URL'])
			del request.session['new_job_url']
		if 'agency' in request.GET:
			initial['Agency'] = int(request.GET['agency'])
		if 'company' in request.GET:
			initial['Company'] = int(request.GET['company'])
		form = forms.NewJobForm( initial=initial, old_companies=Company.objects.filter(User=request.user), old_agencies=Agency.objects.filter(User=request.user) )
	return render_to_response('newjob.html', {'form': form,},context_instance=RequestContext(request))
	
@login_required
def addNewAgency(request):
	if request.method == 'POST':
		form = forms.NewAgencyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			a = Agency(User=request.user, Title=cd['Title'], Note=cd['Note'], URL=cd['URL'])
			a.save()
			return HttpResponseRedirect(a.get_absolute_url())
	else:
		form = forms.NewAgencyForm( )
	return render_to_response('newagency.html', {'form': form,},context_instance=RequestContext(request))

@login_required
def addNewCompany(request):
	if request.method == 'POST':
		form = forms.NewCompanyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			c = Company(User=request.user, Title=cd['Title'], Note=cd['Note'], URL=cd['URL'])
			c.save()
			return HttpResponseRedirect(c.get_absolute_url())
	else:
		form = forms.NewCompanyForm( )
	return render_to_response('newcompany.html', {'form': form,},context_instance=RequestContext(request))

@login_required
@decorators.loadJobOr404
def editJob(request,job):
	if request.method == 'POST':
		form = forms.EditJobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			job.Title, job.Note, job.URL = cd['Title'], cd['Note'], cd['URL']
			job.save()
			return HttpResponseRedirect(job.get_absolute_url())
	else:
		form = forms.EditJobForm( initial={'Title':job.Title, 'Note':job.Note, 'URL':job.URL} )
	return render_to_response('editjob.html', {'form': form, 'job':job},context_instance=RequestContext(request))

@login_required
@decorators.loadAgencyOr404
def editAgency(request,agency):
	if request.method == 'POST':
		form = forms.NewAgencyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			agency.Title, agency.Note, agency.URL  = cd['Title'], cd['Note'], cd['URL']
			agency.save()
			return HttpResponseRedirect(agency.get_absolute_url())
	else:
		form = forms.NewAgencyForm(  initial={'Title':agency.Title, 'Note':agency.Note, 'URL':agency.URL} )
	return render_to_response('editagency.html', {'form': form,'agency':agency},context_instance=RequestContext(request))

@login_required
@decorators.loadCompanyOr404
def editCompany(request,company):
	if request.method == 'POST':
		form = forms.NewCompanyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			company.Title, company.Note, company.URL = cd['Title'], cd['Note'], cd['URL']
			company.save()
			return HttpResponseRedirect(company.get_absolute_url())
	else:
		form = forms.NewCompanyForm(  initial={'Title':company.Title, 'Note':company.Note, 'URL':company.URL} )
	return render_to_response('editcompany.html', {'form': form,'company':company},context_instance=RequestContext(request))


@login_required
@decorators.loadTaskOr404
def editTask(request,task):
	if request.method == 'POST':
		form = forms.NewToDoForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			task.Start, task.End, task.Note = cd['Start'], cd['End'], cd['Note']
			task.save()
			return HttpResponseRedirect(task.get_absolute_url())
	else:
		form = forms.NewToDoForm(  initial={'Start':task.Start, 'End':task.End, 'Note':task.Note} )
	return render_to_response('edittask.html', {'form': form,'task':task},context_instance=RequestContext(request))


@login_required
@decorators.loadNoteOr404
def editNote(request,note):
	if request.method == 'POST':
		form = forms.NewNoteForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			note.Note = cd['Note']
			note.save()
			return HttpResponseRedirect(note.get_absolute_url())
	else:
		form = forms.NewNoteForm(  initial={ 'Note':note.Note} )
	return render_to_response('editnote.html', {'form': form,'note':note},context_instance=RequestContext(request))


@login_required
@decorators.loadCommunicationOr404
def editCommunication(request,communication):
	if request.method == 'POST':
		form = forms.NewCommunicationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			communication.Note = cd['Note']
			communication.save()
			return HttpResponseRedirect(communication.get_absolute_url())
	else:
		form = forms.NewCommunicationForm(  initial={ 'Note':communication.Note} )
	return render_to_response('editcommunication.html', {'form': form,'communication':communication},context_instance=RequestContext(request))


@login_required
@decorators.loadAppointmentOr404
def editAppointment(request,appointment):
	if request.method == 'POST':
		form = forms.NewAppointmentForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			appointment.Start, appointment.End, appointment.Note = cd['Start'], cd['End'], cd['Note']
			appointment.save()
			return HttpResponseRedirect(appointment.get_absolute_url())
	else:
		form = forms.NewAppointmentForm(  initial={'Start':appointment.Start, 'End':appointment.End, 'Note':appointment.Note} )
	return render_to_response('editappointment.html', {'form': form,'appointment':appointment},context_instance=RequestContext(request))

@login_required
def listThings(request, model, includeboring, title, newurl):
	things = model.objects.filter(User=request.user).order_by('Title')
	if not includeboring:
		things = things.filter(IsInteresting=True)
	return render_to_response('listthings.html', {'things': things, 'includeboring':includeboring,'title':title, 'newurl':newurl},context_instance=RequestContext(request))

@login_required
@decorators.loadTaskOr404
def completeTask(request, task):
	if not task.IsCompleted:
		task.IsCompleted = True
		task.save()
		createUserMessage(request.user, 'The task has been completed.', undoURL='/uncompletetodo/'+str(task.id)+'/')
	return HttpResponseRedirect(task.get_absolute_url())

@login_required
@decorators.loadTaskOr404
def uncompleteTask(request, task):
	if task.IsCompleted:
		task.IsCompleted = False
		task.save()
		createUserMessage(request.user, 'The task has been  marked not complete.', undoURL='/completetodo/'+str(task.id)+'/')
	return HttpResponseRedirect(task.get_absolute_url())

@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
def setAgencyOrCompanyInteresting(request, company=False, agency=False):
	if company:
		thing = company
	elif agency:
		thing = agency
	thing.IsInteresting = True
	thing.save()
	return HttpResponseRedirect(thing.get_absolute_url())

@login_required
@decorators.loadJobOr404
def setJobInteresting(request, job):
	job.IsInteresting = True
	job.save()
	if job.Company and not job.Company.IsInteresting:
		createUserMessage(request.user, 'We have marked that you are interested in the company to.')
		job.Company.IsInteresting = True
		job.Company.save()
	if job.Agency and not job.Agency.IsInteresting:
		createUserMessage(request.user, 'We have marked that you are interested in the agency to.')
		job.Agency.IsInteresting = True
		job.Agency.save()
	return HttpResponseRedirect(job.get_absolute_url())

@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
def setAgencyOrCompanyNotInteresting(request,  company=False, agency=False):
	if company:
		thing = company
		jobs = Job.objects.filter(IsInteresting=True, Company=thing)
	elif agency:
		thing = agency
		jobs = Job.objects.filter(IsInteresting=True, Agency=thing)
	if jobs:
		createUserMessage(request.user, 'But you are still interested in some jobs!')
	else:
		thing.IsInteresting = False
		thing.save()
	return HttpResponseRedirect(thing.get_absolute_url())

@login_required
@decorators.loadJobOr404
def setJobNotInteresting(request,  job):
	job.IsInteresting = False
	job.save()
	if job.Company:
		if not Job.objects.filter(IsInteresting=True, Company=job.Company):  #TODO: in Django 1.1 turn into count
			createUserMessage(request.user, 'You are now interested in no jobs at the Company, so we have marked that you are not interested in that either.')
			job.Company.IsInteresting = False
			job.Company.save()
	if job.Agency:
		if not Job.objects.filter(IsInteresting=True, Agency=job.Agency):    #TODO: in Django 1.1 turn into count
			createUserMessage(request.user, 'You are now interested in no jobs at the Agency, so we have marked that you are not interested in that either.')
			job.Agency.IsInteresting = False
			job.Agency.save()
	return HttpResponseRedirect(job.get_absolute_url())


@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
@decorators.loadJobIfSet
def addNote(request, job=False, company=False, agency=False):
	if request.method == 'POST':
		form = forms.NewNoteForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			n = Note(User=request.user, Note=cd['Note'])
			if job:
				n.Job = job
			if company:
				n.Company = company
			if agency:
				n.Agency = agency
			n.save()
			return HttpResponseRedirect(n.get_absolute_url())
	else:
		form = forms.NewNoteForm( )
	return render_to_response('addnote.html',{ 'job':job, 'company':company, 'agency':agency, 'form': form, 'title':'Note'}, context_instance=RequestContext(request))

@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
@decorators.loadJobIfSet
def addCommunication(request, job=False, company=False, agency=False):
	if request.method == 'POST':
		form = forms.NewCommunicationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			n = Communication(User=request.user, Note=cd['Note'])
			if job:
				n.Job = job
			if company:
				n.Company = company
			if agency:
				n.Agency = agency
			n.save()
			return HttpResponseRedirect(n.get_absolute_url())

	else:
		form = forms.NewCommunicationForm( )
	return render_to_response('addcommunication.html',{ 'job':job, 'company':company, 'agency':agency, 'form': form, 'title':'Communication'}, context_instance=RequestContext(request))

@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
@decorators.loadJobIfSet
def addTask(request, job=False, company=False, agency=False):
	if request.method == 'POST':
		form = forms.NewToDoForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			n = Task(User=request.user, Note=cd['Note'], Start=cd['Start'], End=cd['End'])
			if job:
				n.Job = job
			if company:
				n.Company = company
			if agency:
				n.Agency = agency
			n.save()
			return HttpResponseRedirect(n.get_absolute_url())
	else:
		up = getUserProfile(request.user)
		form = forms.NewToDoForm( initial = {'End':(datetime.now()+timedelta(up.TaskDefaultDaystoComplete)).replace(hour=17,minute=0)} )
	return render_to_response('addtodo.html',{ 'job':job, 'company':company, 'agency':agency, 'form': form, 'title':'ToDo'}, context_instance=RequestContext(request))

@login_required
@decorators.loadAgencyIfSet
@decorators.loadCompanyIfSet
@decorators.loadJobIfSet
def addAppointment(request, job=False, company=False, agency=False):
	if request.method == 'POST':
		form = forms.NewAppointmentForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			a = Appointment(User=request.user, Note=cd['Note'], Start=cd['Start'], End=cd['End'])
			if job:
				a.Job = job
			if company:
				a.Company = company
			if agency:
				a.Agency = agency
			a.save()
			return HttpResponseRedirect(a.get_absolute_url())
	else:
		form = forms.NewAppointmentForm( )
	return render_to_response('addappointment.html',{ 'job':job, 'company':company, 'agency':agency, 'form': form, 'title':'Appointment'}, context_instance=RequestContext(request))




@login_required
def giveFeedBack(request):
	if 'FeedBack' in request.POST and request.POST['FeedBack'] and 'FeedBackOnURL' in request.POST:
		recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
		msg = "User: " + request.user.username + "\n\n"
		msg = msg + "Email: " + request.user.email + "\n\n"
		msg = msg + "URL: " + request.POST['FeedBackOnURL'] + "\n\n"
		msg = msg + "Msg:\n\n" + request.POST['FeedBack']
		#print msg
		send_mail(fail_silently=False, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list, subject="Feedback Given on myJobSeek.net", message=msg)
		return render_to_response('thanksforfeedback.html',{ 'url':request.POST['FeedBackOnURL'] }, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')


@login_required
def listCorrespondence(request, pagenumber=1):
	cd = list(Communication.objects.filter(User=request.user).order_by('-Created'))
	cd.extend(EmailMessage.objects.filter(IsDeleted=False,IsSpam=False, User=request.user).order_by('-Created'))
	def compare_created(a, b):
		return cmp(a.Created, b.Created)
	paginator =  Paginator(sorted(cd, compare_created),10)
	try:
		page = paginator.page(pagenumber)
	except EmptyPage:
		raise Http404()
	return render_to_response('correspondence.html', {'paginator': paginator, 'page':page },context_instance=RequestContext(request))


@login_required
def listActivity(request, pagenumber=1):
	objects = list(Note.objects.filter(User=request.user).order_by('-Created'))
	objects.extend(Task.objects.filter(User=request.user).order_by('-Created'))
	objects.extend(Appointment.objects.filter(User=request.user).order_by('-Created'))
	objects.extend(Communication.objects.filter(User=request.user).order_by('-Created'))
	def compare_created(a, b):
		return cmp(b.Created, a.Created)
	paginator =  Paginator(sorted(objects, compare_created),20)
	try:
		page = paginator.page(pagenumber)
	except EmptyPage:
		raise Http404()
	return render_to_response('activity.html', {'paginator': paginator, 'page':page },context_instance=RequestContext(request))

@login_required
def listActivityLast2Weeks(request, pagenumber=1):
	date = datetime.now()-timedelta(14)
	objects = list(Note.objects.filter(User=request.user, Created__gt=date).order_by('-Created'))
	objects.extend(Task.objects.filter(User=request.user, Created__gt=date).order_by('-Created'))
	objects.extend(Appointment.objects.filter(User=request.user, Created__gt=date).order_by('-Created'))
	objects.extend(Communication.objects.filter(User=request.user, Created__gt=date).order_by('-Created'))
	def compare_created(a, b):
		return cmp(b.Created, a.Created)
	return render_to_response('activity-nopages.html', {'title':' for the last 2 weeks', 'object_list': sorted(objects, compare_created) },context_instance=RequestContext(request))


@login_required
def viewInbox(request):
	emails = EmailMessage.objects.filter(User=request.user, IsDeleted=False, IsSpam=False)
	return render_to_response('emails/inbox.html',{ 'emails':emails }, context_instance=RequestContext(request))


@login_required
def viewDeletedBox(request):
	emails = EmailMessage.objects.filter(User=request.user, IsDeleted=True)
	return render_to_response('emails/deleted.html',{ 'emails':emails }, context_instance=RequestContext(request))


@login_required
def viewSpamBox(request):
	emails = EmailMessage.objects.filter(User=request.user, IsSpam=True)
	return render_to_response('emails/spam.html',{ 'emails':emails }, context_instance=RequestContext(request))


@login_required
@decorators.loadEmailMessageOr404
def viewEmailMessage(request, emailmessage):
	if not emailmessage.IsRead:
		emailmessage.IsRead = True
		emailmessage.save()
	return render_to_response('emails/view.html',{ 'emailmessage':emailmessage }, context_instance=RequestContext(request))


@login_required
@decorators.loadEmailMessageOr404
@decorators.loadJobIfSet
def LinkEmailToJob(request, emailmessage, job=False):
	if job:
		emailmessage.Job = job
		emailmessage.save()
		return HttpResponseRedirect(emailmessage.get_absolute_url())
	else:
		jobs = Job.objects.filter(User=request.user, IsInteresting=True)
		boringjobs = () #Job.objects.filter(User=request.user, IsInteresting=False)
		companies = Company.objects.filter(User=request.user, IsInteresting=True)
		boringcompanies = () #Company.objects.filter(User=request.user, IsInteresting=False)
		agencies = Agency.objects.filter(User=request.user, IsInteresting=True)
		boringagencies = () #Agency.objects.filter(User=request.user, IsInteresting=False)
		# boring stuff not used so commented out for efficiency
		return render_to_response('emails/linktojob.html',{  'emailmessage':emailmessage, 'jobs':jobs, 'boringjobs':boringjobs , 'companies':companies, 'boringcompanies':boringcompanies, 'agencies':agencies, 'boringagencies':boringagencies}, context_instance=RequestContext(request))


@login_required
@decorators.loadEmailMessageOr404
@decorators.loadCompanyOr404
def LinkEmailToCompany(request, emailmessage, company):
	emailmessage.Company = company
	emailmessage.save()
	return HttpResponseRedirect(emailmessage.get_absolute_url())

@login_required
@decorators.loadEmailMessageOr404
@decorators.loadAgencyOr404
def LinkEmailToAgency(request, emailmessage, agency):
	emailmessage.Agency = agency
	emailmessage.save()
	return HttpResponseRedirect(emailmessage.get_absolute_url())
	

@login_required
@decorators.loadEmailMessageOr404
def markEmailAsSpam(request, emailmessage):
	if emailmessage.mark_as_spam():
		createUserMessage(request.user, 'The message has been marked as spam.', undoURL='/email/'+str(emailmessage.id)+'/isnotspam/')
	return HttpResponseRedirect(emailmessage.get_absolute_url())


@login_required
@decorators.loadEmailMessageOr404
def markEmailAsNotSpam(request, emailmessage):
	if emailmessage.mark_as_not_spam():
		createUserMessage(request.user, 'The message has been marked as not spam.', undoURL='/email/'+str(emailmessage.id)+'/isspam/')
	return HttpResponseRedirect(emailmessage.get_absolute_url())

@login_required
def searchMyData(request):
	if not 'q' in request.GET or not request.GET['q']:
		createUserMessage(request.user, 'You must enter a term to search for!')
		return HttpResponseRedirect("/")
	searchterm = request.GET['q']
	#lists of parent data
	jobs = list(Job.objects.filter(Q(Title__icontains=searchterm) | Q(Note__icontains=searchterm), User=request.user, IsInteresting=True, ))
	companies = list(Company.objects.filter(Q(Title__icontains=searchterm) | Q(Note__icontains=searchterm), User=request.user, IsInteresting=True, ))
	agencies = list(Agency.objects.filter(Q(Title__icontains=searchterm) | Q(Note__icontains=searchterm), User=request.user, IsInteresting=True, ))
	# load all child data
	cd = list(Note.objects.filter(Note__icontains=searchterm, User=request.user))
	cd.extend(Task.objects.filter(Note__icontains=searchterm, User=request.user))
	cd.extend(Appointment.objects.filter(Note__icontains=searchterm, User=request.user))
	cd.extend(Communication.objects.filter(Note__icontains=searchterm, User=request.user))
	cd.extend(EmailMessage.objects.filter(Q(Subject__icontains=searchterm) | Q(Body__icontains=searchterm), IsDeleted=False,IsSpam=False,User=request.user))
	for data in cd:
		if data.isLinkedToIntrestingThing():
			if data.Job and not data.Job in jobs:
				jobs.append(data.Job)
			if data.Company and not data.Company in companies:
				companies.append(data.Company)
			if data.Agency and not data.Agency in agencies:
				agencies.append(data.Agency)


	return render_to_response('searchmydata.html',{'searchterm':searchterm, 'jobs':jobs, 'companies':companies, 'agencies':agencies,}, context_instance=RequestContext(request))


