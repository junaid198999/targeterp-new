from django.shortcuts import render
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

# Create your views here.
######### Banks Groups

class BanksGroupsListView(LoginRequiredMixin, generic.ListView):
    model = BanksGroups
    context_object_name = 'banksgroups'
    template_name = 'bnk/master/list-banksgroups.html'


class BanksGroupsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = BanksGroups
    form_class = BanksGroupsForm
    template_name = 'bnk/master/create_banksgroups.html'
    success_message = 'Success: banksgroups  was created.'
    success_url = reverse_lazy('bnk:list-banksgroups')


class BanksGroupsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = BanksGroups
    template_name = 'bnk/master/edit_banksgroups.html'
    form_class = BanksGroupsForm
    success_message = 'Success: banks groups was updated.'
    success_url = reverse_lazy("bnk:list-banksgroups")

    def form_valid(self, form):
        banksgroups = form.save()
        banksgroups.save
        return super(BanksGroupsUpdateView, self).form_valid(form)

class BanksGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = BanksGroups
    template_name = 'bnk/master/delete_banksgroups.html'
    success_message = 'Success: banksgroups was deleted.'
    success_url = reverse_lazy('bnk:list-banksgroups')

def deletebanksgroups(request):
    Lc= BanksGroups.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/bnk/banksgroups/")

######### End Banks Groups



######### Banks

class BanksListView(LoginRequiredMixin, generic.ListView):
    model = Banks
    context_object_name = 'banks'
    template_name = 'bnk/master/list-banks.html'


class BanksCreateView(LoginRequiredMixin,  CreateView):
    model = Banks
    form_class = BanksForm
    #fields = '__all__'
    template_name = 'bnk/master/create_banks.html'
    success_message = 'Success: banks was created.'
    success_url = reverse_lazy('bnk:list-banks')


    def get_context_data(self, **kwargs):
        context = super(BanksCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['banksaddresses'] = BanksAddressesFormSet(self.request.POST, instance=self.object)
            context['banksaddresses'].full_clean()

            context['bankscontacts'] = BanksContactsFormSet(self.request.POST, instance=self.object)
            context['bankscontacts'].full_clean()

            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet(self.request.POST, instance=self.object)
            context['bankscreditcardstypes'].full_clean()

        else:
            context['banksaddresses'] = BanksAddressesFormSet(instance=self.object)
            context['bankscontacts'] = BanksContactsFormSet(instance=self.object)
            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet(instance=self.object)

        #print(context['banksaddress'])
        return context

    def form_valid(self, form):
        #self.object = form.save()
        context = self.get_context_data(form=form)
        bnkaddr = context['banksaddresses']
        bnkcont = context['bankscontacts']
        bankcct = context['bankscreditcardstypes']
        response = super().form_valid(form)

        if bnkaddr.is_valid() :
            response = super().form_valid(form)
            bnkaddr.instance = self.object
            bnkaddr.save()
            form.save()
        else:
            context['banksaddresses'] = BanksAddressesFormSet()
            #context['customerscontact'] = CustomersContactsForm()

        if bnkcont.is_valid():
            bnkcont.instance = self.object
            bnkcont.save()
            form.save()
        else:
            print(bnkcont.errors)
            context['bankscontacts'] = BanksAddressesFormSet

        if bankcct.is_valid():
            bankcct.instance = self.object
            bankcct.save()
            form.save()
        else:
            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet


        return response

class BanksUpdateView(LoginRequiredMixin,  UpdateView):
    model = Banks
    template_name = 'bnk/master/edit_banks.html'
    #form_class = CustomersForm
    fields = '__all__'
    success_message = 'Success: Banks was updated.'
    success_url = reverse_lazy("bnk:list-banks")


    def get_context_data(self, **kwargs):
        context = super(BanksUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['banksaddresses'] = BanksAddressesFormSet(self.request.POST, instance=self.object)
            context['banksaddresses'].full_clean()

            context['bankscontacts'] = BanksContactsFormSet(self.request.POST, instance=self.object)
            context['bankscontacts'].full_clean()

            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet(self.request.POST, instance=self.object)
            context['bankscreditcardstypes'].full_clean()

        else:
            context['banksaddresses'] = BanksAddressesFormSet(instance=self.object)
            context['bankscontacts'] = BanksContactsFormSet(instance=self.object)
            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet(instance=self.object)

        #print(context['customersaddress'])
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        bankaddr = context['banksaddresses']
        bankcont = context['bankscontacts']
        bankcct = context['bankscreditcardstypes']

        response = super().form_valid(form)

        if bankaddr.is_valid() :
            bankaddr.instance = self.object
            bankaddr.save()
            form.save()
        else:
            context['banksaddresses'] = BanksAddressesFormSet()
            #context['customerscontact'] = CustomersContactsForm()

        if bankcont.is_valid():
            bankcont.instance = self.object
            bankcont.save()
            form.save()
        else:
            print(bankcont.errors)
            context['bankscontacts'] = BanksContactsFormSet


        if bankcct.is_valid():
            bankcct.instance = self.object
            bankcct.save()
            form.save()
        else:
            context['bankscreditcardstypes'] = BanksCreditCardsTypesFormSet


        return response

class BanksDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Banks
    template_name = 'bnk/master/delete_banks.html'
    success_message = 'Success: Banks was deleted.'
    success_url = reverse_lazy('bnk:list-banks')

def deletebanks(request):
    Lc= Banks.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/bnk/banks/")


######### End Banks


######### BanksDocumentsUnderProcess

class BanksDocumentsUnderProcessListView(LoginRequiredMixin, generic.ListView):
    model = BanksDocumentsUnderProcess
    context_object_name = 'banksdocumentsunderprocess'
    template_name = 'bnk/trans/list-banksdocumentsunderprocess.html'

    def get_queryset(self):

        return BanksDocumentsUnderProcess.objects.filter(isclose=False).values('pk','sourcename','sourceid','bankrefno','bankrefdate','created_date','created_by')



class BanksDocumentsUnderProcessUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = BanksDocumentsUnderProcess
    template_name = 'bnk/trans/edit_banksdocumentsunderprocess.html'
    form_class = BanksDocumentsUnderProcessForm
    success_message = 'Success: Banks Documents Under Process was updated.'
    success_url = reverse_lazy("bnk:list-banksdocumentsunderprocess")

    def form_valid(self, form):

        banksdocumentsunderprocess = form.save()
        banksdocumentsunderprocess.instance = self.object
        banksdocumentsunderprocess.instance.updated_by=self.request.user

        banksdocumentsunderprocess.save
        if 'post' in self.request.POST:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "call bnk_banksdocumentsunderprocessPost(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                messages.success(self.request, 'Successfully Posted')
                return HttpResponseRedirect(self.get_success_url())
            except Exception as e:
                print('errorerror')
                messages.warning(self.request, e)
                return HttpResponseRedirect(self.request.path_info)
                # messages.error(self.request, 'error message kh')
                # return HttpResponse(e)

        return super(BanksDocumentsUnderProcessUpdateView, self).form_valid(form)

class BanksDocumentsUnderProcessDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = BanksDocumentsUnderProcess
    template_name = 'bnk/trans/delete_banksdocumentsunderprocess.html'
    success_message = 'Success: banksdocumentsunderprocess was deleted.'
    success_url = reverse_lazy('bnk:list-banksdocumentsunderprocess')

######### End BanksDocumentsUnderProcess


