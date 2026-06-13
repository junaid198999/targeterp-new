from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    CreateView, ListView, UpdateView)
from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.views.generic.edit import CreateView
from django.utils import timezone
from bootstrap_modal_forms.generic import (BSModalCreateView,BSModalUpdateView,BSModalReadView,BSModalDeleteView)
from django.db import connection
from django.http import HttpResponse
from django.db.models import Max
from django.db.models import Min
from django.apps import apps

from inv.views import to_bool
from django.contrib import messages
driver = None



######### Load Operation Line
def load_duepayment_line(request):
    cust_id = request.GET.get('custid')
    duepayments = CustomersPaymentsSchedule.objects.filter(customer_id=cust_id).exclude(isclose= True).select_related('operation').values('id','duedate','paidamount','dueamount','operation__number').order_by('duedate')
    soarr =[]
    if duepayments.count() > 0:
        for dp in duepayments:
            duedate = dp['duedate'].strftime('%Y-%m-%d')
            print(duedate)
            soarr.append({ 'id':dp['id'],  'duedate': duedate,'dueamount': dp['dueamount'],'paidamount': dp['paidamount']  ,'operationnumber': dp['operation__number']} )

    return render(request, 'ar/dropdownlist/duepayments_lines_list.html', {'duepaymentslines': soarr })

######### End Load Operation Line


######### Load Operation Line Count
def load_duepayment_line_count(request):
    cust_id = request.GET.get('custid')
    duepayments = CustomersPaymentsSchedule.objects.filter(customer_id=cust_id).exclude(isclose= True).order_by('duedate')
    linescount = duepayments.count()
    return render(request, 'ar/dropdownlist/duepayments_line_count_list.html', {'linescount': linescount })


######### End Load Operation Line Count


######### Customers Categories

class CustomersCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = CustomersCategories
    context_object_name = 'customerscategories'
    template_name = 'ar/master/list-customerscategories.html'


class CustomersCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CustomersCategories
    form_class = CustomersCategoriesForm
    template_name = 'ar/master/create_customerscategories.html'
    success_message = 'Success: customers Categories was created.'
    success_url = reverse_lazy('ar:list-customerscategories')


class CustomersCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CustomersCategories
    template_name = 'ar/master/edit_customerscategories.html'
    form_class = CustomersCategoriesForm
    success_message = 'Success: customers Categories was updated.'
    success_url = reverse_lazy("ar:list-customerscategories")

    def form_valid(self, form):
        CustomersCategories = form.save()
        CustomersCategories.save
        return super(CustomersCategoriesUpdateView, self).form_valid(form)

class CustomersCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CustomersCategories
    template_name = 'ar/master/delete_customerscategories.html'
    success_message = 'Success: customers Categories was deleted.'
    success_url = reverse_lazy('ar:list-customerscategories')


######### End Customers Categories


######### Customers Classes

class CustomersClassesListView(LoginRequiredMixin, generic.ListView):
    model = CustomersClasses
    context_object_name = 'customersclasses'
    template_name = 'ar/master/list-customersclasses.html'


class CustomersClassesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CustomersClasses
    form_class = CustomersClassesForm
    template_name = 'ar/master/create_customersclasses.html'
    success_message = 'Success: customers Classes was created.'
    success_url = reverse_lazy('ar:list-customersclasses')


class CustomersClassesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CustomersClasses
    template_name = 'ar/master/edit_customersclasses.html'
    form_class = CustomersClassesForm
    success_message = 'Success: customers Classes was updated.'
    success_url = reverse_lazy("ar:list-customersclasses")

    def form_valid(self, form):
        CustomersClasses = form.save()
        CustomersClasses.save
        return super(CustomersClassesUpdateView, self).form_valid(form)

class CustomersClassesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CustomersClasses
    template_name = 'ar/master/delete_customersclasses.html'
    success_message = 'Success: customers Classes was deleted.'
    success_url = reverse_lazy('ar:list-customersclasses')


######### End Customers Categories


######### Customers

class CustomersListView(LoginRequiredMixin, generic.ListView):
    model = Customers
    context_object_name = 'customers'
    template_name = 'ar/master/list-customers.html'


class CustomersCreateView(LoginRequiredMixin,  CreateView):
    model = Customers
    form_class = CustomersForm
    template_name = 'ar/master/create_customers.html'
    success_message = 'Success: Customers was created.'
    success_url = reverse_lazy('ar:list-customers')


    def get_context_data(self, **kwargs):
        context = super(CustomersCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['customersaddresses'] = CustomersAddressesForm(self.request.POST, instance=self.object)
            context['customersaddresses'].full_clean()

            context['customerscontacts'] = CustomersContactsForm(self.request.POST, instance=self.object)
            context['customerscontacts'].full_clean()
        else:
            context['customersaddresses'] = CustomersAddressesForm(instance=self.object)
            context['customerscontacts'] = CustomersContactsForm(instance=self.object)

        #print(context['customersaddress'])
        return context

    def form_valid(self, form):
        #self.object = form.save()
        context = self.get_context_data(form=form)
        customersaddresses = context['customersaddresses']
        customerscontacts = context['customerscontacts']
        response = super().form_valid(form)

        if customersaddresses.is_valid() :
            response = super().form_valid(form)
            customersaddresses.instance = self.object
            customersaddresses.save()
            form.save()
        else:
            context['customersaddresses'] = CustomersAddressesFormSet()
            #context['customerscontact'] = CustomersContactsForm()

        if customerscontacts.is_valid():
            customerscontacts.instance = self.object
            customerscontacts.save()
            form.save()
        else:
            print(customerscontacts.errors)
            context['customerscontacts'] = CustomersAddressesFormSet


        return response

class CustomersUpdateView(LoginRequiredMixin,  UpdateView):
    model = Customers
    template_name = 'ar/master/edit_customers.html'
    #form_class = CustomersForm
    fields = '__all__'
    success_message = 'Success: Customers was updated.'
    success_url = reverse_lazy("ar:list-customers")


    def get_context_data(self, **kwargs):
        context = super(CustomersUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['customersaddresses'] = CustomersAddressesFormSet(self.request.POST, instance=self.object)
            context['customersaddresses'].full_clean()

            context['customerscontacts'] = CustomersContactsFormSet(self.request.POST, instance=self.object)
            context['customerscontacts'].full_clean()
        else:
            context['customersaddresses'] = CustomersAddressesFormSet(instance=self.object)
            context['customerscontacts'] = CustomersContactsFormSet(instance=self.object)

        #print(context['customersaddress'])
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        custaddr = context['customersaddresses']
        custcont = context['customerscontacts']
        response = super().form_valid(form)

        if custaddr.is_valid() :
            custaddr.instance = self.object
            custaddr.save()
            form.save()
        else:
            context['customersaddresses'] = CustomersAddressesFormSet()
            #context['customerscontact'] = CustomersContactsForm()

        if custcont.is_valid():
            custcont.instance = self.object
            custcont.save()
            form.save()
        else:
            print(custcont.errors)
            context['customerscontacts'] = CustomersContactsFormSet


        return response

class CustomersDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Customers
    template_name = 'ar/master/delete_customers.html'
    success_message = 'Success: Customers was deleted.'
    success_url = reverse_lazy('ar:list-customers')

######### End Customers

######### Customers Journal

class CustomersJourListView(LoginRequiredMixin, ListView):
    model = CustomersJour
    context_object_name = 'customersjour'
    template_name = 'ar/trans/list-customersjour.html'

class CustomersJourCreateView(LoginRequiredMixin,  CreateView):
    model = CustomersJour
    form_class = CustomersJourForm
    #fields = '__all__'
    template_name = 'ar/trans/create_customersjour.html'
    success_message = 'Success: Customers Journal  was created.'
    success_url = reverse_lazy('ar:list-customersjour')

    def get_context_data(self, **kwargs):
        context = super(CustomersJourCreateView, self).get_context_data(**kwargs)
        try:
            maxid = int(CustomersJour.objects.latest('pk').pk) + 1
        except:
            maxid = 1


        context['customers'] = Customers.objects.all().filter(allowaccountentry=True)
        context['maxid'] = maxid
        context['transtypes'] = TransTypes.objects.all().filter(transkind__keyid= 51)
        context['currentdate'] = datetime.now().date().strftime('%Y-%m-%d')



        posperiod = FiscalYearsPeriodsModules.objects.filter(module__code='AR',closedate =None
                                     ).exclude(opendate=None).aggregate(Min('fiscalyearperiod__fromdate'),Max('fiscalyearperiod__todate'))
        if all([posperiod['fiscalyearperiod__fromdate__min'], posperiod['fiscalyearperiod__todate__max']]):
            mindate= posperiod['fiscalyearperiod__fromdate__min'].strftime('%Y-%m-%d')
            maxdate= posperiod['fiscalyearperiod__todate__max'].strftime('%Y-%m-%d')
            context['mindate'] = mindate
            context['maxdate'] = maxdate
        else:
            context['mindate'] = datetime.today()
            context['maxdate'] = datetime.today()

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']





        if self.request.POST:
            context['maxid'] = maxid
            context['customersjourlines'] = CustomersJourLineFormSet(self.request.POST, instance=self.object)
            context['customersjourlines'].full_clean()
        else:
            context['customersjourlines'] = CustomersJourLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        transtype = TransTypes.objects.all().filter(id=form.instance.transtype_id).values()
        print(transtype)
        maxid = CustomersJour.objects.all().filter(transtype_id=form.instance.transtype_id).count()
        journum = transtype[0]['code'] + '-' + str(maxid + 1)


        print('form.instance.transtype_id')
        inistatus = LookUp.objects.filter(keyid=10001).values('id')
        form.instance.status_id = inistatus[0]['id']  # initiated ID
        form.instance.statuschangedby=self.request.user
        form.instance.statusdate = timezone.now()
        form.instance.journalnumber= journum

        customersjourlines = context['customersjourlines']
        print('validate')
        response = super().form_valid(form)
        if customersjourlines.is_valid():
            print('validate customersjourlines')
            response = super().form_valid(form)
            customersjourlines.instance = self.object
            form.save()

            customersjourlines.save()
        else:
            context['customersjourlines'] = CustomersJourLineFormSet()
            maxid = int(CustomersJour.objects.latest('pk').pk) + 1
            context['maxid'] = maxid

        return response

class CustomersJourUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomersJour
    form_class = CustomersJourForm
#    fields = '__all__'
    template_name = 'ar/trans/edit_customersjour.html'
    success_message = 'Success: Customers Journal  was updated.'
    success_url = reverse_lazy("ar:list-customersjour")

    def get_context_data(self, **kwargs):
        context = super(CustomersJourUpdateView, self).get_context_data(**kwargs)

        context['customers'] = Customers.objects.all().filter(allowaccountentry=True)

        op_id = self.kwargs
        otype = CustomersJour.objects.filter(pk=op_id['pk']).values('journalnumber','journaldate','transtype_id')
        journaldate =   otype[0]['journaldate'].strftime('%Y-%m-%d')
        transtypeid = otype[0]['transtype_id']
        context['journaldate'] = journaldate

        context['journalnumber'] = otype[0]['journalnumber']


        posperiod = FiscalYearsPeriodsModules.objects.filter(module__code='AR',closedate =None
                                     ).exclude(opendate=None).aggregate(Min('fiscalyearperiod__fromdate'),Max('fiscalyearperiod__todate'))
        if all([posperiod['fiscalyearperiod__fromdate__min'], posperiod['fiscalyearperiod__todate__max']]):
            mindate= posperiod['fiscalyearperiod__fromdate__min'].strftime('%Y-%m-%d')
            maxdate= posperiod['fiscalyearperiod__todate__max'].strftime('%Y-%m-%d')
            context['mindate'] = mindate
            context['maxdate'] = maxdate
        else:
            context['mindate'] = datetime.today()
            context['maxdate'] = datetime.today()

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']


        model = apps.get_model('crm', 'UserBusinessRoles')
        transrole = model.objects.filter(user_id = self.request.user.pk ).values('id')
        if transrole:
            userbusrole_id = transrole[0]['id']
            model = apps.get_model('crm', 'UserBusinessRolesttline')
            transrole = model.objects.filter(userbusinessrole_id = userbusrole_id , transtype_id = transtypeid ).values()
        else:
            model = apps.get_model('crm', 'UserBusinessRolesttline')
            transrole = model.objects.filter(transtype_id = transtypeid ).values()


        if transrole == None or transrole.count() ==  0 :
            context['cancreate'] = 'False'
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
        else:
            context['cancreate'] =str( to_bool(transrole[0]['cancreate']))
            context['canedit'] =str(to_bool( transrole[0]['canedit']))
            context['canview'] =str(to_bool( transrole[0]['canview']))
            context['cansubmit'] =str(to_bool( transrole[0]['cansubmit']))
            context['canapprove'] =str(to_bool( transrole[0]['canapprove']))
            context['canpost'] = str(to_bool(transrole[0]['canpost']))
            context['canrejct'] = str(to_bool(transrole[0]['canrejct']))
            print('before post')



        if self.request.POST:
            context['customersjourlines'] = CustomersJourLineFormSet(self.request.POST, instance=self.object)
            context['customersjourlines'].full_clean()
        else:
            context['customersjourlines'] = CustomersJourLineFormSet(instance=self.object)
            context['customersjourlines'].full_clean()

            print('else post')

        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)

        customersjourlines = context['customersjourlines']
        response = super().form_valid(form)

        if customersjourlines.is_valid():
            # for childform in  customersjourlines:
            #     print('childform.instance.ledid' )
            #     print(childform.instance.ledid )
            #     if childform.instance.ledger == None and childform.instance.customer == None:
            #         context['customersjourlines'] = CustomersJourLineFormSet()
            #         return response

            # print(childform.instance.ledger)
            # print(childform.instance.customer)

            print('validate customersjourlines')
            response = super().form_valid(form)
            customersjourlines.instance = self.object
            form.save()

            customersjourlines.save()
        else:
            print(customersjourlines.errors)
            context['customersjourlines'] = CustomersJourLineFormSet()
            maxid = int(CustomersJour.objects.latest('pk').pk) + 1
            context['maxid'] = maxid

        return response



class CustomersJourDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CustomersJour
    template_name = 'ar/trans/delete_customersjour.html'
    success_message = 'Success: Customers Journal  was deleted.'
    success_url = reverse_lazy('ar:list-customersjour')


######### End Customers Journal

######### Customers Payments

class CustomersPaymentsListView(LoginRequiredMixin, ListView):
    model = CustomersPayments
    context_object_name = 'customerspayments'
    template_name = 'ar/trans/list-customerspayments.html'


class CustomersPaymentsUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomersPayments
    fields = '__all__'
    template_name = 'ar/trans/edit_customerspayments.html'
#    form_class = customersPaymentsForm
    success_message = 'Success: Customers Payment  was updated.'
    success_url = reverse_lazy("ar:list-customerspayments")

    def post(self, request, *args, **kwargs):
        CustomersPayment = CustomersPayments.objects.get(pk=kwargs['pk'])
        CustomersPayment.save
        cursor = connection.cursor()
        cursor.execute(
            "call gl_PostPayment(90003," + str(CustomersPayment.pk) + "," + str(self.request.user.pk) + "  );")
        path = "ar:list-customerspayments"

        return redirect(path)

    def get_context_data(self, **kwargs):
        context = super(CustomersPaymentsUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['customerspaymentslines'] = CustomersPaymentsLineFormSet(self.request.POST, instance=self.object)
            context['customerspaymentslines'].full_clean()
        else:
            context['customerspaymentslines'] = CustomersPaymentsLineFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        customerspaymentslines = context['customerspaymentslines']

        if customerspaymentslines.is_valid():
            response = super().form_valid(form)
            customerspaymentslines.instance = self.object
            form.save()
            customerspaymentslines.save()
            return response
        elif formset.is_valid() == False:
            print('faild')
            return super().form_invalid(form)


#        LedgerPayment = form.save(commit=False)
#        LedgerPayment.approvaldate = timezone.now()
#        LedgerPayment.approvalby  = self.request.user

 #       LedgerPayment.save

#        return super(LedgerPaymentsUpdateView, self).form_valid(form)


######### End Customers Payments


######### Collections

class CollectionsListView(LoginRequiredMixin, ListView):
    model = Collections
    context_object_name = 'collections'
    template_name = 'ar/trans/list-collections.html'

class CollectionsCreateView(LoginRequiredMixin,  CreateView):
    model = Collections
    form_class = CollectionsForm
    #fields = '__all__'
    template_name = 'ar/trans/create_collections.html'
    success_message = 'Success: Collections was created.'
    success_url = reverse_lazy('ar:list-collections')



    def get_context_data(self, **kwargs):
        context = super(CollectionsCreateView, self).get_context_data(**kwargs)
        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()

        context['currencydecimal'] = 2

        if companyprofile == None :
            messages.error(self.request, 'Please Create Company')
            return reverse('ar:list-collections')

        else:
            context['comusecostcenter1'] = companyprofile['usecostcenter1']
            context['comusecostcenter2'] = companyprofile['usecostcenter2']
            context['comusecostcenter3'] = companyprofile['usecostcenter3']
            context['comusecostcenter4'] = companyprofile['usecostcenter4']

        try:
            maxid = Collections.objects.filter().count() + 1
        except:
            maxid = 1

        context['lastnumber'] =  'COL' + '-' + str(maxid)

        context['currentdate'] = datetime.now().date().strftime('%Y-%m-%d')

        collector = Salesmans.objects.filter(user=self.request.user ).values('id','code','engname','arbname')
        if collector == None or collector.count() ==  0 :
            messages.error(self.request, "You are not a Collector")            
            return context
        context['collector'] = collector
        context['collector_id'] =  collector[0]['id']

        parents=None
        parentids=[]
        customers = Customers.objects.filter(allowaccountentry=True).values()

        context['customers'] = customers

        paymentmethod = PaymentsMethods.objects.filter().exclude(iscredit=True).values()

        context['paymentmethod'] = paymentmethod

        model = apps.get_model('crm', 'UserBusinessRoles')
        collectionrole = model.objects.filter(user_id = self.request.user.pk ).values()
        if collectionrole == None or collectionrole.count() ==  0 :
            context['cancreate'] = 'False'
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'
        else:
            context['cancreate'] =str( to_bool(collectionrole[0]['colcancreate']))
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'




        if self.request.POST:

            context['collectionsduepayments'] = CollectionsDuePaymentsFormSet(self.request.POST, instance=self.object)
            context['collectionsduepayments'].full_clean()

        else:
            context['collectionsduepayments'] = CollectionsDuePaymentsFormSet(instance=self.object)


        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)
        print('before')

        inistatus = LookUp.objects.filter(keyid=10001).values('id')   # PaymentStatus	Initiated
        form.instance.status_id = inistatus[0]['id']  # initiated ID
        form.instance.statuschangedby=self.request.user
        form.instance.statusdate = timezone.now()
        form.instance.collectiondate = timezone.now()

        duepayments = context['collectionsduepayments']
        duepayments.clean()

        if duepayments.is_valid():
            print('duepayments.errors')
            response = super().form_valid(form)
            duepayments.instance = self.object
            duepayments.save()


            form.save()

        elif duepayments.is_valid() == False:
            print(duepayments.errors)
            messages.error(self.request, "Error")
            print(duepayments.errors)
            return super().form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('invalid')
        context = self.get_context_data(form=form)
        print(form.errors)
        return super().form_invalid(form)

class CollectionsUpdateView(LoginRequiredMixin, UpdateView):
    model = Collections
    fields = '__all__'
    template_name = 'ar/trans/edit_collections.html'
    success_message = 'Success: Collections was Updated.'
    success_url = reverse_lazy('ar:list-collections')

    def get_context_data(self, **kwargs):
        context = super(CollectionsUpdateView, self).get_context_data(**kwargs)

        col_id = self.kwargs
        col = Collections.objects.filter(pk=col_id['pk']).values('number','collectiondate','collector_id','amount','customer_id','paymentmethod_id','status__keyid')
        context['number'] = col[0]['number']
        context['amount'] = col[0]['amount']
        context['currentpay'] = col[0]['paymentmethod_id']
        context['customerid'] = col[0]['customer_id']
        statuskeyid = col[0]['status__keyid']

        context['collectiondate'] = col[0]['collectiondate'].strftime('%Y-%m-%d')
        print(col[0]['collector_id'])

        collector = Salesmans.objects.filter(id=col[0]['collector_id'] ).values('id','code','engname','arbname')
        context['collector'] = collector
        context['collector_id'] =  collector[0]['id']


        customers = Customers.objects.filter(allowaccountentry=True).values()

        context['customers'] = customers

        paymentmethod = PaymentsMethods.objects.filter().exclude(iscredit=True).values()

        context['paymentmethod'] = paymentmethod

        model = apps.get_model('crm', 'UserBusinessRoles')
        collectionrole = model.objects.filter(user_id = self.request.user.pk ).values()
        if collectionrole == None or collectionrole.count() ==  0 :
            print(collectionrole)
            context['cancreate'] = 'False'
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'
        else:
            if statuskeyid == 10001:   #initiated
                context['cancreate'] = str(collectionrole[0]['colcancreate'])
                context['canedit'] = str(collectionrole[0]['colcanedit'])
                context['canview'] = str(collectionrole[0]['colcanview'])
                context['cansubmit'] = str(collectionrole[0]['colcansubmit'])
                context['canapprove'] = 'False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'
            elif statuskeyid == 10002:  #submitted
                context['cancreate'] = str(collectionrole[0]['colcancreate'])
                context['canedit'] = str(collectionrole[0]['colcanedit'])
                context['canview'] = str(collectionrole[0]['colcanview'])
                context['cansubmit'] = 'False'
                context['canapprove'] =str( collectionrole[0]['colcanapprove'])
                context['canpost'] = 'False'
                context['canrejct'] = str(collectionrole[0]['colcanrejct'])
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Approved
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = str(collectionrole[0]['colcanpost'])
                context['canrejct'] = 'False'
                context['cancancel'] = str(collectionrole[0]['colcancancel'])

            elif statuskeyid == 10004: #posted
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Rejcted
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Canceled
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'



        if self.request.POST:
            context['collectionsduepayments'] = CollectionsDuePaymentsFormSet(self.request.POST, instance=self.object)
            context['collectionsduepayments'].full_clean()
        else:
            context['collectionsduepayments'] = CollectionsDuePaymentsFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        print('form_valid')
        op_id = self.kwargs
        retisclose = Collections.objects.filter(pk=op_id['pk']).values('isclose','islocked')
        isclose = retisclose[0]['isclose']
        islocked= retisclose[0]['islocked']

        duepayments = context['collectionsduepayments']
        duepayments.clean()

        # if self.request.method == 'POST':
        #     if islocked == True:
        #         try:
        #             raise forms.ValidationError("Error Record Locked")
        #         except Exception as e:
        #             messages.error(self.request, 'Locked Record')
        #             return HttpResponseRedirect(self.request.path_info)


        if duepayments.is_valid():
            try:
                if 'save' in self.request.POST:
                    if islocked == True:
                        try:
                            raise forms.ValidationError("Error Record Locked")
                        except Exception as e:
                            messages.error(self.request, 'Locked Record')
                            return HttpResponseRedirect(self.request.path_info)

                    response = super().form_valid(form)
                    duepayments.instance = self.object
                    duepayments.save()
                    return response

                elif 'post' in self.request.POST:
                    # Only Goods receive Or Goods Delivery
                    print('post')
                    try:
                        cursor = connection.cursor()
                        cursor.execute("call ar_CollectionPost(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request,'Successfully Posted' )
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)

                elif 'approve' in self.request.POST:
                    try:
                        cursor = connection.cursor()
                        cursor.execute("call ar_CollectionApproval(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Approved')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        print('errorerror')
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)
                        #messages.error(self.request, 'error message kh')
                        #return HttpResponse(e)

                elif 'submit' in self.request.POST:
                    try:
                        print("call ar_CollectionSubmit(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")

                        cursor = connection.cursor()
                        cursor.execute("call ar_CollectionSubmit(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Submited')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)

                elif 'reject' in self.request.POST:
                    print('reject')
                    try:
                        print("call ar_CollectionReject(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")

                        cursor = connection.cursor()
                        cursor.execute("call ar_CollectionReject(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Rejected')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)

                elif 'cancel' in self.request.POST:
                    print('cancel')
                    try:
                        print("call ar_CollectionCancel(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")

                        cursor = connection.cursor()
                        cursor.execute("call ar_CollectionCancel(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Canceled')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)



            except Exception as e:
                print(e)


        elif duepayments.is_valid() == False:
            messages.error(self.request, "Error")
            print(duepayments.errors)
            return super().form_invalid(form)



class CollectionsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Collections
    template_name = 'ar/trans/delete_collections.html'
    success_message = 'Success: Collection was deleted.'
    success_url = reverse_lazy('ar:list-collections')

######### End Collections

######### Salesmans Groups

class SalesmansGroupsListView(LoginRequiredMixin, generic.ListView):
    model = SalesmansGroups
    context_object_name = 'salesmansgroups'
    template_name = 'ar/master/list-salesmansgroups.html'


class SalesmansGroupsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = SalesmansGroups
    form_class = SalesmansGroupsForm
    template_name = 'ar/master/create_salesmansgroups.html'
    success_message = 'Success: salesmans groups was created.'
    success_url = reverse_lazy('ar:list-salesmansgroups')


class SalesmansGroupsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = SalesmansGroups
    template_name = 'ar/master/edit_salesmansgroups.html'
    form_class = SalesmansGroupsForm
    success_message = 'Success: Salesmans Groups was updated.'
    success_url = reverse_lazy("ar:list-salesmansgroups")

    def form_valid(self, form):
        salesmansgroups = form.save()
        salesmansgroups.save
        return super(SalesmansGroupsUpdateView, self).form_valid(form)

class SalesmansGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = SalesmansGroups
    template_name = 'ar/master/delete_salesmansgroups.html'
    success_message = 'Success: salesmans groups was deleted.'
    success_url = reverse_lazy('ar:list-salesmansgroups')


######### End Salesmans Groups



######### Salesmans

class SalesmansListView(LoginRequiredMixin, generic.ListView):
    model = Salesmans
    context_object_name = 'salesmans'
    template_name = 'ar/master/list-salesmans.html'


class SalesmansCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Salesmans
    form_class = SalesmansForm
    template_name = 'ar/master/create_salesmans.html'
    success_message = 'Success: salesmans  was created.'
    success_url = reverse_lazy('ar:list-salesmans')


class SalesmansUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Salesmans
    template_name = 'ar/master/edit_salesmans.html'
    form_class = SalesmansForm
    success_message = 'Success: Salesmans was updated.'
    success_url = reverse_lazy("ar:list-salesmans")

    def form_valid(self, form):
        salesmans = form.save()
        salesmans.save
        return super(SalesmansUpdateView, self).form_valid(form)

class SalesmansDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Salesmans
    template_name = 'ar/master/delete_salesmans.html'
    success_message = 'Success: salesmans was deleted.'
    success_url = reverse_lazy('ar:list-salesmans')


######### End Salesmans
