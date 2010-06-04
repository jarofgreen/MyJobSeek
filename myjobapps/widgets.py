__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

__all__ = ('SelectDateWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?) (\d\d?)\:(\d\d?)\:(\d\d?)$')

class SelectDateTimeWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    date_field = '%s_date'
    year_field = '%s_year'
    hour_field = '%s_hour'
    min_field = '%s_min'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+5)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val, hour_val, min_val = value.year, value.month, value.day, value.hour, value.minute
        except AttributeError:
            year_val = month_val = day_val = hour_val = min_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val, hour_val, min_val, throw_away_seconds  = [int(v) for v in match.groups()]

        date_val = "%04s-%02s-%02s" % (year_val,month_val, day_val)

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        output.append("<span id=\"%s_humanreadable\"></span>" % (name))


        output.append("<input type=\"hidden\" name=\"%s\" id=\"%s\" value=\"%s\" onchange=\"updateCalendar(this);\">" % ((self.date_field % name), (self.date_field % name), date_val))

		
        output.append("<span id=\"%s_showcalendar\"><img src=\"/static/calendar.png\" alt=\"Calendar\"></span>&nbsp;&nbsp;&nbsp;" % (name));
        output.append("""<script>Event.observe(window, 'load', function(event) {  Calendar.setup({dateField : '%s',triggerElement : '%s_showcalendar'})});</script>""" % ((self.date_field % name), name))
        output.append("""<script>Event.observe(window, 'load', function(event) {  updateCalendar($(\"%s\")); });</script>""" % ((self.date_field % name)))

        hour_choices = [(i, i) for i in range(0, 23)]
        #if not (self.required and value):
        #    hour_choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        s = Select(choices=hour_choices)
        select_html = s.render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        output.append(":");

        min_choices = [(i, i) for i in range(0, 59)]
        #if not (self.required and value):
        #    hour_choices.insert(0, self.none_value)
        local_attrs['id'] = self.min_field % id_
        s = Select(choices=min_choices)
        select_html = s.render(self.min_field % name, min_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        date = data.get(self.date_field % name)
        bits = date.split("-");
        y = int(bits[0])
        m = int(bits[1])
        d = int(bits[2])
        h = int(data.get(self.hour_field % name))
        min = int(data.get(self.min_field % name))
        return '%04d-%02d-%02d %02d:%02d:00' % (y,m,d, h, min)








