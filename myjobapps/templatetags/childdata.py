__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


from django import template
from myjobapps.models import *
from django.template.loader import get_template
from django.template import Context

register = template.Library()

class ShowCommonDataNode(template.Node):
	def __init__(self, varname, showlocation):
		self.varname, self.showlocation = varname,showlocation

	def render(self, context):
		c = Context({'showlocation':self.showlocation, 'company':context.get('company'), 'agency':context.get('agency'), 'job':context.get('job')})
		if isinstance(context[self.varname], Note):
			t = get_template('childdata-note.html')
			c['note'] = context[self.varname]
		elif isinstance(context[self.varname], Task):
			t = get_template('childdata-task.html')
			c['task'] = context[self.varname]
		elif isinstance(context[self.varname], Appointment):
			t = get_template('childdata-appointment.html')
			c['appointment'] = context[self.varname]
		elif isinstance(context[self.varname], Communication):
			t = get_template('childdata-communication.html')
			c['communication'] = context[self.varname]
		elif isinstance(context[self.varname], EmailMessage):
			t = get_template('childdata-email.html')
			c['email'] = context[self.varname]
			if not c['email'].IsRead:
				c['email'].IsRead = True
				c['email'].save()

		return t.render(c)


def show_common_data(parser, token):
	bits = token.contents.split()
	if len(bits) < 2:
		raise TemplateSyntaxError, "get_latest tag takes at least 1 arguments"
	showlocation = False
	if len(bits) >= 3 and bits[2] == 'showlocation':
		showlocation = True
	return ShowCommonDataNode(bits[1], showlocation)

show_common_data = register.tag(show_common_data)




