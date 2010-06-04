__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


from django.conf.urls.defaults import *
import private_user_files.views as privateuserfiles
from myjobapps.cron import runNightlyCron
#from django.contrib.auth.views import login, logout
from myjobapps import models, views
from os import path
from datetime import datetime

##import django_cron
##django_cron.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),

	# special ones for linking jobs to other things
	(r'^job/(?P<job>\d+)/addcompany/(?P<company>\d+)/$', views.viewJobAddExistingCompany),
	(r'^job/(?P<job>\d+)/addcompany/$',views. viewJobAddCompany),
	(r'^job/(?P<job>\d+)/addagency/(?P<agency>\d+)/$', views.viewJobAddExistingAgency),
	(r'^job/(?P<job>\d+)/addagency/$', views.viewJobAddAgency),

	# standard ones for data objects
	(r'^company/(?P<company>\d+)/markinteresting/$', views.setAgencyOrCompanyInteresting),
	(r'^company/(?P<company>\d+)/marknotinteresting/$', views.setAgencyOrCompanyNotInteresting),
	(r'^company/(?P<company>\d+)/addnote/$', views.addNote),
	(r'^company/(?P<company>\d+)/addtodo/$', views.addTask),
	(r'^company/(?P<company>\d+)/addappointment/$', views.addAppointment),
	(r'^company/(?P<company>\d+)/addcommunication/$', views.addCommunication),
	(r'^company/(?P<company>\d+)/edit/$', views.editCompany),
	(r'^company/(?P<company>\d+)/$', views.viewCompany),

	(r'^agency/(?P<agency>\d+)/markinteresting/$', views.setAgencyOrCompanyInteresting),
	(r'^agency/(?P<agency>\d+)/marknotinteresting/$', views.setAgencyOrCompanyNotInteresting),
	(r'^agency/(?P<agency>\d+)/addnote/$', views.addNote),
	(r'^agency/(?P<agency>\d+)/addtodo/$', views.addTask),
	(r'^agency/(?P<agency>\d+)/addappointment/$', views.addAppointment),
	(r'^agency/(?P<agency>\d+)/addcommunication/$', views.addCommunication),
	(r'^agency/(?P<agency>\d+)/edit/$', views.editAgency),
	(r'^agency/(?P<agency>\d+)/$', views.viewAgency),

	(r'^job/(?P<job>\d+)/markinteresting/$', views.setJobInteresting),
	(r'^job/(?P<job>\d+)/marknotinteresting/$', views.setJobNotInteresting),
	(r'^job/(?P<job>\d+)/addnote/$', views.addNote),
	(r'^job/(?P<job>\d+)/addtodo/$', views.addTask),
	(r'^job/(?P<job>\d+)/addappointment/$', views.addAppointment),
	(r'^job/(?P<job>\d+)/addcommunication/$', views.addCommunication),
	(r'^job/(?P<job>\d+)/edit/$', views.editJob),
	(r'^job/(?P<job>\d+)/$', views.viewJob),

	(r'^calendar/view/(?P<appointment>\d+)/$', views.viewOrphanAppointment ),
	(r'^calendar/addnew/$', views.addAppointment),
	(r'^calendar/(?P<year>\d{4,4})/(?P<month>\d{1,2})/$', views.viewCalendar),
	(r'^calendar/$', views.viewCalendar, { 'year':datetime.now().year, 'month':datetime.now().month}),

	(r'^appointment/(?P<appointment>\d+)/edit/$', views.editAppointment),
	(r'^note/(?P<note>\d+)/edit/$', views.editNote),
	(r'^task/(?P<task>\d+)/edit/$', views.editTask),
	(r'^communication/(?P<communication>\d+)/edit/$', views.editCommunication),


	(r'^files/$', privateuserfiles.listFiles),



	# to do with notes
	(r'^completetodo/(?P<task>\d+)/$', views.completeTask),
	(r'^uncompletetodo/(?P<task>\d+)/$', views.uncompleteTask),

	# listing things
	(r'^jobs/includeboring/$', views.listThings, {'model': models.Job , 'includeboring':True, 'title':'Jobs', 'newurl':'/newjob/'}),
	(r'^companies/includeboring/$', views.listThings, {'model': models.Company , 'includeboring':True, 'title':'Companies' , 'newurl':'/newcompany/'}),
	(r'^agencies/includeboring/$', views.listThings, {'model': models.Agency , 'includeboring':True , 'title':'Agencies', 'newurl':'/newagency/'}),
	(r'^jobs/$', views.listThings, {'model': models.Job  , 'includeboring':False, 'title':'Jobs', 'newurl':'/newjob/'}),
	(r'^companies/$', views.listThings, {'model': models.Company  , 'includeboring':False, 'title':'Companies', 'newurl':'/newcompany/'}),
	(r'^agencies/$', views.listThings, {'model': models.Agency , 'includeboring':False , 'title':'Agencies', 'newurl':'/newagency/'}),

	(r'^correspondence/p(?P<pagenumber>\d+)/$', views.listCorrespondence,),
	(r'^correspondence/$', views.listCorrespondence, { 'pagenumber':1}),

	(r'^activity/p(?P<pagenumber>\d+)/$', views.listActivity,),
	(r'^activity/$', views.listActivity, { 'pagenumber':1}),
	(r'^activity/last2weeks/$', views.listActivityLast2Weeks),

	# new
	(r'^newagency/$', views.addNewAgency),
	(r'^newcompany/$', views.addNewCompany),
	(r'^newjob/$', views.addNewJob),

	# emails
	(r'^email/inbox/$', views.viewInbox),
	(r'^email/deletedbox/$', views.viewDeletedBox),
	(r'^email/spambox/$', views.viewSpamBox),
	(r'^email/(?P<emailmessage>\d+)/$', views.viewEmailMessage),
	(r'^email/(?P<emailmessage>\d+)/isspam/$', views.markEmailAsSpam),
	(r'^email/(?P<emailmessage>\d+)/isnotspam/$', views.markEmailAsNotSpam),
	(r'^email/(?P<emailmessage>\d+)/linktojob/$', views.LinkEmailToJob),
	(r'^email/(?P<emailmessage>\d+)/linktojob/(?P<job>\d+)/$', views.LinkEmailToJob),
	(r'^email/(?P<emailmessage>\d+)/linktoagency/(?P<agency>\d+)/$', views.LinkEmailToAgency),
	(r'^email/(?P<emailmessage>\d+)/linktocompany/(?P<company>\d+)/$', views.LinkEmailToCompany),

	# home and other static pages
	(r'^myprofile/$', views.viewMyProfile),
	(r'^search/$', views.searchMyData),
	(r'^myprofile/edit/$', views.editMyProfile),
	(r'^givefeedback/$', views.giveFeedBack),
	(r'^nightlycron/$', runNightlyCron),
	(r'^robots.txt$', views.viewPublicStaticPage, {'templatename':'robots.txt'}),
	(r'^googlebfebc36470ff0f3c.html$', views.viewPublicStaticPage, {'templatename':'robots.txt'}),
	(r'^aboutus/$', views.viewPublicStaticPage, {'templatename':'aboutus.html'}),
	(r'^faq/$', views.viewPublicStaticPage, {'templatename':'faq.html'}),
	(r'^privacy/$', views.viewPublicStaticPage, {'templatename':'privacy.html'}),
	(r'^termsconditions/$', views.viewPublicStaticPage, {'templatename':'termsconditions.html'}),
	(r'^accounts/', include('registration.urls')),
	(r'^contact/', include('contact_form.urls')),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': path.join(path.dirname(__file__), './static/static/').replace('\\','/')}),
	(r'^$', views.homepageView),
)
