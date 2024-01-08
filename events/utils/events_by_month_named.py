from calendar import month_name
import locale
from events.models import Event


def events_by_month_named():
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    events_by_month = Event.objects.events_by_month_current_year()
    events_by_month_named = {month_name[month_num]: events
                             for month_num, events in events_by_month.items()}
    return events_by_month_named
