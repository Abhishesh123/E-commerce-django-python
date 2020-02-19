from django import template
from datetime import date, timedelta, datetime

register = template.Library()

@register.simple_tag()
def day_differ(date_item):
    date_item = date_item.replace(tzinfo=None)
    delta = datetime.now() - date_item
    return delta.days
