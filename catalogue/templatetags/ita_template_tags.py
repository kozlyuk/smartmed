# -*- coding: utf-8 -*-
from decimal import Decimal
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    get_values = request.GET.copy()
    get_values[field] = value
    return get_values.urlencode()


@register.filter
def value_format(value):
    if value is None:
        return '0.00' + ' ' + settings.DEFAULT_CURRENCY
    return str(round(Decimal(value), 2)) + ' ' + settings.DEFAULT_CURRENCY


@register.simple_tag
def active_status_icon(status):
    if status and 'true':
        return 'done'
    return 'highlight_off'


@register.simple_tag
def active_status_color(status):
    if status and 'true':
        return '#288c6c'
    return 'red'

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()