"""
Copyright (c) 2007-2008, Dj Gilcrease
All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import cPickle
from threading import Timer
from datetime import datetime, time

from django.dispatch import dispatcher
from django.conf import settings

from signals import cron_done
import models

# how often to check if jobs are ready to be run (in seconds)
# in reality if you have a multithreaded server, it may get checked
# more often that this number suggests, so keep an eye on it...
# default value: 300 seconds == 5 min
polling_frequency = getattr(settings, "CRON_POLLING_FREQUENCY", 300)

try:
	# Delete all the old jobs from the database so they don't interfere with this instance of django
	oldJobs = models.Job.objects.all()
	for oldJob in oldJobs:
		oldJob.delete()
except:
	# When you do syncdb for the first time, the table isn't
	# there yet and throws a nasty error... until now
	pass

class AlreadyRegistered(Exception):
	pass

class Job(object):
	# 86400 seconds == 24 hours
	run_every = 86400

	# You can specify that jobs can only run certain times of the days: default is all day
	run_after = time(0,0,0,0)
	run_before = time(23,59,59,999999)

	def run(self, *args, **kwargs):  
		self.job()
		cron_done.send(sender=self, *args, **kwargs)
		
	def job(self):
		"""
		Should be overridden (this way is cleaner, but the old way - overriding run() - will still work)
		"""
		pass

class CronScheduler(object):
	def register(self, job, *args, **kwargs):
		"""
		Register the given Job with the scheduler class
		"""
		
		job_instance = job()
		
		if not isinstance(job_instance, Job):
			raise TypeError("You can only register a Job not a %r" % job)

		job, created = models.Job.objects.get_or_create(name=str(job_instance.__class__))
		if created:
			job.instance = cPickle.dumps(job_instance)
		job.args = cPickle.dumps(args)
		job.kwargs = cPickle.dumps(kwargs)
		job.run_frequency = job_instance.run_every
		job.run_after = job_instance.run_after
		job.run_before = job_instance.run_before
		job.save()

	def execute(self):
		"""
		Queue all Jobs for execution
		"""
		status, created = models.Cron.objects.get_or_create(pk=1)
		
		# This is important for 2 reasons:
		#     1. It keeps us for running more than one instance of the
		#        same job at a time
		#     2. It reduces the number of polling threads because they
		#        get killed off if they happen to check while another
		#        one is already executing a job (only occurs with
		#		 multi-threaded servers)
		if status.executing:
			return

		status.executing = True
		status.save()

		jobs = models.Job.objects.all()
		for job in jobs:
			if job.queued:
				if (datetime.now() - job.last_run).seconds > job.run_frequency and datetime.now().time() > job.run_after and  datetime.now().time() < job.run_before:
					inst = cPickle.loads(str(job.instance))
					args = cPickle.loads(str(job.args))
					kwargs = cPickle.loads(str(job.kwargs))
					
					try:
						inst.run(*args, **kwargs)
						job.last_run = datetime.now()
						job.save()
						
					except Exception:
						# if the job throws an error, just remove it from
						# the queue. That way we can find/fix the error and
						# requeue the job manually
						job.queued = False
						job.save()

		status.executing = False
		status.save()
		
		# Set up for this function to run again
		Timer(polling_frequency, self.execute).start()


cronScheduler = CronScheduler()