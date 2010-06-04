__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

#from django_cron import cronScheduler, Job
from datetime import datetime, time, timedelta
from django.contrib.auth.models import User
from models import Appointment, Task, getUserProfile

class EmailUsersUpcomingAppointmentsAndTasks():   # under django cron should extend Job
	run_every =  60 # 15*60*60  # 15 hours so interacts with below
	run_after = time(1,0,0)  #1am
	run_before = time(19,0,0)  #9am

	def job(self):
		warninadvance = {'appointments':timedelta(4), 'tasks':timedelta(3) }
		for user in User.objects.filter(is_active=True):
			profile = getUserProfile(user)
			if profile.send_Reminder_Email():
				appointments = [ i for i in Appointment.objects.filter(User=user, End__gt=datetime.now(), Start__lt=datetime.now()+timedelta(profile.AppointmentReminderEmailDaysWarnings)).order_by('Start') if i.isLinkedToIntrestingThing()]
				tasks = [ i for i in Task.objects.filter(User=user, End__lt=datetime.now()+timedelta(profile.TaskReminderEmailDaysWarnings), IsCompleted=False).order_by('End') if i.isLinkedToIntrestingThing()]
				if appointments or tasks:
					if user.first_name or user.last_name:
						body = "Dear "+user.first_name +" "+ user.last_name+",\n\n"
					else:
						body = "Dear "+user.username+",\n\n"
					if appointments:
						if len(appointments) == 1:
							body =  body +"You have the following appointment coming up soon:\n\n"
						else:
							body =  body +"You have the following appointments coming up soon:\n\n"
						for appointment in appointments:
							body = body + appointment.Note + "\n\n"
							if appointment.Start.date() != appointment.End.date():
								body = body + "    "+ appointment.Start.strftime("%a %e %b %l:%M %P") + " to " + appointment.End.strftime("%a %e %b %l:%M %P") + "\n"
							else:
								body = body + "    "+ appointment.Start.strftime("%a %e %b %l:%M %P") + " to " + appointment.End.strftime("%l:%M %P") + "\n"
							body = body + "    View details: http://www.myjobseek.net" +appointment.get_absolute_url() + "\n\n"
					if tasks:
						if len(tasks) == 1:
							body =  body +"You have the following task due soon or overdue:\n\n"
						else:
							body =  body +"You have the following tasks due soon or overdue:\n\n"
						for task in tasks:
							body = body + task.Note + "\n\n"
							if task.Start > datetime.now():
								body = body + "    Not meant to be done until: "+ task.Start.strftime("%a %e %b %l:%M %P") + "\n"
							body = body + "    Due: "+ task.End.strftime("%a %e %b %l:%M %P") + "\n"
							body = body + "    View details: http://www.myjobseek.net" +task.get_absolute_url() + "\n\n"
					body = body + "You currently receive emails:\n" + profile.reminder_emails_string()  + "\n(But only if there is anything to remind you of)\n\n"
					body = body + "You can change this and other settings in your profile:\nhttp://www.myjobseek.net/myprofile/\n\n"
					body = body + "Please leave your feedback on myJobSeek by visiting:\nhttp://www.myjobseek.net/contact/\n\nThanks, \nmyJobSeek"
					print body
					user.email_user("Your upcoming appointments or tasks on myjobseek.net", body)

#cronScheduler.register(EmailUsersUpcomingAppointments)


# Couldn't get django-cron to work so did this instead
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

def runNightlyCron(request):
	if request.META['REMOTE_ADDR'] not in ['127.0.0.1']:
		raise Http404()
	c = EmailUsersUpcomingAppointmentsAndTasks();
	c.job()
	return render_to_response('base.html',{ }, context_instance=RequestContext(request))
