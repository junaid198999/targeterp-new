from django.db.models import Sum, Q

from TARGET.crm.middlewares import RequestMiddleware
from TARGET.crm.models import Notification, Salesman, Customer, SalesOrder, Collection, SalesReturnOrder, ToDoList
from TARGET.users.models import User

from django import template
from django.utils import timezone

register = template.Library()
@register.simple_tag
def show_notifications():
    a = Notification.objects.all()
    return {'notifications': a}


@register.simple_tag
def rightsidbar_function():
    request = RequestMiddleware(get_response=None)
    request = request.thread_local.current_request
    setting_arr = []
    if request.user.picture:
        setting_arr.append({'id': request.user.id, 'name': request.user,'picture': request.user.picture,
                      'picture_url': request.user.picture.url, 'notifications': request.user.notification, 'tours': request.user.tour, 'darktheme': request.user.darktheme})
    else:
        setting_arr.append({'id': request.user.id, 'name': request.user.name,'picture': "",
                      'picture_url': "", 'notifications': request.user.notification, 'tours': request.user.tour, 'darktheme': request.user.darktheme})

    return setting_arr

@register.simple_tag
def any_function():
    notes = []
    notofications = Notification.objects.all().filter(read=0).order_by('-urgent', 'read', '-created_date')
    for nots in notofications:
        users = User.objects.get(pk=nots.from_user_id)
        if users.picture:
            notes.append({'pk': nots.pk, 'source': nots.source, 'source_id': nots.source_id , 'message': nots.message, 'from_user': nots.from_user,
                          'to_user': nots.to_user, 'read': nots.read, 'picture': users.picture, 'picture_url': users.picture.url, 'url': nots.url, 'urgent':nots.urgent })
        else:
            notes.append({'pk': nots.pk, 'source': nots.source, 'source_id': nots.source_id , 'message': nots.message, 'from_user': nots.from_user,
                          'to_user': nots.to_user, 'read': nots.read, 'picture': "", 'picture_url': "", 'url': nots.url, 'urgent':nots.urgent })

    return notes

@register.simple_tag
def todolist_function():
    todolists = []
    notofications = ToDoList.objects.all().filter(done=0).order_by('-priority', 'done', '-created_date')
    for nots in notofications:
        todolists.append({'pk': nots.pk, 'task': nots.task, 'user': nots.user,
                      'to_user': nots.to_user, 'done': nots.done, 'priority':nots.priority })

    return notofications

@register.simple_tag
def not_read_count():
    notes = []
    notofications = Notification.objects.all().filter(read=0)
    ncount = 0
    for nots in notofications:
        users = User.objects.get(pk=nots.to_user_id)
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        if request.user == nots.to_user:
            ncount = ncount + 1

    return ncount

@register.simple_tag
def urgent_count():
    notes = []
    notofications = Notification.objects.all().filter(read=0).filter(urgent=1)
    ncount = 0
    for nots in notofications:
        users = User.objects.get(pk=nots.to_user_id)
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        if request.user == nots.to_user:
            ncount = ncount + 1

    return ncount

@register.simple_tag
def salesorders_due_count():
    request = RequestMiddleware(get_response=None)
    request = request.thread_local.current_request
    salesmanid = Salesman.objects.all().filter(reporting_to=request.user.id).values('reporting_to')
    from datetime import datetime
    today = datetime.today()
    currentYear = timezone.now().year
    customers = Customer.objects.all().filter(payment_terms=2)

    orders_due = []

    if request.user.is_superuser is False:
        qcollections = Collection.objects.all()
        if salesmanid.count() == 0:
            salesmanid = Salesman.objects.filter(user=request.user.id)
        elif salesmanid.count() > 0:
            salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=request.user.id))
    else:
        qcollections = Collection.objects.all().filter(customer_id__in=customers)

    if request.user.is_superuser is False:
        customers = customers.filter(salesman__in=salesmanid)

    salesorders = SalesOrder.objects.all().filter(payment_terms=2)
    salesreturns = SalesReturnOrder.objects.all().filter(salesorderid__in=salesorders)

    now = datetime.today()
    dayslater = str(currentYear) + "-01-01"
    count = 0
    totalamount = 0
    for customer in customers :
        qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id=customer.id).filter(
            duedate__range=(dayslater, now))
        totalsalesorder = qsalesorder.aggregate(Sum('total'))
        if totalsalesorder['total__sum'] is None:
            totalsalesorderv = 0
        else:
            totalsalesorderv = totalsalesorder['total__sum']

        salesorderid = qsalesorder.values('pk')

        qsalesreturn = salesreturns.annotate(totalrs=Sum('total')).filter(customer_id = customer.id)
        totalsalesreturn = qsalesreturn.aggregate(Sum('total'))
        if totalsalesreturn['total__sum'] is None:
            totalsalesreturnv = 0
        else:
            totalsalesreturnv = totalsalesreturn['total__sum']

        netsales = totalsalesorderv - totalsalesreturnv

        collections = qcollections \
            .annotate(total=Sum('amount')).filter(customer_id=customer.id).filter(~Q(description__contains='auto created from Sales')).filter(salesorder__in = salesorderid)
        collectionamount = collections.aggregate(total=Sum('amount'))
        collectamount = collectionamount['total']
        if collectamount is None:
            collectamount = 0
        balance = netsales - collectamount
        if balance > 0:
            count = count + 1
            totalamount = totalamount + balance

        orders_due.append({'customer': customer.name, 'salesman': customer.salesman, 'totalamount': netsales,
                            'amount': collectamount,
                            'balance': balance,
                            'channel': customer.channel,
                            'count': count,
                            'totalamount': totalamount
                               })

    return orders_due

