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
driver = None



######### vendors Categories

class VendorsCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = VendorsCategories
    context_object_name = 'vendorscategories'
    template_name = 'ap/master/list-vendorscategories.html'


class VendorsCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = VendorsCategories
    form_class = VendorsCategoriesForm
    template_name = 'ap/master/create_vendorscategories.html'
    success_message = 'Success: vendors Categories was created.'
    success_url = reverse_lazy('ap:list-vendorscategories')


class VendorsCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = VendorsCategories
    template_name = 'ap/master/edit_vendorscategories.html'
    form_class = VendorsCategoriesForm
    success_message = 'Success: vendors Categories was updated.'
    success_url = reverse_lazy("ap:list-vendorscategories")

    def form_valid(self, form):
        vendorsCategories = form.save()
        VendorsCategories.save
        return super(VendorsCategoriesUpdateView, self).form_valid(form)

class VendorsCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = VendorsCategories
    template_name = 'ap/master/delete_vendorscategories.html'
    success_message = 'Success: vendors Categories was deleted.'
    success_url = reverse_lazy('ap:list-vendorscategories')


def deletevendorscategories(request):
    Lc= VendorsCategories.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/vendorscategories/")


######### End vendors Categories


######### vendors Classes

class VendorsClassesListView(LoginRequiredMixin, generic.ListView):
    model = VendorsClasses
    context_object_name = 'vendorsclasses'
    template_name = 'ap/master/list-vendorsclasses.html'


class VendorsClassesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = VendorsClasses
    form_class = VendorsClassesForm
    template_name = 'ap/master/create_vendorsclasses.html'
    success_message = 'Success: vendors Classes was created.'
    success_url = reverse_lazy('ap:list-vendorsclasses')


class VendorsClassesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = VendorsClasses
    template_name = 'ap/master/edit_vendorsclasses.html'
    form_class = VendorsClassesForm
    success_message = 'Success: vendors Classes was updated.'
    success_url = reverse_lazy("ap:list-vendorsclasses")

    def form_valid(self, form):
        vendorsClasses = form.save()
        vendorsClasses.save
        return super(VendorsClassesUpdateView, self).form_valid(form)

class VendorsClassesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = VendorsClasses
    template_name = 'ap/master/delete_vendorsclasses.html'
    success_message = 'Success: vendors Classes was deleted.'
    success_url = reverse_lazy('ap:list-vendorsclasses')


def deletevendorsclasses(request):
    Lc= VendorsClasses.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/vendorsclasses/")


######### End vendors Categories


######### vendors

class VendorsListView(LoginRequiredMixin, ListView):
    model = Vendors
    context_object_name = 'vendors'
    template_name = 'ap/master/list-vendors.html'

class VendorsCreateView(LoginRequiredMixin,  CreateView):
    model = Vendors
    fields = '__all__'
    template_name = 'ap/master/create_vendors.html'
    success_message = 'Success: vendors was created.'
    success_url = reverse_lazy('ap:list-vendors')

    def get_context_data(self, **kwargs):
        context = super(VendorsCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['vendorsaddresses'] = VendorsAddressesFormSet(self.request.POST, instance=self.object)
            context['vendorsaddresses'].full_clean()

            context['vendorscontacts'] = VendorsContactsFormSet(self.request.POST, instance=self.object)
            context['vendorscontacts'].full_clean()


        else:
            context['vendorscontacts'] = VendorsContactsFormSet(instance=self.object)
            context['vendorsaddresses'] = VendorsAddressesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        vendorslines = context['vendorscontacts']
        invlocations = context['vendorsaddresses']
        print('validate')
        response = super().form_valid(form)
        if vendorslines.is_valid():
            response = super().form_valid(form)
            vendorslines.instance = self.object
            vendorslines.save()
            form.save()
        else:
            print(vendorslines.errors)
            context['vendorscontacts'] = VendorsContactsFormSet()

        if vendorslines.is_valid():
            print('validate vendorslines')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['vendorsaddresses'] = VendorsAddressesFormSet

        return response

class VendorsUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendors
    fields = '__all__'
    template_name = 'ap/master/edit_vendors.html'
    success_message = 'Success: vendors was updated.'
    success_url = reverse_lazy("ap:list-vendors")

    def get_context_data(self, **kwargs):
        context = super(VendorsUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['vendorsaddresses'] = VendorsAddressesFormSet(self.request.POST, instance=self.object)
            context['vendorsaddresses'].full_clean()

            context['vendorscontacts'] = VendorsContactsFormSet(self.request.POST, instance=self.object)
            context['vendorscontacts'].full_clean()


        else:
            context['vendorscontacts'] = VendorsContactsFormSet(instance=self.object)
            context['vendorsaddresses'] = VendorsAddressesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        vendorslines = context['vendorscontacts']
        invlocations = context['vendorsaddresses']
        print('validate')
        response = super().form_valid(form)
        if invlocations.is_valid():
            print('validate Addresses')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['vendorsaddresses'] = VendorsAddressesFormSet

        if vendorslines.is_valid():
            print('validate vendorscontacts')
            response = super().form_valid(form)
            vendorslines.instance = self.object

            vendorslines.save()


            form.save()

        else:
            print(vendorslines.errors)
            context['vendorscontacts'] = VendorsContactsFormSet()


        return response

class VendorsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Vendors
    template_name = 'ap/master/delete_vendors.html'
    success_message = 'Success: vendors was deleted.'
    success_url = reverse_lazy('ap:list-vendors')

def deletevendors(request):
    Lc= Vendors.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/vendors/")



######### End vendors


######### Buyers Groups

class BuyersGroupsListView(LoginRequiredMixin, generic.ListView):
    model = BuyersGroups
    context_object_name = 'buyersgroups'
    template_name = 'ap/master/list-buyersgroups.html'


class BuyersGroupsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = BuyersGroups
    form_class = BuyersGroupsForm
    template_name = 'ap/master/create_buyersgroups.html'
    success_message = 'Success: buyers groups was created.'
    success_url = reverse_lazy('ap:list-buyersgroups')


class BuyersGroupsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = BuyersGroups
    template_name = 'ap/master/edit_buyersgroups.html'
    form_class = BuyersGroupsForm
    success_message = 'Success: buyers groups was updated.'
    success_url = reverse_lazy("ap:list-buyersgroups")

    def form_valid(self, form):
        buyersgroups = form.save()
        buyersgroups.save
        return super(BuyersGroupsUpdateView, self).form_valid(form)

class BuyersGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = BuyersGroups
    template_name = 'ap/master/delete_buyersgroups.html'
    success_message = 'Success: buyers groups was deleted.'
    success_url = reverse_lazy('ap:list-buyersgroups')

def deletebuyersgroups(request):
    Lc= BuyersGroups.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/buyersgroups/")
######### End Buyers Groups


######### Buyers

class BuyersListView(LoginRequiredMixin, generic.ListView):
    model = Buyers
    context_object_name = 'buyers'
    template_name = 'ap/master/list-buyers.html'


class BuyersCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Buyers
    form_class = BuyersForm
    template_name = 'ap/master/create_buyers.html'
    success_message = 'Success: buyers was created.'
    success_url = reverse_lazy('ap:list-buyers')


class BuyersUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Buyers
    template_name = 'ap/master/edit_buyers.html'
    form_class = BuyersForm
    success_message = 'Success: buyers was updated.'
    success_url = reverse_lazy("ap:list-buyers")

    def form_valid(self, form):
        buyers = form.save()
        buyers.save
        return super(BuyersUpdateView, self).form_valid(form)

class BuyersDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Buyers
    template_name = 'ap/master/delete_buyers.html'
    success_message = 'Success: buyers  was deleted.'
    success_url = reverse_lazy('ap:list-buyers')

def deletebuyers(request):
    Lc= Buyers.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/buyers/")

######### End Buyers




######### vendors Jour

class VendorsJourListView(LoginRequiredMixin, ListView):
    model = VendorsJour
    context_object_name = 'vendorsjour'
    template_name = 'ap/trans/list-vendorsjour.html'

class VendorsJourCreateView(LoginRequiredMixin,  CreateView):
    model = VendorsJour
    fields = '__all__'
    template_name = 'ap/trans/create_vendorsjour.html'
    success_message = 'Success: vendors Journal was created.'
    success_url = reverse_lazy('ap:list-vendorsjour')

    def get_context_data(self, **kwargs):
        context = super(VendorsJourCreateView, self).get_context_data(**kwargs)
        try:
            maxid = int(VendorsJour.objects.latest('pk').pk) + 1
        except:
            maxid = 1

        #context['customers'] = Vendors.objects.all().filter(allowaccountentry=True)
        context['maxid'] = maxid
        context['transtypes'] = TransTypes.objects.all().filter(transkind__keyid= 51)
        context['maxdate'] = timezone.now().strftime('%Y-%m-%d')

        if self.request.POST:
            context['vendorsjourline'] = VendorsJourLineFormSet(self.request.POST, instance=self.object)
            context['vendorsjourline'].full_clean()

        else:
            context['vendorsjourline'] = VendorsJourLineFormSet(instance=self.object)
        return context





    def form_valid(self, form):

        print('validate')
        context = self.get_context_data(form=form)
        vendorsjourline = context['vendorsjourline']
        print('validate')
        response = super().form_valid(form)
        if vendorsjourline.is_valid():
            print('validate vendorsjourline')
            response = super().form_valid(form)
            vendorsjourline.instance = self.object

            vendorsjourline.save()
            form.save()

        else:
           # print(vendorsjourline.errors)
            context['vendorsjourline'] = VendorsJourLineFormSet()


        return response

class VendorsJourUpdateView(LoginRequiredMixin, UpdateView):
    model = VendorsJour
    fields = '__all__'
    template_name = 'ap/trans/edit_vendorsjour.html'
    success_message = 'Success: vendors Journal was updated.'
    success_url = reverse_lazy("ap:list-vendorsjour")

    def get_context_data(self, **kwargs):
        context = super(VendorsJourUpdateView, self).get_context_data(**kwargs)

        jour_id = self.kwargs
        jour = VendorsJour.objects.filter(pk=jour_id['pk']).values('transtype_id','journalnumber','journaldate')

        context['journalnumber'] = jour[0]['journalnumber']

        context['journaldate'] = jour[0]['journaldate'].strftime('%Y-%m-%d')



        if self.request.POST:
            context['vendorsjourline'] = VendorsJourLineFormSet(self.request.POST, instance=self.object)
            context['vendorsjourline'].full_clean()

        else:
            context['vendorsjourline'] = VendorsJourLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        vendorsjourline = context['vendorsjourline']
        print('validate')
        response = super().form_valid(form)

        if vendorsjourline.is_valid():
            print('validate vendorsjourline')
            response = super().form_valid(form)
            vendorsjourline.instance = self.object
            vendorsjourline.save()
            form.save()

        else:
            print(vendorsjourline.errors)
            context['vendorsjourline'] = VendorsJourLineFormSet()

        return response

class VendorsJourDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = VendorsJour
    template_name = 'ap/master/delete_vendorsjour.html'
    success_message = 'Success: vendors Jouranl was deleted.'
    success_url = reverse_lazy('ap:list-vendorsjour')

def deletevendorsjour(request):
    Lc= VendorsJour.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/ap/vendorsjour/")
######### End vendors Jour

