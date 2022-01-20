
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    CreateView, ListView, UpdateView)
from datetime import datetime
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                                  BSModalUpdateView,
                                                  BSModalReadView,
                                                  BSModalDeleteView)


driver = None
######### Modules

class ModulesListView(LoginRequiredMixin, generic.ListView):
    model = Modules
    context_object_name = 'modules'
    template_name = 'sy/setting/list-modules.html'

class ModulesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Modules
    form_class = ModulesForm
    template_name = 'sy/setting/create_modules.html'
    success_message = 'Success: Modules was created.'
    success_url = reverse_lazy('sy:list-modules')

class ModulesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Modules
    template_name = 'sy/setting/edit_modules.html'
    form_class = ModulesForm
    success_message = 'Success: Modules was updated.'
    success_url = reverse_lazy("sy:list-modules")

    def form_valid(self, form):
        Modules = form.save()
        Modules.save
        return super(ModulesUpdateView, self).form_valid(form)

class ModulesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Modules
    template_name = 'sy/setting/delete_modules.html'
    success_message = 'Success: Modules was deleted.'
    success_url = reverse_lazy('sy:list-modules')
######### End Modules

######### LookUp

class LookUpListView(LoginRequiredMixin, generic.ListView):
    model = LookUp
    context_object_name = 'lookup'
    template_name = 'sy/setting/list-lookup.html'

class LookUpCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = LookUp
    form_class = LookUpForm
    template_name = 'sy/setting/create_lookup.html'
    success_message = 'Success: LookUp was created.'
    success_url = reverse_lazy('sy:list-lookup')

class LookUpUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = LookUp
    template_name = 'sy/setting/edit_lookup.html'
    form_class = LookUpForm
    success_message = 'Success: LookUp was updated.'
    success_url = reverse_lazy("sy:list-lookup")

    def form_valid(self, form):
        LookUp = form.save()
        LookUp.save
        return super(LookUpUpdateView, self).form_valid(form)

class LookUpDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = LookUp
    template_name = 'sy/setting/delete_lookup.html'
    success_message = 'Success: LookUp was deleted.'
    success_url = reverse_lazy('sy:list-lookup')
######### End LookUp

######### Fiscal Years

class FiscalYearsListView(LoginRequiredMixin, ListView):
    model = FiscalYears
    context_object_name = 'fiscalyears'
    template_name = 'sy/master/list-fiscalyears.html'


class FiscalYearsCreateView(LoginRequiredMixin,  CreateView):
    model = FiscalYears
    form_class = FiscalYearsForm
    template_name = 'sy/master/create_fiscalyears.html'
    success_message = 'Success: Fiscal Years  was created.'
    success_url = reverse_lazy('sy:list-fiscalyears')

    maxid = 0


    def get_context_data(self, **kwargs):
        context = super(FiscalYearsCreateView, self).get_context_data(**kwargs)

        try:
            maxid = int(FiscalYears.objects.latest('pk').pk) + 1
        except:
            maxid = 1

        # context['maxid'] = maxid
        # context['mindate'] = '2020-12-05'

        # trant_id = 'none'
        # context['trant_id'] = trant_id

        # context['maxdate'] = '2020-12-25'
        # if self.request.POST:
        #     context['fiscalyearsperiods'] = FiscalYearsPeriodsFormSet(self.request.POST, instance=self.object)
        #     context['fiscalyearsperiods'].full_clean()
        # else:
        #     context['fiscalyearsperiods'] = FiscalYearsPeriodsFormSet(instance=self.object)
        # print(context)
        return context

    # def form_valid(self, form):
    #     context = self.get_context_data(form=form)
    #     fiscalyearsperiods = context['fiscalyearsperiods']

    #     print(fiscalyearsperiods)       

    #     # response = None
    #     if fiscalyearsperiods.is_valid():
    #         print("valid")
    #         response = super().form_valid(form)
    #         fiscalyearsperiods.instance = self.object
    #         print(fiscalyearsperiods.instance)
    #         form.save()
    #         fiscalyearsperiods.save()
    #         return response
    #     else:
    #         print("invalid")
    #         context['fiscalyearsperiods'] = FiscalYearsPeriodsFormSet()
    #         maxid = int(FiscalYears.objects.latest('pk').pk) + 1
    #         context['maxid'] = maxid
    #         return super().form_invalid(form)



class FiscalYearsUpdateView(LoginRequiredMixin, UpdateView):
    model = FiscalYears
    template_name = 'sy/master/edit_fiscalyears.html'
    success_message = 'Success: Fiscal Years  was updated.'
    success_url = reverse_lazy("sy:list-fiscalyears")
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(FiscalYearsUpdateView, self).get_context_data(**kwargs)

#        context['ledger'] = Ledger.objects.all().filter(allowaccountentry=True)

        context['mindate'] = '2020-12-05'
        context['maxdate'] = '2020-12-25'


        if self.request.POST:
            context['fiscalyearsperiods'] = FiscalYearsPeriodsFormSet(self.request.POST, instance=self.object)
            context['fiscalyearsperiods'].full_clean()
        else:
            context['fiscalyearsperiods'] = FiscalYearsPeriodsFormSet(instance=self.object)
        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['fiscalyearsperiods']
        print(context)

        if formset.is_valid():

            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        elif formset.is_valid() == False:
            return super().form_invalid(form)



class FiscalYearsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = FiscalYears
    template_name = 'sy/master/delete_fiscalyears.html'
    success_message = 'Success: FiscalYears  was deleted.'
    success_url = reverse_lazy('gl:list-fiscalyears')


######### End Fiscal Years

#########  Fiscal Years Periods Modules

class FiscalYearsPeriodsModulesListView(LoginRequiredMixin, generic.ListView):
    model = FiscalYearsPeriodsModules
    context_object_name = 'fiscalyearsperiodsmodules'
    template_name = 'sy/master/list-fiscalyearsperiodsmodules.html'

class FiscalYearsPeriodsModulesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = FiscalYearsPeriodsModules
    template_name = 'sy/master/edit_fiscalyearsperiodsmodules.html'
    form_class = FiscalYearsPeriodsModulesForm
    success_message = 'Success: Fiscal Years Periods Modules was updated.'
    success_url = reverse_lazy("sy:list-fiscalyearsperiodsmodules")

    def form_valid(self, form):
        FiscalYearsPeriodsModules = form.save()
        FiscalYearsPeriodsModules.save
        return super(FiscalYearsPeriodsModulesUpdateView, self).form_valid(form)

######### End Fiscal Years Periods Modules

######### Payments Methods

class PaymentsMethodsListView(LoginRequiredMixin, generic.ListView):
    model = PaymentsMethods
    context_object_name = 'paymentsmethods'
    template_name = 'sy/master/list-paymentsmethods.html'

class PaymentsMethodsCreateView(LoginRequiredMixin,BSModalCreateView):
    model = PaymentsMethods
    form_class = PaymentsMethodsForm
    template_name = 'sy/master/create_paymentsmethods.html'
    success_message = 'Success: Payment Method was created.'
    success_url = reverse_lazy('sy:list-paymentsmethods')

class PaymentsMethodsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = PaymentsMethods
    template_name = 'sy/master/edit_paymentsmethods.html'
    form_class = PaymentsMethodsForm
    success_message = 'Success: paymentsmethods was updated.'
    success_url = reverse_lazy("sy:list-paymentsmethods")

    def form_valid(self, form):
        PaymentsMethods = form.save()
        PaymentsMethods.save
        return super(PaymentsMethodsUpdateView, self).form_valid(form)

class PaymentsMethodsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = PaymentsMethods
    template_name = 'sy/master/delete_paymentsmethods.html'
    success_message = 'Success: paymentsmethods was deleted.'
    success_url = reverse_lazy('sy:list-paymentsmethods')
######### End  Payments Methods


######### Ledgers Types

class CreditCardsTypesListView(LoginRequiredMixin, generic.ListView):
    model = CreditCardsTypes
    context_object_name = 'creditcardstypes'
    template_name = 'sy/master/list-creditcardstypes.html'


class CreditCardsTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = CreditCardsTypes
    form_class = CreditCardsTypesForm
    template_name = 'sy/master/create_creditcardstypes.html'
    success_message = 'Success: Credit Cards Types was created.'
    success_url = reverse_lazy('sy:list-creditcardstypes')

class CreditCardsTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = CreditCardsTypes
    template_name = 'sy/master/edit_creditcardstypes.html'
    form_class = CreditCardsTypesForm
    success_message = 'Success: Credit Cards Types was updated.'
    success_url = reverse_lazy("sy:list-creditcardstypes")

    def form_valid(self, form):
        CreditCardsTypes = form.save()
        CreditCardsTypes.save
        return super(CreditCardsTypesUpdateView, self).form_valid(form)

class CreditCardsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CreditCardsTypes
    template_name = 'sy/master/delete_creditcardstypes.html'
    success_message = 'Success: creditcardstypes was deleted.'
    success_url = reverse_lazy('sy:list-creditcardstypes')
######### End Ledgers Types


######### Languages

class LanguagesListView(LoginRequiredMixin, generic.ListView):
    model = Languages
    context_object_name = 'languages'
    template_name = 'sy/setting/list-languages.html'

class LanguagesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Languages
    form_class = LanguagesForm
    template_name = 'sy/setting/create_languages.html'
    success_message = 'Success: Languages was created.'
    success_url = reverse_lazy('sy:list-languages')

class LanguagesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Languages
    template_name = 'sy/setting/edit_languages.html'
    form_class = LanguagesForm
    success_message = 'Success: Languages was updated.'
    success_url = reverse_lazy("sy:list-languages")

    def form_valid(self, form):
        Languages = form.save()
        Languages.save
        return super(LanguagesUpdateView, self).form_valid(form)

class LanguagesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Languages
    template_name = 'sy/setting/delete_languages.html'
    success_message = 'Success: languages was deleted.'
    success_url = reverse_lazy('sy:list-languages')
######### End Languages


######### Nationalities

class NationalitiesListView(LoginRequiredMixin, generic.ListView):
    model = Nationalities
    context_object_name = 'nationalities'
    template_name = 'sy/master/list-nationalities.html'

class NationalitiesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Nationalities
    form_class = NationalitiesForm
    template_name = 'sy/master/create_nationalities.html'
    success_message = 'Success: Nationalities was created.'
    success_url = reverse_lazy('sy:list-nationalities')

class NationalitiesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Nationalities
    template_name = 'sy/master/edit_nationalities.html'
    form_class = NationalitiesForm
    success_message = 'Success: Nationalities was updated.'
    success_url = reverse_lazy("sy:list-nationalities")

    def form_valid(self, form):
        Nationalities = form.save()
        Nationalities.save
        return super(NationalitiesUpdateView, self).form_valid(form)

class NationalitiesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Nationalities
    template_name = 'sy/master/delete_nationalities.html'
    success_message = 'Success: nationalities was deleted.'
    success_url = reverse_lazy('sy:list-nationalities')
######### End Nationalities


######### Regions

class RegionsListView(LoginRequiredMixin, generic.ListView):
    model = Regions
    context_object_name = 'regions'
    template_name = 'sy/master/list-regions.html'

class RegionsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Regions
    form_class = RegionsForm
    template_name = 'sy/master/create_regions.html'
    success_message = 'Success: Regions was created.'
    success_url = reverse_lazy('sy:list-regions')

class RegionsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Regions
    template_name = 'sy/master/edit_regions.html'
    form_class = RegionsForm
    success_message = 'Success: Regions was updated.'
    success_url = reverse_lazy("sy:list-regions")

    def form_valid(self, form):
        Regions = form.save()
        Regions.save
        return super(RegionsUpdateView, self).form_valid(form)

class RegionsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Regions
    template_name = 'sy/master/delete_regions.html'
    success_message = 'Success: Regions was deleted.'
    success_url = reverse_lazy('sy:list-regions')
######### End Regions


######### Countries

class CountriesListView(LoginRequiredMixin, generic.ListView):
    model = Countries
    context_object_name = 'countries'
    template_name = 'sy/master/list-countries.html'

class CountriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Countries
    form_class = CountriesForm
    template_name = 'sy/master/create_countries.html'
    success_message = 'Success: Countries was created.'
    success_url = reverse_lazy('sy:list-countries')

class CountriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Countries
    template_name = 'sy/master/edit_countries.html'
    form_class = CountriesForm
    success_message = 'Success: Countries was updated.'
    success_url = reverse_lazy("sy:list-countries")

    def form_valid(self, form):
        Countries = form.save()
        Countries.save
        return super(CountriesUpdateView, self).form_valid(form)

class CountriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Countries
    template_name = 'sy/master/delete_countries.html'
    success_message = 'Success: Regions was deleted.'
    success_url = reverse_lazy('sy:list-countries')
######### End Countries


######### Areas

class AreasListView(LoginRequiredMixin, generic.ListView):
    model = Areas
    context_object_name = 'areas'
    template_name = 'sy/master/list-areas.html'

class AreasCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Areas
    form_class = AreasForm
    template_name = 'sy/master/create_areas.html'
    success_message = 'Success: Areas was created.'
    success_url = reverse_lazy('sy:list-areas')

class AreasUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Areas
    template_name = 'sy/master/edit_areas.html'
    form_class = AreasForm
    success_message = 'Success: Areas was updated.'
    success_url = reverse_lazy("sy:list-areas")

    def form_valid(self, form):
        Areas = form.save()
        Areas.save
        return super(AreasUpdateView, self).form_valid(form)

class AreasDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Areas
    template_name = 'sy/master/delete_areas.html'
    success_message = 'Success: Areas was deleted.'
    success_url = reverse_lazy('sy:list-areas')
######### End Areas


######### Cities

class CitiesListView(LoginRequiredMixin, generic.ListView):
    model = Cities
    context_object_name = 'cities'
    template_name = 'sy/master/list-cities.html'

class CitiesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Cities
    form_class = CitiesForm
    template_name = 'sy/master/create_cities.html'
    success_message = 'Success: Cities was created.'
    success_url = reverse_lazy('sy:list-cities')

class CitiesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Cities
    template_name = 'sy/master/edit_cities.html'
    form_class = CitiesForm
    success_message = 'Success: Cities was updated.'
    success_url = reverse_lazy("sy:list-cities")

    def form_valid(self, form):
        Cities = form.save()
        Cities.save
        return super(CitiesUpdateView, self).form_valid(form)

class CitiesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Cities
    template_name = 'sy/master/delete_cities.html'
    success_message = 'Success: Cities was deleted.'
    success_url = reverse_lazy('sy:list-cities')
######### End Cities



######### Districts

class DistrictsListView(LoginRequiredMixin, generic.ListView):
    model = Districts
    context_object_name = 'districts'
    template_name = 'sy/master/list-districts.html'

class DistrictsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Districts
    form_class = DistrictsForm
    template_name = 'sy/master/create_districts.html'
    success_message = 'Success: Districts was created.'
    success_url = reverse_lazy('sy:list-districts')

class DistrictsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Districts
    template_name = 'sy/master/edit_districts.html'
    form_class = DistrictsForm
    success_message = 'Success: Districts was updated.'
    success_url = reverse_lazy("sy:list-districts")

    def form_valid(self, form):
        Districts = form.save()
        Districts.save
        return super(DistrictsUpdateView, self).form_valid(form)

class DistrictsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Districts
    template_name = 'sy/master/delete_districts.html'
    success_message = 'Success: Districts was deleted.'
    success_url = reverse_lazy('sy:list-districts')
######### End Districts


######### AddressesTypes

class AddressesTypesListView(LoginRequiredMixin, generic.ListView):
    model = AddressesTypes
    context_object_name = 'addressestypes'
    template_name = 'sy/master/list-addressestypes.html'

class AddressesTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = AddressesTypes
    form_class = AddressesTypesForm
    template_name = 'sy/master/create_addressestypes.html'
    success_message = 'Success: AddressesTypes was created.'
    success_url = reverse_lazy('sy:list-addressestypes')

class AddressesTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = AddressesTypes
    template_name = 'sy/master/edit_addressestypes.html'
    form_class = AddressesTypesForm
    success_message = 'Success: AddressesTypes was updated.'
    success_url = reverse_lazy("sy:list-addressestypes")

    def form_valid(self, form):
        AddressesTypes = form.save()
        AddressesTypes.save
        return super(DistrictsUpdateView, self).form_valid(form)

class AddressesTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = AddressesTypes
    template_name = 'sy/master/delete_addressestypes.html'
    success_message = 'Success: AddressesTypes was deleted.'
    success_url = reverse_lazy('sy:list-addressestypes')
######### End AddressesTypes


######### ContactsTypes

class ContactsTypesListView(LoginRequiredMixin, generic.ListView):
    model = ContactsTypes
    context_object_name = 'contactstypes'
    template_name = 'sy/master/list-contactstypes.html'

class ContactsTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ContactsTypes
    form_class = ContactsTypesForm
    template_name = 'sy/master/create_contactstypes.html'
    success_message = 'Success: Contacts Types was created.'
    success_url = reverse_lazy('sy:list-contactstypes')

class ContactsTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ContactsTypes
    template_name = 'sy/master/edit_contactstypes.html'
    form_class = ContactsTypesForm
    success_message = 'Success: Contacts Types was updated.'
    success_url = reverse_lazy("sy:list-contactstypes")

    def form_valid(self, form):
        ContactsTypes = form.save()
        ContactsTypes.save
        return super(ContactsTypesUpdateView, self).form_valid(form)

class ContactsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ContactsTypes
    template_name = 'sy/master/delete_contactstypes.html'
    success_message = 'Success: Contacts Types was deleted.'
    success_url = reverse_lazy('sy:list-contactstypes')
######### End ContactsTypes


######### BusinessActivitiesTypes

class BusinessActivitiesTypesListView(LoginRequiredMixin, generic.ListView):
    model = BusinessActivitiesTypes
    context_object_name = 'businessactivitiestypes'
    template_name = 'sy/master/list-businessactivitiestypes.html'

class BusinessActivitiesTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = BusinessActivitiesTypes
    form_class = BusinessActivitiesTypesForm
    template_name = 'sy/master/create_businessactivitiestypes.html'
    success_message = 'Success: Business Activities Types was created.'
    success_url = reverse_lazy('sy:list-businessactivitiestypes')

class BusinessActivitiesTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = BusinessActivitiesTypes
    template_name = 'sy/master/edit_businessactivitiestypes.html'
    form_class = BusinessActivitiesTypesForm
    success_message = 'Success: Business Activities Types was updated.'
    success_url = reverse_lazy("sy:list-businessactivitiestypes")

    def form_valid(self, form):
        BusinessActivitiesTypes = form.save()
        BusinessActivitiesTypes.save
        return super(BusinessActivitiesTypesUpdateView, self).form_valid(form)

class BusinessActivitiesTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = BusinessActivitiesTypes
    template_name = 'sy/master/delete_businessactivitiestypes.html'
    success_message = 'Success: Business Activities Types was deleted.'
    success_url = reverse_lazy('sy:list-businessactivitiestypes')
######### End BusinessActivitiesTypes


######### Taxes

class TaxesListView(LoginRequiredMixin, ListView):
    model = Taxes
    context_object_name = 'taxes'
    template_name = 'sy/master/list-taxes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TaxesCreateView(LoginRequiredMixin,  CreateView):
    model = Taxes
    fields = '__all__'
    template_name = 'sy/master/create_taxes.html'
    success_message = 'Success: Taxes created.'
    success_url = reverse_lazy('sy:list-taxes')

    def get_context_data(self, **kwargs):
        context = super(TaxesCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['taxeslines'] = TaxesLinesFormSet(self.request.POST, instance=self.object)
            context['taxeslines'].full_clean()
        else:
            context['taxeslines'] = TaxesLinesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        taxeslines = context['taxeslines']
        taxeslines.clean()
        response = super().form_valid(form)
        if taxeslines.is_valid():
            print('validate')
            response = super().form_valid(form)
            taxeslines.instance = self.object
            taxeslines.save()
            form.save()
            print(taxeslines.errors)
            #return response
        elif taxeslines.is_valid() == False:
            print(taxeslines.errors)

            print(taxeslines.errors)
            return super().form_invalid(form)

        return response

class TaxesUpdateView(LoginRequiredMixin, UpdateView):
    model = Taxes
    fields = '__all__'
    template_name = 'sy/master/edit_taxes.html'
    success_message = 'Success: Taxes was updated.'
    success_url = reverse_lazy("sy:list-taxes")


    def get_context_data(self, **kwargs):
        context = super(TaxesUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['taxeslines'] = TaxesLinesFormSet(self.request.POST, instance=self.object)
            context['taxeslines'].full_clean()
        else:
            context['taxeslines'] = TaxesLinesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        taxeslines = context['taxeslines']
        taxeslines.clean()
        print('validate')
        if taxeslines.is_valid():
            try:
                response = super().form_valid(form)
                taxeslines.instance = self.object
                taxeslines.save()
                form.save()
                print(taxeslines.errors)

                return response
            except Exception as e:
                print(taxeslines.errors)

        elif taxeslines.is_valid() == False:

            print(taxeslines.errors)
            return super().form_invalid(form)

class TaxesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Taxes
    template_name = 'sy/master/delete_taxes.html'
    success_message = 'Success: Taxes was deleted.'
    success_url = reverse_lazy('sy:list-taxes')

######### End Taxes


######### Taxes Groups

class TaxesGroupsListView(LoginRequiredMixin, ListView):
    model = TaxesGroups
    context_object_name = 'taxesgroups'
    template_name = 'sy/master/list-taxesgroups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TaxesGroupsCreateView(LoginRequiredMixin,  CreateView):
    model = TaxesGroups
    form_class = TaxesGroupsForm
    #fields = '__all__'
    template_name = 'sy/master/create_taxesgroups.html'
    success_message = 'Success: Taxes created.'
    success_url = reverse_lazy('sy:list-taxesgroups')

    def get_context_data(self, **kwargs):
        context = super(TaxesGroupsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['taxesgroupslines'] = TaxesGroupsLinesFormSet(self.request.POST, instance=self.object)
            context['taxesgroupslines'].full_clean()
        else:
            context['taxesgroupslines'] = TaxesGroupsLinesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        taxesgroupslines = context['taxesgroupslines']
        taxesgroupslines.clean()
        response = super().form_valid(form)
        if taxesgroupslines.is_valid():
            print('validate')
            response = super().form_valid(form)
            taxesgroupslines.instance = self.object
            taxesgroupslines.save()
            form.save()
            print(taxesgroupslines.errors)
            #return response
        elif taxesgroupslines.is_valid() == False:
            print(taxesgroupslines.errors)

            print(taxesgroupslines.errors)
            return super().form_invalid(form)

        return response

class TaxesGroupsUpdateView(LoginRequiredMixin, UpdateView):
    model = TaxesGroups
    fields = '__all__'
    template_name = 'sy/master/edit_taxesgroups.html'
    success_message = 'Success: Taxes Groups was updated.'
    success_url = reverse_lazy("sy:list-taxesgroups")


    def get_context_data(self, **kwargs):
        context = super(TaxesGroupsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['taxesgroupslines'] = TaxesGroupsLinesFormSet(self.request.POST, instance=self.object)
            context['taxesgroupslines'].full_clean()
        else:
            context['taxesgroupslines'] = TaxesGroupsLinesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        taxesgroupslines = context['taxesgroupslines']
        taxesgroupslines.clean()
        print('validate')
        if taxesgroupslines.is_valid():
            try:
                response = super().form_valid(form)
                taxesgroupslines.instance = self.object
                taxesgroupslines.save()
                form.save()
                print(taxesgroupslines.errors)

                return response
            except Exception as e:
                print(taxesgroupslines.errors)

        elif taxesgroupslines.is_valid() == False:

            print(taxesgroupslines.errors)
            return super().form_invalid(form)

class TaxesGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = TaxesGroups
    template_name = 'sy/master/delete_taxesgroups.html'
    success_message = 'Success: Taxes Groups was deleted.'
    success_url = reverse_lazy('sy:list-taxesgroups')

######### End Taxes Groups

######### company Profile

class CompanyProfileListView(LoginRequiredMixin, ListView):
    model = CompanyProfile
    context_object_name = 'companyprofile'
    template_name = 'sy/setting/list-companyprofile.html'

class CompanyProfileCreateView(LoginRequiredMixin,  CreateView):
    model = CompanyProfile
    fields = '__all__'
    template_name = 'sy/setting/create_companyprofile.html'
    success_message = 'Success: company profile was created.'
    success_url = reverse_lazy('sy:list-companyprofile')

    def get_context_data(self, **kwargs):
        context = super(CompanyProfileCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet(self.request.POST, instance=self.object)
            context['companyprofileaddresses'].full_clean()

            context['companyprofilecontacts'] = CompanyProfileContactsFormSet(self.request.POST, instance=self.object)
            context['companyprofilecontacts'].full_clean()


        else:
            context['companyprofilecontacts'] = CompanyProfileContactsFormSet(instance=self.object)
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        companyprofilelines = context['companyprofilecontacts']
        invlocations = context['companyprofileaddresses']
        print('validate')
        response = super().form_valid(form)
        if companyprofilelines.is_valid():
            print('validate companyprofileContacts')
            response = super().form_valid(form)
            companyprofilelines.instance = self.object

            companyprofilelines.save()
            form.save()

        else:
            print(companyprofilelines.errors)
            context['companyprofilecontacts'] = CompanyProfileContactsFormSet()

        if companyprofilelines.is_valid():
            print('validate companyprofilelines')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet

        return response

class CompanyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyProfile
    fields = '__all__'
    template_name = 'sy/setting/edit_companyprofile.html'
    success_message = 'Success: company profile was updated.'
    success_url = reverse_lazy("sy:list-companyprofile")

    def get_context_data(self, **kwargs):
        context = super(CompanyProfileUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet(self.request.POST, instance=self.object)
            context['companyprofileaddresses'].full_clean()

            context['companyprofilecontacts'] = CompanyProfileContactsFormSet(self.request.POST, instance=self.object)
            context['companyprofilecontacts'].full_clean()


        else:
            context['companyprofilecontacts'] = CompanyProfileContactsFormSet(instance=self.object)
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        companyprofilelines = context['companyprofilecontacts']
        invlocations = context['companyprofileaddresses']
        print('validate')
        response = super().form_valid(form)
        if invlocations.is_valid():
            print('validate Addresses')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['companyprofileaddresses'] = CompanyProfileAddressesFormSet

        if companyprofilelines.is_valid():
            print('validate companyprofilecontacts')
            response = super().form_valid(form)
            companyprofilelines.instance = self.object

            companyprofilelines.save()


            form.save()

        else:
            print(companyprofilelines.errors)
            context['companyprofilecontacts'] = CompanyProfileContactsFormSet()


        return response

class CompanyProfileDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CompanyProfile
    template_name = 'sy/setting/delete_companyprofile.html'
    success_message = 'Success: company profile was deleted.'
    success_url = reverse_lazy('sy:list-companyprofile')


######### End company Profile



######### Prices levels

class PriceLevelsListView(LoginRequiredMixin, generic.ListView):
    model = PriceLevels
    context_object_name = 'pricelevels'
    template_name = 'sy/master/list-pricelevels.html'


class PriceLevelsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = PriceLevels
    form_class = PriceLevelsForm
    template_name = 'sy/master/create_pricelevels.html'
    success_message = 'Success: prices levels was created.'
    success_url = reverse_lazy('sy:list-pricelevels')


class PriceLevelsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = PriceLevels
    template_name = 'sy/master/edit_pricelevels.html'
    form_class = PriceLevelsForm
    success_message = 'Success: prices levels was updated.'
    success_url = reverse_lazy("sy:list-pricelevels")

    def form_valid(self, form):
        pricelevels = form.save()
        pricelevels.save
        return super(PriceLevelsUpdateView, self).form_valid(form)

class PriceLevelsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = PriceLevels
    template_name = 'sy/master/delete_pricelevels.html'
    success_message = 'Success: prices levels was deleted.'
    success_url = reverse_lazy('sy:list-pricelevels')


######### End Prices levels




######### Payments Tearms

class PaymentsTearmsListView(LoginRequiredMixin, generic.ListView):
    model = PaymentsTearms
    context_object_name = 'paymentstearms'
    template_name = 'sy/master/list-paymentstearms.html'


class PaymentsTearmsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = PaymentsTearms
    form_class = PaymentsTearmsForm
    template_name = 'sy/master/create_paymentstearms.html'
    success_message = 'Success: Payment Tearm was created.'
    success_url = reverse_lazy('sy:list-paymentstearms')


class PaymentsTearmsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = PaymentsTearms
    template_name = 'sy/master/edit_paymentstearms.html'
    form_class = PaymentsTearmsForm
    success_message = 'Success: Payment Tearm was updated.'
    success_url = reverse_lazy("sy:list-paymentstearms")

    def form_valid(self, form):
        paymentstearms = form.save()
        paymentstearms.save
        return super(PaymentsTearmsUpdateView, self).form_valid(form)

class PaymentsTearmsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = PaymentsTearms
    template_name = 'sy/master/delete_paymentstearms.html'
    success_message = 'Success: Payment Tearm was deleted.'
    success_url = reverse_lazy('sy:list-paymentstearms')


######### End Payments Tearms



######### Cash Discount Roles

class CashDiscountsRolesListView(LoginRequiredMixin, ListView):
    model = CashDiscountsRoles
    context_object_name = 'cashdiscountsroles'
    template_name = 'sy/master/list-cashdiscountsroles.html'

class CashDiscountsRolesCreateView(LoginRequiredMixin,  CreateView):
    model = CashDiscountsRoles
    form_class = CashDiscountsRolesForm
    #fields = '__all__'
    template_name = 'sy/master/create_cashdiscountsroles.html'
    success_message = 'Success: Cash Discounts Roles  was created.'
    success_url = reverse_lazy('sy:list-cashdiscountsroles')

    def get_context_data(self, **kwargs):
        context = super(CashDiscountsRolesCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet(self.request.POST, instance=self.object)
            context['cashdiscountsrolesline'].full_clean()
        else:
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        cashdiscountsrolesline = context['cashdiscountsrolesline']
        print('validate')
        response = super().form_valid(form)
        if cashdiscountsrolesline.is_valid():
            print('validate cashdiscountsrolesline')
            response = super().form_valid(form)
            cashdiscountsrolesline.instance = self.object
            form.save()

            cashdiscountsrolesline.save()
        else:
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet()

        return response

class CashDiscountsRolesUpdateView(LoginRequiredMixin, UpdateView):
    model = CashDiscountsRoles
    form_class = CashDiscountsRolesForm
#    fields = '__all__'
    template_name = 'sy/master/edit_cashdiscountsroles.html'
    success_message = 'Success: Cash Discounts Roles  was updated.'
    success_url = reverse_lazy('sy:list-cashdiscountsroles')

    def get_context_data(self, **kwargs):
        context = super(CashDiscountsRolesUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet(self.request.POST, instance=self.object)
            context['cashdiscountsrolesline'].full_clean()
        else:
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet(instance=self.object)
            context['cashdiscountsrolesline'].full_clean()

            print('else post')

        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)

        cashdiscountsrolesline = context['cashdiscountsrolesline']
        response = super().form_valid(form)

        if cashdiscountsrolesline.is_valid():
            response = super().form_valid(form)
            cashdiscountsrolesline.instance = self.object
            form.save()

            cashdiscountsrolesline.save()
        else:
            print(cashdiscountsrolesline.errors)
            context['cashdiscountsrolesline'] = CashDiscountsRolesLineFormSet()

        return response



class CashDiscountsRolesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CashDiscountsRoles
    template_name = 'sy/master/delete_cashdiscountsroles.html'
    success_message = 'Success: Cash Discounts Roles  was Deleted.'
    success_url = reverse_lazy('sy:list-cashdiscountsroles')


######### End Cash Discount Roles



