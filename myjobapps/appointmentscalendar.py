__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."


# Thanks to http://www.djangosnippets.org/snippets/129/
from datetime import date, timedelta
from myjobapps.models import Appointment
from datetime import date, timedelta

def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def appointmentscalendar(request, year, month):
  

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    event_list = [i for i in Appointment.objects.filter(User=request.user, End__gte=first_day_of_calendar, Start__lte=last_day_of_calendar) if i.isLinkedToIntrestingThing()]
  
    month_cal = []
    week = []
    week_headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = []
        for event in event_list:
            if day >= event.Start.date() and day <= event.End.date():
                cal_day['event'].append(event)
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': month_cal, 'headers': week_headers}
