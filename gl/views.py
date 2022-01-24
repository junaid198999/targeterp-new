import calendar, io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from ar.models import CustomersCategories
from .forms import *
from .models import *
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    CreateView, ListView, UpdateView)
from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum, F, IntegerField, Q, Count
from django.views.generic import TemplateView, DetailView, FormView

import _datetime
#from . import signals
from django.apps import apps

from django.views.generic.edit import CreateView
from django.utils import timezone
from bootstrap_modal_forms.generic import (BSModalCreateView,BSModalUpdateView,BSModalReadView,BSModalDeleteView)
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from itertools import chain
from sy.models import CompanyProfile,FiscalYearsPeriodsModules

from django.db.models import Max
from django.db.models import Min
from django.apps import apps

driver = None





def index(request):
    return render(request, 'gl/index.html')

######### Ledgers Types

class LedgersTypesListView(LoginRequiredMixin, generic.ListView):
    model = LedgersTypes
    context_object_name = 'ledgerstypes'
    template_name = 'gl/list-ledgerstypes.html'


class LedgersTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = LedgersTypes
    form_class = LedgersTypesForm
    template_name = 'gl/create_ledgerstypes.html'
    success_message = 'Success: Ledger Type was created.'
    success_url = reverse_lazy('gl:list-ledgerstypes')

class LedgersTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = LedgersTypes
    template_name = 'gl/edit_ledgerstypes.html'
    form_class = LedgersTypesForm
    success_message = 'Success: ledgers Types was updated.'
    success_url = reverse_lazy("gl:list-ledgerstypes")

    def form_valid(self, form):
        LedgersTypes = form.save()
        LedgersTypes.save
        return super(LedgersTypesUpdateView, self).form_valid(form)

class LedgersTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = LedgersTypes
    template_name = 'gl/delete_ledgerstypes.html'
    success_message = 'Success: ledgerstypes was deleted.'
    success_url = reverse_lazy('gl:list-ledgerstypes')
######### End Ledgers Types

######### Ledgers Categories

class LedgersCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = LedgersCategories
    context_object_name = 'ledgerscategories'
    template_name = 'gl/master/list-ledgerscategories.html'


class LedgersCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = LedgersCategories
    form_class = LedgersCategoriesForm
    template_name = 'gl/master/create_ledgerscategories.html'
    success_message = 'Success: Ledger Categories was created.'
    success_url = reverse_lazy('gl:list-ledgerscategories')


class LedgersCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = LedgersCategories
    template_name = 'gl/master/edit_ledgerscategories.html'
    form_class = LedgersCategoriesForm
    success_message = 'Success: Ledgers Categories was updated.'
    success_url = reverse_lazy("gl:list-ledgerscategories")

    def form_valid(self, form):
        LedgersCategories = form.save()
        LedgersCategories.save
        return super(LedgersCategoriesUpdateView, self).form_valid(form)

class LedgersCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = LedgersCategories
    template_name = 'gl/master/delete_ledgerscategories.html'
    success_message = 'Success: Ledgers Categories was deleted.'
    success_url = reverse_lazy('gl:list-ledgerscategories')


######### End Ledgers Categories

######### Ledgers

class LedgerListView(LoginRequiredMixin, generic.ListView):
    model = Ledger
    context_object_name = 'ledger'
    template_name = 'gl/master/list-ledger.html'


class LedgerCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Ledger
    form_class = LedgerForm
    template_name = 'gl/master/create_ledger.html'
    success_message = 'Success: Ledger was created.'
    success_url = reverse_lazy('gl:list-ledger')


class LedgerUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Ledger
    template_name = 'gl/master/edit_ledger.html'
    form_class = LedgerForm
    success_message = 'Success: Ledger was updated.'
    success_url = reverse_lazy("gl:list-ledger")

    def form_valid(self, form):
        Ledger = form.save()
        Ledger.save
        return super(LedgerUpdateView, self).form_valid(form)

class LedgerDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Ledger
    template_name = 'gl/master/delete_ledger.html'
    success_message = 'Success: Ledgers was deleted.'
    success_url = reverse_lazy('gl:list-ledger')

######### End Ledgers

######### Cost Categories

class CostCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = CostCategories
    context_object_name = 'costcategories'
    template_name = 'gl/master/list-costcategories.html'


class CostCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CostCategories
    form_class = CostCategoriesForm
    template_name = 'gl/master/create_costcategories.html'
    success_message = 'Success: Cost Categories was created.'
    success_url = reverse_lazy('gl:list-costcategories')


class CostCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CostCategories
    template_name = 'gl/master/edit_costcategories.html'
    form_class = CostCategoriesForm
    success_message = 'Success: Cost Categories was updated.'
    success_url = reverse_lazy("gl:list-costcategories")

    def form_valid(self, form):
        CostCategories = form.save()
        CostCategories.save
        return super(CostCategoriesUpdateView, self).form_valid(form)

class CostCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CostCategories
    template_name = 'gl/master/delete_costcategories.html'
    success_message = 'Success: Cost Categories was deleted.'
    success_url = reverse_lazy('gl:list-costcategories')


######### End Cost Categories


######### Cost Centers Levels

class CostCentersLevelsListView(LoginRequiredMixin, generic.ListView):
    model = CostCentersLevels
    context_object_name = 'costcenterslevels'
    template_name = 'gl/master/list-CostCentersLevels.html'


class CostCentersLevelsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CostCentersLevels
    form_class = CostCentersLevelsForm
    template_name = 'gl/master/create_costcenterslevels.html'
    success_message = 'Success: Cost Centers Levels was created.'
    success_url = reverse_lazy('gl:list-costcenterslevels')


class CostCentersLevelsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CostCentersLevels
    template_name = 'gl/master/edit_costcenterslevels.html'
    form_class = CostCentersLevelsForm
    success_message = 'Success: Cost Centers Levels was updated.'
    success_url = reverse_lazy("gl:list-costcenterslevels")

    def form_valid(self, form):
        CostCentersLevels = form.save()
        CostCentersLevels.save
        return super(CostCentersLevelsUpdateView, self).form_valid(form)

class CostCentersLevelsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CostCentersLevels
    template_name = 'gl/master/delete_costcenterslevels.html'
    success_message = 'Success: Cost Centers Levels was deleted.'
    success_url = reverse_lazy('gl:list-costcenterslevels')


######### End Cost Centers Levels

######### Cost Centers

class CostCentersListView(LoginRequiredMixin, generic.ListView):
    model = CostCenters
    context_object_name = 'costcenters'
    template_name = 'gl/master/list-CostCenters.html'


class CostCentersCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CostCenters
    form_class = CostCentersForm
    template_name = 'gl/master/create_costcenters.html'
    success_message = 'Success: Cost Centers  was created.'
    success_url = reverse_lazy('gl:list-costcenters')


class CostCentersUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CostCenters
    template_name = 'gl/master/edit_costcenters.html'
    form_class = CostCentersForm
    success_message = 'Success: Cost Centers  was updated.'
    success_url = reverse_lazy("gl:list-costcenters")

    def form_valid(self, form):
        CostCenters = form.save()
        CostCenters.save
        return super(CostCentersUpdateView, self).form_valid(form)

class CostCentersDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CostCenters
    template_name = 'gl/master/delete_costcenters.html'
    success_message = 'Success: Cost Centers  was deleted.'
    success_url = reverse_lazy('gl:list-costcenters')


######### End Cost Centers


######### Trans Types

class TransTypesListView(LoginRequiredMixin, generic.ListView):
    model = TransTypes
    context_object_name = 'transtypes'
    template_name = 'gl/master/list-transtypes.html'


class TransTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = TransTypes
    form_class = TransTypesForm
    template_name = 'gl/master/create_transtypes.html'
    success_message = 'Success: Trans Types  was created.'
    success_url = reverse_lazy('gl:list-transtypes')


class TransTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = TransTypes
    template_name = 'gl/master/edit_transtypes.html'
    form_class = TransTypesForm
    success_message = 'Success: Trans Types  was updated.'
    success_url = reverse_lazy("gl:list-transtypes")

    def form_valid(self, form):
        TransTypes = form.save()
        TransTypes.save
        return super(TransTypesUpdateView, self).form_valid(form)

class TransTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = TransTypes
    template_name = 'gl/master/delete_transtypes.html'
    success_message = 'Success: Trans Types  was deleted.'
    success_url = reverse_lazy('gl:list-transtypes')    

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except:
            # context = { "error" : "Can't delete this Trans Type Becasue it's releted somewhere" }
            return render(request, "gl/master/list-transtypes.html" , {"error": "Can't delete this Trans Type Becasue it's releted somewhere"})



######### End Trans Types


######### LEdger Journal

class LedgerJourListView(LoginRequiredMixin, ListView):
    model = LedgerJour
    context_object_name = 'ledgerjour'
    template_name = 'gl/trans/list-ledgerjour.html'


class LedgerJourCreateView(LoginRequiredMixin,  CreateView):
    model = LedgerJour
    form_class = LedgerJourForm
    #fields = '__all__'
    template_name = 'gl/trans/create_ledgerjour.html'
    success_message = 'Success: Ledger Journal  was created.'
    success_url = reverse_lazy('gl:list-ledgerjour')


    def get_context_data(self, **kwargs):

        context = super(LedgerJourCreateView, self).get_context_data(**kwargs)
        try:
            maxid = int(LedgerJour.objects.latest('pk').pk) + 1
        except:
            maxid = 1

        context['ledger'] = Ledger.objects.all().filter(allowaccountentry=True)
        context['maxid'] = maxid
        context['transtypes'] = TransTypes.objects.all().filter(transkind__keyid=51) # "General Journal"
        context['currentdate'] = datetime.now().date().strftime('%Y-%m-%d')

        posperiod = FiscalYearsPeriodsModules.objects.filter(module__code='AR',closedate =None
                                     ).exclude(opendate=None).aggregate(Min('fiscalyearperiod__fromdate'),Max('fiscalyearperiod__todate'))
        mindate= posperiod['fiscalyearperiod__fromdate__min']
        maxdate= posperiod['fiscalyearperiod__todate__max']
        if mindate:
            mindate = mindate.strftime('%Y-%m-%d')
        else:
            mindate = datetime.today()
        if maxdate:
            mixdate = maxdate.strftime('%Y-%m-%d')
        else:
            maxdate = datetime.today()
        
        context['mindate'] = mindate
        context['maxdate'] = maxdate


        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()

        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']

        if self.request.POST:
            context['maxid'] = maxid
            context['ledgerjourlines'] = LedgerJourLineFormSet(self.request.POST, instance=self.object)
            context['ledgerjourlines'].full_clean()            
        else:
            context['ledgerjourlines'] = LedgerJourLineFormSet(instance=self.object)        
        return context

    def form_valid(self, form):

        context = self.get_context_data(form=form)
        transtype = TransTypes.objects.all().filter(id=form.instance.transtype_id).values()
        maxid = LedgerJour.objects.all().filter(transtype_id=form.instance.transtype_id).count()
        journum = transtype[0]['code'] + '-' + str(maxid + 1)

        print('form.instance.transtype_id')
        inistatus = LookUp.objects.filter(keyid=10001).values('id')
        form.instance.status_id = inistatus[0]['id']  # initiated ID
        form.instance.statuschangedby=self.request.user
        form.instance.statusdate = timezone.now()
        form.instance.journalnumber= journum

        ledgerjourlines = context['ledgerjourlines']
        response = super().form_valid(form)

        if ledgerjourlines.is_valid():
            print('validate legerjourline')
            response = super().form_valid(form)
            ledgerjourlines.instance = self.object
            form.save()
            ledgerjourlines.save()

        else:
            print(ledgerjourlines.errors)

            context['ledgerjourlines'] = LedgerJourLineFormSet()
            maxid = int(LedgerJour.objects.latest('pk').pk) + 1
            context['maxid'] = maxid

        return response

class LedgerJourUpdateView(LoginRequiredMixin, UpdateView):
    model = LedgerJour
    form_class = LedgerJourForm
    #fields = '__all__'
    template_name = 'gl/trans/edit_ledgerjour.html'
    success_message = 'Success: Ledger Journal  was updated.'
    success_url = reverse_lazy("gl:list-ledgerjour")

    def get_context_data(self, **kwargs):
        context = super(LedgerJourUpdateView, self).get_context_data(**kwargs)

        context['ledger'] = Ledger.objects.all().filter(allowaccountentry=True)

        op_id = self.kwargs
        otype = LedgerJour.objects.filter(pk=op_id['pk']).values('journalnumber','journaldate','transtype_id')
        journaldate =   otype[0]['journaldate'].strftime('%Y-%m-%d')
        transtypeid = otype[0]['transtype_id']
        context['journaldate'] = journaldate
        context['journalnumber'] = otype[0]['journalnumber']


        posperiod = FiscalYearsPeriodsModules.objects.filter(module__code='AR',closedate =None
                                     ).exclude(opendate=None).aggregate(Min('fiscalyearperiod__fromdate'),Max('fiscalyearperiod__todate'))
        mindate= posperiod['fiscalyearperiod__fromdate__min']
        maxdate= posperiod['fiscalyearperiod__todate__max']
        if mindate:
            mindate = mindate.strftime('%Y-%m-%d')
        else:
            mindate = datetime.today()
        if maxdate:
            mixdate = maxdate.strftime('%Y-%m-%d')
        else:
            maxdate = datetime.today()
        
        context['mindate'] = mindate
        context['maxdate'] = maxdate

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']

        # model = apps.get_model('crm', 'UserBusinessRoles')
        # transrole = model.objects.filter(user_id = self.request.user.pk ).values('id')
        # userbusrole_id = None
        # if transrole:
        #     userbusrole_id = transrole[0]['id']

        # model = apps.get_model('crm', 'UserBusinessRolesttline')
        # transrole = model.objects.filter(transtype_id = transtypeid )
        # if userbusrole_id:
        #     transrole = transrole.filter(userbusinessrole_id = userbusrole_id).values('id')

        # if transrole == None or transrole.count() ==  0 :
        #     context['cancreate'] = 'False'
        #     context['canedit'] = 'False'
        #     context['canview'] = 'False'
        #     context['cansubmit'] = 'False'
        #     context['canapprove'] = 'False'
        #     context['canpost'] = 'False'
        #     context['canrejct'] = 'False'
        # else:
        #     print(transrole[0])
        #     context['cancreate'] =str( to_bool(transrole[0]['cancreate']))
        #     context['canedit'] =str(to_bool( transrole[0]['canedit']))
        #     context['canview'] =str(to_bool( transrole[0]['canview']))
        #     context['cansubmit'] =str(to_bool( transrole[0]['cansubmit']))
        #     context['canapprove'] =str(to_bool( transrole[0]['canapprove']))
        #     context['canpost'] = str(to_bool(transrole[0]['canpost']))
        #     context['canrejct'] = str(to_bool(transrole[0]['canrejct']))

        if self.request.POST:
            context['ledgerjourlines'] = LedgerJourLineFormSet(self.request.POST, instance=self.object)
            context['ledgerjourlines'].full_clean()
        else:
            context['ledgerjourlines'] = LedgerJourLineFormSet(instance=self.object)
        return context


    def form_valid(self, form):
        print('validate')

        context = self.get_context_data(form=form)

        ledgerjourlines = context['ledgerjourlines']
        response = super().form_valid(form)


        if ledgerjourlines.is_valid():
            response = super().form_valid(form)
            ledgerjourlines.instance = self.object
            form.save()
            ledgerjourlines.save()
            return response
        elif ledgerjourlines.is_valid() == False:            
            return super().form_invalid(form)



class LedgerJourDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = LedgerJour
    template_name = 'gl/trans/delete_ledgerjour.html'
    success_message = 'Success: Ledger Journal  was deleted.'
    success_url = reverse_lazy('gl:list-LedgerJour')


######### End Ledger Journal

######### Load Data

def load_transtypes(request):
    transtypes_id = request.GET.get('transtypes')
    transtypes = transtypes_id.objects.filter(transtypes_id=transtypes_id).order_by('code')
    return render(request, 'gl/dropdownlist/transtypes_dropdown_list.html', {'transtypes': transtypes})

######### End Load Data



######### Treasuries

class TreasuriesListView(LoginRequiredMixin, generic.ListView):
    model = Treasuries
    context_object_name = 'treasuries'
    template_name = 'gl/treasury/list-treasuries.html'


class TreasuriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Treasuries
    form_class = TreasuriesForm
    template_name = 'gl/treasury/create_treasuries.html'
    success_message = 'Success: Treasuries  was created.'
    success_url = reverse_lazy('gl:list-treasuries')


class TreasuriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Treasuries
    template_name = 'gl/treasury/edit_treasuries.html'
    form_class = TreasuriesForm
    success_message = 'Success: Treasuries  was updated.'
    success_url = reverse_lazy("gl:list-treasuries")

    def form_valid(self, form):
        Treasuries = form.save()
        Treasuries.save
        return super(TreasuriesUpdateView, self).form_valid(form)

class TreasuriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Treasuries
    template_name = 'gl/treasury/delete_treasuries.html'
    success_message = 'Success: Treasuries  was deleted.'
    success_url = reverse_lazy('gl:list-treasuries')


######### End Treasuries


######### Treasuries Orders

class TreasuriesOrdersListView(LoginRequiredMixin, generic.ListView):
    model = TreasuriesOrders
    context_object_name = 'treasuriesorders'
    template_name = 'gl/treasury/list-treasuriesorders.html'


class TreasuriesOrdersCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = TreasuriesOrders
    form_class = TreasuriesOrdersForm
    template_name = 'gl/treasury/create_treasuriesorders.html'
    success_message = 'Success: Treasuries Orders  was created.'
    success_url = reverse_lazy('gl:list-treasuriesorders')

    def get_context_data(self, **kwargs):
        context = super(TreasuriesOrdersCreateView, self).get_context_data(**kwargs)
        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']
        return context


    def form_valid(self, form):
        TreasuriesOrders = form.save()
        TreasuriesOrders.paymentmethod = TreasuriesOrders.transtype.paymentmethod
        TreasuriesOrders.paymentdirection  = TreasuriesOrders.transtype.paymentdirection
        TreasuriesOrders.save
        return super(TreasuriesOrdersCreateView, self).form_valid(form)


class TreasuriesOrdersUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = TreasuriesOrders
    template_name = 'gl/treasury/edit_treasuriesorders.html'
    form_class = TreasuriesOrdersForm
    success_message = 'Success: Treasuries Orders  was updated.'
    success_url = reverse_lazy("gl:list-treasuriesorders")

    def get_context_data(self, **kwargs):
        context = super(TreasuriesOrdersUpdateView, self).get_context_data(**kwargs)
        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        print(companyprofile)
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        approvaldate_dt = data['approvaldate']
        print(approvaldate_dt)
        if form.is_valid():
            if approvaldate_dt is None:
                print(approvaldate_dt)
                TreasuriesOrders = form.save()
                TreasuriesOrders.paymentmethod = TreasuriesOrders.transtype.paymentmethod
                TreasuriesOrders.paymentdirection = TreasuriesOrders.transtype.paymentdirection
                TreasuriesOrders.save
                return super(TreasuriesOrdersUpdateView, self).form_valid(form)
            else:
                return HttpResponse("Order is posted")



"""
    def form_valid(self, form):
        
        TreasuriesOrders = form.save()
        TreasuriesOrders.paymentmethod = TreasuriesOrders.transtype.paymentmethod
        TreasuriesOrders.paymentdirection  = TreasuriesOrders.transtype.paymentdirection


        TreasuriesOrders.save
        return super(TreasuriesOrdersUpdateView, self).form_valid(form)
"""





class TreasuriesOrdersDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = TreasuriesOrders
    template_name = 'gl/treasury/delete_treasuriesorders.html'
    success_message = 'Success: Treasuries Orders was deleted.'
    success_url = reverse_lazy('gl:list-treasuriesorders')


######### End Treasuries Orders


######### Treasuries Orders Approval


class TreasuriesOrdersApprovalListView(LoginRequiredMixin, generic.ListView):
#    model = TreasuriesOrders
    queryset = TreasuriesOrders.objects.filter(approvaldate=None)

    context_object_name = 'treasuriesorders'
    fields='__al__'
    template_name = 'gl/treasury/list-treasuriesordersapproval.html'


class TreasuriesOrdersApprovalUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = TreasuriesOrders
    template_name = 'gl/treasury/edit_treasuriesordersapproval.html'
    form_class = TreasuriesOrdersApprovalForm
    success_message = 'Success: Treasuries Orders Approval  was updated.'
    success_url = reverse_lazy("gl:list-treasuriesordersapproval")


    def get_context_data(self, **kwargs):
        context = super(TreasuriesOrdersApprovalUpdateView, self).get_context_data(**kwargs)
        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']
        return context

    def post(self,request,*args, **kwargs):
        TreasuriesOrder = TreasuriesOrders.objects.get(pk=kwargs['pk'])
        TreasuriesOrder.save()
        print("call gl_TreasuriesOrdersApproval(" + str(TreasuriesOrder.pk) + "," + str(self.request.user.pk) + "  );")
        cursor = connection.cursor()
        cursor.execute("call gl_TreasuriesOrdersApproval(" + str(TreasuriesOrder.pk) + "," + str(self.request.user.pk) + "  );")
        path = "gl:list-treasuriesordersapproval"

        return redirect(path)


######### End Treasuries Orders Approval

######### Ledger Payments

class LedgerPaymentsListView(LoginRequiredMixin, ListView):
    model = LedgerPayments
    context_object_name = 'ledgerpayments'
    template_name = 'gl/treasury/list-ledgerpayments.html'


class LedgerPaymentsUpdateView(LoginRequiredMixin, UpdateView):
    model = LedgerPayments
    fields = '__all__'
    template_name = 'gl/treasury/edit_ledgerpayments.html'
#    form_class = LedgerPaymentsForm
    success_message = 'Success: Ledger Payment  was updated.'
    success_url = reverse_lazy("gl:list-ledgerpayments")

    def post(self, request, *args, **kwargs):
        print('companyprofile')

        LedgerPayment = LedgerPayments.objects.get(pk=kwargs['pk'])
        LedgerPayment.save
        #        print("call gl_TreasuriesOrdersApproval(" + str(TreasuriesOrder.pk) + "," + str(self.request.user.pk) + "  );")
        cursor = connection.cursor()
        cursor.execute(
            "call gl_PostPayment(90001," + str(LedgerPayment.pk) + "," + str(self.request.user.pk) + "  );")
        path = "gl:list-ledgerpayments"

        return redirect(path)

    def get_context_data(self, **kwargs):
        context = super(LedgerPaymentsUpdateView, self).get_context_data(**kwargs)

        #context['ledger'] = Ledger.objects.all().filter(allowaccountentry=True)

        #context['mindate'] = '2020-12-05'
        #context['maxdate'] = '2020-12-25'
        #       context['ledgerjour'] =LedgerJour.objects.filter(pk=self.kwargs['pk'])
        # context['costcenter1'] = CostCenters.objects.all()

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        print(companyprofile)
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']

        if self.request.POST:
            context['ledgerpaymentslines'] = LedgerPaymentsLineFormSet(self.request.POST, instance=self.object)
            context['ledgerpaymentslines'].full_clean()
        else:
            context['ledgerpaymentslines'] = LedgerPaymentsLineFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        ledgerpaymentslines = context['ledgerpaymentslines']

        if ledgerpaymentslines.is_valid():
            response = super().form_valid(form)
            ledgerpaymentslines.instance = self.object
            form.save()
            ledgerpaymentslines.save()
            return response
        elif ledgerpaymentslines.is_valid() == False:
            print('faild')
            return super().form_invalid(form)


#        LedgerPayment = form.save(commit=False)
#        LedgerPayment.approvaldate = timezone.now()
#        LedgerPayment.approvalby  = self.request.user

 #       LedgerPayment.save

#        return super(LedgerPaymentsUpdateView, self).form_valid(form)


######### End Ledger Payments



