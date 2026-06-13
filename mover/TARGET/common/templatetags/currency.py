from django import template
from django.conf import settings
from django.shortcuts import render

from TARGET.crm.models import Currency, Notification

register = template.Library()

@register.simple_tag
def Currency_List():
    currencies = Currency.objects.all().values()
    return currencies

