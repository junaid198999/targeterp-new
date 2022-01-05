import datetime
import calendar, io

from django.contrib.auth.models import Group

from TARGET.users.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from num2words import num2words

from django.contrib import messages, admin
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.db.models import Sum, F, IntegerField, Q, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date

from . import signals
from rest_framework.response import Response
from django.db.models import ProtectedError

from .forms import CustomerForm, CountryForm, AreaForm, CityForm, ChannelForm, \
    WarehouseForm, SalesmanForm, BranchForm, CategoryForm, ProductForm, AccountForm, UomForm, WarehouseTypeForm, \
    VendorForm, PurchaseOrderProductsFormSet, PurchaseReturnOrderProductsFormSet, SalesOrderProductsFormSet, \
    SalesReturnOrderProductsFormSet, TransferOrderProductsFormSet, \
    TargetBuildingBlocksProductsFormSet, \
    TargetBuildingBlocksAccountsProductsFormSet, \
    TargetBuildingBlocksChannelsProductsFormSet,FinancialYearForm, TargetBuildingBlocksExceptFormSet, \
    ProductUnitsForm, CollectionForm, CurrencyForm, UserForm, ExtendUserCreationForm, GroupForm, \
    UserPermissions, GroupPermissions, CompanyForm, NotificationForm, LeadForm, OpportunityForm, \
    OpportunityProductsFormSet, ActivityForm, CommissionDetailsFormFormSet, \
    AccountingChildForm, AccTransactionsDetailsFormSet, \
    SalesmanEditForm, DoctorForm, PharmacyForm, ClassForm, PharmacyCategoryForm, \
    ContractProductsFormSet, SpecialtyForm, VisitForm
from .models import Customer, City, Area, Country, Channel, Warehouse, Salesman, Branch, Category, \
    Product, Account, Uom, WarehouseType, Vendor, PurchaseOrder, Transactions, \
    PurchaseReturnOrder, SalesOrder, SalesReturnOrder, TransferOrder, \
    TargetBuildingBlocksProducts, TargetBuildingBlocks, TargetBuildingBlocksAccountsProducts, \
    TargetBuildingBlocksAccounts, TargetBuildingBlocksChannelsProducts, TargetBuildingBlocksChannels, \
    TargetTransactions, FinancialYear, UnitsName, Collection, Currency, SalesReturnProduct, \
    SalesProduct, Company, Notification, Calender, Events, Lead, Opportunity, Activities, OpportunityProduct, \
    Commission_Details, Commission,Commission_Calc, AccountingChild, AccountingParent, AccountingType, AccTransactions, \
    Doctor, Pharmacy, Class, PharmacyCategory, Contract, \
    DoctorVisits, DoctorDates, Specialty

from django.urls import reverse_lazy

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

from django.contrib.auth.models import Permission
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.parse
driver = None

Link = "https://web.whatsapp.com/"
wait = None
class logout_view(LogoutView):
    template_name = 'account/logout.html'

class MyModelAdmin(admin.ModelAdmin):
    ...

    def get_actions(self, request):
        actions = super(MyModelAdmin, self).get_actions(request)
        if self.request.user.is_staff is False:
            del actions['delete_selected']
        return actions

class login_view(LoginView):
    template_name = 'account/login.html'

class backup_view(LoginView):
    template_name = 'backup/backup_view.html'

class UomListView(LoginRequiredMixin, generic.ListView):
    model = Uom
    context_object_name = 'uoms'
    template_name = 'crm/setting/list-uoms.html'

class UomCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_uom.html'
    form_class = UomForm
    success_message = 'Success: UOM was created.'
    success_url = reverse_lazy('crm:uoms')

class UomUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Uom
    template_name = 'crm/setting/edit_uom.html'
    form_class = UomForm
    success_message = 'Success: UOM was updated.'
    success_url = reverse_lazy("crm:uoms")

class UomDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Uom
    template_name = 'crm/setting/delete_uom.html'
    success_message = 'Success: UOM was deleted.'
    success_url = reverse_lazy('crm:uoms')

    def post(request,*args, **kwargs):
        uom = get_object_or_404(Uom, pk=kwargs['pk'])
        try:
            uom.delete()
            path = "/crm/uoms/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)


def country_list(request):
    countries = Country.objects.all()
    context = {
        'countries': countries
    }
    return render(request, 'crm/setting/list-countries.html', context)

class CountryListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'crm.view_country'
    model = Country
    context_object_name = 'countries'
    template_name = 'crm/setting/list-countries.html'

class CountryCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_country.html'
    form_class = CountryForm
    success_message = 'Success: Country was created.'
    success_url = reverse_lazy('crm:countries')

class CountryUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Country
    template_name = 'crm/setting/edit_country.html'
    form_class = CountryForm
    success_message = 'Success: Country was updated.'
    success_url = reverse_lazy("crm:countries")

class CountryDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Country
    template_name = 'crm/setting/delete_country.html'
    success_message = 'Success: Country was deleted.'
    success_url = reverse_lazy('crm:countries')

    def post(request,*args, **kwargs):
        country = get_object_or_404(Country, pk=kwargs['pk'])
        try:
            country.delete()
            path = "/crm/countries/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

def area_list(request):
    areas = Area.objects.all()
    context = {
        'areas': areas
    }
    return render(request, 'crm/setting/list-areas.html', context)

class AreaListView(LoginRequiredMixin, generic.ListView):
    model = Area
    context_object_name = 'areas'
    template_name = 'crm/setting/list-areas.html'

class AreaCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_area.html'
    form_class = AreaForm
    success_message = 'Success: Area was created.'
    success_url = reverse_lazy('crm:areas')

class AreaUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Area
    template_name = 'crm/setting/edit_area.html'
    form_class = AreaForm
    success_message = 'Success: Area was updated.'
    success_url = reverse_lazy("crm:areas")

class AreaDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Area
    template_name = 'crm/setting/delete_area.html'
    success_message = 'Success: Area was deleted.'
    success_url = reverse_lazy('crm:areas')

    def post(request,*args, **kwargs):
        area = get_object_or_404(Area, pk=kwargs['pk'])
        try:
            area.delete()
            path = "/crm/areas/"
        except ProtectedError:
            path = "/crm/pages/"

class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'crm/users/list-users.html'
    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            form = User.objects.all().exclude(pk=1)
        else:
            form = User.objects.filter(pk=self.request.user.id)

        context = {'users': form}
        return context

class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/users/create_user.html'
    form_class = ExtendUserCreationForm()
    success_message = 'Success: user was created.'
    success_url = reverse_lazy('crm:users')

    def get(self, request, *args, **kwargs):
        form = ExtendUserCreationForm()

        context = {'form': form}
        return render(self.request, 'crm/users/create_user.html', context)

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            form = ExtendUserCreationForm(self.request.POST)

            if form.is_valid():
                users = User.objects.all().exclude(pk=1)
                companies = Company.objects.all().values()
                allowed_users = companies[0]['allowed_users']
                if allowed_users is None:
                    allowed_users = 0
                if allowed_users != 0:
                    if users.count() < allowed_users:
                        form.save()
                else:
                    form.save()

        else:
            form = ExtendUserCreationForm()

        context = {'form': form}
        return redirect('/crm/users/')

class UserDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = User
    template_name = 'crm/users/delete_user.html'
    success_message = 'Success: user was deleted.'
    success_url = reverse_lazy('crm:users')

    def post(request,*args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        try:
            user.delete()
            path = "/crm/users/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'crm/users/edit_user.html'
    form_class = UserForm
    success_message = 'Success: user was updated.'
    success_url = reverse_lazy("crm:users")

    def get(self, request, **kwargs):
        self.object = User.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'crm/groups/list-groups.html'

class GroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/groups/create_group.html'
    form_class = GroupForm
    success_message = 'Success: group was created.'
    success_url = reverse_lazy('crm:groups')

    def get(self, request, *args, **kwargs):
        form = GroupForm()

        context = {'form': form}
        return render(self.request, 'crm/groups/create_group.html', context)

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            form = GroupForm(self.request.POST)

            if form.is_valid():
                group = form.save()
        else:
            form = GroupForm()

        context = {'form': form}
        return redirect('/crm/groups/')

class GroupDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Group
    template_name = 'crm/groups/delete_group.html'
    success_message = 'Success: group was deleted.'
    success_url = reverse_lazy('crm:groups')

    def post(request,*args, **kwargs):
        groups = get_object_or_404(Group, pk=kwargs['pk'])
        try:
            groups.delete()
            path = "/crm/groups/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'crm/groups/edit_group.html'
    form_class = GroupForm
    success_message = 'Success: group was updated.'
    success_url = reverse_lazy("crm:groups")

class UserPermissionUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    all_permissions = Permission.objects.filter(content_type__app_label='app label',
                                                content_type__model='lower case model name')
    template_name = 'crm/users/edit_user_permission.html'
    form_class = UserPermissions
    success_message = 'Success: user was updated.'
    success_url = reverse_lazy("crm:users")


class GroupPermissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'crm/groups/edit_group_permission.html'
    form_class = GroupPermissions
    success_message = 'Success: group was updated.'
    success_url = reverse_lazy("crm:groups")

def Warehouse_list(request):
    warehouses = Area.objects.all()
    context = {
        'warehouses': warehouses
    }
    return render(request, 'crm/setting/list-warehouses.html', context)

class WarehouseListView(LoginRequiredMixin, generic.ListView):
    model = Warehouse
    context_object_name = 'warehouses'
    template_name = 'crm/setting/list-warehouses.html'

class WarehouseCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_warehouse.html'
    form_class = WarehouseForm
    success_message = 'Success: Warehouse was created.'
    success_url = reverse_lazy('crm:warehouses')

class WarehouseUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Warehouse
    template_name = 'crm/setting/edit_warehouse.html'
    form_class = WarehouseForm
    success_message = 'Success: Warehouse was updated.'
    success_url = reverse_lazy("crm:warehouses")

class WarehouseDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Warehouse
    template_name = 'crm/setting/delete_warehouse.html'
    success_message = 'Success: Warehouse was deleted.'
    success_url = reverse_lazy('crm:warehouses')

    def post(request,*args, **kwargs):
        warehouses = get_object_or_404(Warehouse, pk=kwargs['pk'])
        try:
            warehouses.delete()
            path = "/crm/warehouses/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class WarehouseTypeListView(LoginRequiredMixin, generic.ListView):
    model = WarehouseType
    context_object_name = 'warehousetypes'
    template_name = 'crm/setting/list-warehousetypes.html'

class WarehouseTypeCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_warehousetype.html'
    form_class = WarehouseTypeForm
    success_message = 'Success: Warehouse Type was created.'
    success_url = reverse_lazy('crm:warehousetypes')

class WarehouseTypeUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = WarehouseType
    template_name = 'crm/setting/edit_warehousetype.html'
    form_class = WarehouseTypeForm
    success_message = 'Success: Warehouse Type was updated.'
    success_url = reverse_lazy("crm:warehousetypes")

class WarehouseTypeDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = WarehouseType
    template_name = 'crm/setting/delete_warehousetype.html'
    success_message = 'Success: Warehouse Type was deleted.'
    success_url = reverse_lazy('crm:warehousetypes')

    def post(request,*args, **kwargs):
        warehousetypes = get_object_or_404(WarehouseType, pk=kwargs['pk'])
        try:
            warehousetypes.delete()
            path = "/crm/warehousetypes/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

def city_list(request):
    cities = City.objects.all()
    context = {
        'cities': cities
    }
    return render(request, 'crm/setting/list-cities.html', context)

class CityListView(LoginRequiredMixin, generic.ListView):
    model = City
    context_object_name = 'cities'
    template_name = 'crm/setting/list-cities.html'

class CityCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/setting/create_city.html'
    form_class = CityForm
    success_message = 'Success: City was created.'
    success_url = reverse_lazy('crm:cities')

class CityUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = City
    template_name = 'crm/setting/edit_city.html'
    form_class = CityForm
    success_message = 'Success: City was updated.'
    success_url = reverse_lazy("crm:cities")

class CityDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = City
    template_name = 'crm/setting/delete_city.html'
    success_message = 'Success: City was deleted.'
    success_url = reverse_lazy('crm:cities')

    def post(request,*args, **kwargs):
        cities = get_object_or_404(City, pk=kwargs['pk'])
        try:
            cities.delete()
            path = "/crm/cities/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

def customer_list(request):
    customers = Customer.objects.all().filter(status=1)
    context = {
        'customers': customers
    }
    return render(request, 'crm/customers/crm-customers.html', context)

class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'crm/customers/crm-customers.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Customer.objects.filter(salesman__in=salesmanid).filter(status=1)

        context = {'customers': form}
        return context
class CustomerCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/customers/create_customer.html'
    form_class = CustomerForm
    success_message = 'Success: Customer was created.'
    success_url = reverse_lazy('crm:customers')
    def get_context_data(self, **kwargs):
        form = CustomerForm
        countries = Country.objects.all()
        context = {'form': form, 'countries': countries}
        return context

class CustomerUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Customer
    template_name = 'crm/customers/edit_customer.html'
    form_class = CustomerForm
    success_message = 'Success: Customer was updated.'
    success_url = reverse_lazy("crm:customers")
    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['areas'] = Area.objects.all()
        context['cities'] = City.objects.all()
        customers = Customer.objects.all().filter(pk=self.kwargs['pk']).values()
        context['country_id'] = customers[0]['country_id']
        context['area_id'] = customers[0]['area_id']
        context['city_id'] = customers[0]['city_id']
        context['address'] = customers[0]['address']
        print(customers[0]['area_id'])
        print(customers[0]['city_id'])
        return context

class CustomerDetailView(LoginRequiredMixin, BSModalReadView):
    model = Customer
    template_name = 'crm/customers/detail_customer.html'

class CustomerDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Customer
    template_name = 'crm/customers/delete_customer.html'
    success_message = 'Success: Customer was deleted.'
    success_url = reverse_lazy('crm:customers')

    def post(request,*args, **kwargs):
        customers = get_object_or_404(Customer, pk=kwargs['pk'])
        try:
            customers.delete()
            path = "/crm/customers/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class DoctorListView(LoginRequiredMixin, generic.ListView):
    model = Doctor
    context_object_name = 'doctors'
    template_name = 'crm/doctors/list-doctors.html'

class DoctorCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Doctor
    template_name = 'crm/doctors/create_doctor.html'
    form_class = DoctorForm
    success_message = 'Success: doctor was created.'
    success_url = reverse_lazy('crm:doctors')

    def get_context_data(self, **kwargs):
        context = super(DoctorCreateView, self).get_context_data(**kwargs)
        context['classes'] = Class.objects.all().filter(doctor_c=True)
        mapbox_access_token = 'pk.eyJ1Ijoic2FtZXJkYSIsImEiOiJja2QzeWl1NjYwY2l0MndvY3U2ZnNkdGdyIn0.Y9OXtoHXye02-IGIsvpp5g'
        context['mapbox_access_token'] = mapbox_access_token

        return context

class DoctorUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Doctor
    template_name = 'crm/doctors/edit_doctor.html'
    form_class = DoctorForm
    success_message = 'Success: doctor was updated.'
    success_url = reverse_lazy("crm:doctors")

    def get_context_data(self, **kwargs):
        context = super(DoctorUpdateView, self).get_context_data(**kwargs)
        doctorcat = Doctor.objects.all().filter(pk=self.kwargs['pk']).values()
        context['category_id'] = doctorcat[0]['doctor_category_id']
        context['clases'] = Class.objects.all().filter(doctor_c=True)

        return context

class DoctorDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Doctor
    template_name = 'crm/doctors/delete_doctor.html'
    success_message = 'Success: doctor was deleted.'
    success_url = reverse_lazy('crm:doctors')

    def post(request,*args, **kwargs):
        doctors = get_object_or_404(Doctor, pk=kwargs['pk'])
        try:
            doctors.delete()
            path = "/crm/doctors/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class DoctorApproveView(LoginRequiredMixin, BSModalDeleteView):
    model = Doctor
    template_name = 'crm/doctors/approve_doctor.html'
    success_message = 'Success: doctor has approved.'
    success_url = reverse_lazy('crm:doctors')

    def post(request,*args, **kwargs):
        doctors = Doctor.objects.get(pk=kwargs['pk'])

        doctors.approved = 1
        doctors.save()
        path = "/crm/doctors/"

        return redirect(path)

class ClassListView(LoginRequiredMixin, generic.ListView):
    model = Class
    context_object_name = 'classes'
    template_name = 'crm/classes/list-classes.html'

class ClassCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Class
    template_name = 'crm/classes/create_class.html'
    form_class = ClassForm
    success_message = 'Success: doctor was created.'
    success_url = reverse_lazy('crm:classes')

class ClassUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Class
    template_name = 'crm/classes/edit_class.html'
    form_class = ClassForm
    success_message = 'Success: class was updated.'
    success_url = reverse_lazy("crm:classes")

class ClassDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Class
    template_name = 'crm/classes/delete_class.html'
    success_message = 'Success: class was deleted.'
    success_url = reverse_lazy('crm:classes')

    def post(request,*args, **kwargs):
        classes = get_object_or_404(Class, pk=kwargs['pk'])
        try:
            classes.delete()
            path = "/crm/classes/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class SpecialtyListView(LoginRequiredMixin, generic.ListView):
    model = Specialty
    context_object_name = 'specialties'
    template_name = 'crm/doctor_specialties/list-specialties.html'

class SpecialtyCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Specialty
    template_name = 'crm/doctor_specialties/create_specialty.html'
    form_class = SpecialtyForm
    success_message = 'Success: specialties was created.'
    success_url = reverse_lazy('crm:specialties')

class SpecialtyUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Specialty
    template_name = 'crm/doctor_specialties/edit_specialty.html'
    form_class = SpecialtyForm
    success_message = 'Success: specialties was updated.'
    success_url = reverse_lazy("crm:specialties")

class SpecialtyDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Specialty
    template_name = 'crm/doctor_specialties/delete_specialty.html'
    success_message = 'Success: specialties was deleted.'
    success_url = reverse_lazy('crm:specialties')

    def post(request,*args, **kwargs):
        specialties = get_object_or_404(Specialty, pk=kwargs['pk'])
        try:
            specialties.delete()
            path = "/crm/doctor_specialties/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class PharmacyListView(LoginRequiredMixin, generic.ListView):
    model = Pharmacy
    context_object_name = 'pharmacies'
    template_name = 'crm/pharmacies/list-pharmacies.html'

class PharmacyCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Pharmacy
    template_name = 'crm/pharmacies/create_pharmacy.html'
    form_class = PharmacyForm
    success_message = 'Success: Pharmacy was created.'
    success_url = reverse_lazy('crm:pharmacies')

class PharmacyUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Pharmacy
    template_name = 'crm/pharmacies/edit_pharmacy.html'
    form_class = PharmacyForm
    success_message = 'Success: pharmacy was updated.'
    success_url = reverse_lazy("crm:pharmacies")

class PharmacyDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Pharmacy
    template_name = 'crm/pharmacies/delete_pharmacy.html'
    success_message = 'Success: pharmacy was deleted.'
    success_url = reverse_lazy('crm:pharmacies')

    def post(request,*args, **kwargs):
        pharmacies = get_object_or_404(Pharmacy, pk=kwargs['pk'])
        try:
            pharmacies.delete()
            path = "/crm/pharmacies/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class PharmacyApproveView(LoginRequiredMixin, BSModalDeleteView):
    model = Pharmacy
    template_name = 'crm/pharmacies/approve_pharmacy.html'
    success_message = 'Success: pharmacy has approved.'
    success_url = reverse_lazy('crm:pharmacies')

    def post(request,*args, **kwargs):
        pharmacies = Pharmacy.objects.get(pk=kwargs['pk'])

        pharmacies.approved = 1
        pharmacies.save()
        path = "/crm/pharmacies/"

        return redirect(path)

class PharmacyCategoryListView(LoginRequiredMixin, generic.ListView):
    model = PharmacyCategory
    context_object_name = 'pharmacycategories'
    template_name = 'crm/pharmacy_categories/list-pharmacycategories.html'

class PharmacyCategoryCreateView(LoginRequiredMixin, BSModalCreateView):
    model = PharmacyCategory
    template_name = 'crm/pharmacy_categories/create_pharmacycategory.html'
    form_class = PharmacyCategoryForm
    success_message = 'Success: pharmacy category was created.'
    success_url = reverse_lazy('crm:pharmacycategories')

class PharmacyCategoryUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = PharmacyCategory
    template_name = 'crm/pharmacy_categories/edit_pharmacycategory.html'
    form_class = PharmacyCategoryForm
    success_message = 'Success: pharmacycategory was updated.'
    success_url = reverse_lazy("crm:pharmacycategories")

class PharmacyCategoryDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = PharmacyCategory
    template_name = 'crm/pharmacy_categories/delete_pharmacycategory.html'
    success_message = 'Success: pharmacycategory was deleted.'
    success_url = reverse_lazy('crm:pharmacycategories')

    def post(request,*args, **kwargs):
        pharmacycategories = get_object_or_404(PharmacyCategory, pk=kwargs['pk'])
        try:
            pharmacycategories.delete()
            path = "/crm/pharmacy_categories/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

def ChartOfAccountsListView(request):
    if request.method == "POST":
        number = request.POST.get('number', '')
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        selected = request.POST.get('selected', '')
        user = request.user
        new_child = AccountingChild(name=name, number=number, description=description, user=user)
        new_child.save()
        AccountingParent.objects.get(id=request.POST.get('sub')).accounting_child.add(new_child)
        prot = AccountingType.objects.all()
        accounting_list = AccountingParent.objects.all()
        return render(request, 'crm/accounting/list-chartofaccounts.html', {"prot": prot, 'selected': selected, "accounting_list" : accounting_list })
    prot = AccountingType.objects.all()
    accounting_list = AccountingParent.objects.all()
    return render(request, 'crm/accounting/list-chartofaccounts.html', {"prot": prot, "accounting_list" : accounting_list })

class ChartOfAccountsEditView(LoginRequiredMixin, BSModalUpdateView):
    model = AccountingChild
    template_name = 'crm/accounting/edit_chartofaccount.html'
    form_class = AccountingChildForm
    success_message = 'Success: COA was updated.'
    success_url = reverse_lazy("crm:chartofaccounts")
    def get_context_data(self, **kwargs):
        child_id = self.kwargs['pk']
        context = super(ChartOfAccountsEditView, self).get_context_data(**kwargs)
        parents = AccountingParent.objects.get(accounting_child=child_id)
        context['parent_id'] = parents.id
        accounting_list = AccountingParent.objects.all().filter(accounting_child=child_id)
        context['accounting_list'] = accounting_list
        prot = AccountingType.objects.all().filter(accounting_parent=parents.id)
        context['prot'] = prot
        return context

    def form_valid(self, form):
        child_id = self.kwargs['pk']
        AccountingParent.objects.get(id=self.request.GET.get('oldsub')).accounting_child.remove(child_id)
        AccountingParent.objects.get(id=self.request.POST.get('sub')).accounting_child.add(child_id)
        response = super().form_valid(form)
        return response

class ChartOfAccountsCreateView(LoginRequiredMixin, BSModalCreateView):
    model = AccountingChild
    template_name = 'crm/accounting/create_chartofaccount.html'
    form_class = AccountingChildForm
    success_message = 'Success: COA was updated.'
    success_url = reverse_lazy("crm:chartofaccounts")

    def get_context_data(self, **kwargs):
        child_id = self.request.GET.get('parent')
        context = super(ChartOfAccountsCreateView, self).get_context_data(**kwargs)
        parents = AccountingParent.objects.get(id=child_id)
        context['parent_id'] = parents.id
        accounting_list = AccountingParent.objects.all().filter(id=child_id)
        context['accounting_list'] = accounting_list
        prot = AccountingType.objects.all().filter(accounting_parent=parents.id)
        context['prot'] = prot
        return context

class ChartOfAccountsCreateAllView(LoginRequiredMixin, BSModalCreateView):
    model = AccountingChild
    template_name = 'crm/accounting/create_chartofaccount.html'
    form_class = AccountingChildForm
    success_message = 'Success: COA was updated.'
    success_url = reverse_lazy("crm:chartofaccounts")

    def get_context_data(self, **kwargs):
        context = super(ChartOfAccountsCreateAllView, self).get_context_data(**kwargs)
        prot = AccountingType.objects.all()
        context['prot'] = prot
        return context

class AccountListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'crm.view_account'
    model = Account
    context_object_name = 'accounts'
    template_name = 'crm/accounts/list-accounts.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Account.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Account.objects.filter(salesman__in=salesmanid)

        context = {'accounts': form}
        return context

class AccountCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/accounts/create_account.html'
    form_class = AccountForm
    success_message = 'Success: Account was created.'
    success_url = reverse_lazy('crm:accounts')

class AccountUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Account
    template_name = 'crm/accounts/edit_account.html'
    form_class = AccountForm
    success_message = 'Success: Account was updated.'
    success_url = reverse_lazy("crm:accounts")

class AccountDetailView(LoginRequiredMixin, BSModalReadView):
    model = Account
    template_name = 'crm/accounts/detail_account.html'

class AccountDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Account
    template_name = 'crm/accounts/delete_account.html'
    success_message = 'Success: Account was deleted.'
    success_url = reverse_lazy('crm:accounts')

    def post(request,*args, **kwargs):
        accounts = get_object_or_404(Account, pk=kwargs['pk'])
        try:
            accounts.delete()
            path = "/crm/accounts/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class CalendarListView(LoginRequiredMixin, generic.ListView):
    model = Calender
    context_object_name = 'calendars'
    template_name = 'crm/calendar/list-calendar.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        form = Calender.objects.all()
        events = Events.objects.all()
        users = User.objects.all()

        context = {'calender': form, 'users': users, 'events': events}
        return context

class CalendarVisitListView(LoginRequiredMixin, generic.ListView):
    model = Calender
    context_object_name = 'calendars'
    template_name = 'crm/visits/list-calendar-visit.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        form = Calender.objects.all()
        events = Events.objects.all()
        users = User.objects.all()
        doctorvisits = DoctorVisits.objects.all().filter( added=1).values()
        visit_count = doctorvisits.count()
        print(visit_count)

        context = {'calender': form, 'year_v': '2020', 'month_v': '07', 'day_v': '01', 'visit_count':visit_count, 'users': users, 'events': events}
        return context

class CalendarVisitCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/visits/create_visit.html'
    form_class = VisitForm
    success_message = 'Success: activity was created.'
    success_url = reverse_lazy('crm:calendar_visit')

    def get(self, request, *args, **kwargs):
        form = VisitForm()
        DocV_Arr = []
        daysv = []
        try:
            date_list1 = request.GET.get('arr_value')
            date_list = date_list1.split(",")
        except:
            date_list = ''

        print(date_list)
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            customers = Customer.objects.all().filter(status=1)
            leads = Lead.objects.all()
            opportunities = Opportunity.objects.all()
            salesmanid = ''
            salesmanname = ''
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            salesmanq = salesmanid.values()
            salesmanid = salesmanq[0]['id']
            salesmanname = salesmanq[0]['name']
        i = 0
        doctors = Doctor.objects.all()
        print(request.user)
        for ls in date_list:
            for Docs in doctors:
                try:
                    DocVisit = DoctorVisits.objects.filter(date_p=parse_date(ls), doctor=Docs.pk)
                    print(DocVisit.count())
                    if DocVisit.count() == 0:
                        DoctorVisits.objects.create(date_p=parse_date(ls), doctor=Docs, user=request.user)
                except:
                    pass
            mon = datetime.datetime.strftime(parse_date(ls), '%B')
            day_n = parse_date(ls).day
            day_name = datetime.datetime.strftime(parse_date(ls), '%A')
            daysv.append({'day': str(day_n) +' '+ day_name})
            print('daysv', daysv)
            i = i + 1
        print(i)
        if i == 1:
            doctorvisits = DoctorVisits.objects.all().filter(date_p=date_list[0], added=0).values()
        else:
            doctorvisits = DoctorVisits.objects.all().filter(date_p__in=date_list, added=0).values()

        if doctorvisits.count() > 0:
            docv_dist = doctorvisits.order_by('doctor').values_list('doctor', flat=True).distinct()
            doctors = Doctor.objects.all().filter(pk__in=docv_dist)
        else:
            doctors = Doctor.objects.all()

        classes = Class.objects.all().values()
        context = {'salesmanid': salesmanid, 'salesmanname': salesmanname,
                   'date_list': date_list, 'doctors': doctors, 'classes': classes,
                   'date_list1':date_list1, 'mon': mon, 'daysv': daysv}
        return render(self.request, 'crm/visits/create_visit.html', context)

class CalendarVisitDeleteView(LoginRequiredMixin, CreateView):
    template_name = 'crm/visits/delete_visit.html'
    form_class = ActivityForm
    success_message = 'Success: activity was created.'
    success_url = reverse_lazy('crm:calendar_visit')

    def get(self, request, *args, **kwargs):
        form = ActivityForm()
        doctors_arr = []
        DocV_Arr = []
        daysv = []
        try:
            date_list1 = request.GET.get('arr_value')
            date_list = date_list1.split(",")
        except:
            date_list = ''

        print(date_list)
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            salesmanid = ''
            salesmanname = ''
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            salesmanq = salesmanid.values()
            salesmanid = salesmanq[0]['id']
            salesmanname = salesmanq[0]['name']
        i = 0
        doctors = Doctor.objects.all()
        for ls in date_list:
            mon = datetime.datetime.strftime(parse_date(ls), '%B')
            day_n = parse_date(ls).day
            day_name = datetime.datetime.strftime(parse_date(ls), '%A')
            daysv.append({'day': str(day_n) +' '+ day_name})
            print('daysv', daysv)
            i = i + 1
        print(i)
        if i == 1:
            doctorvisits = DoctorVisits.objects.all().filter(date_p=date_list[0], added=1).values()
            docv_dist = doctorvisits.order_by('doctor').values_list('doctor', flat=True).distinct()
            doctors = Doctor.objects.all().filter(pk__in=docv_dist)
            for Docs in doctors:
                doctorvisits = DoctorVisits.objects.all().filter(doctor=Docs, date_p=date_list[0], added=1).values()
                for DocV in doctorvisits:
                    DocV_Arr.append({'id': DocV['doctor_id'], 'doctors': Docs.__dict__, 'date_p': DocV['date_p'] })
        else:
            doctorvisits = DoctorVisits.objects.all().filter(date_p__in=date_list, added=1).values()
            docv_dist = doctorvisits.order_by('doctor').values_list('doctor', flat=True).distinct()
            doctors = Doctor.objects.all().filter(pk__in=docv_dist)
            for Docs in doctors:
                doctorvisits = DoctorVisits.objects.all().filter(doctor=Docs, date_p__in=date_list, added=1).values()
                for DocV in doctorvisits:
                    DocV_Arr.append({'id': DocV['doctor_id'], 'doctors': Docs.__dict__, 'date_p': DocV['date_p'] })

        print(DocV_Arr)
        context = {'form': form, 'salesmanid': salesmanid, 'salesmanname': salesmanname,
                   'date_list': date_list, 'doctors': doctors, 'doctorvisits': DocV_Arr,
                   'date_list1':date_list1, 'mon': mon, 'daysv': daysv}
        return render(self.request, 'crm/visits/delete_visit.html', context)


    def post(self, request, *args, **kwargs):
        if self.request.POST:
            form = ActivityForm(self.request.POST)

            if form.is_valid():
                group = form.save()
        else:
            form = ActivityForm()

        context = {'form': form}
        return redirect('/crm/calendar_visit/')

class CalendarVisitPrintView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        try:
            date_list = request.GET.get('month')
        except:
            date_list = ''

        mon = int(date_list)
        mon_name = calendar.month_name[mon]
        print(mon)
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            doctor_visits = DoctorVisits.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
                doctor_visits = DoctorVisits.objects.filter(salesman__in=salesmanid)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                doctor_visits = DoctorVisits.objects.all().filter(salesman__in=salesmanid)

        doctorvisits = doctor_visits.filter(date_p__month=mon, added=1).order_by('date_p')
        print(doctorvisits.__dict__)

        companies = Company.objects.all()
        if companies is not None:
            logo = companies
        else:
            logo = '/static/images/logo-light.png'
        context = {'doctorvisits': doctorvisits , 'mon': mon, 'mon_name': mon_name, 'logo': logo}
        return render(self.request, 'crm/visits/print_visit.html', context)

def save_visits(request):
    doctorv_arr=[]
    doctorId = str(request.GET.get('doctor'))
    dataP = request.GET.get('date_p')
    try:
        date_list1 = request.GET.get('arr_value')
        date_list = date_list1.split(",")
    except:
        date_list = ''
    doctors = Doctor.objects.get(pk=doctorId)
    print(doctorId)
    print(dataP)
    doctors_count = DoctorVisits.objects.filter(date_p=dataP,doctor=doctors, user=request.user)
    if doctors_count.count() > 0:
        d_count = False
    else:
        d_count = True
    print(d_count)
    # if d_count:
    #     DoctorVisits.objects.create(date_p=dataP,doctor=doctors, user=request.user)
    doctordates = DoctorDates.objects.get(date_p=dataP, doctor=doctors, user=request.user)
    doctordates.added = 1
    doctordates.save()
    doctorvisits = DoctorVisits.objects.all().order_by('id').filter(date_p=dataP, doctor=doctorId, user=request.user).values().first()
    print(doctorvisits)
    i = 0
    for ls in date_list:
        print(ls)
        i = i + 1
    print(i)
    doctor_count = 1

    doctorv_arr.append({'datetoadd': doctordates.date_p, 'doc_count': doctor_count,'id': doctorvisits['doctor_id'], 'doctor': doctorvisits['doctor_id'], 'date_p': doctorvisits['date_p'], 'user': doctorvisits['user_id'], 'added': doctorvisits['added']})
    print('doctorv_arr', doctorv_arr)
    return JsonResponse(doctorv_arr, safe=False)

def retrieve_visits(request):
    yearV = request.GET.get('yearv')
    monthV = request.GET.get('monthv')
    dayV = request.GET.get('dayv')
    visit_day = 7
    visit_t = 0
    visit_p = 0
    datev = parse_date(str(yearV) + '-' + str(monthV) + '-' + str(dayV))
    print(datev)
    doctors_count = DoctorVisits.objects.filter(date_p=datev, added=1, user=request.user)
    if doctors_count.count() > 0:
        d_count = doctors_count.count()
        visit_p = round( d_count / visit_day * 100)
        visit_t = round( 100 - visit_p)
        print(visit_p)
        print(visit_t)
    else:
        d_count = 0
    print(d_count)
    return JsonResponse({'visits_count': d_count, 'visit_p': visit_p, 'visit_t': visit_t}, safe=False)

def save_dates(request):
    doctorId = request.GET.get('doctor')
    dataP = request.GET.get('date_p')
    date_list1 = dataP
    date_list = date_list1.split(",")
    print(doctorId)
    i = 0
    print(date_list)
    for datv in date_list:
        print(datv)
        datev = parse_date(datv)
        print(datev)
        doctors = Doctor.objects.get(id=doctorId)
        print(doctors.__dict__)
        check_doc_dates = DoctorDates.objects.all().filter(date_p=datev, doctor=doctors, user=request.user)
        if check_doc_dates.count() == 0:
            DoctorDates.objects.create(date_p=datev, doctor=doctors, user=request.user)
        i = i + 1

    i = 0
    for ls in date_list:
        print(ls)
        i = i + 1
    if i == 1:
        firstdate = DoctorDates.objects.all().order_by('id').filter(date_p=date_list[0], doctor=doctors, user=request.user, added = 0).values().first()
    else:
        print('date_list', date_list)
        firstdate = DoctorDates.objects.all().order_by('id').filter(date_p__in=date_list, doctor=doctors, user=request.user, added = 0).values().first()
        print(firstdate)
    return JsonResponse({'dat_count': str(i), 'firstdate': firstdate['date_p']}, safe=False)

def save_visits_true(request):
    doctors = str(request.GET.get('doctor'))
    dataP = str(request.GET.get('date_p'))

    print(doctors)
    print(dataP)
    doctorvisits = DoctorVisits.objects.get(date_p=dataP,doctor=doctors, user=request.user)
    doctorvisits.added = 1
    doctorvisits.save()

    return JsonResponse({'addedv': True}, safe=False)

def delete_visits(request):
    doctors = str(request.GET.get('doctor'))
    dataP = str(request.GET.get('date_p'))
    print(doctors)
    print(dataP)
    doctorvisits = DoctorVisits.objects.get(date_p=dataP,doctor=doctors, user=request.user)
    doctorvisits.added = 0
    doctorvisits.save()
    doctordates = DoctorDates.objects.get(date_p=dataP,doctor=doctors, user=request.user)
    doctordates.added = 0
    doctordates.save()

    return JsonResponse({'addedv': False}, safe=False)

class CompanyListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'crm.view_company'
    model = Company
    context_object_name = 'companies'
    template_name = 'crm/company/list-company.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        form = Company.objects.all()

        context = {'companies': form}
        return context

class CompanyUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Company
    template_name = 'crm/company/edit_company.html'
    form_class = CompanyForm
    success_message = 'Success: Company was updated.'
    success_url = reverse_lazy("crm:company")

class CompanyDetailView(LoginRequiredMixin, BSModalReadView):
    model = Company
    template_name = 'crm/company/detail_company.html'

class BranchListView(LoginRequiredMixin, generic.ListView):
    model = Branch
    context_object_name = 'branches'
    template_name = 'crm/branches/list-branches.html'

class BranchCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/branches/create_branch.html'
    form_class = BranchForm
    success_message = 'Success: Branch was created.'
    success_url = reverse_lazy('crm:branches')

class BranchUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Branch
    template_name = 'crm/branches/edit_branch.html'
    form_class = BranchForm
    success_message = 'Success: Branch was updated.'
    success_url = reverse_lazy("crm:branches")

class BranchDeleteView(BSModalDeleteView):
    model = Branch
    template_name = 'crm/branches/delete_branch.html'
    success_message = 'Success: Branch was deleted.'
    success_url = reverse_lazy('crm:branches')

class ChannelListView(LoginRequiredMixin, generic.ListView):
    model = Channel
    context_object_name = 'channels'
    template_name = 'crm/channels/list-channels.html'

class ChannelCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/channels/create_channel.html'
    form_class = ChannelForm
    success_message = 'Success: Customer was created.'
    success_url = reverse_lazy('crm:channels')

class ChannelUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Channel
    template_name = 'crm/channels/edit_channel.html'
    form_class = ChannelForm
    success_message = 'Success: Channel was updated.'
    success_url = reverse_lazy("crm:channels")

class ChannelDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Channel
    template_name = 'crm/channels/delete_channel.html'
    success_message = 'Success: Channel was deleted.'
    success_url = reverse_lazy('crm:channels')

    def post(request,*args, **kwargs):
        channels = get_object_or_404(Channel, pk=kwargs['pk'])
        try:
            channels.delete()
            path = "/crm/channels/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class SalesmanListView(LoginRequiredMixin, generic.ListView):
    model = Salesman
    context_object_name = 'salesmans'
    template_name = 'crm/salesmans/list-salesmans.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Salesman.objects.all()
        else:
            if salesmanid.count() == 0:
                form = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                form = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        context = {'salesmans': form}
        return context

class SalesmanCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/salesmans/create_salesman.html'
    form_class = SalesmanForm
    success_message = 'Success: Salesman was created.'
    success_url = reverse_lazy('crm:salesmans')


    def form_valid(self, form):
        if self.request.POST and self.request.is_ajax():
            salesmans = Salesman.objects.all()
            companies = Company.objects.all().values()
            allowed_users = companies[0]['allowed_users']
            if allowed_users is None:
                allowed_users = 0
            if allowed_users != 0:
                if salesmans.count() < allowed_users:
                    form.save()
                else:
                    pass
            else:
                form.save()

        return HttpResponseRedirect('/crm/salesmans/')

class SalesmanUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Salesman
    template_name = 'crm/salesmans/edit_salesman.html'
    form_class = SalesmanEditForm
    success_message = 'Success: Salesman was updated.'
    success_url = reverse_lazy("crm:salesmans")

class SalesmanDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Salesman
    template_name = 'crm/salesmans/delete_salesman.html'
    success_message = 'Success: Salesman was deleted.'
    success_url = reverse_lazy('crm:salesmans')

    def post(request,*args, **kwargs):
        salesmans = get_object_or_404(Salesman, pk=kwargs['pk'])
        try:
            salesmans.delete()
            path = "/crm/salesmans/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

def load_areas(request):
    country_id = request.GET.get('country')
    areas = Area.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'crm/dropdownlist/area_dropdown_list_options.html', {'areas': areas})

def load_country_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'crm/dropdownlist/city_dropdown_list_options.html', {'cities': cities})

def load_cities_Json(request):
    cities_arr=[]
    area_id = request.GET.get('area')
    cities = City.objects.filter(area_id=area_id).order_by('name').values()
    for CityV in cities:
        cities_arr.append({'id': CityV['id'], 'name': CityV['name']})
    return JsonResponse(cities_arr, safe=False)

def load_cities(request):
    area_id = request.GET.get('area')
    cities = City.objects.filter(area_id=area_id).order_by('name')
    return render(request, 'crm/dropdownlist/city_dropdown_list_options.html', {'cities': cities})

def load_cities_r(request):
    area_id = request.GET.get('area')
    cities = City.objects.filter(area_id=area_id).order_by('name')
    return render(request, 'crm/dropdownlist/city_r_dropdown_list_options.html', {'cities': cities})

def load_accounts(request):
    channel_id = request.GET.get('channel')
    accounts = Account.objects.filter(channel_id=channel_id).order_by('name')
    return render(request, 'crm/dropdownlist/account_dropdown_list_options.html', {'accounts': accounts})

def load_saleman(request):
    customer_id = request.GET.get('customer')
    customers = Customer.objects.filter(pk=customer_id).order_by('name').values('salesman')
    salesmen = Salesman.objects.filter(pk=customers[0]['salesman']).order_by('name').values('id','name')
    return render(request, 'crm/dropdownlist/salesman_dropdown_list_options.html', {'salesmen': salesmen})

def load_salesorder(request):
    customer_id = request.GET.get('customer')
    salesorders = SalesOrder.objects.filter(customer=customer_id).filter(paid=0).values()

    salesarr = []
    for so in salesorders :
        salesreturnorders = SalesReturnOrder.objects.values('salesorderid').order_by('salesorderid').annotate(
            totalsr=Sum('total')).filter(salesorderid=so['id'])
        totalsr = salesreturnorders.aggregate(Sum('total'))
        try:
            salesretordetotal = totalsr['total__sum']
        except:
            salesretordetotal = 0

        if salesreturnorders.count() > 0:
            salesordetotal = so['total']
            totalv = salesordetotal - salesretordetotal
            if int(totalv) != 0:
                salesarr.append({'id': so['id']})
        else:
            salesarr.append({'id': so['id']})

    return render(request, 'crm/dropdownlist/salesorder_dropdown_list_options.html', {'salesorders': salesarr})

def load_uom(request):
    product_id = request.GET.get('product')
    products = Product.objects.filter(pk=product_id).order_by('name').values('uom')
    uoms = Uom.objects.filter(pk=products[0]['uom']).order_by('name').values('id', 'name')
    return render(request, 'crm/dropdownlist/uom_dropdown_list_options.html', {'uoms': uoms})

def load_payment_terms(request):
    customer_id = request.GET.get('customer')
    customers = Customer.objects.filter(pk=customer_id).order_by('name')
    return render(request, 'crm/dropdownlist/payment_terms_dropdown_list_options.html', {'customers': customers})

def load_salesorders(request):
    salesorder_id = request.GET.get('salesorder')
    salesorders = SalesOrder.objects.values().filter(pk=salesorder_id).order_by('pk')


    return render(request, 'crm/dropdownlist/salesorders_dropdown_list_options.html', {'salesorders': salesorders })

def load_salesorders_salesman(request):
    salesorder_id = request.GET.get('salesorder')
    salesorders = SalesOrder.objects.filter(pk=salesorder_id).order_by('pk')
    return render(request, 'crm/dropdownlist/salesorders_salesman_dropdown_list_options.html', {'salesorders': salesorders })

def load_salesorders_warehouse(request):
    salesorder_id = request.GET.get('salesorder')
    salesorders = SalesOrder.objects.filter(pk=salesorder_id).order_by('pk')
    return render(request, 'crm/dropdownlist/salesorders_warehouse_dropdown_list_options.html', {'salesorders': salesorders })

def load_salesorders_product(request):
    salesorder_id = request.GET.get('salesorder')
    salesorders = SalesProduct.objects.all().filter(salesorder=salesorder_id).order_by('pk')
    salesreturnorders = SalesReturnOrder.objects.all().filter(salesorderid=salesorder_id).values('pk')
    soarr = []
    if salesorders.count() > 0:
        for so in salesorders:
            salesreturnproducts = SalesReturnProduct.objects.all().filter(salesorder__in=salesreturnorders).filter(product=so.product_id)
            salesreturnproductsq = salesreturnproducts.aggregate(Sum('qty'))
            companies = Company.objects.all().values()
            if companies is not None:
                taxv = companies[0]['tax']
            else:
                taxv = 0

            if salesreturnproducts.count() > 0 :
                if salesreturnproductsq['qty__sum'] is not None:
                    if so.qty > salesreturnproductsq['qty__sum']:
                        netqty = so.qty - salesreturnproductsq['qty__sum']
                        if taxv > 0:
                            ntaxv = ((netqty * taxv) /100) * so.price
                        btsubtotal = netqty * so.price
                        subtotal = (netqty * so.price) + ntaxv

                        soarr.append({'salesorder': salesorder_id, 'product_id': so.product_id, 'product_name': so.product.name,
                                      'qty': netqty, 'price': so.price, 'uom_id': so.uom_id,
                                      'uom_name': so.uom.name, 'discount': so.discount, 'subtotal': subtotal, 'bt_total': btsubtotal, 'tax': ntaxv })
            else:
                soarr.append({'salesorder': salesorder_id, 'product_id': so.product_id, 'product_name': so.product.name,
                              'qty': so.qty, 'price': so.price, 'uom_id': so.uom_id,
                              'uom_name': so.uom.name, 'discount': so.discount, 'subtotal': so.subtotal,
                              'bt_total': so.bt_total, 'tax': so.tax})
    return render(request, 'crm/dropdownlist/salesorders_product_dropdown_list_options.html', {'salesorders': soarr })

def load_salesorders_product_count(request):
    salesorder_id = request.GET.get('salesordern')
    salesorders = SalesProduct.objects.filter(salesorder=salesorder_id).order_by('pk')

    salesreturnorders = SalesReturnOrder.objects.all().filter(salesorderid=salesorder_id).values('pk')
    soarr = []
    if salesorders.count() > 0:
        productcounts = salesorders.count()
        for so in salesorders:
            salesreturnproducts = SalesReturnProduct.objects.all().filter(salesorder__in=salesreturnorders).filter(product=so.product_id)
            salesreturnproductsq = salesreturnproducts.aggregate(Sum('qty'))
            if salesreturnproducts.count() > 0 :
                if salesreturnproductsq['qty__sum'] is not None:
                    if so.qty <= salesreturnproductsq['qty__sum']:
                        productcounts = productcounts - 1

    return render(request, 'crm/dropdownlist/salesorders_product_count_dropdown_list_options.html', {'productcount': productcounts })

def check_lead(request):
    opp_id = request.GET.get('pk')
    opportunities = Opportunity.objects.get(pk=opp_id)
    if opportunities.lead.conv_customer_id is None:
        customers = 0
    else:
        customer_id = opportunities.lead.conv_customer_id
        customers = Customer.objects.filter(pk=customer_id)
        customers = customers.count()
    return render(request, 'crm/dropdownlist/check_lead_count.html', {'customers': customers})

def check_sales_status(request):
    sales_id = request.GET.get('pk')
    salesorders = SalesOrder.objects.get(pk=sales_id)
    if salesorders.status is None:
        customers = 0
    elif salesorders.status == 2:
        approved = 1
    return render(request, 'crm/dropdownlist/check_sales_status.html', {'approved': approved})

def load_duedate(request):
    customer_id = request.GET.get('customer')
    customers = Customer.objects.filter(pk=customer_id).order_by('name')
    return render(request, 'crm/dropdownlist/duedate_dropdown_list_options.html', {'customers': customers})

def load_payment_days(request):
    customer_id = request.GET.get('customer')
    customers = Customer.objects.filter(pk=customer_id).order_by('name')
    return render(request, 'crm/dropdownlist/payment_days_dropdown_list_options.html', {'customers': customers })

def load_salesorder_total(request):
    salesorder_id = request.GET.get('salesorder_id')
    salesorders = SalesOrder.objects.filter(pk=salesorder_id).order_by('pk')
    return render(request, 'crm/dropdownlist/salesorder_total_dropdown_list_options.html', {'salesorders': salesorders })

def load_salesreturnorder_total(request):
    salesorder_id = request.GET.get('salesorder_id')
    salesreturnorders = SalesReturnOrder.objects.values('salesorderid').order_by('salesorderid').annotate(totalsr=Sum('total')).filter(salesorderid=salesorder_id)
    totalsr = salesreturnorders.aggregate(Sum('total'))
    try:
        total_sr = totalsr['total__sum']
    except:
        total_sr = 0
    return render(request, 'crm/dropdownlist/salesreturnorder_total_dropdown_list_options.html', {'salesreturnorders': total_sr })

def load_collection_total(request):
    salesorder_id = request.GET.get('salesorder_id')
    collections = Collection.objects.values('salesorder').order_by('salesorder').annotate(totalsr=Sum('amount')).filter(salesorder=salesorder_id)
    totalco = collections.aggregate(Sum('amount'))
    try:
        total_co = totalco['amount__sum']
    except:
        total_co = 0
    return render(request, 'crm/dropdownlist/collection_total_dropdown_list_options.html', {'collections': total_co })

def load_salesorder_net_total(request):
    salesorder_id = request.GET.get('salesorder_id')
    salesorders = SalesOrder.objects.filter(pk=salesorder_id).order_by('pk').values()
    try:
        total_so = salesorders[0]['total']
    except:
        total_so = 0
    if total_so is None:
        total_so = 0

    salesreturnorders = SalesReturnOrder.objects.values('salesorderid').order_by('salesorderid').annotate(totalsr=Sum('total')).filter(salesorderid=salesorder_id)
    totalsr = salesreturnorders.aggregate(Sum('total'))
    try:
        total_sr = totalsr['total__sum']
    except:
        total_sr = 0
    if total_sr is None:
        total_sr = 0

    collections = Collection.objects.values('salesorder').order_by('salesorder').annotate(totalsr=Sum('amount')).filter(salesorder=salesorder_id)
    totalco = collections.aggregate(Sum('amount'))
    try:
        total_co = totalco['amount__sum']
    except:
        total_co = 0
    if total_co is None:
        total_co = 0
    nettotal = total_so - total_sr - total_co

    return render(request, 'crm/dropdownlist/salesorder_nettotal_dropdown_list_options.html', {'salesorders': nettotal })

def load_unitprice(request):
    product_id = request.GET.get('product')
    unit_id = int(request.GET.get('unit'))
    products = Product.objects.filter(pk=product_id).order_by('name')
    return render(request, 'crm/dropdownlist/unitprice_dropdown_list_options.html', {'products': products, 'unit': unit_id })

def load_channels(request):
    channel_id = request.GET.get('channel')
    channels = Channel.objects.filter(channel_id=channel_id).order_by('name')
    return render(request, 'crm/dropdownlist/channel_dropdown_list_options.html', {'channels': channels})

def load_salesmans(request):
    salesman_id = request.GET.get('salesman')
    salesmans = Salesman.objects.filter(salesman_id=salesman_id).order_by('name')
    return render(request, 'crm/dropdownlist/salesman_dropdown_list_options.html', {'salesmans': salesmans})

def dashboard1_view(request):
    return render(request, "dashboard/dashboard1.html")

def dashboard2_view(request):
    currentYear = timezone.now().year
    querysourcetotal = Transactions.objects.values('source').order_by('source') \
        .annotate(total=Sum('total')).filter(created_date__year = currentYear)


    queryavailablestock = Transactions.objects.annotate(totalq=Sum('ctrqty')).values('ctrqty')
    totalqty = queryavailablestock.aggregate(Sum('ctrqty'))

    qproductactual = Transactions.objects.annotate(Sum('ctrqty')).filter(
        Q(source='SalesOrder') | Q(source='SalesReturnOrder') | Q(source='TransferOut') | Q(source='TransferIn'))
    qqproductactual = qproductactual.aggregate(total=Sum('ctrqty'))
    try:
        productactual = qqproductactual['total']
    except:
        productactual = 0
    if productactual == None:
        productactual = 0

    qproductpur = Transactions.objects.annotate(Sum('ctrqty')).filter(
        Q(source='PurchaseOrder') | Q(source='PurchaseReturnOrder'))
    qqproductpur = qproductpur.aggregate(total=Sum('ctrqty'))
    try:
        productpurchase = qqproductpur['total']
    except:
        productpurchase = 0
    if productpurchase == None:
        productpurchase = 0


    netstock = productpurchase - productactual

    ctrqty = netstock

    custcount = Customer.objects.all().count()
    chcount = Channel.objects.all().count()
    citycount = City.objects.all().count()


    financialyears = FinancialYear.objects.all()
    targettransactions = TargetTransactions.objects.all().filter(created_date__year = currentYear)
    today = datetime.date.today()
    months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11', '12']
    current_month1 = months[today.month]
    current_month = int(current_month1)
    for financialyear in financialyears:
        if financialyear.m1 == current_month:
            cmonths= 'm1'
            monthn = '1'
            monthname= 'Jan'
            numberofdays = 31
        elif financialyear.m2 == current_month:
            cmonths= 'm2'
            monthn = '2'
            monthname= 'Feb'
            numberofdays = 28
        elif financialyear.m3 == current_month:
            cmonths= 'm3'
            monthn = '3'
            monthname= 'Mar'
            numberofdays = 31
        elif financialyear.m4 == current_month:
            cmonths= 'm4'
            monthn = '4'
            monthname= 'Apr'
            numberofdays = 30
        elif financialyear.m5 == current_month:
            cmonths = 'm5'
            monthn = '5'
            monthname= 'May'
            numberofdays = 31
        elif financialyear.m6 == current_month:
            cmonths = 'm6'
            monthn = '6'
            monthname= 'Jun'
            numberofdays = 30
        elif financialyear.m7 == current_month:
            cmonths = 'm7'
            monthn = '7'
            monthname= 'Jul'
            numberofdays = 31
        elif financialyear.m8 == current_month:
            cmonths = 'm8'
            monthn = '8'
            monthname= 'Aug'
            numberofdays = 31
        elif financialyear.m9 == current_month:
            cmonths = 'm9'
            monthn = '9'
            monthname= 'Sep'
            numberofdays = 30
        elif financialyear.m10 == current_month:
            cmonths = 'm10'
            monthn = '10'
            monthname= 'Oct'
            numberofdays = 31
        elif financialyear.m11 == current_month:
            cmonths = 'm11'
            monthn = '11'
            monthname= 'Nov'
            numberofdays = 30
        elif financialyear.m12 == current_month:
            cmonths = 'm12'
            monthn = '12'
            monthname= 'Dec'
            numberofdays = 31

    querytotalpurchase = querysourcetotal.filter(source='PurchaseOrder').values('total').filter(created_date__month = int(monthn)).filter(created_date__year=currentYear)
    totalpurchase = querytotalpurchase.aggregate(Sum('total'))

    querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(created_date__month = int(monthn)).filter(created_date__year=currentYear)
    totalsales = querytotalsales.aggregate(Sum('total'))

    querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(created_date__month = int(monthn)).filter(created_date__year=currentYear)
    totalsalesreturn = querytotalsalesreturn.aggregate(Sum('total'))

    querytotalpurchasereturn = querysourcetotal.filter(source='PurchaseReturnOrder').values('total').filter(created_date__month = int(monthn)).filter(created_date__year=currentYear)
    totalpurchasereturn = querytotalpurchasereturn.aggregate(Sum('total'))
    if totalpurchasereturn['total__sum'] is not None:
        netpurchase = totalpurchase['total__sum'] + totalpurchasereturn['total__sum']
    else:
        netpurchase = totalpurchase['total__sum']


    currentday = timezone.now().day
    daysspent = round(currentday / numberofdays * 100)
    querymonthlytarget = targettransactions.annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)

    totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
    totalmonthlytargets = totalmonthlytarget['total__sum']

    querymonthlysales = Transactions.objects.values('source').order_by('source')\
        .annotate(total=Sum('total')).filter(created_date__month=monthn).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
    totalmonthlysaless = querymonthlysales.aggregate(Sum('total'))
    try:
        totalmonthlysaless = round(int(totalmonthlysaless['total__sum']),1)
    except:
        totalmonthlysaless = 0



    # Sales vs Target - Monthly view
    allmonthsales = []

    mc=0
    allmonthsales = []
    while mc < 12 :
        salesmonths = 'm' + str(mc+1)

        monthfinancialyear = financialyears.values(salesmonths)
        queryallmonthsales = Transactions.objects.annotate(month=ExtractMonth('created_date')).values('month').order_by(
            'month').filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthfinancialyear[0][salesmonths]) \
            .annotate(total=Sum('total')).values('month', 'total').filter(created_date__year = currentYear)

        queryallmonthtarget = targettransactions.annotate(total=Sum(F(salesmonths)*F('price'), output_field=IntegerField())).order_by('total')
        totalallmonthtarget = queryallmonthtarget.aggregate(Sum('total'))
        try:
            ee = queryallmonthsales[0]['total']
            if totalallmonthtarget['total__sum'] is not None:
                allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': queryallmonthsales[0]['total'], 'target': totalallmonthtarget['total__sum']})
            else:
                allmonthsales.append(
                    {'month': monthfinancialyear[0][salesmonths], 'sales': queryallmonthsales[0]['total'],
                     'target': 0 })
        except :
            if totalallmonthtarget['total__sum'] is not None:
                allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                      'target': totalallmonthtarget['total__sum']})
            else:
                allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                      'target': 0})
        mc += 1

    querytotalsalescustomer = Transactions.objects.values('customer') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by('-total').filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querymonthlytargetcustomer = targettransactions.values('customer')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('-total')

    querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querytotaltargetchannel = TargetTransactions.objects.values('channel')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('total').filter(created_date__year = currentYear)

    channelcount = int(querytotalsaleschannel.count())
    channelTotal = []
    channelLabel = ''
    channelLabels =[]
    channelsales =[]
    c=0
    while c < channelcount :
        channelLabel1 = Channel.objects.filter(pk=querytotalsaleschannel[c]['channel']).values('name')
        channeltargettotalq = querytotaltargetchannel.filter(channel=querytotalsaleschannel[c]['channel'])
        try:
            temp = querytotaltargetchannel[c]['total']
            channelsales.append(
                {'channel':channelLabel1[0]['name'],
                 'sales':round(int(querytotalsaleschannel[c]['total'])/totalmonthlysaless*100),
                 'salest':round(int(querytotalsaleschannel[c]['total'])),
                 'target': round(int(channeltargettotalq[0]['total'])) - round(
                     int(querytotalsaleschannel[c]['total'])),
                 'targetFull': round(int(querytotaltargetchannel[c]['total']))
                 }
            )
        except:
            channelsales.append(
                {'channel':channelLabel1[0]['name'],
                 'sales':round(int(querytotalsaleschannel[c]['total'])/totalmonthlysaless*100),
                 'salest':round(int(querytotalsaleschannel[c]['total'])),
                 'target': 0
                 }
            )

        c += 1


    querytotalsalescustomer = Transactions.objects.values('customer') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by('-total').filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querymonthlytargetcustomer = targettransactions.values('customer')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('-total')

    querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querytotaltargetarea = TargetTransactions.objects.values('area')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('total').filter(created_date__year = currentYear)

    arealcount = int(querytotalsalesarea.count())
    areaTotal = []
    areaLabel = ''
    areaLabels =[]
    areasales =[]
    c=0
    while c < arealcount :
        areaLabel1 = Area.objects.filter(pk=querytotalsalesarea[c]['area']).values('name')
        areatargettotalq = querytotaltargetarea.filter(area=querytotalsalesarea[c]['area'])
        try:
            temp = querytotaltargetarea[c]['total']
            areasales.append(
                {'area':areaLabel1[0]['name'],
                 'sales':round(int(querytotalsalesarea[c]['total'])/totalmonthlysaless*100,0),
                 'salest':round(int(querytotalsalesarea[c]['total'])),
                 'target': round(int(areatargettotalq[0]['total'])) - round(
                     int(querytotalsalesarea[c]['total'])),
                 'targetFull': round(int(querytotaltargetarea[c]['total']))
                 }
            )
        except:
            areasales.append(
                {'area':areaLabel1[0]['name'],
                 'sales':round(int(querytotalsalesarea[c]['total'])/totalmonthlysaless*100,0),
                 'salest':round(int(querytotalsalesarea[c]['total'])),
                 'target': 0
                 }
            )

        c += 1

    querytotalsalessalesman = Transactions.objects.values('salesman') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by('-total').filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querymonthlytargetsalesman = TargetTransactions.objects.values('salesman')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('-total').filter(created_date__year = currentYear)

    salesmancount = int(querytotalsalessalesman.count())
    salesmanTotal = []
    salesmanLabel = ''
    salesmanLabels =[]
    salesmantargetLabels = []
    salesmantargettotal = []
    s=0
    while s < salesmancount :
        salesmanLabel = Salesman.objects.filter(pk=querytotalsalessalesman[s]['salesman']).values('name')
        salesmantargettotalq = querymonthlytargetsalesman.filter(salesman=querytotalsalessalesman[s]['salesman'])
        if salesmantargettotalq.count() > 0 :
            salesmantargetLabel = Salesman.objects.filter(pk=salesmantargettotalq[0]['salesman']).values('name')
            salesmanTotal.append(
                {
                    'salesman': salesmanLabel[0]['name'],
                    'total': round(int(querytotalsalessalesman[s]['total']), 1),
                    'target': round(int(salesmantargettotalq[0]['total']),1) - round(int(querytotalsalessalesman[s]['total']), 1)
                 }
            )
        else:
            salesmanTotal.append(
                {'salesman': salesmanLabel[0]['name'], 'total': round(int(querytotalsalessalesman[s]['total']), 1),
                 'target': 0})
        s += 1


    querytotalsalescategory = Transactions.objects.values('category') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by('-total').filter(created_date__month=monthn).filter(created_date__year = currentYear)

    querymonthlytargetcategory = TargetTransactions.objects.values('category')\
        .annotate(total=Sum(F(cmonths)*F('price'), output_field=IntegerField())).order_by('-total').filter(created_date__year = currentYear)

    categorycount = int(querytotalsalescategory.count())
    categoryLabel = ''
    categorytargetLabels = []
    categorytargettotal = []
    categorysalesTotal = []
    categorytargettotal = []
    cat=0
    while cat < categorycount :
        categoryLabel = Category.objects.filter(pk=querytotalsalescategory[cat]['category']).values('name')

        categorytargettotalq = querymonthlytargetcategory.filter(category=querytotalsalescategory[cat]['category'])
        if categorytargettotalq.count() > 0 :
            categorytargetLabel = Category.objects.filter(pk=categorytargettotalq[0]['category']).values('name')
            categorysalesTotal.append(
                {'category': categoryLabel[0]['name'], 'sales': round(int(querytotalsalescategory[cat]['total']), 1), 'target': round(int(categorytargettotalq[0]['total']),1) - round(int(querytotalsalescategory[cat]['total']), 1)})
        else:
            categorysalesTotal.append(
                {'category': categoryLabel[0]['name'], 'sales': round(int(querytotalsalescategory[cat]['total']), 1), 'target': 0})
            categorytargetLabels.append('')
            categorytargettotal.append(0)
        cat += 1

    qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
        .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year = currentYear)
    chcount = int(qtotchsm1.count())
    chsm1 = 0
    chsmqs1 = []
    while chsm1 < chcount :
        qtotsm = qtotchsm1.values('salesman','total').order_by('-total').filter(channel_id=qtotchsm1[chsm1]['channel'])
        chsmLabel = Channel.objects.filter(pk=qtotchsm1[chsm1]['channel']).values('name')
        chsmsalesmanLabel = Salesman.objects.filter(pk=qtotsm[0]['salesman']).values('name')
        chsmqs1.append({'channel': chsmLabel[0]['name'], 'salesman':chsmsalesmanLabel[0]['name'], 'total': round(int(qtotsm[0]['total']),1)} )
        chsm1 += 1



    ch1 = 0
    chq1 = []
    while ch1 < chcount :
        qtot = qtotchsm1.values('customer','total').order_by('-total').filter(channel_id=qtotchsm1[ch1]['channel'])
        chLabel = Channel.objects.filter(pk=qtotchsm1[ch1]['channel']).values('name')
        chLabels = Customer.objects.filter(pk=qtot[0]['customer']).values('name')
        chq1.append({'customer': chLabels[0]['name'], 'channel': chLabel[0]['name'], 'total': round(int(qtot[0]['total']),1)} )
        ch1 += 1

    if totalmonthlysaless is None:
        totalmonthlysaless=0
    if totalmonthlytargets is None:
        totalmonthlytargets = 0
    if chcount is None:
        chcount = 0
    targetvsactual = totalmonthlysaless - totalmonthlytargets
    if totalmonthlysaless > totalmonthlytargets:
        totalmonthlysalessperc = round(((((totalmonthlysaless - totalmonthlytargets ) /totalmonthlysaless)) * 100))
        totalmonthlytargetsperc = 0
    else:
        totalmonthlytargetsperc = round(((totalmonthlysaless  / totalmonthlytargets ) *100))
        totalmonthlysalessperc = 0

    qcollections = Collection.objects.all()
    qqcollections = qcollections.values('customer').order_by('customer') \
        .annotate(total=Sum('amount')).filter(created_date__month=monthn).filter(created_date__year = currentYear)
    collectionamount = qqcollections.aggregate(total=Sum('amount'))
    collectamount = collectionamount['total']
    if collectamount is None:
        collectamount = 0

    context = {
        'custcount': custcount,
        'chcount': chcount,
        'citycount': citycount,
        'totalpurchase': totalpurchase,
        'totalsales': totalsales,
        'totalsalesreturn': totalsalesreturn,
        'totalpurchasereturn': totalpurchasereturn,
        'netpurchase': netpurchase,
        'totalqty': totalqty,
        'ctrqty':ctrqty,
        'querymonthlytarget': querymonthlytarget,
        'totalmonthlytargets': totalmonthlytargets,
        'totalmonthlysaless': totalmonthlysaless,
        'targettransactions':targettransactions,
        'targetvsactual': targetvsactual,
        'cmonths': cmonths,
        'monthname': monthname,
        'totalmonthlytargetsperc': totalmonthlytargetsperc,
        'totalmonthlysalessperc': totalmonthlysalessperc,
        'daysspent': daysspent,
        'querytotalsaleschannel': querytotalsaleschannel,
        'querytotalsalessalesman': querytotalsalessalesman,
        'querymonthlytargetsalesman': querymonthlytargetsalesman,
        'channelTotal' : channelTotal,
        'channelcount' : range(0, channelcount),
        'channelLabels': channelLabels,
        'salesmanTotal': salesmanTotal,
        'salesmanLabels': salesmanLabels,
        'salesmantargettotal': salesmantargettotal,
        'salesmantargetLabels': salesmantargetLabels,
        'querytotalsalescategory': querytotalsalescategory,
        'categorytargetLabels': categorytargetLabels,
        'categorytargettotal': categorytargettotal,
        'chsmqs1' : chsmqs1,
        'chq1': chq1,
        'queryallmonthsales': queryallmonthsales,
        'channelsales': channelsales,
        'categorysalesTotal': categorysalesTotal,
        'allmonthsales': allmonthsales,
        'querytotaltargetchannel': querytotaltargetchannel,
        'channelsales': channelsales,
        'areasales': areasales,
        'collectamount': collectamount,

    }
    return render(request, "dashboard/dashboard2.html", context)

def dashboard3_view(request):
    custcount = Customer.objects.all().count()
    chcount = Channel.objects.all().count()
    context = {
        'custcount': custcount,
        'chcount': chcount
    }
    return render(request, "dashboard/dashboard3.html", context)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'crm/categories/list-categories.html'

class CategoryCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/categories/create_category.html'
    form_class = CategoryForm
    success_message = 'Success: Category was created.'
    success_url = reverse_lazy('crm:categories')

class CategoryUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Category
    template_name = 'crm/categories/edit_category.html'
    form_class = CategoryForm
    success_message = 'Success: Category was updated.'
    success_url = reverse_lazy("crm:categories")

class CategoryDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Category
    template_name = 'crm/categories/delete_category.html'
    success_message = 'Success: Category was deleted.'
    success_url = reverse_lazy('crm:categories')

    def post(request,*args, **kwargs):
        categories = get_object_or_404(Category, pk=kwargs['pk'])
        try:
            categories.delete()
            path = "/crm/categories/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'crm/products/list-products.html'

class ProductCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/products/create_product.html'
    form_class = ProductForm
    success_message = 'Success: Product was created.'
    success_url = reverse_lazy('crm:products')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        unitsnames = UnitsName.objects.all().values('unit_1','unit_2')
        context['unit1'] = unitsnames[0]['unit_1']
        context['unit2'] = unitsnames[0]['unit_2']
        return context

class ProductUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Product
    template_name = 'crm/products/edit_product.html'
    form_class = ProductForm
    success_message = 'Success: Product was updated.'
    success_url = reverse_lazy("crm:products")

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        unitsnames = UnitsName.objects.all().values('unit_1','unit_2')
        context['unit1'] = unitsnames[0]['unit_1']
        context['unit2'] = unitsnames[0]['unit_2']
        return context


def Error500View(request):
    path = request.POST.get('next', '/')
    context = {'message': path}
    return render(request, "crm/pages/500.html", context)

class ProductDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Product
    template_name = 'crm/products/delete_product.html'
    success_message = 'Success: Product was deleted.'
    success_url = reverse_lazy('crm:products')

    def post(request,*args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        try:
            product.delete()
            path = "/crm/products/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)



def note_clear_all(request):
    notification_id = request.GET.get('pk')
    userid = request.user.id
    notificationsq = Notification.objects.filter(to_user=userid)
    for note in notificationsq:
        notifications = Notification.objects.get(id=note.pk)
        notifications.read = True
        notifications.save()
    return redirect('/crm/notifications/')

def note_read(request):
    notification_id = request.GET.get('pk')
    note1 = Notification.objects.get(id=notification_id)
    if note1.read:
        note1.read = False
        note1.save()
    else:
        note1.read = True
        note1.save()
    return redirect('/crm/notifications/')

def note_read_top(request):
    notification_id = request.GET.get('pk')
    note1 = Notification.objects.get(id=notification_id)
    if note1.read:
        note1.read = False
        note1.save()
    else:
        note1.read = True
        note1.save()
    return redirect('/crm/notifications/')

def note_status(request):
    user_id = request.user.id
    noteid = request.GET.get('note')
    if int(noteid) == 2: noteid =0
    note_users = User.objects.get(pk=user_id)
    note_users.notification = int(noteid)
    note_users.save()

def tour_status(request):
    user_id = request.user.id
    tourid = request.GET.get('tour')
    if int(tourid) == 2: tourid =0
    tour_users = User.objects.get(pk=user_id)
    tour_users.tour = int(tourid)
    tour_users.save()

def save_calendar(request):
    user_id = request.user.id
    tital = request.GET.get('tital')
    start = request.GET.get('start')
    end = request.GET.get('end')
    classname = request.GET.get('classname')
    Calender.objects.create(source='Calendar', source_id=1,
                                message=tital, from_user=request.user,
                                start=start, end=end, classname=classname, to_user=request.user)

def save_calendar_visit(request):
    user_id = request.user.id
    tital = request.GET.get('tital')
    start = request.GET.get('start')
    end = request.GET.get('end')
    classname = request.GET.get('classname')
    Calender.objects.create(source='Calendar', source_id=1,
                                message=tital, from_user=request.user,
                                start=start, end=end, classname=classname, to_user=request.user)
    return JsonResponse({'add':False})

def create_event(request):
    user_id = request.user.id
    tital = request.GET.get('tital')
    classname = request.GET.get('classname')
    Events.objects.create(title=tital, user=request.user, classname=classname)

def update_event(request):
    user_id = request.user.id
    tital = request.GET.get('tital')
    classname = request.GET.get('classname')
    # Events.objects.update(title=tital, user=request.user, classname=classname)

def dark_status(request):
    user_id = request.user.id
    darkid = request.GET.get('dark')
    if int(darkid) == 2: darkid =0
    dark_users = User.objects.get(pk=user_id)
    dark_users.darktheme = int(darkid)
    dark_users.save()

def theme_color(request):
    user_id = request.user.id
    colorid = request.GET.get('color')
    color_users = User.objects.get(pk=user_id)
    color_users.color = colorid
    color_users.save()


class NotificationListView(LoginRequiredMixin, generic.ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'crm/notifications/list-notifications.html'

    def get_context_data(self, **kwargs):
        notificationid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Notification.objects.all().order_by('read', '-created_date')
        else:
            if notificationid.count() == 0:
                form = Notification.objects.filter(to_user=self.request.user.id).order_by('read', '-created_date')
            elif notificationid.count() > 0:
                form = Notification.objects.filter(Q(to_user__in=notificationid) | Q(to_user=self.request.user.id)).order_by('read', '-created_date')

        context = {'notifications': form}
        return context

class NotificationCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/notifications/create_notification.html'
    form_class = NotificationForm
    success_message = 'Success: Notification was updated.'
    success_url = reverse_lazy("crm:notifications")
    def get_context_data(self, **kwargs):
        context = super(NotificationCreateView, self).get_context_data(**kwargs)
        from_user = User.objects.get(id=self.request.user.id)
        context['fromuser'] = from_user
        return context

class NotificationUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Notification
    template_name = 'crm/notifications/edit_notification.html'
    form_class = NotificationForm
    success_message = 'Success: Notification was updated.'
    success_url = reverse_lazy("crm:notifications")
    def get_context_data(self, **kwargs):
        noteid = self.kwargs['pk']
        context = super(NotificationUpdateView, self).get_context_data(**kwargs)
        from_user = Notification.objects.get(pk=noteid)
        context['fromuser'] = from_user.from_user
        return context


class NotificationReplyView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/notifications/reply_notification.html'
    form_class = NotificationForm
    success_message = 'Success: Notification was updated.'
    success_url = reverse_lazy("crm:notifications")
    def get_context_data(self, **kwargs):
        noteid = self.kwargs['pk']
        context = super(NotificationReplyView, self).get_context_data(**kwargs)
        to_user = Notification.objects.get(pk=noteid)
        context['source'] = to_user.source
        context['fromuser'] = to_user.from_user
        context['touser'] = to_user.to_user
        return context


class NotificationWhatsAppView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        noteid = self.kwargs['pk']
        to_user = Notification.objects.get(pk=noteid)
        salesmans = Salesman.objects.get(user=to_user.to_user)

        whatsapp_login()

        name = to_user.from_user.username
        if to_user.message is not None:
            message = to_user.message
        else:
            message = ""
        if to_user.url is not None:
            url = to_user.url
        else:
            url = ""

        messages = "Task: " + to_user.source  + "\n" +  "From: " + name + "\n" + "Message: " + message + "\n" + "URL: " + url
        send_message_to_unsavaed_contact(salesmans.mobile,messages , 1)
        driver.close()  # Close the Open tab
        driver.quit()
        context = {'Success': True}
        return render(self.request, 'crm/notifications/list-notifications.html', context)

def whatsapp_login():
    global wait, driver, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    driver = webdriver.Chrome(options=chrome_options, executable_path='C:\\chromedriver.exe')
    wait = WebDriverWait(driver, 20)
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB IF DISPLAYED")
    driver.get(Link)
    driver.maximize_window()
    print("QR CODE SCANNED")

def send_message(name,msg,count):
    user_group_xpath = '//span[@title = "{}"]'.format(name)
    for retry in range(3):
        try:
            sleep(3)
            wait.until(EC.presence_of_element_located((By.XPATH, user_group_xpath))).click()
            break
        except Exception:
            print("retry:{} {} not found in your contact list".format(retry,name))
            if retry==2:return
    msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    for index in range(count):
        msg_box.send_keys(msg)
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()
    print("Message send successfully.")

def send_attachment(name, file_name):
    user_group_xpath = '//span[@title = "{}"]'.format(name)
    print("in send_attachment method")
    for retry in range(3):
        try:
            sleep(3)
            wait.until(EC.presence_of_element_located((By.XPATH, user_group_xpath))).click()
            break
        except Exception:
            print("retry:{} {} not found in your contact list".format(retry,name))
            if retry==2:return
    attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
    attachment_box.click()
    attachment = driver.find_element_by_xpath(
        '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    attachment.send_keys(file_name)
    sleep(5)
    send = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send-light"]')))
    send.click()
    print("File send successfully.")

def send_message_to_unsavaed_contact(number,msg,count):
    # Reference : https://faq.whatsapp.com/en/android/26000030/
    print("In send_message_to_unsavaed_contact method")
    params = {'phone': str(number), 'text': str(msg)}
    end = urllib.parse.urlencode(params)
    final_url = Link + 'send?' + end
    print(final_url)
    driver.get(final_url)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@title = "Menu"]')))
    print("Page loaded successfully.")
    for retry in range(3):
        try:
            sleep(5)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[3]/button'))).click()
            break
        except Exception as e:
            print("Fail during click on send button.")
            if retry==2:return
    msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    for index in range(count-1):
        msg_box.send_keys(msg)
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()
    print("Message sent successfully.")

def send_attachment_to_unsavaed_contact(number, file_name):
    print("In send_attachment_to_unsavaed_contact method")
    params = {'phone': str(number)}
    end = urllib.parse.urlencode(params)
    final_url = Link + 'send?' + end
    print(final_url)
    driver.get(final_url)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//div[@title = "Menu"]')))
    print("Page loaded successfully.")
    for retry in range(3):
        try:
            sleep(5)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@title = "Attach"]'))).click()
            break
        except Exception as e:
            print("Fail during click on Attachment button.")
            if retry==2:return
    attachment = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    attachment.send_keys(file_name)
    sleep(5)
    send = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send-light"]')))
    send.click()
    print("File sent successfully.")


class NotificationDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Notification
    template_name = 'crm/notifications/delete_notification.html'
    success_message = 'Success: notification was deleted.'
    success_url = reverse_lazy('crm:notifications')


class VendorListView(LoginRequiredMixin, generic.ListView):
    model = Vendor
    context_object_name = 'vendors'
    template_name = 'crm/vendors/list-vendors.html'

class VendorCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'crm/vendors/create_vendor.html'
    form_class = VendorForm
    success_message = 'Success: Vendor was created.'
    success_url = reverse_lazy('crm:vendors')

class VendorUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Vendor
    template_name = 'crm/vendors/edit_vendor.html'
    form_class = VendorForm
    success_message = 'Success: Vendor was updated.'
    success_url = reverse_lazy("crm:vendors")

class VendorDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Vendor
    template_name = 'crm/vendors/delete_vendor.html'
    success_message = 'Success: Vendor was deleted.'
    success_url = reverse_lazy('crm:vendors')

    def post(request,*args, **kwargs):
        vendors = get_object_or_404(Vendor, pk=kwargs['pk'])
        try:
            vendors.delete()
            path = "/crm/vendors/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class PurchaseOrderCreate(LoginRequiredMixin, CreateView):
    model = PurchaseOrder
    context_object_name = 'purchaseorders'
    fields = ['vendor', 'salesman', 'subject', 'duedate', 'payment_terms']

class PuchaseOrderListView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    context_object_name = 'purchaseorders'
    template_name = 'crm/purchaseorder/list-purchaseorders.html'

class PuchaseOrderInvoiceView(LoginRequiredMixin, UpdateView):
    model = PurchaseOrder
    template_name = 'crm/purchaseorder/purchaseorder_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchaseorder')

    def get_context_data(self, **kwargs):
        poid = self.kwargs['pk']
        vendorid = PurchaseOrder.objects.filter(pk=poid).values()
        vendor_id = vendorid[0]['vendor_id']
        vendors = Vendor.objects.all().filter(pk=vendor_id)
        context = super(PuchaseOrderInvoiceView, self).get_context_data(**kwargs)
        context['purchaseproducts'] = PurchaseOrderProductsFormSet(instance=self.object)
        context['vendors'] = vendors
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class PurchaseProductCreate(LoginRequiredMixin, CreateView):
    model = PurchaseOrder
    template_name = 'crm/purchaseorder/create_purchaseorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchaseorder')

    def get_context_data(self, **kwargs):
        context = super(PurchaseProductCreate, self).get_context_data(**kwargs)
        try:
            maxpoid = int(PurchaseOrder.objects.latest('pk').pk) + 1
        except:
            maxpoid = 1

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['purchaseorder_prefix'] = salesorders[0]['purchase_prefix']
        else:
            context['purchaseorder_prefix'] = 'PO-'

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if self.request.POST:
            context['maxpoid'] = maxpoid
            context['purchaseproducts'] = PurchaseOrderProductsFormSet(self.request.POST, instance=self.object)
            context['purchaseproducts'].full_clean()
            context['unitslist'] = unitslist
        else:
            context['maxpoid'] = maxpoid
            context['purchaseproducts'] = PurchaseOrderProductsFormSet(instance=self.object)
            context['unitslist'] = unitslist
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        purchaseproducts = context['purchaseproducts']
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if purchaseproducts.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, purchaseproducts=purchaseproducts))
        if purchaseproducts.is_valid():
            response = super().form_valid(form)
            purchaseproducts.instance = self.object
            purchaseproducts.save()
        else:
            salesorders = Company.objects.all().values()
            if salesorders is not None:
                context['purchaseorder_prefix'] = salesorders[0]['purchase_prefix']
            else:
                context['purchaseorder_prefix'] = 'PO-'
            maxpoid = int(PurchaseOrder.objects.latest('pk').pk) + 1
            context['maxpoid'] = maxpoid
            context['purchaseproducts'] = PurchaseOrderProductsFormSet()
            context['unitslist'] = unitslist
        return response

class PurchaseOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseOrder
    template_name = 'crm/purchaseorder/edit_purchaseorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchaseorder')

    def get_context_data(self, **kwargs):
        context = super(PurchaseOrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['purchaseproducts'] = PurchaseOrderProductsFormSet(self.request.POST, instance=self.object)
            context['purchaseproducts'].full_clean()
        else:
            context['purchaseproducts'] = PurchaseOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['purchaseproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class PuchaseReturnOrderInvoiceView(LoginRequiredMixin, UpdateView):
    model = PurchaseReturnOrder
    template_name = 'crm/purchaseorder/purchasereturnorder_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchasereturnorder')

    def get_context_data(self, **kwargs):
        poid = self.kwargs['pk']
        vendorid = PurchaseReturnOrder.objects.filter(pk=poid).values()
        vendor_id = vendorid[0]['vendor_id']
        vendors = Vendor.objects.all().filter(pk=vendor_id)
        context = super(PuchaseReturnOrderInvoiceView, self).get_context_data(**kwargs)
        context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet(instance=self.object)
        context['vendors'] = vendors
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class PuchaseReturnOrderListView(LoginRequiredMixin, ListView):
    model = PurchaseReturnOrder
    context_object_name = 'purchasereturnorders'
    template_name = 'crm/purchaseorder/list-purchasereturnorders.html'

class PurchaseReturnProductCreate(LoginRequiredMixin, CreateView):
    model = PurchaseReturnOrder
    template_name = 'crm/purchaseorder/create_purchasereturnorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchasereturnorder')

    def get_context_data(self, **kwargs):
        context = super(PurchaseReturnProductCreate, self).get_context_data(**kwargs)
        try:
            maxpoid = int(PurchaseReturnOrder.objects.latest('pk').pk) + 1
        except:
            maxpoid = 1

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['purchasereturnorder_prefix'] = salesorders[0]['purchase_return_prefix']
        else:
            context['purchasereturnorder_prefix'] = 'PRO-'

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if self.request.POST:
            context['maxpoid'] = maxpoid
            context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet(self.request.POST, instance=self.object)
            context['purchasereturnproducts'].full_clean()
            context['unitslist'] = unitslist
        else:
            context['maxpoid'] = maxpoid
            context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet(instance=self.object)
            context['unitslist'] = unitslist
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        purchasereturnproducts = context['purchasereturnproducts']
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if purchasereturnproducts.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, purchasereturnproducts=purchasereturnproducts))
        if purchasereturnproducts.is_valid():
            response = super().form_valid(form)
            purchasereturnproducts.instance = self.object
            purchasereturnproducts.save()
        else:
            salesorders = Company.objects.all().values()
            if salesorders is not None:
                context['purchasereturnorder_prefix'] = salesorders[0]['purchase_return_prefix']
            else:
                context['purchasereturnorder_prefix'] = 'PRO-'
            maxpoid = int(PurchaseReturnOrder.objects.latest('pk').pk) + 1
            context['maxpoid'] = maxpoid
            context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet()
            context['unitslist'] = unitslist
        return response

class PurchaseReturnOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = PurchaseReturnOrder
    template_name = 'crm/purchaseorder/edit_purchasereturnorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:purchasereturnorder')

    def get_context_data(self, **kwargs):
        context = super(PurchaseReturnOrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet(self.request.POST, instance=self.object)
            context['purchasereturnproducts'].full_clean()
        else:
            context['purchasereturnproducts'] = PurchaseReturnOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['purchasereturnproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class SalesOrderInvoiceView(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'crm/salesorder/salesorder_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:saleseorder')

    def get_context_data(self, **kwargs):
        salesid = self.kwargs['pk']
        customerid = SalesOrder.objects.filter(pk=salesid).values()
        customer_id = customerid[0]['customer_id']
        warehouses = Warehouse.objects.filter(pk=customerid[0]['warehouse_id']).values()
        customers = Customer.objects.all().filter(pk=customer_id)
        context = super(SalesOrderInvoiceView, self).get_context_data(**kwargs)
        context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
        context['customers'] = customers
        context['address'] = warehouses[0]['address']
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class SalesOrderListView(LoginRequiredMixin, ListView):
    model = SalesOrder
    context_object_name = 'salesorders'
    template_name = 'crm/salesorder/list-salesorders.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = SalesOrder.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = SalesOrder.objects.filter(salesman__in=salesmanid)

        context = {'salesorders': form}
        return context

class SalesProductCreate(LoginRequiredMixin, CreateView):
    model = SalesOrder
    template_name = 'crm/salesorder/create_salesorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesorder')

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        context = super(SalesProductCreate, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['customers'] = Customer.objects.all().filter(status=1).values()
        else:
            context['customers'] = Customer.objects.all().values().filter(salesman__in=salesmanid).filter(status=1)

        salesmans = Salesman.objects.filter(user=self.request.user.id).values()
        if salesmans.count() == 1:
            if salesmans[0]['allowed_discount'] is not None:
                context['allowed_discount'] = salesmans[0]['allowed_discount']
            else:
                context['allowed_discount'] = 0
        else:
            context['allowed_discount'] = 0

        try:
            maxsoid = int(SalesOrder.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            context['taxv'] = salesorders[0]['tax']
            context['tax_number'] = salesorders[0]['tax_number']
            context['sales_auto'] = salesorders[0]['sales_auto']
        else:
            context['salesorder_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['sales_auto'] = 0


        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['salesproducts'] = SalesOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        salesproducts = context['salesproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        balanceq = SalesOrder.objects.all().filter(customer=form.instance.customer.id)
        balance = balanceq.values('customer').order_by('customer').annotate(total=Sum('total'))
        totalsalesorder = balance.aggregate(Sum('total'))
        if totalsalesorder['total__sum'] is None:
            totalsalesorderv = 0
        else:
            totalsalesorderv = totalsalesorder['total__sum']

        customers = Customer.objects.all().filter(pk=form.instance.customer.id).values()

        collectionq = Collection.objects.all().filter(customer=form.instance.customer.id)
        collections = collectionq.values('customer').order_by('customer').annotate(total=Sum('amount'))
        totalcollection = collections.aggregate(Sum('total'))
        if totalcollection['total__sum'] is None:
            totalcollectionv = 0
        else:
            totalcollectionv = totalcollection['total__sum']

        if customers[0]['credit_limit'] is None:
            creditlimit = 0
            totalordersv =0
        else:
            creditlimit = customers[0]['credit_limit']
            totalordersv = totalsalesorderv + form.instance.total

        if salesproducts.is_valid() == False or (creditlimit != 0 and totalordersv - totalcollectionv > creditlimit):
            creditlimit = totalordersv - creditlimit - totalcollectionv
            return self.render_to_response(self.get_context_data(form=form, salesproducts=salesproducts, creditlimit=creditlimit, customerid= form.instance.customer.id, duedatev = form.instance.customer.duedate ))

        if salesproducts.is_valid():
            response = super().form_valid(form)
            salesproducts.instance = self.object
            salesproducts.save()
        else:
            context['salesproducts'] = SalesOrderProductsFormSet()
            salesorders = Company.objects.all().values()
            if salesorders is not None:
                context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            else:
                context['salesorder_prefix'] = 'SO-'
            maxsoid = int(SalesOrder.objects.latest('pk').pk) + 1
            context['maxsoid'] = maxsoid
            context['unitslist'] = unitslist

        return response

class SalesOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'crm/salesorder/edit_salesorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesorder')

    def get_context_data(self, **kwargs):
        context = super(SalesOrderUpdateView, self).get_context_data(**kwargs)
        salesorders = Company.objects.all().values()
        if self.request.POST:
            context['salesproducts'] = SalesOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
            context['sales_auto'] = salesorders[0]['sales_auto']
        else:
            context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
            context['sales_auto'] = salesorders[0]['sales_auto']
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class SalesOrderChangeView(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'crm/salesorder/change_salesorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesorder')

    def get_context_data(self, **kwargs):
        context = super(SalesOrderChangeView, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(user=self.request.user.id).values()
        context['salesmanid'] = salesmanid[0]['id']
        context['salesmanname'] = salesmanid[0]['name']

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            context['taxv'] = salesorders[0]['tax']
            context['tax_number'] = salesorders[0]['tax_number']
            context['sales_auto'] = salesorders[0]['sales_auto']
        else:
            context['salesorder_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['sales_auto'] = 0
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        salesorders = SalesOrder.objects.filter(pk=self.kwargs['pk']).values('customer')
        customers = Customer.objects.get(pk=salesorders[0]['customer'])
        context['duedatev'] = customers.duedate
        context['paymentdays'] = customers.payment_days

        if self.request.POST:
            context['unitslist'] = unitslist
            context['salesproducts'] = SalesOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if formset.is_valid() :
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        elif formset.is_valid() == False:
            context['unitslist'] = unitslist
            return super().form_invalid(form)

class ContractInvoiceView(LoginRequiredMixin, UpdateView):
    model = Contract
    template_name = 'crm/contract/contract_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:contract')

    def get_context_data(self, **kwargs):
        contractid = self.kwargs['pk']
        customerid = Contract.objects.filter(pk=contractid).values()
        customer_id = customerid[0]['customer_id']
        customers = Customer.objects.all().filter(pk=customer_id).values()
        context = super(ContractInvoiceView, self).get_context_data(**kwargs)
        context['contractproducts'] = ContractProductsFormSet(instance=self.object)
        context['customers'] = customers
        context['address'] = customers[0]['address']
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    context_object_name = 'contracts'
    template_name = 'crm/contract/list-contracts.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Contract.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Contract.objects.filter(salesman__in=salesmanid)

        context = {'contracts': form}
        return context

class ContractProductCreate(LoginRequiredMixin, CreateView):
    model = Contract
    template_name = 'crm/contract/create_contract.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:contract')

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        context = super(ContractProductCreate, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['customers'] = Customer.objects.all().filter(status=1).values()
        else:
            context['customers'] = Customer.objects.all().values().filter(salesman__in=salesmanid).filter(status=1)

        salesmans = Salesman.objects.filter(user=self.request.user.id).values()
        try:
            maxsoid = int(Contract.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        companies = Company.objects.all().values()
        if companies is not None:
            try:
                context['contract_prefix'] = companies[0]['contract_prefix']
            except:
                context['contract_prefix'] = 'CO-'
        else:
            context['contract_prefix'] = 'CO-'


        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            customerid = self.request.POST.get('customer')
            contracts = Contract.objects.all()
            if contracts.count() > 0:
                context['error'] = "True"
            else:
                context['error'] = "False"

            context['contractproducts'] = ContractProductsFormSet(self.request.POST, instance=self.object)
            context['contractproducts'].full_clean()
        else:
            context['error'] = "False"
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['contractproducts'] = ContractProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        contractproducts = context['contractproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if contractproducts.is_valid() == False :
            return self.render_to_response(self.get_context_data(form=form, contractproducts=contractproducts, customerid= form.instance.customer.id ))

        if contractproducts.is_valid():
            response = super().form_valid(form)
            contractproducts.instance = self.object
            contractproducts.save()
        else:
            context['contractproducts'] = ContractProductsFormSet()
            companies = Company.objects.all().values()
            if companies is not None:
                try:
                    context['contract_prefix'] = companies[0]['contract_prefix']
                except:
                    context['contract_prefix'] = 'CO-'
            else:
                context['contract_prefix'] = 'CO-'
            try:
                maxsoid = int(Contract.objects.latest('pk').pk) + 1
            except:
                maxsoid = 1
            context['maxsoid'] = maxsoid
            context['unitslist'] = unitslist

        return response

class ContractUpdateView(LoginRequiredMixin, UpdateView):
    model = Contract
    template_name = 'crm/contract/edit_contract.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:contract')

    def get_context_data(self, **kwargs):
        context = super(ContractUpdateView, self).get_context_data(**kwargs)
        companies = Company.objects.all().values()
        if self.request.POST:
            context['contractproducts'] = ContractProductsFormSet(self.request.POST, instance=self.object)
            context['contractproducts'].full_clean()
        else:
            context['contractproducts'] = ContractProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['contractproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class ContractChangeView(LoginRequiredMixin, UpdateView):
    model = Contract
    template_name = 'crm/contract/change_contract.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:contract')

    def get_context_data(self, **kwargs):
        context = super(ContractChangeView, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(user=self.request.user.id).values()
        context['salesmanid'] = salesmanid[0]['id']
        context['salesmanname'] = salesmanid[0]['name']

        companies = Company.objects.all().values()
        if companies is not None:
            try:
                context['contract_prefix'] = companies[0]['contract_prefix']
            except:
                context['contract_prefix'] = 'CO-'
        else:
            context['contract_prefix'] = 'CO-'
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        contracts = Contract.objects.filter(pk=self.kwargs['pk'])

        if self.request.POST:
            context['unitslist'] = unitslist
            context['contractproducts'] = ContractProductsFormSet(self.request.POST, instance=self.object)
            context['contractproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['contractproducts'] = ContractProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['contractproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if formset.is_valid() :
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        elif formset.is_valid() == False:
            context['unitslist'] = unitslist
            return super().form_invalid(form)

class ApproveContractView(LoginRequiredMixin, BSModalDeleteView):
    model = Contract
    template_name = 'crm/contract/approve_contract.html'
    success_message = 'Success: Sales Order Approved.'
    success_url = reverse_lazy('crm:contract')

    def post(request,*args, **kwargs):
        contracts = Contract.objects.get(pk=kwargs['pk'])
        contracts.status = 2
        contracts.save()
        for sd in SalesProduct.objects.all().filter(contract=contracts.pk):
            sd.status = 2
            sd.save()
        path = "/crm/contract/"

        return redirect(path)


class AccTransactionsInvoiceView(LoginRequiredMixin, UpdateView):
    model = AccTransactions
    template_name = 'crm/acctransactions/acctransactions_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:saleseorder')

    def get_context_data(self, **kwargs):
        salesid = self.kwargs['pk']
        customerid = AccTransactions.objects.filter(pk=salesid).values()
        customer_id = customerid[0]['customer_id']
        warehouses = Warehouse.objects.filter(pk=customerid[0]['warehouse_id']).values()
        customers = Customer.objects.all().filter(pk=customer_id)
        context = super(AccTransactionsInvoiceView, self).get_context_data(**kwargs)
        context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(instance=self.object)
        context['customers'] = customers
        context['address'] = warehouses[0]['address']
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class AccTransactionsListView(LoginRequiredMixin, ListView):
    model = AccTransactions
    context_object_name = 'acctransactions'
    template_name = 'crm/acctransactions/list-acctransactions.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = AccTransactions.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = AccTransactions.objects.filter(salesman__in=salesmanid)

        context = {'acctransactions': form}
        return context

class AccTransactionsCreate(LoginRequiredMixin, CreateView):
    model = AccTransactions
    template_name = 'crm/acctransactions/create_acctransactions.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:acctransactions')

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        context = super(AccTransactionsCreate, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['customers'] = Customer.objects.all().filter(status=1).values()
        else:
            context['customers'] = Customer.objects.all().values().filter(salesman__in=salesmanid).filter(status=1)

        salesmans = Salesman.objects.filter(user=self.request.user.id).values()
        if salesmans.count() == 1:
            if salesmans[0]['allowed_discount'] is not None:
                context['allowed_discount'] = salesmans[0]['allowed_discount']
            else:
                context['allowed_discount'] = 0
        else:
            context['allowed_discount'] = 0

        try:
            maxsoid = int(AccTransactions.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        companies = Company.objects.all().values()
        if companies is not None:
            context['acctransactions_prefix'] = companies[0]['sales_prefix']
            context['taxv'] = companies[0]['tax']
            context['tax_number'] = companies[0]['tax_number']
            context['sales_auto'] = companies[0]['sales_auto']
        else:
            context['acctransactions_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['sales_auto'] = 0


        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(self.request.POST, instance=self.object)
            context['acctransactionsdetails'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        acctransactionsdetails = context['acctransactionsdetails']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})


        if acctransactionsdetails.is_valid() == False :
            return self.render_to_response(self.get_context_data(form=form, acctransactionsdetails=acctransactionsdetails ))

        if acctransactionsdetails.is_valid():
            response = super().form_valid(form)
            acctransactionsdetails.instance = self.object
            acctransactionsdetails.save()
        else:
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet()
            companies = Company.objects.all().values()
            if companies is not None:
                context['acctransactions_prefix'] = companies[0]['sales_prefix']
            else:
                context['acctransactions_prefix'] = 'SO-'
            maxsoid = int(AccTransactions.objects.latest('pk').pk) + 1
            context['maxsoid'] = maxsoid
            context['unitslist'] = unitslist

        return response

class AccTransactionsUpdateView(LoginRequiredMixin, UpdateView):
    model = AccTransactions
    template_name = 'crm/acctransactions/edit_acctransactions.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:acctransactions')

    def get_context_data(self, **kwargs):
        context = super(AccTransactionsUpdateView, self).get_context_data(**kwargs)
        acctransactions = Company.objects.all().values()
        if self.request.POST:
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(self.request.POST, instance=self.object)
            context['acctransactionsdetails'].full_clean()
            context['sales_auto'] = acctransactions[0]['sales_auto']
        else:
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(instance=self.object)
            context['sales_auto'] = acctransactions[0]['sales_auto']
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['acctransactionsdetails']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class AccTransactionsChangeView(LoginRequiredMixin, UpdateView):
    model = AccTransactions
    template_name = 'crm/acctransactions/change_acctransactions.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:acctransactions')

    def get_context_data(self, **kwargs):
        context = super(AccTransactionsChangeView, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(user=self.request.user.id).values()
        context['salesmanid'] = salesmanid[0]['id']
        context['salesmanname'] = salesmanid[0]['name']

        acctransactions = Company.objects.all().values()
        if acctransactions is not None:
            context['acctransactions_prefix'] = acctransactions[0]['sales_prefix']
            context['taxv'] = acctransactions[0]['tax']
            context['tax_number'] = acctransactions[0]['tax_number']
            context['sales_auto'] = acctransactions[0]['sales_auto']
        else:
            context['acctransactions_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['sales_auto'] = 0
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        acctransactions = AccTransactions.objects.filter(pk=self.kwargs['pk']).values('customer')
        customers = Customer.objects.get(pk=acctransactions[0]['customer'])
        context['duedatev'] = customers.duedate
        context['paymentdays'] = customers.payment_days

        if self.request.POST:
            context['unitslist'] = unitslist
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(self.request.POST, instance=self.object)
            context['acctransactionsdetails'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['acctransactionsdetails'] = AccTransactionsDetailsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['acctransactionsdetails']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if formset.is_valid() :
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        elif formset.is_valid() == False:
            context['unitslist'] = unitslist
            return super().form_invalid(form)


class SalesReturnUpdateView(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'crm/salesorder/create_salesrturn.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesorder')

    def get_context_data(self, **kwargs):
        context = super(SalesReturnUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['salesproducts'] = SalesOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class SalesReturnUpdateView11(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'crm/salesorder/create_salesrturn.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesorder')

    def get_context_data(self, **kwargs):
        context = super(SalesReturnUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['salesproducts'] = SalesOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['salesproducts'] = SalesOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class SalesReturnOrderInvoiceView(LoginRequiredMixin, UpdateView):
    model = SalesReturnOrder
    template_name = 'crm/salesorder/salesreturnorder_invoice.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesreturnorder')

    def get_context_data(self, **kwargs):
        salesid = self.kwargs['pk']
        customerid = SalesReturnOrder.objects.filter(pk=salesid).values()
        customer_id = customerid[0]['customer_id']
        warehouses = Warehouse.objects.filter(pk=customerid[0]['warehouse_id']).values()
        customers = Customer.objects.all().filter(pk=customer_id)
        context = super(SalesReturnOrderInvoiceView, self).get_context_data(**kwargs)
        context['address'] = warehouses[0]['address']
        context['salesreturnproducts'] = SalesReturnOrderProductsFormSet(instance=self.object)
        context['customers'] = customers
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class SalesReturnOrderListView(LoginRequiredMixin, ListView):
    model = SalesReturnOrder
    context_object_name = 'salesreturnorders'
    template_name = 'crm/salesorder/list-salesreturnorders.html'
    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            form = Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        if self.request.user.is_superuser:
            form = SalesReturnOrder.objects.all()
        else:
            form = SalesReturnOrder.objects.filter(salesman__in=salesmanid)

        context = {'salesreturnorders': form}
        return context

def total_a(s):
    stt = 10
    yy = total_a(stt)
    return s

class SalesReturnProductCreate(LoginRequiredMixin, CreateView):
    model = SalesReturnOrder
    template_name = 'crm/salesorder/create_salesreturnorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesreturnorder')

    def get_context_data(self, **kwargs):

        context = super(SalesReturnProductCreate, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if salesmanid.count() == 0:
            salesmanid = Salesman.objects.filter(user=self.request.user.id)
        elif salesmanid.count() > 0:
            salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        if self.request.user.is_superuser:
            context['customers'] = Customer.objects.all().filter(status=1).values()
            context['salesorders'] = SalesOrder.objects.all().order_by('customer').filter(customer__status=1)

        else:
            context['customers'] = Customer.objects.all().values().filter(salesman__in=salesmanid).filter(status=1)
            context['salesorders'] = SalesOrder.objects.all().filter(salesman__in=salesmanid).order_by('customer').filter(customer__status=1)


        try:
            maxsoid = int(SalesReturnOrder.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['salesreturnorder_prefix'] = salesorders[0]['sales_return_prefix']
            context['taxv'] = salesorders[0]['tax']
            context['tax_number'] = salesorders[0]['tax_number']
        else:
            context['salesreturnorder_prefix'] = 'SRO-'
            context['taxv'] = 0
            context['tax_number'] = 0

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['salesreturnproducts'] = SalesReturnOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesreturnproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['maxsoid'] = maxsoid
            context['salesreturnproducts'] = SalesReturnOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        salesreturnproducts = context['salesreturnproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        salesorders = Company.objects.all().values()
        if salesorders is not None:
            salesret_prefix = salesorders[0]['sales_return_prefix']
        else:
            salesret_prefix = 'SRO-'
        try:
            maxsoid = int(SalesReturnOrder.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        salesreturn_number = salesret_prefix + str(maxsoid)
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if salesreturnproducts.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, salesreturnproducts=salesreturnproducts))
        if salesreturnproducts.is_valid():
            response = super().form_valid(form)
            salesreturnproducts.instance = self.object
            salesreturnproducts.save()
        else:
            context['salesreturnorder_prefix'] = salesret_prefix

            context['maxsoid'] = maxsoid
            context['salesreturnproducts'] = SalesReturnOrderProductsFormSet()
            context['unitslist'] = unitslist
        return response

class SalesReturnOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = SalesReturnOrder
    template_name = 'crm/salesorder/edit_salesreturnorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:salesreturnorder')

    def get_context_data(self, **kwargs):
        context = super(SalesReturnOrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['salesreturnproducts'] = SalesReturnOrderProductsFormSet(self.request.POST, instance=self.object)
            context['salesreturnproducts'].full_clean()
        else:
            context['salesreturnproducts'] = SalesReturnOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesreturnproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TransferOrderListView(LoginRequiredMixin, ListView):
    model = TransferOrder
    context_object_name = 'transferorders'
    template_name = 'crm/transferorder/list-transferorders.html'

class TransferProductCreate(LoginRequiredMixin, CreateView):
    model = TransferOrder
    template_name = 'crm/transferorder/create_transferorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:transferorder')

    def get_context_data(self, **kwargs):
        context = super(TransferProductCreate, self).get_context_data(**kwargs)

        try:
            maxtoid = int(TransferOrder.objects.latest('pk').pk) + 1
        except:
            maxtoid = 1

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['transferorder_prefix'] = salesorders[0]['transfer_prefix']
        else:
            context['transferorder_prefix'] = 'TR-'

        context['maxtoid'] = maxtoid
        if self.request.POST:
            context['transferproducts'] = TransferOrderProductsFormSet(self.request.POST, instance=self.object)
            context['transferproducts'].full_clean()
        else:
            context['transferproducts'] = TransferOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        transferproducts = context['transferproducts']
        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['transferorder_prefix'] = salesorders[0]['transfer_prefix']
        else:
            context['transferorder_prefix'] = 'TR-'

        try:
            maxtoid = int(TransferOrder.objects.latest('pk').pk) + 1
        except:
            maxtoid = 1

        if transferproducts.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, transferproducts=transferproducts))
        if transferproducts.is_valid():
            response = super().form_valid(form)
            transferproducts.instance = self.object
            transferproducts.save()
        else:
            context['transferproducts'] = TransferOrderProductsFormSet()
            context['maxtoid'] = maxtoid
        return response

class TransferOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = TransferOrder
    template_name = 'crm/transferorder/edit_transferorder.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:transferorder')

    def get_context_data(self, **kwargs):
        context = super(TransferOrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['transferproducts'] = TransferOrderProductsFormSet(self.request.POST, instance=self.object)
            context['transferproducts'].full_clean()
        else:
            context['transferproducts'] = TransferOrderProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['transferproducts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TargetBildingBlocksListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocks
    context_object_name = 'targetbuildingblocks'
    template_name = 'crm/target/list-targetbuildingblocks.html'

    def get_context_data(self, **kwargs):
        years = int(datetime.date.today().year)
        context = super(TargetBildingBlocksListView, self).get_context_data(**kwargs)
        context['targetbuildingblocks'] = TargetBuildingBlocks.objects.all().filter(year=years)

        return context

class TargetBuildingBlocksCreateView(LoginRequiredMixin, CreateView):

    model = TargetBuildingBlocks
    template_name = 'crm/target/create_targetbuildingblocks.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:targetbuildingblocks')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocks'] = TargetBuildingBlocksProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocks'].full_clean()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksExcetion'].full_clean()
        else:
            context['targetbuildingblocks'] = TargetBuildingBlocksProductsFormSet(instance=self.object)
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblocks = context['targetbuildingblocks']
        targetbuildingblocksExcetion = context['targetbuildingblocksExcetion']
        if targetbuildingblocks.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, targetbuildingblocks=targetbuildingblocks))
        if targetbuildingblocksExcetion.is_valid():
            response = super().form_valid(form)
            targetbuildingblocksExcetion.instance = self.object
            targetbuildingblocksExcetion.save()
        if targetbuildingblocks.is_valid():
            response = super().form_valid(form)
            targetbuildingblocks.instance = self.object
            targetbuildingblocks.save()

        else:
            context['targetbuildingblocks'] = TargetBuildingBlocksProductsFormSet()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet()
        return response

class TargetBuildingBlocksRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        target_id = int(request.GET.get('id'))
        targets = TargetBuildingBlocks.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksProducts.objects.filter(targetbuildingblocks=targets.id)
        for tproduct in targetproducts:
            instance = TargetBuildingBlocksProducts.objects.get(pk= tproduct.id)
            signals.post_save_TargetBuildingBlocksProducts(sender=TargetBuildingBlocksProducts, instance=instance, created=False)
        return redirect('/crm/targetbuildingblocks/')

class TargetBuildingBlocksAccountsRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        target_id = int(request.GET.get('id'))
        targets = TargetBuildingBlocksAccounts.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksAccountsProducts.objects.filter(targetbuildingblocksaccounts=targets.id)
        for tproduct in targetproducts:
            instance = TargetBuildingBlocksAccountsProducts.objects.get(pk= tproduct.id)
            signals.post_save_TargetBuildingBlocksAccounts(sender=TargetBuildingBlocksAccountsProducts, instance=instance, created=False)
        return redirect('/crm/targetbuildingblocksaccounts/')

class TargetBuildingBlocksChannelsRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        target_id = int(request.GET.get('id'))
        targets = TargetBuildingBlocksChannels.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksChannelsProducts.objects.filter(targetbuildingblockschannels=targets.id)
        for tproduct in targetproducts:
            instance = TargetBuildingBlocksChannelsProducts.objects.get(pk= tproduct.id)
            signals.post_save_TargetBuildingBlocksChannels(sender=TargetBuildingBlocksChannelsProducts, instance=instance, created=False)
        return redirect('/crm/targetbuildingblockschannels/')


class TargetBuildingBlocksUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocks
    template_name = 'crm/target/edit_targetbuildingblocks.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:targetbuildingblocks')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocks'] = TargetBuildingBlocksProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocks'].full_clean()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksExcetion'].full_clean()
        else:
            context['targetbuildingblocks'] = TargetBuildingBlocksProductsFormSet(instance=self.object)
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['targetbuildingblocks']
        targetbuildingblocksExcetion = context['targetbuildingblocksExcetion']
        if targetbuildingblocksExcetion.is_valid():
            response = super().form_valid(form)
            targetbuildingblocksExcetion.instance = self.object
            targetbuildingblocksExcetion.save()
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TargetBuildingBlocksAccountsListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocksAccounts
    context_object_name = 'targetbuildingblocksaccounts'
    template_name = 'crm/target/list-targetbuildingblocksaccounts.html'

    def get_context_data(self, **kwargs):
        years = int(datetime.date.today().year)
        context = super(TargetBuildingBlocksAccountsListView, self).get_context_data(**kwargs)
        context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccounts.objects.all().filter(year=years)

        return context



class TargetBuildingBlocksAccountsCreateView(LoginRequiredMixin, CreateView):
    model = TargetBuildingBlocksAccounts
    template_name = 'crm/target/create_targetbuildingblocksaccounts.html'
    fields = ['name','account','customer_size','channel','year']
    success_url = reverse_lazy('crm:targetbuildingblocksaccounts')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksAccountsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksaccounts'].full_clean()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblocksaccounts = context['targetbuildingblocksaccounts']
        if targetbuildingblocksaccounts.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, targetbuildingblocksaccounts=targetbuildingblocksaccounts))
        if targetbuildingblocksaccounts.is_valid():
            response = super().form_valid(form)
            targetbuildingblocksaccounts.instance = self.object
            targetbuildingblocksaccounts.save()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsProductsFormSet()
        return response

class TargetBuildingBlocksAccountsUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocksAccounts
    template_name = 'crm/target/edit_targetbuildingblocksaccounts.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:targetbuildingblocksaccounts')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksAccountsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksaccounts'].full_clean()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['targetbuildingblocksaccounts']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TargetBuildingBlocksChannelsListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocksChannels
    context_object_name = 'targetbuildingblockschannels'
    template_name = 'crm/target/list-targetbuildingblockschannels.html'

    def get_context_data(self, **kwargs):
        years = int(datetime.date.today().year)
        context = super(TargetBuildingBlocksChannelsListView, self).get_context_data(**kwargs)
        context['targetbuildingblockschannels'] = TargetBuildingBlocksChannels.objects.all().filter(year=years)

        return context

class TargetBuildingBlocksChannelsCreateView(LoginRequiredMixin, CreateView):
    model = TargetBuildingBlocksChannels
    template_name = 'crm/target/create_targetbuildingblockschannels.html'
    fields = ['name','customer_size','channel','year']
    success_url = reverse_lazy('crm:targetbuildingblockschannels')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksChannelsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblockschannels'].full_clean()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblockschannels = context['targetbuildingblockschannels']
        if targetbuildingblockschannels.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, targetbuildingblockschannels=targetbuildingblockschannels))
        if targetbuildingblockschannels.is_valid():
            response = super().form_valid(form)
            targetbuildingblockschannels.instance = self.object
            targetbuildingblockschannels.save()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsProductsFormSet()
        return response

class TargetBuildingBlocksChannelsUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocksChannels
    template_name = 'crm/target/edit_targetbuildingblockschannels.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:targetbuildingblockschannels')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksChannelsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsProductsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblockschannels'].full_clean()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['targetbuildingblockschannels']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

def fetch_price(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method=='GET':
        price = product.price
        return HttpResponse(price)

class FinancialYearListView(LoginRequiredMixin, generic.ListView):
    model = FinancialYear
    context_object_name = 'financialyears'
    template_name = 'crm/setting/list-financialyears.html'

class FinancialYearUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = FinancialYear
    template_name = 'crm/setting/edit_financialyears.html'
    form_class = FinancialYearForm
    success_message = 'Success: Area was updated.'
    success_url = reverse_lazy("crm:financialyears")

class ProductUnitsListView(LoginRequiredMixin, generic.ListView):
    model = UnitsName
    context_object_name = 'productunits'
    template_name = 'crm/setting/list-productunits.html'

class ProductUnitsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = UnitsName
    template_name = 'crm/setting/edit_productunits.html'
    form_class = ProductUnitsForm
    success_message = 'Success: Unit was updated.'
    success_url = reverse_lazy("crm:productunits")

# Reports
class SalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channels_id = int(request.GET.get('channel'))
        except:
            channels_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channelar = []
        channels = Channel.objects.all()

        if channels_id != 9898989998 :
            channel_name = channels.filter(pk=channels_id).values('name')
            channelname = channel_name[0]['name']
        else:
            channelname =''

        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = channels.filter(parent_channel_id=channels_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:

            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        totalqty = queryavailablestock.aggregate(qty=Sum('ctrqty'))



        salesorders = SalesOrder.objects.all()



        m=1
        totalmonthlytargets = 0
        totalmonthlytargetsqty = 0
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        tablear = []
        temonth = int(monthn)
        customers = Customer.objects.all().filter(salesman__in=salesmanid)
        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)
        if transactions.count() == 0:
            tablear.append({'month': '', 'salesqty': 0,
                            'salestotal': 0,
                            'targetqty': 0,
                            'targettotal': 0,
                            'achievedqtym': 0,
                            'achievedpercm': 0,
                            'achievedqtythisy': 0,
                            'achievedtotalthisy': 0,
                            'totalmonthlytargets': 0,
                            'totalmonthlytargetsqty': 0,
                            'achievedqtylasty': 0,
                            'achievedtotallasty': 0,
                            'monthint': 0,
                            'collectamount': 0,

                            })
        else:
            while m <= 12 :
                monthss = "m" + str(m)

                querymonthlyqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
                stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
                if stotalmqty['qty__sum'] is None:
                    stotalmqty['qty__sum'] = 0

                querymonthlysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
                stotalmsales = querymonthlysales.aggregate(Sum('total'))
                if stotalmsales['total__sum'] is None:
                    stotalmsales['total__sum'] = 0


                queryyearlyqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
                stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
                if stotalyqty['qty__sum'] is None:
                    stotalyqty['qty__sum'] = 0

                qyearlysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
                stotalysales = qyearlysales.aggregate(Sum('total'))
                if stotalysales['total__sum'] is None:
                    stotalysales['total__sum'] = 0

                queryyearlytarget = targettransactions.annotate(total=Sum(F(monthss) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
                if totalyearlytarget['total__sum'] is None:
                    totalyearlytarget['total__sum'] = 0
                queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
                if totalyearlytargetqty['qty__sum'] is None:
                    totalyearlytargetqty['qty__sum'] = 0

                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0


                if city_id != 9898989998 or areas_id != 9898989998 or channels_id != 9898989998:
                    querymonthlycustomers = transactions.values('customer_id')
                    collections = qcollections.values('customer').order_by('customer') \
                        .annotate(total=Sum('amount')).filter(created_date__month=m).filter(customer_id__in=querymonthlycustomers)
                else:
                    collections = qcollections.values('customer').order_by('customer') \
                        .annotate(total=Sum('amount')).filter(created_date__month=m)

                collectionamount = collections.aggregate(total=Sum('amount'))
                collectamount = collectionamount['total']
                if collectamount is None:
                    collectamount = 0

                querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1)
                totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
                if totalmonthlylastsalesqty['qty__sum'] is None:
                    totalmonthlylastsalesqty['qty__sum'] = 0

                querymonthlylastysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1)
                totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
                if totalmonthlylastysales['total__sum'] is None:
                    totalmonthlylastysales['total__sum'] = 0

                try:
                    achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
                except:
                    achievedqtym = 0
                try:
                    achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
                except:
                    achievedpercm = 0
                try:
                    achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
                except:
                    achievedqtythisy = 0
                try:
                    achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
                except:
                    achievedtotalthisy = 0
                if achievedqtym > 0:
                    try:
                        achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
                    except:
                        achievedqtylasty = 0.0
                else:
                    achievedqtylasty = 0.0


                if achievedpercm > 0:
                    try:
                        achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
                    except:
                        achievedtotallasty = 0.0
                else:
                    achievedtotallasty = 0.0

                mname = calendar.month_name[m]

                if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                    tablear.append({'month': mname, 'salesqty': stotalmqty['qty__sum'],
                                    'salestotal': int(round(stotalmsales['total__sum'])),
                                    'targetqty': totalyearlytargetqty['qty__sum'],
                                    'targettotal': int(round(totalyearlytarget['total__sum'])),
                                    'achievedqtym': achievedqtym,
                                    'achievedpercm': achievedpercm,
                                    'achievedqtythisy': achievedqtythisy,
                                    'achievedtotalthisy': achievedtotalthisy,
                                    'totalmonthlytargets': totalmonthlytargets,
                                    'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                    'achievedqtylasty': achievedqtylasty,
                                    'achievedtotallasty': achievedtotallasty,
                                    'monthint': m,
                                    'collectamount': collectamount,

                                    })

                m += 1


        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'salesorders': salesorders,
            'tablear': tablear,
            'channels': channels,
            'areas': areas,
            'channels_id': channels_id,
            'channelname': channelname,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'temonth': temonth,
        }
        return render(request, 'crm/reports/rep-sales.html', context)

class CommissionRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channels_id = int(request.GET.get('channel'))
        except:
            channels_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channelar = []
        channels = Channel.objects.all()

        if channels_id != 9898989998 :
            channel_name = channels.filter(pk=channels_id).values('name')
            channelname = channel_name[0]['name']
        else:
            channelname =''

        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = channels.filter(parent_channel_id=channels_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:

            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        totalqty = queryavailablestock.aggregate(qty=Sum('ctrqty'))



        salesorders = SalesOrder.objects.all()



        m=1
        totalmonthlytargets = 0
        totalmonthlytargetsqty = 0
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        tablear = []
        temonth = int(monthn)
        customers = Customer.objects.all().filter(salesman__in=salesmanid)
        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        if transactions.count() == 0:
            tablear.append({'month': '', 'salesqty': 0,
                            'salestotal': 0,
                            'targetqty': 0,
                            'targettotal': 0,
                            'achievedqtym': 0,
                            'achievedpercm': 0,
                            'achievedqtythisy': 0,
                            'achievedtotalthisy': 0,
                            'totalmonthlytargets': 0,
                            'totalmonthlytargetsqty': 0,
                            'achievedqtylasty': 0,
                            'achievedtotallasty': 0,
                            'monthint': 0,
                            'collectamount': 0,

                            })
        else:

            while m <= 12 :
                monthss = "m" + str(m)

                querymonthlyqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
                stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
                if stotalmqty['qty__sum'] is None:
                    stotalmqty['qty__sum'] = 0

                querymonthlysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
                stotalmsales = querymonthlysales.aggregate(Sum('total'))
                if stotalmsales['total__sum'] is None:
                    stotalmsales['total__sum'] = 0


                queryyearlyqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
                stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
                if stotalyqty['qty__sum'] is None:
                    stotalyqty['qty__sum'] = 0

                qyearlysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
                stotalysales = qyearlysales.aggregate(Sum('total'))
                if stotalysales['total__sum'] is None:
                    stotalysales['total__sum'] = 0

                queryyearlytarget = targettransactions.annotate(total=Sum(F(monthss) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
                if totalyearlytarget['total__sum'] is None:
                    totalyearlytarget['total__sum'] = 0
                queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
                if totalyearlytargetqty['qty__sum'] is None:
                    totalyearlytargetqty['qty__sum'] = 0

                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0


                if city_id != 9898989998 or areas_id != 9898989998 or channels_id != 9898989998:
                    querymonthlycustomers = transactions.values('customer_id')
                    collections = qcollections.values('customer').order_by('customer') \
                        .annotate(total=Sum('amount')).filter(created_date__month=m).filter(customer_id__in=querymonthlycustomers)
                else:
                    collections = qcollections.values('customer').order_by('customer') \
                        .annotate(total=Sum('amount')).filter(created_date__month=m)

                collectionamount = collections.aggregate(total=Sum('amount'))
                collectamount = collectionamount['total']
                if collectamount is None:
                    collectamount = 0

                querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                    .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1)
                totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
                if totalmonthlylastsalesqty['qty__sum'] is None:
                    totalmonthlylastsalesqty['qty__sum'] = 0

                querymonthlylastysales = transactions.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1)
                totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
                if totalmonthlylastysales['total__sum'] is None:
                    totalmonthlylastysales['total__sum'] = 0

                try:
                    achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
                except:
                    achievedqtym = 0
                try:
                    achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
                except:
                    achievedpercm = 0
                try:
                    achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
                except:
                    achievedqtythisy = 0
                try:
                    achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
                except:
                    achievedtotalthisy = 0
                if achievedqtym > 0:
                    try:
                        achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
                    except:
                        achievedqtylasty = 0.0
                else:
                    achievedqtylasty = 0.0


                if achievedpercm > 0:
                    try:
                        achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
                    except:
                        achievedtotallasty = 0.0
                else:
                    achievedtotallasty = 0.0

                mname = calendar.month_name[m]

                if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                    tablear.append({'month': mname, 'salesqty': stotalmqty['qty__sum'],
                                    'salestotal': stotalmsales['total__sum'],
                                    'targetqty': totalyearlytargetqty['qty__sum'],
                                    'targettotal': totalyearlytarget['total__sum'],
                                    'achievedqtym': achievedqtym,
                                    'achievedpercm': achievedpercm,
                                    'achievedqtythisy': achievedqtythisy,
                                    'achievedtotalthisy': achievedtotalthisy,
                                    'totalmonthlytargets': totalmonthlytargets,
                                    'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                    'achievedqtylasty': achievedqtylasty,
                                    'achievedtotallasty': achievedtotallasty,
                                    'monthint': m,
                                    'collectamount': collectamount,

                                    })
                m += 1


        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'salesorders': salesorders,
            'tablear': tablear,
            'channels': channels,
            'areas': areas,
            'channels_id': channels_id,
            'channelname': channelname,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'temonth': temonth,
        }
        return render(request, 'crm/reports/commission-sales.html', context)

class CatSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']

        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id

        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            customers = Customer.objects.filter(salesman__in=salesmanid)
            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))



        salesorders = SalesOrder.objects.all()


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)
        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        totalmonthlytargetsqty = 0
        totalmonthlytargets = 0
        if channelcount == 0:
            channelear.append({'channel': '', 'salesqty': 0,
                               'salestotal': 0,
                               'targetqty': 0,
                               'targettotal': 0,
                               'targetrmain': 0,
                               'achievedqtym': 0,
                               'achievedpercm': 0,
                               'achievedqtythisy': 0,
                               'achievedtotalthisy': 0,
                               'totalmonthlytargets': 0,
                               'totalmonthlytargetsqty': 0,
                               'achievedqtylasty': 0,
                               'achievedtotallasty': 0,
                               'monthint': 0,
                               'collectamount': 0,

                               })

        for channel in channels :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0

            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlycustomers = customers.filter(channel_id = channel.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act

            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(channel_id = channel.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(channel_id = channel.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'channel': channel.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': int(stotalmsales['total__sum']),
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': int(targetrmain),
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })

        mname = calendar.month_name[thismonth]
        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'categories_id': categories_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,

        }
        return render(request, 'crm/reports/category-sales.html', context)

class AreaSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
            customers = Customer.objects.filter(salesman__in=salesmanid)

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))



        salesorders = SalesOrder.objects.all()


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        totalmonthlytargetsqty = 0
        totalmonthlytargets = 0
        if areacount == 0:
            channelear.append({'area': '', 'salesqty': 0,
                               'salestotal': 0,
                               'targetqty': 0,
                               'targettotal': 0,
                               'targetrmain': 0,
                               'achievedqtym': 0,
                               'achievedpercm': 0,
                               'achievedqtythisy': 0,
                               'achievedtotalthisy': 0,
                               'totalmonthlytargets': 0,
                               'totalmonthlytargetsqty': 0,
                               'achievedqtylasty': 0,
                               'achievedtotallasty': 0,
                               'monthint': 0,
                               'collectamount': 0,

                               })
        for area in areas :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlycustomers = customers.filter(area_id = area.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(area_id = area.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(area_id = area.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'area': area.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': int(stotalmsales['total__sum']),
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': int(targetrmain),
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })

        mname = calendar.month_name[thismonth]
        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,

        }
        return render(request, 'crm/reports/area-sales.html', context)

class CustomerSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()

        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

        if self.request.user.is_superuser is False:
            trans_cust = transactions.order_by().values('customer').distinct().filter(salesman__in=salesmanid)
            customers = Customer.objects.filter(salesman__in=salesmanid).filter(id__in=trans_cust)
        else:
            trans_cust = transactions.order_by().values('customer').distinct()
            customers = Customer.objects.all().filter(id__in=trans_cust)
            salesmanid = Salesman.objects.all()

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        mname = calendar.month_name[thismonth]
        totalmonthlytargetsqty = 0
        totalmonthlytargets = 0
        num_customers = 0

        if customers.count() == 0:
            channelear.append({'customer': '', 'salesqty': 0,
                               'salestotal': 0,
                               'targetqty': 0,
                               'targettotal': 0,
                               'targetrmain': 0,
                               'achievedqtym': 0,
                               'achievedpercm': 0,
                               'achievedqtythisy': 0,
                               'achievedtotalthisy': 0,
                               'totalmonthlytargets': 0,
                               'totalmonthlytargetsqty': 0,
                               'achievedqtylasty': 0,
                               'achievedtotallasty': 0,
                               'monthint': 0,
                               'collectamount': 0,

                               })

        transactions = transactions.order_by('customer').values('customer').filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder'))
        targettransactions = targettransactions.order_by('customer').values('customer')
        qcollections = qcollections.values('customer').order_by('customer')

        for customer in customers :

            querymonthlyqty = transactions.annotate(qty=Sum('ctrqty'),total=Sum('total')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            try:
                stotalmqty = querymonthlyqty[0]['qty']
            except:
                stotalmqty = 0

            try:
                stotalmsales = querymonthlyqty[0]['total']
            except:
                stotalmsales = 0


            queryyearlyqty = transactions.annotate(qty=Sum('ctrqty'), total=Sum('total')).filter(created_date__month__lte=thismonth).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            try:
                stotalyqty = queryyearlyqty[0]['qty']
            except:
                stotalyqty = 0

            try:
                stotalysales = queryyearlyqty[0]['total']
            except:
                stotalysales = 0

            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField()), qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            try:
                totalyearlytarget = queryyearlytarget[0]['total']
            except:
                totalyearlytarget = 0

            try:
                totalyearlytargetqty = queryyearlytarget[0]['qty']
            except:
                totalyearlytargetqty = 0

            mm = 1
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
                try:
                    totalmonthlytarget = querymonthlytarget[0]['total']
                except:
                    totalmonthlytarget = 0
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
                try:
                    totalmonthlytargetqty = querymonthlytargetqty[0]['qty']
                except:
                    totalmonthlytargetqty = 0
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty
                except:
                    totalmonthlytargetsqty = 0
                mm += 1

            collections = qcollections.annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(customer_id=customer.id)
            try:
                collectamount = collections[0]['total']
            except:
                collectamount = 0

            querymonthlylastsalesqty = transactions.annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(created_date__year = currentYear-1).filter(customer_id = customer.id)
            try:
                totalmonthlylastsalesqty = querymonthlylastsalesqty[0]['qty']
            except:
                totalmonthlylastsalesqty = 0

            try:
                totalmonthlylastysales = querymonthlylastsalesqty[0]['total']
            except:
                totalmonthlylastysales = 0

            try:
                achievedqtym = round(stotalmqty / totalyearlytargetqty  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales / totalyearlytarget  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty / totalmonthlylastsalesqty  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales / totalmonthlylastysales  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget - stotalmsales
            mname = calendar.month_name[thismonth]

            if totalyearlytarget != 0 or stotalmsales !=0:
                channelear.append({'customer': customer.name, 'salesqty': stotalmqty,
                                'salestotal': int(stotalmsales),
                                'targetqty': totalyearlytargetqty,
                                'targettotal': totalyearlytarget,
                                'targetrmain': int(targetrmain),
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount':collectamount,

                                })
                num_customers = num_customers + 1
                if stotalmsales != 0:
                    activecustomers = activecustomers + 1

        if num_customers is None or num_customers == 0:
            activecustomersper = 0
        else:
            activecustomersper = round(activecustomers / num_customers * 100)


        context = {
            'channelear': channelear,
            'channels': channels,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return render(request, 'crm/reports/customer-sales.html', context)

class SalesmanSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        salesmans = Salesman.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        totalmonthlytargetsqty = 0
        totalmonthlytargets = 0
        if salesmans.count() == 0:
            channelear.append({'salesman': '', 'salesqty': 0,
                               'salestotal': 0,
                               'targetqty': 0,
                               'targettotal': 0,
                               'targetrmain': 0,
                               'achievedqtym': 0,
                               'achievedpercm': 0,
                               'achievedqtythisy': 0,
                               'achievedtotalthisy': 0,
                               'totalmonthlytargets': 0,
                               'totalmonthlytargetsqty': 0,
                               'achievedqtylasty': 0,
                               'achievedtotallasty': 0,
                               'monthint': 0,
                               'collectamount': 0,

                               })
        for salesman in salesmans :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1

            querymonthlycustomers = customers.filter(salesman_id = salesman.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]


            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'salesman': salesman.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': int(stotalmsales['total__sum']),
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': int(targetrmain),
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        mname = calendar.month_name[thismonth]
        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets

        if num_customers > 0:
            activecustomersper = round(activecustomers / num_customers * 100)
        else:
            activecustomersper = 0

        context = {
            'channelear': channelear,
            'channels': channels,
            'salesmans': salesmans,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return render(request, 'crm/reports/salesman-sales.html', context)

class ProductSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        products = Product.objects.all()
        categories = Category.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)
        totalmonthlytargetsqty = 0
        totalmonthlytargets = 0
        if products.count() == 0:
            channelear.append({'product': '', 'salesqty': 0,
                               'salestotal': 0,
                               'targetqty': 0,
                               'targettotal': 0,
                               'targetrmain': 0,
                               'achievedqtym': 0,
                               'achievedpercm': 0,
                               'achievedqtythisy': 0,
                               'achievedtotalthisy': 0,
                               'totalmonthlytargets': 0,
                               'totalmonthlytargetsqty': 0,
                               'achievedqtylasty': 0,
                               'achievedtotallasty': 0,
                               'monthint': 0,
                               'collectamount': 0,

                               })
        for product in products :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(product_id = product.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(product_id = product.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'product': product.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': int(stotalmsales['total__sum']),
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': int(targetrmain),
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        mname = calendar.month_name[thismonth]
        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets
        if num_customers > 0:
            activecustomersper = round(activecustomers / num_customers * 100)
        else:
            activecustomersper = 0

        context = {
            'channelear': channelear,
            'channels': channels,
            'products': products,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'categories_id':categories_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return render(request, 'crm/reports/product-sales.html', context)

class CollectionRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 365

        from datetime import datetime
        today = datetime.today()
        currentYear = timezone.now().year

        channels = Channel.objects.all()
        qcustomers = Customer.objects.all().filter(payment_terms=2)
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
            else:
                customers = qcustomers
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                customers = qcustomers

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            customers = customers.filter(salesman__in=salesmanid)


        salesorders = SalesOrder.objects.all().filter(payment_terms=2)
        salesreturns = SalesReturnOrder.objects.all().filter(salesorderid__in = salesorders)

        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        currentday = timezone.now()

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all()
        else:
            qcollections = Collection.objects.all().filter(customer_id__in=customers)

        now = datetime.today()
        if month_id != 9898989998 and month_id != 0 and month_id != 365:
            dayslater = timezone.now() + timezone.timedelta(days=month_id)
        elif month_id == 0:
            dayslater = str('2010') + "-01-01"
        elif month_id == 365:
            daysstart = str('2010') + "-01-01"
            dayslater = str(currentYear) + "-12-31"
        else:
            dayslater = str(currentYear) + "-12-31"
            # month_id = (datetime.strptime(dayslater, "%Y-%m-%d") - now).days
        totalsalesorderv = 0
        if customers.count() == 0:
            channelear.append({'customer': '', 'salesman': '', 'totalamount': 0,
                               'amount': 0,
                               'balance': 0,
                               'channel': '',
                               })

        for customer in customers :
            if month_id != 9898989998 and month_id != 0 and month_id != 365:
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(now, dayslater))
                totalsalesorder = qsalesorder.aggregate(Sum('total'))
            elif month_id != 9898989998 and month_id == 0 :
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(dayslater, now))
                totalsalesorder = qsalesorder.aggregate(Sum('total'))
            elif month_id == 365 :
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(daysstart, dayslater))
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
            if netsales != 0:
                channelear.append({'customer': customer.name, 'salesman': customer.salesman, 'totalamount': netsales,
                                'amount': int(collectamount),
                                'balance': int(balance),
                                'channel': customer.channel,

                                   })

        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'month_id': month_id

        }
        return render(request, 'crm/reports/collection-sales.html', context)

class CatTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.filter(user=self.request.user.id).values()

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            targettransactions = targettransactions.filter(salesman=salesmanid[0]['id'])


        salesorders = SalesOrder.objects.all()


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if categories.count() == 0:
            channelear.append({'category': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })

        for category in categories :
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0


            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(total=Sum(F(montht)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id=category.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0



                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(created_date__year=currentYear).filter(category_id=category.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'category': category.name,'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 !=0 and t2 !=0 and t3 !=0 and t4 !=0 and t5 !=0 and t6 !=0 and t7 !=0 and t8 !=0 and t9 !=0 and t10 !=0 and t11 !=0 and t12 !=0 :
                channelear.append({'category': category.name,
                                't1': t1,'t2': t2,'t3': t3,'t4': t4,'t5': t5,'t6': t6,'t7': t7,'t8': t8,'t9': t9,'t10': t10,'t11': t11,'t12': t12,
                                'q1': q1,'q2': q2,'q3': q3,'q4': q4,'q5': q5,'q6': q6,'q7': q7,'q8': q8,'q9': q9,'q10': q10,'q11': q11,'q12': q12,
                                'monthint': thismonth,

                                })


        mname = calendar.month_name[thismonth]

        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/category-target.html', context)

class ChaTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            category_id = int(request.GET.get('category'))
        except:
            category_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Category.objects.all().filter(parent_category=category_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and category_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif category_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=category_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=category_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=category_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=category_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and category_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif category_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if channels.count() == 0:
            channelear.append({'channel': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })
        for channel in channels :
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0


            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(total=Sum(F(montht)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id=channel.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0



                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(created_date__year=currentYear).filter(channel_id=channel.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'channel': channel.name,'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 !=0 and t2 !=0 and t3 !=0 and t4 !=0 and t5 !=0 and t6 !=0 and t7 !=0 and t8 !=0 and t9 !=0 and t10 !=0 and t11 !=0 and t12 !=0 :
                channelear.append({'channel': channel.name,
                                't1': t1,'t2': t2,'t3': t3,'t4': t4,'t5': t5,'t6': t6,'t7': t7,'t8': t8,'t9': t9,'t10': t10,'t11': t11,'t12': t12,
                                'q1': q1,'q2': q2,'q3': q3,'q4': q4,'q5': q5,'q6': q6,'q7': q7,'q8': q8,'q9': q9,'q10': q10,'q11': q11,'q12': q12,
                                'monthint': thismonth,

                                })

        mname = calendar.month_name[thismonth]
        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'category_id': category_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/channel-target.html', context)

class AreaTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)
        qcollections = Collection.objects.all()

        if areas.count() == 0:
            channelear.append({'area': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })
        for area in areas:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(area_id=area.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0

                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(area_id=area.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'area': area.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'area': area.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        mname = calendar.month_name[thismonth]
        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/area-target.html', context)

class CustTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        customers = Customer.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if customers.count() == 0:
            channelear.append({'customer': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })

        for customer in customers:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'customer': customer.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'customer': customer.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        mname = calendar.month_name[thismonth]
        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/customer-target.html', context)

class SalesmanTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        categories = Category.objects.all()
        salesmans = Salesman.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()


        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if salesmans.count() == 0:
            channelear.append({'salesman': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })
        for salesman in salesmans:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(salesman_id=salesman.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(salesman_id=salesman.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'salesman': salesman.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'salesman': salesman.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        mname = calendar.month_name[thismonth]
        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/salesman-target.html', context)

class ProductTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        categories = Category.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(
                    category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id).filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id).filter(
                    city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id).filter(
                    area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(
                    category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                targettransactions = TargetTransactions.objects.all()
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)


        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if products.count() == 0:
            channelear.append({'product': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })

        for product in products:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(product_id=product.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(product_id=product.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'product': product.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'product': product.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        mname = calendar.month_name[thismonth]
        context = {
            'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'categories_id': categories_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'crm/reports/product-target.html', context)

class StorageAnalysisRepRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]

        areas = Area.objects.all()
        products = Product.objects.all()
        cities = City.objects.all()

        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        if areas_id != 9898989998 and city_id == 9898989998:
            transactions = Transactions.objects.all().filter(area_id=areas_id)
            targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            warehouses = Warehouse.objects.all().filter(area_id=areas_id)
        elif city_id != 9898989998 and areas_id == 9898989998:
            transactions = Transactions.objects.all().filter(city_id=city_id)
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            warehouses = Warehouse.objects.all().filter(city_id=city_id)
        elif city_id != 9898989998 and areas_id != 9898989998:
            transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            warehouses = Warehouse.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
        else:
            transactions = Transactions.objects.all()
            targettransactions = TargetTransactions.objects.all()
            warehouses = Warehouse.objects.all()

        catear = []

        totalactual = 0
        totaltarget = 0
        diffperc = 0
        netstock = 0
        reservestock = 0
        msafetystock = 0
        qproducttarget = ''
        warehousecap = 0
        qqproductactual = ''
        qqproductpur = ''
        qqtransferin= ''
        qqtransferout = ''
        msafetys = 0
        qqproducttarget = ''

        for product in products:
            qproduct = products.annotate(total=Sum(F('ti')*F('hi'))).filter(pk=product.id)
            msafetys = qproduct.aggregate(Sum('total'))
            try:
                msafetystock = msafetys['total__sum']
            except:
                msafetystock = 0
            if msafetystock == None:
                msafetystock = 0

            qproduct = products.values('monthly_safety_stock').filter(pk=product.id)
            try:
                sstock = qproduct[0]['monthly_safety_stock']
            except:
                sstock = 0
            if sstock == None:
                sstock = 0

            qproductactual = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder'))
            qqproductactual = qproductactual.aggregate(total = Sum('ctrqty'))
            try:
                productactual = qqproductactual['total']
            except:
                productactual = 0
            if productactual == None:
                productactual = 0

            qproductpur = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(
                Q(source='PurchaseOrder') | Q(source='PurchaseReturnOrder'))
            qqproductpur = qproductpur.aggregate(total=Sum('ctrqty'))
            try:
                productpurchase = qqproductpur['total']
            except:
                productpurchase = 0
            if productpurchase == None:
                productpurchase = 0

            qtransferin = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(source='TransferIn').filter(created_date__year=currentYear)
            qqtransferin = qtransferin.aggregate(total=Sum('ctrqty'))
            try:
                transferin = qqtransferin['total']
            except:
                transferin = 0
            if transferin == None:
                transferin = 0

            qtransferout = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(source='TransferOut').filter(created_date__year=currentYear)
            qqtransferout = qtransferout.aggregate(total=Sum('ctrqty'))
            try:
                qtransferout = qqtransferout['total']
            except:
                qtransferout = 0
            if qtransferout == None:
                qtransferout = 0

            netstock = productpurchase - productactual + qtransferout + transferin

            if productactual != 0 and msafetystock != 0:
                totalactual = totalactual + round(netstock /  msafetystock)


            qsproduct = products.filter(pk=product.id).values('monthly_safety_stock')
            msafetys = qsproduct[0]['monthly_safety_stock']
            if msafetys == None:
                msafetys = 0


            qproducttarget = targettransactions.annotate(total=Sum(F('m1')+F('m2')+F('m3')+F('m4')+F('m5')+F('m6')+F('m7')+F('m8')+F('m9')+F('m10')+F('m11')+F('m12'), output_field=IntegerField()))\
                .filter(product_id=product.id).filter(created_date__year=currentYear)
            qqproducttarget = qproducttarget.aggregate(Sum('total'))

            if qqproducttarget['total__sum'] != None:
                producttarget = qqproducttarget['total__sum']
                avgproducttarget = qqproducttarget['total__sum'] / 12
            else:
                producttarget = 0
                avgproducttarget = 0


            if msafetys == 0:
                msafetys = 1
            if msafetystock == 0:
                msafetystock = 1
            if producttarget != 0:
                totaltarget = totaltarget +  producttarget / 12 * msafetys / msafetystock
            if avgproducttarget != 0:
                reservestock = avgproducttarget * sstock
            else:
                reservestock = 0
            catear.append({'product': product.name, 'diff': round(netstock)-round(reservestock), 'reservestock': round(reservestock), 'available': netstock})

        qwarehouse = warehouses.annotate(Sum('capacity')).values('capacity')
        warhouseqty = qwarehouse.aggregate(qty=Sum('capacity'))
        if warhouseqty['qty'] != None:
            warehousecap = warhouseqty['qty']
        else:
            warehousecap = 0


        if netstock > 0 and reservestock > 0:
            diffperc = round((round(warehousecap) - round(totaltarget)) / warehousecap * 100,1)


        context = {
            'areas': areas,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'catear': catear,
            'qtranswarehouse': targettransactions,
            'TIHITotal': msafetystock,
            'targetqty': qproducttarget,
            'recom': totaltarget,
            'ssize': warehousecap,
            'occupied': totalactual,
            'recommend': round(totaltarget,1),
            'qqproductactual': qqproductactual,
            'qqproductpur': qqproductpur,
            'qqtransferin': qqtransferin,
            'qqtransferout' : qqtransferout,
            'msafetys': msafetys,
            'qqproducttarget': qqproducttarget,
            'notes': diffperc,


        }
        return render(request, 'crm/reports/storageanalysis-rep.html', context)

class CollectionInvoiceView(LoginRequiredMixin, BSModalUpdateView):
    model = Collection
    template_name = 'crm/collections/collection_invoice.html'
    form_class = CollectionForm
    success_url = reverse_lazy('crm:collections')
    def get_context_data(self, **kwargs):
        coid = self.kwargs['pk']
        collections = Collection.objects.filter(pk=coid).values()
        total = num2words(collections[0]['amount'])
        context = super(CollectionInvoiceView, self).get_context_data(**kwargs)
        context['total'] = total
        companies = Company.objects.all()
        if companies is not None:
            context['logo'] = companies
        else:
            context['logo'] = '/static/images/logo-light.png'
        return context

class CollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    context_object_name = 'collections'
    template_name = 'crm/collections/list-collections.html'

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        if self.request.user.is_superuser:
            form = Collection.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            customers = Customer.objects.all().filter(salesman__in=salesmanid)

            form = Collection.objects.filter(customer_id__in=customers)

        context = {'collections': form}
        return context

class CollectionCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Collection
    template_name = 'crm/collections/create_collection.html'
    form_class = CollectionForm
    success_message = 'Success: Collection was created.'
    success_url = reverse_lazy("crm:collections")

    def get_context_data(self, **kwargs):
        context = super(CollectionCreateView, self).get_context_data(**kwargs)

        salesorders = SalesOrder.objects.all()

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        if self.request.user.is_superuser:
            customers = Customer.objects.filter(payment_terms=2).filter(status=1)
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            customers = Customer.objects.all().filter(payment_terms=2).filter(salesman__in=salesmanid).filter(status=1)
        context['salesorders'] = salesorders
        context['customers'] = customers
        return context


class CollectionUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Collection
    template_name = 'crm/collections/edit_collection.html'
    form_class = CollectionForm
    success_message = 'Success: Collection was updated.'
    success_url = reverse_lazy("crm:collections")

class CollectionDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Collection
    template_name = 'crm/collections/delete_collection.html'
    success_message = 'Success: Collection was deleted.'
    success_url = reverse_lazy('crm:collections')

class CurrencyListView(LoginRequiredMixin, generic.ListView):
    model = Currency
    context_object_name = 'currencies'
    template_name = 'crm/currencies/list-currencies.html'

class CurrencyCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Currency
    template_name = 'crm/currencies/create_currency.html'
    form_class = CurrencyForm
    success_message = 'Success: Currency was created.'
    success_url = reverse_lazy("crm:currencies")

class CurrencyUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Currency
    template_name = 'crm/currencies/edit_currency.html'
    form_class = CurrencyForm
    success_message = 'Success: currency was updated.'
    success_url = reverse_lazy("crm:currencies")

class CurrencyDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Currency
    template_name = 'crm/currencies/delete_currency.html'
    success_message = 'Success: currency was deleted.'
    success_url = reverse_lazy('crm:currencies')

    def post(request,*args, **kwargs):
        currencies = get_object_or_404(Currency, pk=kwargs['pk'])
        try:
            currencies.delete()
            path = "/crm/currencies/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class LeadListView(LoginRequiredMixin, ListView):
    permission_required = 'crm.view_lead'
    model = Lead
    context_object_name = 'leads'
    template_name = 'crm/lead/list-leads.html'

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        if self.request.user.is_superuser:
            form = Lead.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Lead.objects.all().filter(salesman__in=salesmanid)
        opparr = []
        if form.count() == 0:
            opparr.append({'status': '', 'totalsum': 0})

        for p in form.values('status').order_by('status').annotate(total=Sum('amount')):
            try:
                totalamount = p['total']
            except:
                totalamount = 0

            if totalamount is None:
                totalamount = 0

            if totalamount > 0:
                opparr.append({'status': p['status'], 'totalsum': round(p['total'], 0)})

        currentY = timezone.now().year
        generalq = form.annotate(total=Count('status')).filter(created_date__year=currentY)

        totalactive = generalq.count()

        wonopp = generalq.filter(status='16')
        totalwon = wonopp.count()

        lostopp = generalq.filter(status='18')
        totallost = lostopp.count()

        context = {'leads': form, 'opparr': opparr, 'totalactive': totalactive, 'totalwon': totalwon, 'totallost': totallost}
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/lead/create_lead.html'
    form_class = LeadForm
    success_message = 'Success: Lead was created.'
    success_url = reverse_lazy('crm:leads')

def json_example(request):
    return Response({"key":"val"} )

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = 'crm/lead/edit_lead.html'
    form_class = LeadForm
    success_message = 'Success: lead was updated.'
    success_url = reverse_lazy("crm:leads")


class LeadDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Lead
    template_name = 'crm/lead/delete_lead.html'
    success_message = 'Success: lead was deleted.'
    success_url = reverse_lazy('crm:leads')

    def post(request,*args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs['pk'])
        try:
            lead.delete()
            path = "/crm/leads/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)

class LeadConvertView(LoginRequiredMixin, BSModalDeleteView):
    model = Lead
    template_name = 'crm/lead/convert_lead.html'
    success_message = 'Success: lead was converted.'
    success_url = reverse_lazy('crm:leads')

    def post(request,*args, **kwargs):
        lead = Lead.objects.get(pk=kwargs['pk'])
        Lead_Convert(kwargs['pk'])
        try:
            channels = Channel.objects.get(name='Converted')
        except:
            channels = Channel.objects.create(name='Converted', description='This Channel have been created for the converted leads purpose')
        try:
            customers = Customer.objects.create(name=lead.name, description=lead.description, salesman=lead.salesman
                                    , country=lead.country, area=lead.area, city=lead.city,
                                    address=lead.address, channel=channels, customer_size=1, payment_terms=1)
            lead.converted = 1
            lead.conv_customer_id = customers.pk
            lead.conv_date = datetime.date.today()
            lead.save()
            context = {'message':'Leads has Successfully converted to customer'}
            path = "/crm/leads/"
        except ProtectedError:
            context = {'message':'Leads not converted'}
            path = "/crm/pages/"


        return redirect(path)

class ApproveSalesOrderView(LoginRequiredMixin, BSModalDeleteView):
    model = SalesOrder
    template_name = 'crm/salesorder/approve_salesorder.html'
    success_message = 'Success: Sales Order Approved.'
    success_url = reverse_lazy('crm:salesorder')

    def post(request,*args, **kwargs):
        salesorders = SalesOrder.objects.get(pk=kwargs['pk'])
        salesorders.status = 2
        salesorders.save()
        for sd in SalesProduct.objects.all().filter(salesorder=salesorders.pk):
            sd.status = 2
            sd.save()
        path = "/crm/salesorder/"

        return redirect(path)


class OpportunityConvertView(LoginRequiredMixin, BSModalDeleteView):
    model = Opportunity
    template_name = 'crm/opportunity/convert_opportunity.html'
    success_message = 'Success: opportunity was converted.'
    success_url = reverse_lazy('crm:opportunities')

    def post(request,*args, **kwargs):
        opportunity = Opportunity.objects.get(pk=kwargs['pk'])
        opportunityproducts = OpportunityProduct.objects.filter(opportunity_id=kwargs['pk'])
        warehouses = Warehouse.objects.all().first()
        try:
            maxsoid = int(SalesOrder.objects.latest('pk').pk) + 1

            companies = Company.objects.all().values()
            if companies is not None:
                prefix = companies[0]['sales_prefix']
                taxv = companies[0]['tax']
                tax_numberv = companies[0]['tax_number']
            else:
                prefix = 'SO-'
                taxv = 0
                tax_numberv = 0
            if opportunity.source == 1:
                leads = Lead.objects.get(pk=opportunity.lead_id)
                customers = Customer.objects.get(pk=leads.conv_customer_id)

            elif opportunity.source == 2:
                customers = Customer.objects.get(pk=opportunity.customer_id)
            salesorders = SalesOrder(customer=customers, subject=opportunity.name, salesman=opportunity.salesman
                                    , total=opportunity.amount, warehouse=warehouses, status=1, payment_terms=customers.payment_terms,
                                     payment_days=customers.payment_days, duedate=customers.duedate, tax_number=tax_numberv, so_tax=opportunity.so_tax, subtotal=opportunity.subtotal, salesorder_number=prefix + str(maxsoid))
            salesorders.save()
            for so in opportunityproducts:
                salesproducts = SalesProduct.objects.create(product=so.product, qty=so.qty, price = so.price, uom=so.uom,
                                          discount=so.discount, tax=so.tax, subtotal=so.subtotal
                                          , bt_total=so.bt_total, salesorder_id=salesorders.pk)
                salesproducts.save()
            opportunity.converted = 1
            opportunity.stage = 16
            opportunity.conv_salesorder_id = salesorders.pk
            opportunity.conv_date = datetime.date.today()
            opportunity.save()
            context = {'message':'opportunities has Successfully converted to customer'}
            path = "/crm/opportunities/"
        except ProtectedError:
            context = {'message':'opportunities not converted'}
            path = "/crm/pages/"


        return redirect(path)



class OpportunityListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'crm.view_opportunity'
    model = Opportunity
    context_object_name = 'opportunities'
    template_name = 'crm/opportunity/list-opportunities.html'

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        if self.request.user.is_superuser:
            form = Opportunity.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Opportunity.objects.all().filter(salesman__in=salesmanid)
        opparr = []
        # for p in Opportunity.objects.raw('SELECT id, name, closedate, amount, sumstage.stage, source, salesman_id , type, probability, next_step, created_date FROM crm_opportunity '
        #                                     'INNER JOIN (SELECT stage, sum(amount) AS AmountTotal '
        #                                     'FROM crm_opportunity GROUP BY stage) sumstage '
        #                                     'ON crm_opportunity.stage = sumstage.stage '
        #                                     'AND crm_opportunity.amount = sumstage.AmountTotal'):

        # for p in Opportunity.objects.all().values('stage','source').order_by('stage', 'source').annotate(total=Sum('amount')):
        if form.count() == 0:
            opparr.append({'stage':'', 'totalsum': 0})

        for p in form.values('stage').order_by('stage').annotate(total=Sum('amount')):
            try:
                totalamount = p['total']
            except:
                totalamount = 0

            if totalamount is None:
                totalamount = 0

            if totalamount > 0:
                # try:
                #     sourceid = p['source']
                # except:
                #     sourceid = 0

                # opparr.append({'stage': p['stage'], 'source': sourceid, 'totalsum': round(p['total'], 0)})
                opparr.append({'stage': p['stage'], 'totalsum': round(p['total'], 0)})

        currentY = timezone.now().year
        generalq = form.annotate(total=Count('stage')).filter(created_date__year=currentY)

        totalactive = generalq.count()

        wonopp = generalq.filter(stage='16')
        totalwon = wonopp.count()

        lostopp = generalq.filter(stage='18')
        totallost = lostopp.count()

        context = {'opportunities': form, 'opparr': opparr, 'totalactive': totalactive, 'totalwon': totalwon, 'totallost': totallost}
        return context

class OpportunityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/opportunity/create_opportunity.html'
    form_class = OpportunityForm
    success_message = 'Success: opportunity was created.'
    success_url = reverse_lazy('crm:opportunities')

    def get(self, request, *args, **kwargs):
        form = OpportunityForm()
        # salesmanid = Salesman.objects.all().filter(user=self.request.user.id).values()
        # context = {'form': form, 'salesmanid': salesmanid[0]['id'],'salesmanname': salesmanid[0]['name']}
        context = {}

        return render(self.request, 'crm/opportunity/create_opportunity.html', context)


    def post(self, request, *args, **kwargs):
        if self.request.POST:
            form = OpportunityForm(self.request.POST)

            if form.is_valid():
                group = form.save()
        else:
            form = OpportunityForm()

        context = {'form': form}
        return redirect('/crm/opportunities/')

class OpportunityCreateView1(LoginRequiredMixin, CreateView):
    template_name = 'crm/opportunity/create_opportunity1.html'
    form_class = OpportunityForm
    success_message = 'Success: opportunity was created.'
    success_url = reverse_lazy('crm:opportunities')

    def get_context_data(self, **kwargs):
        context = super(OpportunityCreateView1, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            customers = Customer.objects.all().filter(status=1)
            leads = Lead.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
                customers = Customer.objects.filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.filter(salesman__in=salesmanid)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                customers = Customer.objects.all().filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.all().filter(salesman__in=salesmanid)
            salesmanq = salesmanid.values()
            context['salesmanid'] = salesmanq[0]['id']
            context['salesmanname'] = salesmanq[0]['name']

        # salesmanid = Salesman.objects.all().filter(user=self.request.user.id).values()

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            context['taxv'] = salesorders[0]['tax']
            print(salesorders[0]['tax'])
            context['tax_number'] = salesorders[0]['tax_number']
            context['customers'] = customers
            context['leads'] = leads
        else:
            context['salesorder_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['customers'] = ''
            context['leads'] = ''

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['salesproducts'] = OpportunityProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['salesproducts'] = OpportunityProductsFormSet(instance=self.object)
        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)
        salesproducts = context['salesproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if salesproducts.is_valid() == False and form.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, salesproducts=salesproducts, customerid= form.instance.customer.id, duedatev = form.instance.customer.duedate ))

        if salesproducts.is_valid():
            response = super().form_valid(form)
            salesproducts.instance = self.object
            salesproducts.save()
        elif salesproducts.is_valid() == False and form.is_valid() == False:
            context['salesproducts'] = OpportunityProductsFormSet()
            salesorders = Company.objects.all().values()
            if salesorders is not None:
                context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            else:
                context['salesorder_prefix'] = 'SO-'
            context['unitslist'] = unitslist
        elif form.is_valid() == True:
            response = super().form_valid(form)
            form.instance = self.object
            form.save()


        return response

class OpportunityUpdateView(LoginRequiredMixin, UpdateView):
    model = Opportunity
    template_name = 'crm/opportunity/edit_opportunity.html'
    form_class = OpportunityForm
    success_message = 'Success: opportunity was updated.'
    success_url = reverse_lazy("crm:opportunities")

    def get_context_data(self, **kwargs):
        context = super(OpportunityUpdateView, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            customers = Customer.objects.all().filter(status=1)
            leads = Lead.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
                customers = Customer.objects.filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.filter(salesman__in=salesmanid)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                customers = Customer.objects.all().filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.all().filter(salesman__in=salesmanid)
            salesmanq = salesmanid.values()
            context['salesmanid'] = salesmanq[0]['id']
            context['salesmanname'] = salesmanq[0]['name']

        salesorders = Company.objects.all().values()
        if salesorders is not None:
            context['salesorder_prefix'] = salesorders[0]['sales_prefix']
            context['taxv'] = salesorders[0]['tax']
            context['tax_number'] = salesorders[0]['tax_number']
            context['customers'] = customers
            context['leads'] = leads
        else:
            context['salesorder_prefix'] = 'SO-'
            context['taxv'] = 0
            context['tax_number'] = 0
            context['customers'] = ''
            context['leads'] = ''
        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})

        if self.request.POST:
            context['unitslist'] = unitslist
            context['salesproducts'] = OpportunityProductsFormSet(self.request.POST, instance=self.object)
            context['salesproducts'].full_clean()
        else:
            context['unitslist'] = unitslist
            context['salesproducts'] = OpportunityProductsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['salesproducts']

        qunits = UnitsName.objects.all()
        units = qunits.values('unit_1','unit_2')
        unitslist = []
        if units.count() > 0:
            unit1 = units[0]['unit_1']
            unit2 = units[0]['unit_2']
            unitslist.append({'id':1 , 'unit':unit1})
            unitslist.append({'id':2 , 'unit':unit2})
        if formset.is_valid() :
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        elif formset.is_valid() == False and form.is_valid() == False:
            context['unitslist'] = unitslist
            return super().form_invalid(form)
        elif form.is_valid() == True:
            response = super().form_valid(form)
            form.instance = self.object
            form.save()
            return response


class OpportunityDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Opportunity
    template_name = 'crm/opportunity/delete_opportunity.html'
    success_message = 'Success: opportunity was deleted.'
    success_url = reverse_lazy('crm:opportunities')

    def post(request,*args, **kwargs):
        opportunity = get_object_or_404(Opportunity, pk=kwargs['pk'])
        try:
            opportunity.delete()
            path = "/crm/opportunities/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)


def Set_Currency(request):
    id = int(request.GET.get('id'))
    Cur_url = request.GET.get('curl')
    currencies_all = Currency.objects.all()
    Currency.objects.update(default=False)
    currencies = Currency.objects.all().get(pk=id)
    currencies.default = True
    currencies.save()
    return request

def languages(request):
    return render(request, 'languages/index.html')

def contact_upload(request):
    template = 'crm/lead/lead_upload.html'
    prompt = {'order': 'order of the csv file should be name, tel, address'}
    context = {'success': 2}

    if request.method == 'GET':
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    if request.user.is_superuser:
        salesmanid = Salesman.objects.all().filter(name='admin')
        if salesmanid.count() == 0:
            Salesman.objects.create(name='admin', user=request.user, email='admin@gmail.com')
        salesmanid = Salesman.objects.get(name='admin')
    else:
        salesmanid = Salesman.objects.get(user=request.user.id)


    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        try:
            _, created = Lead.objects.update_or_create(
                name=column[0],
                title=column[1],
                department=column[2],
                office_phone=column[3],
                mobile=column[4],
                fax=column[5],
                account_name=column[6],
                website=column[7],
                email=column[8],
                address=column[9],
                postal_code=column[10],
                other_address=column[11],
                other_postal_code=column[12],
                status_description=column[13],
                lead_description=column[14],
                description=column[15],
                opportunity_name=column[16],
                amount=column[17],
                referred_by=column[18],
                donotcall=column[19],
                status=1,
                lead_Source=12,
                salesman=salesmanid,
            )
            context = {'success': 1}
        except:
            context = {'success': 2}

    return render(request, template, context)

def Lead_Convert(request):
    template = 'crm/lead/list-leads.html'

    leads = Lead.objects.get(pk=request)

    try:
        Customer.objects.create(name=leads.name, description=leads.description, salesman=leads.salesman
                                    , country=leads.country, area=leads.area, city=leads.city,
                                    address=leads.address, channel=1)
        leads.converted = 1
        leads.save()
        context = {'created': 1}

    except:
        context = {'created': 0}

    return context

class ActivityListView(LoginRequiredMixin, generic.ListView):
    permission_required = 'crm.view_activity'
    model = Activities
    context_object_name = 'avtivities'
    template_name = 'crm/activities/list-activities.html'

    def get_context_data(self, **kwargs):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        if self.request.user.is_superuser:
            form = Activities.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            form = Activities.objects.all().filter(salesman__in=salesmanid)

        context = {'avtivities': form}
        return context

class ActivityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'crm/activities/create_activity.html'
    form_class = ActivityForm
    success_message = 'Success: activity was created.'
    success_url = reverse_lazy('crm:activities')

    def get(self, request, *args, **kwargs):
        form = ActivityForm()
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            customers = Customer.objects.all().filter(status=1)
            leads = Lead.objects.all()
            opportunities = Opportunity.objects.all()
            salesmanid = ''
            salesmanname = ''
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
                customers = Customer.objects.filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.filter(salesman__in=salesmanid)
                opportunities = Opportunity.objects.filter(salesman__in=salesmanid)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                customers = Customer.objects.all().filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.all().filter(salesman__in=salesmanid)
                opportunities = Opportunity.objects.all().filter(salesman__in=salesmanid)
            salesmanq = salesmanid.values()
            salesmanid = salesmanq[0]['id']
            salesmanname = salesmanq[0]['name']

        context = {'form': form, 'salesmanid': salesmanid, 'salesmanname': salesmanname, 'customers': customers, 'leads': leads, 'opportunities': opportunities}
        return render(self.request, 'crm/activities/create_activity.html', context)


    def post(self, request, *args, **kwargs):
        if self.request.POST:
            form = ActivityForm(self.request.POST)

            if form.is_valid():
                group = form.save()
        else:
            form = ActivityForm()

        context = {'form': form}
        return redirect('/crm/activities/')

class ActivityDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Activities
    template_name = 'crm/activities/delete_activity.html'
    success_message = 'Success: activity was deleted.'
    success_url = reverse_lazy('crm:activities')

    def post(request,*args, **kwargs):
        activity = get_object_or_404(Activities, pk=kwargs['pk'])
        try:
            activity.delete()
            path = "/crm/activities/"
        except ProtectedError:
            path = "/crm/pages/"

        return redirect(path)


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activities
    template_name = 'crm/activities/edit_activity.html'
    form_class = ActivityForm
    success_message = 'Success: activity was updated.'
    success_url = reverse_lazy("crm:activities")

    def get_context_data(self, **kwargs):
        context = super(ActivityUpdateView, self).get_context_data(**kwargs)

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            customers = Customer.objects.all().filter(status=1)
            leads = Lead.objects.all()
            opportunities = Opportunity.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.all().filter(user=self.request.user.id)
                customers = Customer.objects.filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.filter(salesman__in=salesmanid)
                opportunities = Opportunity.objects.filter(salesman__in=salesmanid)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.all().filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                customers = Customer.objects.all().filter(salesman__in=salesmanid).filter(status=1)
                leads = Lead.objects.all().filter(salesman__in=salesmanid)
                opportunities = Opportunity.objects.all().filter(salesman__in=salesmanid)
            salesmanq = salesmanid.values()
            context['salesmanid'] = salesmanq[0]['id']
            context['salesmanname'] = salesmanq[0]['name']

        context['customers'] = customers
        context['leads'] = leads
        context['opportunities'] = leads

        return context


class Commission_CalcListView(LoginRequiredMixin, ListView):
    model = Commission_Calc
    context_object_name = 'commissions'
    template_name = 'crm/commission_calc/list-commissions.html'

    def get_context_data(self, **kwargs):
        years = int(datetime.date.today().year)
        context = super(Commission_CalcListView, self).get_context_data(**kwargs)
        context['commissions'] = Commission_Calc.objects.all()

        return context

class CommissionDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Commission_Calc
    template_name = 'crm/commission_calc/delete_commission_calc.html'
    success_message = 'Success: commission was deleted.'
    success_url = reverse_lazy('crm:commissions_calc')


def CommissionCreate_Calc(request):
    salesmans = Salesman.objects.exclude(Q(commission__isnull=True))
    salesman_count = salesmans.count()

    today = datetime.date.today()
    currentYear = timezone.now().year
    months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11', '12']
    current_month1 = months[today.month]
    current_month = int(current_month1)

    financialyears = FinancialYear.objects.all()

    for financialyear in financialyears:
        Quarter1 = [financialyear.m1, financialyear.m2, financialyear.m3]
        Quarter2 = [financialyear.m4, financialyear.m5, financialyear.m6]
        Quarter3 = [financialyear.m7, financialyear.m8, financialyear.m9]
        Quarter4 = [financialyear.m10, financialyear.m11, financialyear.m12]
        FirstHalf = [financialyear.m1, financialyear.m2, financialyear.m3, financialyear.m4, financialyear.m5,
                     financialyear.m6]
        SecondHalf = [financialyear.m7, financialyear.m8, financialyear.m9, financialyear.m10, financialyear.m11,
                      financialyear.m12]
        FullYear = [financialyear.m1, financialyear.m2, financialyear.m3, financialyear.m4, financialyear.m5,
                     financialyear.m6, financialyear.m7, financialyear.m8, financialyear.m9, financialyear.m10, financialyear.m11,
                      financialyear.m12]
        numberofdaysQ1 = 31 + 28 + 31
        numberofdaysQ2 = 30 + 31 + 30
        numberofdaysQ3 = 31 + 31 + 30
        numberofdaysQ4 = 31 + 30 + 31
        numberofdaysFH = 31 + 28 + 31 + 30 + 31 + 30
        numberofdaysSH = 31 + 31 + 30 + 31 + 30 + 31
        numberofdaysFY = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31
        if financialyear.m1 == current_month:
            cmonths = 'm1'
            monthn = '1'
            monthname = 'Jan'
            numberofdays = 31
            current_quarter = 'Quarter1'
        elif financialyear.m2 == current_month:
            cmonths = 'm2'
            monthn = '2'
            monthname = 'Feb'
            numberofdays = 28
            current_quarter = 'Quarter1'
        elif financialyear.m3 == current_month:
            cmonths = 'm3'
            monthn = '3'
            monthname = 'Mar'
            numberofdays = 31
            current_quarter = 'Quarter1'
        elif financialyear.m4 == current_month:
            cmonths = 'm4'
            monthn = '4'
            monthname = 'Apr'
            numberofdays = 30
            current_quarter = 'Quarter2'
        elif financialyear.m5 == current_month:
            cmonths = 'm5'
            monthn = '5'
            monthname = 'May'
            numberofdays = 31
            current_quarter = 'Quarter2'
        elif financialyear.m6 == current_month:
            cmonths = 'm6'
            monthn = '6'
            monthname = 'Jun'
            numberofdays = 30
            current_quarter = 'Quarter2'
        elif financialyear.m7 == current_month:
            cmonths = 'm7'
            monthn = '7'
            monthname = 'Jul'
            numberofdays = 31
            current_quarter = 'Quarter3'
        elif financialyear.m8 == current_month:
            cmonths = 'm8'
            monthn = '8'
            monthname = 'Aug'
            numberofdays = 31
            current_quarter = 'Quarter3'
        elif financialyear.m9 == current_month:
            cmonths = 'm9'
            monthn = '9'
            monthname = 'Sep'
            numberofdays = 30
            current_quarter = 'Quarter3'
        elif financialyear.m10 == current_month:
            cmonths = 'm10'
            monthn = '10'
            monthname = 'Oct'
            numberofdays = 31
            current_quarter = 'Quarter4'
        elif financialyear.m11 == current_month:
            cmonths = 'm11'
            monthn = '11'
            monthname = 'Nov'
            numberofdays = 30
            current_quarter = 'Quarter4'
        elif financialyear.m12 == current_month:
            cmonths = 'm12'
            monthn = '12'
            monthname = 'Dec'
            numberofdays = 31
            current_quarter = 'Quarter4'

    if current_quarter == 'Quarter1':
        Quarter = Quarter1
        cmonth1 = 'm1'
        cmonth2 = 'm2'
        cmonth3 = 'm3'
        QQ = 1
        numberofdays = numberofdaysQ1
    elif current_quarter == 'Quarter2':
        Quarter = Quarter2
        cmonth1 = 'm4'
        cmonth2 = 'm5'
        cmonth3 = 'm6'
        QQ = 2
        numberofdays = numberofdaysQ2
    elif current_quarter == 'Quarter3':
        Quarter = Quarter3
        cmonth1 = 'm7'
        cmonth2 = 'm8'
        cmonth3 = 'm9'
        QQ = 3
        numberofdays = numberofdaysQ3
    elif current_quarter == 'Quarter4':
        Quarter = Quarter4
        cmonth1 = 'm10'
        cmonth2 = 'm11'
        cmonth3 = 'm12'
        QQ = 4
        numberofdays = numberofdaysQ4

    thismonth = int(monthn)

    for sm in salesmans:
        commission_details = Commission_Details.objects.all().filter(comission_id=sm.commission)
        qsales = Transactions.objects.values('source').order_by('source') \
            .annotate(total=Sum('total')).filter(
            Q(source='SalesOrder')).values('total').filter(
            created_date__year=currentYear).filter(salesman_id=sm.id)
        stotalmsales = qsales.aggregate(Sum('total'))
        if stotalmsales['total__sum'] is None:
            sales_total = 0
        else:
            sales_total = stotalmsales['total__sum']
            
        qsalesreturn = Transactions.objects.values('source').order_by('source') \
            .annotate(total=Sum('total')).filter(
            Q(source='SalesReturnOrder')).values('total').filter(
            created_date__year=currentYear).filter(salesman_id=sm.id)
        stotalmsales_return = qsalesreturn.aggregate(Sum('total'))
        if stotalmsales_return['total__sum'] is None:
            sales_return_total = 0
        else:
            sales_return_total = stotalmsales_return['total__sum'] * -1

        customers = Customer.objects.filter(salesman_id=sm)
        qcollections = Collection.objects.values('customer').order_by('customer') \
            .annotate(total=Sum('amount')).filter(
            created_date__year=currentYear).filter(customer_id__in=customers)
        scollection = qcollections.aggregate(total=Sum('amount'))
        if scollection['total'] is None:
            collection_total = 0
        else:
            collection_total = scollection['total']

        totalmonthlytargets = 0
        totalmonthlytargetsqty = 0
        for cd in commission_details:
            if cd.calculation == 1:
                mm = 1
                while mm <= thismonth:
                    monthex = Commission_Calc.objects.filter(description=cd.description, month=mm , salesman=sm)
                    if monthex.count() == 0:
                        monthss = "m" + str(mm)

                        qsales = Transactions.objects.values('source').order_by('source') \
                            .annotate(total=Sum('total')).filter(Q(source='SalesOrder')).filter(created_date__year=currentYear).filter(
                            created_date__month=mm).filter(salesman_id=sm.id)
                        stotalmsales = qsales.aggregate(Sum('total'))
                        if stotalmsales['total__sum'] is None:
                            sales_total = 0
                        else:
                            sales_total = stotalmsales['total__sum']

                        qsalesreturn = Transactions.objects.values('source').order_by('source') \
                            .annotate(total=Sum('total')).filter(
                            Q(source='SalesReturnOrder')).values('total').filter(
                            created_date__year=currentYear).filter(
                            created_date__month=mm).filter(salesman_id=sm.id)
                        stotalmsales_return = qsalesreturn.aggregate(Sum('total'))
                        if stotalmsales_return['total__sum'] is None:
                            sales_return_total = 0
                        else:
                            sales_return_total = stotalmsales_return['total__sum'] * -1

                        customers = Customer.objects.filter(salesman_id=sm)
                        qcollections = Collection.objects.values('customer').order_by('customer') \
                            .annotate(total=Sum('amount')).filter(
                            created_date__year=currentYear).filter(customer_id__in=customers).filter(
                            created_date__month=mm)
                        scollection = qcollections.aggregate(total=Sum('amount'))
                        if scollection['total'] is None:
                            collection_total = 0
                        else:
                            collection_total = scollection['total']

                        querymonthlytarget = TargetTransactions.objects.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = sm)
                        totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                        try:
                            totalmonthlytargets = totalmonthlytarget['total__sum']
                        except:
                            totalmonthlytargets = 0

                        if cd.commission_on == 1:
                            if cd.commission_type == 1:
                                if cd.on_what == 1:
                                    if cd.onvalue <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 3:
                                    if cd.onvalue >= totalmonthlytargetsqty:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 4:
                                    if int(totalmonthlytargetsqty * cd.onvalue) <= qsalesqty:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0

                            elif cd.commission_type == 2:
                                if cd.on_what == 1:
                                    if cd.onvalue <= collection_total:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= collection_total:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                        elif cd.commission_on == 2:
                            if cd.commission_type == 1:
                                if cd.on_what == 1:
                                    if cd.onvalue <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 3:
                                    if cd.onvalue >= totalmonthlytargetsqty:
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 4:
                                    if int(totalmonthlytargetsqty * cd.onvalue) <= qsalesqty:
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0

                            elif cd.commission_type == 2:
                                if cd.on_what == 1:
                                    if cd.onvalue <= collection_total:
                                        comm_value = cd.commission_value * collection_total
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= collection_total:
                                        comm_value = cd.commission_value * collection_total
                                    else:
                                        comm_value = 0

                        Commission_Calc.objects.create(month=mm, salesman=sm, description=cd.description, calc_desc=monthss,
                                                       target=totalmonthlytargets, sales=sales_total,
                                                       sales_return=sales_return_total, collection=collection_total,
                                                       commission=comm_value, paid_amount=0, paid=False, comission_id=sm.commission)
                    mm += 1

            elif cd.calculation == 2:
                mm = 1
                while mm <= QQ:
                    Quarter_n = "Quarter" + str(mm)
                    monthex = Commission_Calc.objects.filter(description=cd.description, calc_desc=Quarter_n, salesman=sm)
                    if monthex.count() <= 0:
                        if Quarter_n == 'Quarter1':
                            Quarter = Quarter1
                            cmonth1 = 'm1'
                            cmonth2 = 'm2'
                            cmonth3 = 'm3'
                            numberofdays = numberofdaysQ1
                        elif Quarter_n == 'Quarter2':
                            Quarter = Quarter2
                            cmonth1 = 'm4'
                            cmonth2 = 'm5'
                            cmonth3 = 'm6'
                            numberofdays = numberofdaysQ2
                        elif Quarter_n == 'Quarter3':
                            Quarter = Quarter3
                            cmonth1 = 'm7'
                            cmonth2 = 'm8'
                            cmonth3 = 'm9'
                            numberofdays = numberofdaysQ3
                        elif Quarter_n == 'Quarter4':
                            Quarter = Quarter4
                            cmonth1 = 'm10'
                            cmonth2 = 'm11'
                            cmonth3 = 'm12'
                            numberofdays = numberofdaysQ4

                        qsalesreturn = Transactions.objects.values('source').order_by('source') \
                            .annotate(total=Sum('total')).filter(Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter).filter(salesman_id=sm.id)
                        stotalmsales_return = qsalesreturn.aggregate(Sum('total'))
                        if stotalmsales_return['total__sum'] is None:
                            sales_return_total = 0
                        else:
                            sales_return_total = stotalmsales_return['total__sum'] * -1

                        qsales = Transactions.objects.values('source').order_by('source') \
                            .annotate(total=Sum('total')).filter(Q(source='SalesOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter).filter(salesman_id=sm.id)
                        stotalmsales = qsales.aggregate(Sum('total'))
                        if stotalmsales['total__sum'] is None:
                            sales_total = 0
                        else:
                            sales_total = stotalmsales['total__sum']

                        qsalesqty = Transactions.objects.values('source').order_by('source') \
                            .annotate(total=Sum('ctrqty')).filter(Q(source='SalesOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter).filter(salesman_id=sm.id)
                        stotalmsalesqty = qsalesqty.aggregate(Sum('total'))
                        if stotalmsalesqty['total__sum'] is None:
                            salesqty_total = 0
                        else:
                            salesqty_total = stotalmsalesqty['total__sum']

                        querymonthlytarget = TargetTransactions.objects.values('area') \
                            .values('salesman_id').order_by('salesman_id').annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).filter(
                            created_date__year=currentYear).filter(salesman_id=sm.id)
                        totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                        if totalmonthlytarget['total__sum'] is None:
                            totalmonthlytargets = 0
                        else:
                            totalmonthlytargets = totalmonthlytarget['total__sum']
                        queryyearlytargetqty = TargetTransactions.objects.values('salesman_id').order_by('salesman_id').annotate(
                            qty=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)), output_field=IntegerField())).filter(
                            created_date__year=currentYear).filter(salesman_id=sm.id)
                        totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
                        if totalyearlytargetqty['qty__sum'] is None:
                            totalmonthlytargetsqty = 0
                        else:
                            totalmonthlytargetsqty = totalyearlytargetqty['qty__sum']

                        customers = Customer.objects.filter(salesman_id=sm)
                        qcollections = Collection.objects.values('customer').order_by('customer') \
                            .annotate(total=Sum('amount')).filter(
                            created_date__year=currentYear).filter(created_date__month__in=Quarter).filter(customer_id__in=customers)
                        scollection = qcollections.aggregate(total=Sum('amount'))
                        if scollection['total'] is None:
                            collection_total = 0
                        else:
                            collection_total = scollection['total']

                        if cd.commission_on == 1:
                            if cd.commission_type == 1:
                                if cd.on_what == 1:
                                    if cd.onvalue <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 3:
                                    if cd.onvalue >= totalmonthlytargetsqty:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 4:
                                    if int(totalmonthlytargetsqty * cd.onvalue) <= qsalesqty:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0

                            elif cd.commission_type == 2:
                                if cd.on_what == 1:
                                    if cd.onvalue <= collection_total:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= collection_total:
                                        comm_value = cd.commission_value
                                    else:
                                        comm_value = 0
                        elif cd.commission_on == 2:
                            if cd.commission_type == 1:
                                if cd.on_what == 1:
                                    if cd.onvalue <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= (sales_total - sales_return_total):
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 3:
                                    if cd.onvalue >= totalmonthlytargetsqty:
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 4:
                                    if int(totalmonthlytargetsqty * cd.onvalue) <= qsalesqty:
                                        comm_value = cd.commission_value * (sales_total - sales_return_total)
                                    else:
                                        comm_value = 0

                            elif cd.commission_type == 2:
                                if cd.on_what == 1:
                                    if cd.onvalue <= collection_total:
                                        comm_value = cd.commission_value * collection_total
                                    else:
                                        comm_value = 0
                                elif cd.on_what == 2:
                                    if int(totalmonthlytargets * cd.onvalue) <= collection_total:
                                        comm_value = cd.commission_value * collection_total
                                    else:
                                        comm_value = 0

                        Commission_Calc.objects.create(month=mm, salesman=sm, description=cd.description, calc_desc=Quarter_n,
                                                       target=totalmonthlytargets, sales=sales_total,
                                                       sales_return=sales_return_total, collection=collection_total,
                                                       commission=comm_value, paid_amount=0, paid=False, comission_id=sm.commission)
                    mm += 1

            elif cd.calculation == 3:
                monthn = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                Quarter = "None"



    commission_list = Commission.objects.all()
    context = {
        'commissions': Commission_Calc.objects.all()
    }
    return redirect('/crm/commissions_calc/')

class CommissionListView(LoginRequiredMixin, ListView):
    model = Commission
    context_object_name = 'commissions'
    template_name = 'crm/commission/list-commissions.html'

    def get_context_data(self, **kwargs):
        years = int(datetime.date.today().year)
        context = super(CommissionListView, self).get_context_data(**kwargs)
        context['commissions'] = Commission.objects.all().filter(year=years)

        return context

class CommissionCreateView(LoginRequiredMixin, CreateView):

    model = Commission
    template_name = 'crm/commission/create_commission.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:commissions')

    def get_context_data(self, **kwargs):
        context = super(CommissionCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['commissions'] = CommissionDetailsFormFormSet(self.request.POST, instance=self.object)
            context['commissions'].full_clean()
        else:
            context['commissions'] = CommissionDetailsFormFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        commissions = context['commissions']
        if commissions.is_valid() == False:
            return self.render_to_response(self.get_context_data(form=form, commissions=commissions))
        if commissions.is_valid():
            response = super().form_valid(form)
            commissions.instance = self.object
            commissions.save()

        else:
            context['commissions'] = CommissionDetailsFormFormSet()
        return response

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    template_name = 'crm/commission/edit_commission.html'
    fields = '__all__'
    success_url = reverse_lazy('crm:commissions')

    def get_context_data(self, **kwargs):
        context = super(CommissionUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['commissions'] = CommissionDetailsFormFormSet(self.request.POST, instance=self.object)
            context['commissions'].full_clean()
        else:
            context['commissions'] = CommissionDetailsFormFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['commissions']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)
