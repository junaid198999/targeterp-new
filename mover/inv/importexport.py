import calendar, io
import math
import os
from itertools import chain

from django.contrib import messages


import route53
from dateutil.relativedelta import relativedelta
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.expressions import RawSQL
from django.utils.formats import get_format
from django.views.generic.detail import SingleObjectMixin

from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.export import export
from num2words import num2words

from django.contrib import messages, admin
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.db.models import Sum, F, IntegerField, Q, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from rest_framework import serializers

from . import signals
from rest_framework.response import Response
from django.db.models import ProtectedError

from .forms import *
from .models import *

from django.urls import reverse_lazy, reverse
from gl.views import *
from gl.models import *
from sy.views import *
from sy.models import *

from rp.views import *
from rp.models import *
from ar.models import *
from ap.models import *






from django.views.generic import (
    CreateView, ListView, UpdateView)

from django.views import generic
from django.contrib.auth.views import (
    LoginView, LogoutView,
)
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                                  BSModalUpdateView,
                                                  BSModalReadView,
                                                  BSModalDeleteView)

from django.contrib.auth.models import Permission, ContentType
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.parse
from datetime import datetime, date
import datetime
driver = None

Link = "https://web.whatsapp.com/"
wait = None


from .models import *
from TARGET.crm.models import *


def DataImport(request):
    template = 'in/import_export/import.html'
    prompt = {'object': 'order of the csv file should be name, tel, address'}
    context = {'success': 2}
    try:
        source = request.POST.get('source')
    except:
        source = ''
    if request.method == 'GET':
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    print(source)
    for column in csv.reader(io_string, delimiter=',', quotechar="|" ):
        #print(column)
        if source == "Products":
            brands = Brand.objects.all().filter(name=column[14]).values()
            if brands.count() == 0:
                print('new brand')
                brands = Brand.objects.create(name=column[14])
                brand_id = brands.pk
                brands.save()
            else:
                brand_id = brands[0]['id']
            print('brand_id', brand_id)
            subbrands = Brand.objects.all().filter(name=column[15]).values()
            if subbrands.count() == 0:
                print('new sub brand')
                subbrands = Brand.objects.create(name=column[15], parent_brand_id=brand_id)
                sub_brand_id = subbrands.pk
                subbrands.save()
            else:
                sub_brand_id = subbrands[0]['id']
            print(column[15])
            categories = Category.objects.all().filter(name=column[3]).values()
            if categories.count() == 0:
                print('new cat')
                categories = Category.objects.create(name=column[3])
                categories.save()
                category_id = categories.pk
            else:
                category_id = categories[0]['id']

            uoms1 = Uom.objects.all().filter(pk=column[5]).values()
            uoms2 = Uom.objects.all().filter(pk=column[7]).values()
            print(column[5])

            _, created = Product.objects.update_or_create(
                name=column[0],
                defaults={
                'sku':column[1],
                'description':column[2],
                'category_id':category_id,
                'barcode':column[4],
                'unit_1':column[5],
                'price':column[6],
                'unit_2':column[7],
                'price_2':column[8],
                'uom_id':uoms1[0]['id'],
                'uom2_id':uoms2[0]['id'],
                'packing':column[9],
                'weight':column[10],
                'monthly_safety_stock':column[11],
                'ti':column[12],
                'hi':column[13],
                'brand_id':sub_brand_id,
                'cost':column[16],
                },
            )
            context = {'success': 1}
        elif source == "Categories":
            try:
                _, created = Category.objects.update_or_create(
                    name=column[0],
                    defaults={'description': column[1]},
            )
                context = {'success': 1}
            except:
                context = {'success': 2}
            #Account Receivable (Customers)
        elif source == "ARCustomers":
            try:
                currency = Currency.objects.all().filter(code='SAR').values()
                if currency.count() == 0:
                    currency = Currency.objects.create(name='SAR')
                    currency_id = currency.pk
                else:
                    currency_id = currency[0]['id']


                classes = CustomersClasses.objects.all().filter(code=column[5]).values()
                if classes.count() == 0:
                    classes = CustomersClasses.objects.create(code=column[5],engname=column[6],arbname= column[7],isdefault=False,allowchaneged=False,currency_id=currency_id,creditlimit=column[11],creditdays=column[12])
                    class_id = classes.pk
                else:
                    class_id = classes[0]['id']


                salesmans = Salesman.objects.all().filter(name=column[13]).values()
                if salesmans.count() == 0:
                    salesmans = Salesman.objects.create(name=column[13],  salesmangroups_id='')
                    salesman_id = salesmans.pk
                else:
                    salesman_id = salesmans[0]['id']

                visitclass = VisitsClasses.objects.all().filter(code=column[14]).values()
                if visitclass.count() == 0:
                    visitclass = VisitsClasses.objects.create(code=column[14],engname=column[14],arbname= column[14])
                    visitclass_id = visitclass.pk
                else:
                    visitclass_id = visitclass[0]['id']

                lang = Languages.objects.all().filter(code=column[24]).values()
                if lang.count() == 0:
                    lang = Languages.objects.create(code=column[24], engname=column[24], arbname=column[24])
                    lang_id = lang.pk
                else:
                    lang_id = lang[0]['id']


                busact = BusinessActivitiesTypes.objects.all().filter(code=column[26]).values()
                if busact.count() == 0:
                    busact = BusinessActivitiesTypes.objects.create(code=column[26], engname=column[26], arbname=column[26])
                    busact_id = busact.pk
                else:
                    busact_id = busact[0]['id']


                status = LookUp.objects.all().filter(keyname='AccountStatus' , engname=column[16]).values()
                if status.count() == 0:
                    status_id = None
                else:
                    status_id = status[0]['id']


                size = LookUp.objects.all().filter(keyname='AccountSize' , engname=column[15]).values()
                if size.count() == 0:
                    accountsize_id = None
                else:
                    accountsize_id = size[0]['id']

                parent = Customers.objects.all().filter(code=column[4]).values()
                if parent.count() == 0:
                    parent_id = None
                else:
                    parent_id = parent[0]['id']


                creditlimit = column[17]
                if creditlimit == '':
                    creditlimit = 0
                else:
                    creditlimit = Decimal(creditlimit)


                creditdays = column[19]
                if creditdays == '':
                    creditdays = 0
                else:
                    creditdays = Decimal(creditdays)


                _, created = Customers.objects.update_or_create(
                    code=column[0],
                    defaults={
                        'engname': column[1],
                        'arbname': column[2],
                        'shortengname': column[3],
                        'shortarbname': column[3],
                        'creditlimit': creditlimit,
                        'creditdays': creditdays,
                        'mandatorycreditlimit': to_bool(column[29]),
                        'iscash': to_bool(column[30]),
                        'iscredit': to_bool(column[31]),
                        'allowtarget':to_bool(column[32]),
                        'allowaccountentry': to_bool(column[33]),
                        'noofemployees': None, #Decimal(column[27]),
                        'statusdate': None,
                        'statusreason': None,
                        'statuschangedby_id': None,
                        'vatgroup': None,
                        'vatregnumber': None,
                        'agingstyle_id': None,
                        'customercategory_id': None,
                        'paymenttearm_id': None,
                        'arledger_id': None,
                        'startbusinessdate': None,

                        'language_id': lang_id,
                        'customerclass_id': class_id,
                        'visitclass_id': visitclass_id,
                        'salesperson_id': salesman_id,
                        'accountsize_id': accountsize_id,
                        'currency_id': currency_id,
                        'businessactivitytype_id': busact_id,
                        'status_id': status_id,
                        'parent_id': parent_id

                    },
                )

                cust = Customers.objects.all().filter(code=column[0]).values()
                if cust.count() == 0:
                    cust_id = None
                else:
                    cust_id = cust[0]['id']

                conttype = ContactsTypes.objects.all().filter(code=column[22]).values()
                if conttype.count() == 0:
                    conttype = ContactsTypes.objects.create(code=column[22], engname=column[22], arbname=column[22])
                    conttype_id = conttype.pk
                else:
                    conttype_id = conttype[0]['id']



                _, created = CustomersContacts .objects.update_or_create(
                    engname=column[20],
                    defaults={
                        'customer_id': cust_id,
                        'contacttype_id': conttype_id,
                        'arbname': column[20],
                        'remarks': column[21],
                        'value': column[23],
                        'inactive': False

                    },
                )

                country = Countries.objects.all().filter(engname=column[34]).values()
                if country.count() == 0:
                    country = Countries.objects.create(code=column[34], engname=column[34], arbname=column[34])
                    country_id = country.pk
                else:
                    country_id = country[0]['id']


                area = Areas.objects.all().filter(engname=column[35]).values()
                if area.count() == 0:
                    area = Areas.objects.create(code=column[35], engname=column[35], arbname=column[35] ,country_id=country_id )
                    area_id = area.pk
                else:
                    area_id = area[0]['id']



                city = Cities.objects.all().filter(engname=column[36]).values()
                if city.count() == 0:
                    city = Cities.objects.create(code=column[36], engname=column[36], arbname=column[36],country_id=country_id, area_id =area_id )
                    city_id = city.pk
                else:
                    city_id = city[0]['id']

                addtype = AddressesTypes.objects.all().filter(code='CURRENT').values()
                if addtype.count() == 0:
                    addtype = AddressesTypes.objects.create(code='CURRENT', engname='CURRENT', arbname='العنوان الحالي')
                    addtype_id = addtype.pk
                else:
                    addtype_id = addtype[0]['id']



                _, created = CustomersAddresses .objects.update_or_create(
                    customer_id=cust_id,
                    defaults={
                        'addresstype_id': addtype_id,
                        'country_id': country_id,
                        'city_id': city_id

                    },
                )

                context = {'success': 1}
            except Exception as e:
                print(e)

                #print('error')
                context = {'success': 2}



        elif source == "Customers":
            try:
                channels = Channel.objects.all().filter(name=column[2]).values()
                if channels.count() == 0:
                    channels = Channel.objects.create(name=column[2])
                    channel_id = channels.pk
                else:
                    channel_id = channels[0]['id']
                print(channels)

                salesmans = Salesman.objects.all().filter(name=column[4]).values()
                if salesmans.count() == 0:
                    users = User.objects.create(name=column[4])
                    print("users",users)
                    users.save()
                    user_id = users.pk
                    print("id",user_id)
                    salesmans = Salesman.objects.create(name=column[4], user_id=user_id, salesmangroups_id='')
                    salesman_id = salesmans.pk
                else:
                    salesman_id = salesmans[0]['id']
                    user_id = salesmans[0]['user_id']
                print(salesmans)
                print(user_id)

                accounts = Account.objects.all().filter(name=column[3]).values()
                if accounts.count() == 0:
                    accounts = Account.objects.create(name=column[3], salesman_id=salesman_id, channel_id=channel_id)
                    account_id = accounts.pk
                else:
                    account_id = accounts[0]['id']
                print(accounts)

                ccountries = Country.objects.all().filter(name=column[5]).values()
                if ccountries.count() == 0:
                    ccountries = Country.objects.create(name=column[5])
                    country_id = ccountries.pk
                else:
                    country_id = ccountries[0]['id']
                print(ccountries)
                print(country_id)

                areas = Area.objects.all().filter(name=column[6]).values()
                if areas.count() == 0:
                    areas = Area.objects.create(name=column[6], country_id=country_id)
                    area_id = areas.pk
                else:
                    area_id = areas[0]['id']
                print(areas)
                print(area_id)

                ccities = City.objects.all().filter(name=column[7]).values()
                if ccities.count() == 0:
                    ccities = City.objects.create(name=column[7], country_id=country_id, area_id=area_id)
                    city_id = ccities.pk
                else:
                    city_id = ccities[0]['id']
                print(ccities)
                try:
                    print(int(column[12]))
                    libilityV = column[12]
                except:
                    libilityV = 0

                try:
                    print(int(column[9]))
                    credit_limitV = column[9]
                except:
                    credit_limitV = 0

                try:
                    print(int(column[11]))
                    payment_daysV = column[11]
                except:
                    payment_daysV = 0

                _, created = Customer.objects.update_or_create(
                    name=column[0],
                    defaults={
                        'description': column[1],
                        'channel_id': channel_id,
                        'account_id': account_id,
                        'salesman_id': salesman_id,
                        'country_id': country_id,
                        'area_id': area_id,
                        'city_id': city_id,
                        'customer_size': 1,
                        'address': column[8],
                        'credit_limit': credit_limitV,
                        'payment_terms': column[10],
                        'payment_days': payment_daysV,
                        'libility': libilityV,
                        'contact1_name': column[13],
                        'contact1_title': column[14],
                        'contact1_mobile': column[15],
                        'contact2_name': column[16],
                        'contact2_title': column[17],
                        'contact2_mobile': column[18],
                        'contact3_name': column[19],
                        'contact3_title': column[20],
                        'contact3_mobile': column[21],
                        'store_code': column[22],
                        'retail_brand_name': column[23],
                        'store_format': column[24],
                        'status': column[25],
                    },
                )
                context = {'success': 1}
            except:
                context = {'success': 2}
        elif source == "Vendors":
            try:
                vcountries = Country.objects.all().filter(name=column[6]).values()
                if vcountries.count() == 0:
                    vcountries = Country.objects.create(name=column[6])
                    country_id = vcountries.pk
                else:
                    country_id = vcountries[0]['id']
                print(vcountries)
                print(country_id)

                vcities = City.objects.all().filter(name=column[7]).values()
                if vcities.count() == 0:
                    vcities = City.objects.create(name=column[7], country_id=country_id, area_id=area_id)
                    city_id = vcities.pk
                else:
                    city_id = vcities[0]['id']
                print(vcities)
                _, created = Vendor.objects.update_or_create(
                    name=column[0],
                    defaults={
                        'description': column[1],
                        'contact_person': column[2],
                        'mobile': column[3],
                        'office_phone': column[4],
                        'email': column[5],
                        'country_id': country_id,
                        'city_id': city_id,
                        'address': column[8],
                    },
                )
                context = {'success': 1}
            except:
                context = {'success': 2}

            #Account Payable (Vendors)
        elif source == "APVendors":
            try:

                currency = Currency.objects.all().filter(code='SAR').values()
                if currency.count() == 0:
                    currency = Currency.objects.create(name='SAR')
                    currency_id = currency.pk
                else:
                    currency_id = currency[0]['id']



                classcreditlimit = column[11]
                if classcreditlimit == '':
                    classcreditlimit = 0
                else:
                    classcreditlimit = Decimal(classcreditlimit)

                classcreditdays = column[12]
                if classcreditdays == '':
                    classcreditdays = 0
                else:
                    classcreditdays = Decimal(classcreditdays)


                classes = VendorsClasses.objects.all().filter(code=column[5]).values()
                if classes.count() == 0:
                    classes = VendorsClasses.objects.create(code=column[5],engname=column[6],arbname= column[7],isdefault=False,allowchaneged=False,currency_id=currency_id,creditlimit=classcreditlimit,creditdays=classcreditdays)
                    class_id = classes.pk
                else:
                    class_id = classes[0]['id']

                # buyer_id = None
                buyers = Buyers.objects.all().filter(code=column[13]).values()
                print(buyers.count())
                if buyers.count() == 0:
                    buyers = Buyers.objects.create(code = column[13] ,engname =column[13] ,arbname=column[13])
                    buyer_id = buyers.pk
                else:
                    buyer_id = buyers[0]['id']


                lang = Languages.objects.all().filter(code=column[24]).values()
                if lang.count() == 0:
                    lang = Languages.objects.create(code=column[24], engname=column[24], arbname=column[24])
                    lang_id = lang.pk
                else:
                    lang_id = lang[0]['id']


                busact = BusinessActivitiesTypes.objects.all().filter(code=column[26]).values()
                if busact.count() == 0:
                    busact = BusinessActivitiesTypes.objects.create(code=column[26], engname=column[26], arbname=column[26])
                    busact_id = busact.pk
                else:
                    busact_id = busact[0]['id']


                status = LookUp.objects.all().filter(keyname='AccountStatus' , engname=column[16]).values()
                if status.count() == 0:
                    status_id = None
                else:
                    status_id = status[0]['id']


                size = LookUp.objects.all().filter(keyname='AccountSize' , engname=column[15]).values()
                if size.count() == 0:
                    accountsize_id = None
                else:
                    accountsize_id = size[0]['id']

                parent = Vendors.objects.all().filter(code=column[4]).values()
                if parent.count() == 0:
                    parent_id = None
                else:
                    parent_id = parent[0]['id']


                creditlimit = column[17]
                if creditlimit == '':
                    creditlimit = 0
                else:
                    creditlimit = Decimal(creditlimit)


                creditdays = column[19]
                if creditdays == '':
                    creditdays = 0
                else:
                    creditdays = Decimal(creditdays)


                _, created = Vendors.objects.update_or_create(
                    code=column[0],
                    defaults={
                        'engname': column[1],
                        'arbname': column[2],
                        'shortengname': column[3],
                        'shortarbname': column[3],
                        'creditlimit': creditlimit,
                        'creditdays': creditdays,
                        'mandatorycreditlimit': to_bool(column[29]),
                        'iscash': to_bool(column[30]),
                        'iscredit': to_bool(column[31]),
                        'allowtarget':to_bool(column[32]),
                        'allowaccountentry': to_bool(column[33]),
                        'noofemployees': None, #Decimal(column[27]),
                        'statusdate': None,
                        'statusreason': None,
                        'statuschangedby_id': None,
                        'vatgroup': None,
                        'vatregnumber': None,
                        'agingstyle_id': None,
                        'vendorcategory_id': None,
                        'paymenttearm_id': None,
                        'apledger_id': None,
                        'startbusinessdate': None,

                        'language_id': lang_id,
                        'vendorclass_id': class_id,
                        #'visitclass_id': visitclass_id,
                        'buyer_id': buyer_id,
                        'accountsize_id': accountsize_id,
                        'currency_id': currency_id,
                        'businessactivitytype_id': busact_id,
                        'status_id': status_id,
                        'parent_id': parent_id

                    },
                )
                print('22222')

                vend = Vendors.objects.all().filter(code=column[0]).values()
                if vend.count() == 0:
                    vend_id = None
                else:
                    vend_id = vend[0]['id']

                conttype = ContactsTypes.objects.all().filter(code=column[22]).values()
                if conttype.count() == 0:
                    conttype = ContactsTypes.objects.create(code=column[22], engname=column[22], arbname=column[22])
                    conttype_id = conttype.pk
                else:
                    conttype_id = conttype[0]['id']

                print('333333')


                _, created = VendorsContacts .objects.update_or_create(
                    engname=column[20],
                    defaults={
                        'vendor_id': vend_id,
                        'contacttype_id': conttype_id,
                        'arbname': column[20],
                        'remarks': column[21],
                        'value': column[23],
                        'inactive': False

                    },
                )

                country = Countries.objects.all().filter(engname=column[34]).values()
                if country.count() == 0:
                    country = Countries.objects.create(code=column[34], engname=column[34], arbname=column[34])
                    country_id = country.pk
                else:
                    country_id = country[0]['id']


                area = Areas.objects.all().filter(engname=column[35]).values()
                if area.count() == 0:
                    area = Areas.objects.create(code=column[35], engname=column[35], arbname=column[35] ,country_id=country_id )
                    area_id = area.pk
                else:
                    area_id = area[0]['id']



                city = Cities.objects.all().filter(engname=column[36]).values()
                if city.count() == 0:
                    city = Cities.objects.create(code=column[36], engname=column[36], arbname=column[36],country_id=country_id , area_id =area_id )
                    city_id = city.pk
                else:
                    city_id = city[0]['id']

                addtype = AddressesTypes.objects.all().filter(code='CURRENT').values()
                if addtype.count() == 0:
                    addtype = AddressesTypes.objects.create(code='CURRENT', engname='CURRENT', arbname='العنوان الحالي')
                    addtype_id = addtype.pk
                else:
                    addtype_id = addtype[0]['id']



                _, created = VendorsAddresses .objects.update_or_create(
                    vendor_id=vend_id,
                    defaults={
                        'addresstype_id': addtype_id,
                        'country_id': country_id,

                        'city_id': city_id

                    },
                )

                context = {'success': 1}
            except Exception as e:
                print(e)

                #print('error')
                context = {'success': 2}


        elif source == "VendorBalance":
            try:
                fyp = None  # We have to read fiscalyearperiod From Table column[1]
                print(column[2])
                vendor = Vendors.objects.all().filter(code=column[2]).values()
                if vendor.count() == 0:
                    # 'do Nothing'
                    vendor_id = 'NULL'
                    print('vendor Not Found' + column[2])
                else:
                    vendor_id = vendor[0]['id']

                print(vendor_id)
                cc1 = CostCenters.objects.all().filter(code=column[3]).values()
                if cc1.count() == 0:
                    # 'do Nothing'
                    cc1_id = None
                #                    print('cc1 Not Found' + column[3])
                else:
                    cc1_id = cc1[0]['id']

                cc2 = CostCenters.objects.all().filter(code=column[4]).values()
                if cc2.count() == 0:
                    # 'do Nothing'
                    cc2_id = None
                #                   print('cc2 Not Found' + column[4])
                else:
                    cc2_id = cc2[0]['id']

                cc3 = CostCenters.objects.all().filter(code=column[5]).values()
                if cc3.count() == 0:
                    # 'do Nothing'
                    cc3_id = None
                #                  print('cc3 Not Found' + column[5])
                else:
                    cc3_id = cc3[0]['id']

                cc4 = CostCenters.objects.all().filter(code=column[6]).values()
                if cc4.count() == 0:
                    # 'do Nothing'
                    cc4_id = None
                #                 print('cc4 Not Found' + column[6])
                else:
                    cc4_id = cc4[0]['id']

                dramount_amnt = column[7]
                cramount_amnt = column[8]
                dramountfc_amnt = column[9]
                cramountfc_amnt = column[10]
                print(dramount_amnt)

                _, created = VendorCostBalances.objects.update_or_create(
                    serial=column[0],
                    defaults={
                        'fiscalyearperiod': fyp,
                        'vendor_id': vendor_id,
                        'costcenter1_id': cc1_id,
                        'costcenter2_id': cc2_id,
                        'costcenter3_id': cc3_id,
                        'costcenter4_id': cc4_id,
                        'dramount': dramount_amnt,
                        'cramount': cramount_amnt,
                        'dramountfc': dramountfc_amnt,
                        'cramountfc': cramountfc_amnt,
                        'lastvendortrans': None,

                    },

                )
                context = {'success': 1}
            except:
                context = {'success': 2}





        elif source == "Ledger":
            try:
                #print(column[3])
                ledgertype = LedgersTypes.objects.all().filter(code=column[3]).values()
                if ledgertype.count() == 0:
                    ledgertype = LedgersTypes.objects.create(code=column[3],engname=column[1],arbname=column[1])
                    ledgertype_id = ledgertype.pk
                else:
                    ledgertype_id = ledgertype[0]['id']
                print(ledgertype)
                print(ledgertype_id)

                ledgercat = LedgersCategories.objects.all().filter(code=column[5]).values()
                if ledgercat.count() == 0:
                    ledgercat = LedgersCategories.objects.create(code=column[5], engname=column[6],arbname=column[6])
                    ledgercat_id = ledgercat.pk
                else:
                    ledgercat_id = ledgercat[0]['id']
                print(ledgercat)
                print(ledgercat_id)

                currency = Currency.objects.all().filter(code='SAR').values()
                if currency.count() == 0:
                    currency = Currency.objects.create(name='SAR')
                    currency_id = currency.pk
                else:
                    currency_id = currency[0]['id']
                print(currency)
                print(currency_id)

                _, created = Ledger.objects.update_or_create(
                    code=column[0],
                    defaults={
                        'segment1': column[0],
                        'engname': column[1],
                        'arbname': column[2],
                        'ledgertype_id': ledgertype_id,
                        'ledgercategory_id': ledgercat_id,
                        'allowaccountentry': column[4],
                        'currency_id': currency_id,
                        'budgetenabled':False,
                        'checkbudget':False,
                        'inactive':False,
                        'inactivereason':'',
                        'debitbalance':False,


                },

                )
                print(created)
                context = {'success': 1}
            except:
                context = {'success': 2}

        elif source == "LedgerBalance":
            try:
                fyp = None # We have to read fiscalyearperiod From Table column[1]
                print(column[2])
                ledger = Ledger.objects.all().filter(code=column[2]).values()
                if ledger.count() == 0:
                    # 'do Nothing'
                    ledger_id = 'NULL'
                    print('ledger Not Found' + column[2])
                else:
                    ledger_id = ledger[0]['id']

                print(ledger_id)
                cc1 = CostCenters.objects.all().filter(code=column[3]).values()
                if cc1.count() == 0:
                    # 'do Nothing'
                    cc1_id = None
#                    print('cc1 Not Found' + column[3])
                else:
                    cc1_id = cc1[0]['id']



                cc2 = CostCenters.objects.all().filter(code=column[4]).values()
                if cc2.count() == 0:
                    # 'do Nothing'
                    cc2_id = None
 #                   print('cc2 Not Found' + column[4])
                else:
                    cc2_id = cc2[0]['id']

                cc3 = CostCenters.objects.all().filter(code=column[5]).values()
                if cc3.count() == 0:
                    # 'do Nothing'
                    cc3_id = None
  #                  print('cc3 Not Found' + column[5])
                else:
                    cc3_id = cc3[0]['id']

                cc4 = CostCenters.objects.all().filter(code=column[6]).values()
                if cc4.count() == 0:
                    # 'do Nothing'
                    cc4_id = None
   #                 print('cc4 Not Found' + column[6])
                else:
                    cc4_id = cc4[0]['id']

                dramount_amnt =column[7]
                cramount_amnt =column[8]
                dramountfc_amnt =column[9]
                cramountfc_amnt =column[10]
                print(dramount_amnt)

                _, created = LedgerCostBalances.objects.update_or_create(
                    serial=column[0],
                    defaults={
                        'fiscalyearperiod': fyp,
                        'ledger_id': ledger_id,
                        'costcenter1_id': cc1_id,
                        'costcenter2_id': cc2_id,
                        'costcenter3_id': cc3_id,
                        'costcenter4_id': cc4_id,
                        'dramount': dramount_amnt,
                        'cramount': cramount_amnt,
                        'dramountfc':dramountfc_amnt,
                        'cramountfc':cramountfc_amnt,
                        'lastledgertrans':None,

                },

                )
                print(created)
                context = {'success': 1}
            except:
                context = {'success': 2}

        elif source == "SystemLookUp":
            try:
                _, created = LookUp.objects.update_or_create(
                    keyid=column[0],
                    defaults={
                        'keyname': column[1],
                        'code': column[2],
                        'engname': column[3],
                        'arbname': column[4],
                        'value': column[5],
                        'remarks': column[6],
                    },
                )

                context = {'success': 1}
            except:
                context = {'success': 2}


        elif source == "SystemModules":
            try:
                _, created = Modules.objects.update_or_create(
                    code=column[0],
                    defaults={
                        'engname': column[1],
                        'arbname': column[2],
                        'isregistered': to_bool( column[3]),
                        'isfydependant': to_bool(column[4]),
                        'isgl': to_bool(column[5]),
                        'isar': to_bool(column[6]),
                        'isap': to_bool(column[7]),
                        'isfa': to_bool(column[8]),
                        'isin': to_bool(column[9]),
                        'ishr': to_bool(column[10]),
                        'isfc': to_bool(column[11]),
                        'ispm': to_bool(column[12]),
                    },
                )
                print(created)
                context = {'success': 1}
            except:
                print(created)
                context = {'success': 2}




        elif source == "CustomerBalance":
            try:
                fyp = None  # We have to read fiscalyearperiod From Table column[1]

                customer = Customers.objects.all().filter(code=column[2]).values()
                if customer.count() == 0:
                    # 'do Nothing'
                    customer_id = 'NULL'
                    print('customer Not Found' + column[2])
                else:
                    customer_id = customer[0]['id']

                print(customer_id)
                cc1 = CostCenters.objects.all().filter(code=column[3]).values()
                if cc1.count() == 0:
                    # 'do Nothing'
                    cc1_id = None
                #                    print('cc1 Not Found' + column[3])
                else:
                    cc1_id = cc1[0]['id']

                cc2 = CostCenters.objects.all().filter(code=column[4]).values()
                if cc2.count() == 0:
                    # 'do Nothing'
                    cc2_id = None
                #                   print('cc2 Not Found' + column[4])
                else:
                    cc2_id = cc2[0]['id']

                cc3 = CostCenters.objects.all().filter(code=column[5]).values()
                if cc3.count() == 0:
                    # 'do Nothing'
                    cc3_id = None
                #                  print('cc3 Not Found' + column[5])
                else:
                    cc3_id = cc3[0]['id']

                cc4 = CostCenters.objects.all().filter(code=column[6]).values()
                if cc4.count() == 0:
                    # 'do Nothing'
                    cc4_id = None
                #                 print('cc4 Not Found' + column[6])
                else:
                    cc4_id = cc4[0]['id']

                dramount_amnt = column[7]
                cramount_amnt = column[8]
                dramountfc_amnt = column[9]
                cramountfc_amnt = column[10]
                print('dramount_amnt')
                print(customer_id)
                _, created = CustomerCostBalances.objects.update_or_create(
                    serial=column[0],
                    defaults={
                        'fiscalyearperiod': fyp,
                        'customer_id': customer_id,
                        'costcenter1_id': cc1_id,
                        'costcenter2_id': cc2_id,
                        'costcenter3_id': cc3_id,
                        'costcenter4_id': cc4_id,
                        'dramount': dramount_amnt,
                        'cramount': cramount_amnt,
                        'dramountfc': dramountfc_amnt,
                        'cramountfc': cramountfc_amnt,
                        'lastcustomertrans': None,

                    },

                )
                print('khaldoun')
                print(created)
                context = {'success': 1}
            except:

                context = {'success': 2}

        elif source == "InvLocations":
            try:
                country = Countries.objects.all().filter(code=column[10]).values()
                if country.count() == 0:
                    country = Countries.objects.create(code=column[10], engname=column[11], arbname=column[12])
                    country_id = country.pk
                else:
                    country_id = country[0]['id']


                city = Cities.objects.all().filter(code=column[13]).values()
                if city.count() == 0:
                    city = Cities.objects.create(code=column[13], engname=column[14], arbname=column[15],country_id=country_id  )
                    city_id = city.pk
                else:
                    city_id = city[0]['id']

                inlocType = InventoriesLocationsTypes.objects.all().filter(code=column[10]).values()
                if country.count() == 0:
                    country = Countries.objects.create(code=column[10], engname=column[11], arbname=column[12])
                    country_id = country.pk
                else:
                    country_id = country[0]['id']


                warehouse = Warehouse.objects.all().filter(name=column[19]).values()
                if ccountries.count() == 0:
                    ccountries = Country.objects.create(name=column[5])
                    country_id = ccountries.pk
                else:
                    country_id = ccountries[0]['id']


                channels = Channel.objects.all().filter(name=column[2]).values()
                if channels.count() == 0:
                    channels = Channel.objects.create(name=column[2])
                    channel_id = channels.pk
                else:
                    channel_id = channels[0]['id']
                print(channels)

                salesmans = Salesman.objects.all().filter(name=column[4]).values()
                if salesmans.count() == 0:
                    users = User.objects.create(name=column[4])
                    print("users",users)
                    users.save()
                    user_id = users.pk
                    print("id",user_id)
                    salesmans = Salesman.objects.create(name=column[4], user_id=user_id, salesmangroups_id='')
                    salesman_id = salesmans.pk
                else:
                    salesman_id = salesmans[0]['id']
                    user_id = salesmans[0]['user_id']
                print(salesmans)
                print(user_id)

                accounts = Account.objects.all().filter(name=column[3]).values()
                if accounts.count() == 0:
                    accounts = Account.objects.create(name=column[3], salesman_id=salesman_id, channel_id=channel_id)
                    account_id = accounts.pk
                else:
                    account_id = accounts[0]['id']
                print(accounts)

                print(ccities)
                try:
                    print(int(column[12]))
                    libilityV = column[12]
                except:
                    libilityV = 0

                try:
                    print(int(column[9]))
                    credit_limitV = column[9]
                except:
                    credit_limitV = 0

                try:
                    print(int(column[11]))
                    payment_daysV = column[11]
                except:
                    payment_daysV = 0

                _, created = Customer.objects.update_or_create(
                    name=column[0],
                    defaults={
                        'description': column[1],
                        'channel_id': channel_id,
                        'account_id': account_id,
                        'salesman_id': salesman_id,
                        'country_id': country_id,
                        'area_id': area_id,
                        'city_id': city_id,
                        'customer_size': 1,
                        'address': column[8],
                        'credit_limit': credit_limitV,
                        'payment_terms': column[10],
                        'payment_days': payment_daysV,
                        'libility': libilityV,
                        'contact1_name': column[13],
                        'contact1_title': column[14],
                        'contact1_mobile': column[15],
                        'contact2_name': column[16],
                        'contact2_title': column[17],
                        'contact2_mobile': column[18],
                        'contact3_name': column[19],
                        'contact3_title': column[20],
                        'contact3_mobile': column[21],
                        'store_code': column[22],
                        'retail_brand_name': column[23],
                        'store_format': column[24],
                        'status': column[25],
                    },
                )
                context = {'success': 1}
            except:
                context = {'success': 2}





        elif source == "Doctors":
            try:
                specialties = Specialty.objects.all().filter(name=column[2]).values()
                if specialties.count() == 0:
                    specialties = Specialty.objects.create(name=column[2])
                    specialty_id = specialties.pk
                else:
                    specialty_id = specialties[0]['id']
                print(specialties)

                salesmans = Salesman.objects.all().filter(name=column[5]).values()
                if salesmans.count() == 0:
                    users = User.objects.create(name=column[5])
                    print("users",users)
                    users.save()
                    user_id = users.pk
                    print("id",user_id)
                    salesmans = Salesman.objects.create(name=column[5], user_id=user_id, salesmangroups_id='')
                    salesman_id = salesmans.pk
                else:
                    salesman_id = salesmans[0]['id']
                    user_id = salesmans[0]['user_id']
                print(salesmans)
                print(user_id)
                print(column[3])

                customers = Customer.objects.all().filter(name=column[3]).values()
                if customers.count() > 0:
                    customer1_id = customers[0]['id']
                else:
                    customer1_id = None
                    context = {'success': 2, 'customer': '1'}
                customers = Customer.objects.all().filter(name=column[4]).values()
                if customers.count() > 0:
                    customer2_id = customers[0]['id']
                else:
                    customer2_id = ''
                    context = {'success': 2, 'customer': '2'}

                calsses = Class.objects.all().filter(name=column[7]).values()
                if calsses.count() == 0:
                    calsses = Class.objects.create(name=column[7], visits=3, doctor_c=True)
                    class_id = calsses.pk
                else:
                    class_id = calsses[0]['id']
                print(calsses)


                _, created = Doctor.objects.update_or_create(
                    name=column[0],
                    defaults={
                        'dgree': column[1],
                        'specialty_id': specialty_id,
                        'account1_id': customer1_id,
                        'account2_id': customer2_id,
                        'salesman_id': salesman_id,
                        'mobile': column[6],
                        'doctor_category_id': class_id,
                        'monthly_target': column[8],
                        'note': column[9],
                    },
                )
                context = {'success': 1}
            except:
                context = {'success': 2}

    return render(request, template, context)

def download_csv(request, queryset):
  if not request.user.is_staff:
    raise PermissionDenied

  model = queryset.model
  model_fields = model._meta.fields + model._meta.many_to_many
  field_names = [field.name for field in model_fields]

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="export.csv"; charset=utf-8'

  # the csv writer
  writer = csv.writer(response, delimiter=";")
  # Write a first row with header information
  writer.writerow(field_names)
  # Write data rows
  for row in queryset:
      values = []
      for field in field_names:
          value = getattr(row, field)
          if callable(value):
              try:
                  value = value() or ''
              except:
                  value = 'Error retrieving value'
          if value is None:
              value = ''
          values.append(value)
      writer.writerow(values)
  return response

def Export(request):
    template = 'in/import_export/export.html'
    context = {'success': 2}
    try:
        source = request.POST.get('source')
    except:
        source = ''
    print(source)
    if source == "Products":
        data = download_csv(request, Product.objects.all())
        context = {'success': 1}
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Products.csv"; charset=utf-8'
        return response
    elif source == "Categories":
        data = download_csv(request, Category.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Categories.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Customers":
        data = download_csv(request, Customer.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Customers.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Vendors":
        data = download_csv(request, Vendor.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Vendors.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Doctors":
        data = download_csv(request, Doctor.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Doctors.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "SalesOrders":
        data = download_csv(request, SalesProduct.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SalesOrders.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "SalesReturnOrder":
        data = download_csv(request, SalesReturnOrder.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SalesReturnOrder.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Leads":
        data = download_csv(request, Lead.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Leads.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Channels":
        data = download_csv(request, Channel.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Channels.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Samples":
        data = download_csv(request, SampleProduct.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Samples.csv"; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Collections":
        data = download_csv(request, Collection.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Collections.csv; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "Salesmen":
        data = download_csv(request, Salesman.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Salesmen.csv; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "PurchaseOrder":
        data = download_csv(request, PurchaseProduct.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PurchaseOrder.csv; charset=utf-8'
        context = {'success': 1}
        return response
    elif source == "PurchaseReturnOrder":
        data = download_csv(request, PurchaseReturnProduct.objects.all())
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="PurchaseReturnOrder.csv; charset=utf-8'
        context = {'success': 1}
        return response
    else:
        return render(request, template, context)


def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))
