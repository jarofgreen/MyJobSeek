__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import StrAndUnicode, force_unicode
from itertools import chain
from django.utils.html import escape, conditional_escape


class SelectNewOrExisting(Widget):

	def __init__(self, attrs=None, choices=(), old_data=()):
		super(SelectNewOrExisting, self).__init__(attrs)
		# choices can be any iterable, but we may need to render this widget
		# multiple times. Thus, collapse it into a list so it can be consumed
		# more than once.
		self.choices = list(choices)
		self.old_data = list(old_data)

	def render(self, name, value, attrs=None, choices=()):
		if value is None: value = ''
		final_attrs = self.build_attrs(attrs, name=name)
		final_attrs['onchange'] = "SelectNewOrExistingWidgetChange(this)"
		output = [u'<select%s>' % flatatt(final_attrs)]
		options = self.render_options(value,)
		if options:
			output.append(options)
		if str(value)[0:4] == "NEW:":
			output.append('</select><span id="id_'+name+'_new"> or new: <input type="text" style="width: 50%"  name="'+name+'_New" value="'+escape(value[4:])+'"></span>')
		else:
			output.append('</select><span id="id_'+name+'_new"> or new: <input type="text" style="width: 50%"  name="'+name+'_New"></span>')
		output.append("<script>SelectNewOrExistingWidgetChange($('id_%s'))</script>" % name)
		return mark_safe(u'\n'.join(output))

	def render_options(self, value):
		if str(value)[0:4] != "NEW:" and value:
			value = int(value)
		else:
			value = 0
		def render_option(option_value, option_label):
			option_value = force_unicode(option_value)
			selected_html = (int(option_value) == int(value)) and u' selected="selected"' or ''
			return u'<option value="%s"%s>%s</option>' % (
				escape(option_value), selected_html,
				conditional_escape(force_unicode(option_label)))
		output = []
		output.append(render_option('0', ' '))
		for option in self.old_data:
			output.append(render_option(option.id, option.Title))
		return u'\n'.join(output)

	def value_from_datadict(self, data, files, name):
		# firstly can we load an old one
		if data.get(name):
			id = int(data.get(name))
			if id > 0:
				return id
		# no? return a new title
		return "NEW:"+data.get(name+'_New','')

