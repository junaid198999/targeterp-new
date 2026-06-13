import json

from django import template
from django.conf import settings
from TARGET.crm.models import Currency

register = template.Library()


@register.inclusion_tag('widgets/profile-widget.html')
def user_profile(*args, **kwargs):
    stats = kwargs.pop('stats')
    stats = str(stats).replace("'", '"')
    try:
        kwargs['stats'] = json.loads(stats)
    except json.decoder.JSONDecodeError:
        pass
    return kwargs


@register.inclusion_tag('widgets/stat-widget.html')
def stat(*args, **kwargs):
    return kwargs

from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()

@register.filter(name='currency')
def currency(value):
    currencies = Currency.objects.filter(active=True, default=True).values()
    if currencies.count() == 0:
        curr_s = 'SAR'
    elif currencies.count() == 1:
        curr_s = currencies[0]['symbol']
    elif currencies.count() > 1:
        curr_s = currencies[0]['symbol']
    if value == None or  value == "None":
        conv_num = 0
    else:
        print(value)
        conv_num = int(float(value.replace(',', '')) * float(currencies[0]['rate']))

    try:
#        return 'SAR ' + str(round(int(value) / 3.75,0))
        return curr_s + ' ' + str(intcomma(conv_num) )
    except:
        return curr_s + str(intcomma(conv_num))

@register.filter(name='currency_decimal')
def currency_decimal(value):
    currencies = Currency.objects.filter(active=True, default=True).values()
    if currencies.count() == 0:
        curr_s = 'SAR'
    elif currencies.count() == 1:
        curr_s = currencies[0]['symbol']
    elif currencies.count() > 1:
        curr_s = currencies[0]['symbol']
    if value == None or  value == "None":
        conv_num = 0
    else:
        print(value)
        conv_num = format(float(float(value.replace(',', '')) * float(currencies[0]['rate'])),".2f")

    try:
#        return 'SAR ' + str(round(int(value) / 3.75,0))
        return curr_s + ' ' + str(intcomma(conv_num) )
    except:
        return curr_s + str(intcomma(conv_num))

@register.filter(name='currency_no_symbol')
def currency(value):
    currencies = Currency.objects.filter(active=True, default=True).values()

    if value == None or  value == "None":
        conv_num = 0
    else:
        conv_num = int(float(value.replace(',', '')) * float(currencies[0]['rate']))

    try:
#        return 'SAR ' + str(round(int(value) / 3.75,0))
        return str(intcomma(conv_num))
    except:
        return str(intcomma(conv_num))

@register.filter(name='currency_no_comma')
def currency(value):
    currencies = Currency.objects.filter(active=True, default=True).values()
    print(value)
    if value == None or  value == "None":
        conv_num = 0
    else:
        conv_num = int(float(value) * float(currencies[0]['rate']))
    print(conv_num)

    try:
#        return 'SAR ' + str(round(int(value) / 3.75,0))
        return conv_num
    except:
        return conv_num




