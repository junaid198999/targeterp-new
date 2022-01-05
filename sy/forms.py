from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from djangoformsetjs.utils import formset_media_js
from django.forms.widgets import  DateInput,DateTimeInput
#from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget


######### Modules
class ModulesForm(BSModalForm):
    class Meta:
        model = Modules
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### LookUp
class LookUpForm(BSModalForm):
    class Meta:
        model = LookUp
        exclude = ['keyname','keyid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### Fiscal Years
class FiscalYearsForm(forms.ModelForm):
    class Meta:
        model = FiscalYears
        exclude = ()


class FiscalYearsPeriodsForm(forms.ModelForm):
    class Meta:
        model = FiscalYearsPeriods
        exclude = ()
        widgets = {
            'fromdate': forms.DateInput(),
            'todate': forms.DateInput()
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(FiscalYearsPeriodsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


FiscalYearsPeriodsFormSet = inlineformset_factory(FiscalYears, FiscalYearsPeriods,form=FiscalYearsPeriodsForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Fiscal Years


######### Fiscal Years Periods Modules
class FiscalYearsPeriodsModulesForm(BSModalForm):

    class Meta:
        model = FiscalYearsPeriodsModules
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Fiscal Years Periods Modules


######### Payments Methods
class PaymentsMethodsForm(BSModalForm):

    class Meta:
        model = PaymentsMethods


        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Payments Methods

######### Credit Cards Types

class CreditCardsTypesForm(BSModalForm):
    class Meta:
        model = CreditCardsTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Credit Cards Types


######### Languages Form

class LanguagesForm(BSModalForm):
    class Meta:
        model = Languages
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Languages Form


######### Nationalities Form

class NationalitiesForm(BSModalForm):
    class Meta:
        model = Nationalities
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Nationalities Form

######### Regions Form

class RegionsForm(BSModalForm):
    class Meta:
        model = Regions
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Regions Form


######### Countries Form

class CountriesForm(BSModalForm):
    class Meta:
        model = Countries
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Countries Form



######### Areas Form

class AreasForm(BSModalForm):
    class Meta:
        model = Areas
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Areas Form

######### Cities Form

class CitiesForm(BSModalForm):
    class Meta:
        model = Cities
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Cities Form

######### Districts Form

class DistrictsForm(BSModalForm):
    class Meta:
        model = Districts
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Districts Form


######### AddressesTypes Form

class AddressesTypesForm(BSModalForm):
    class Meta:
        model = AddressesTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End AddressesTypes Form

######### ContactsTypes Form

class ContactsTypesForm(BSModalForm):
    class Meta:
        model = ContactsTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End ContactsTypes Form


######### BusinessActivitiesTypes Form

class BusinessActivitiesTypesForm(BSModalForm):
    class Meta:
        model = BusinessActivitiesTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End BusinessActivitiesTypes Form


######### Taxes
class TaxesForm(forms.ModelForm):
    class Meta:
        model = Taxes
        exclude = []

class TaxesLinesForm(forms.ModelForm):
    class Meta:
        model = TaxesLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TaxesLinesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TaxesLinesFormSet = inlineformset_factory(Taxes, TaxesLine  ,form=TaxesLinesForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Taxes



######### Taxes Groups
class TaxesGroupsForm(forms.ModelForm):
    class Meta:
        model = TaxesGroups
        exclude = []


class TaxesGroupsLinesForm(forms.ModelForm):
    #fromdate = forms.DateField(required=False, label='From Date',widget=forms.TextInput(attrs={'class': 'datepicker'}))
    #fromdate = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    fromdate = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    todate = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = TaxesGroupsLine

        exclude = ()
        widgets = {
            #'fromdate': DateWidget(attrs={'id': "fromdateid"}, usel10n=True, bootstrap_version=3)
            #'fromdate': DateInput(),


        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TaxesGroupsLinesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


TaxesGroupsLinesFormSet = inlineformset_factory(TaxesGroups, TaxesGroupsLine  ,form=TaxesGroupsLinesForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Taxes Groups

######### Company Profile
class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ()

class CompanyProfileAddressesForm(forms.ModelForm):
    class Meta:
        model = CompanyProfileAddresses
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CompanyProfileAddressesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

CompanyProfileAddressesFormSet = inlineformset_factory(CompanyProfile, CompanyProfileAddresses ,form=CompanyProfileAddressesForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class CompanyProfileContactsForm(forms.ModelForm):
    class Meta:
        model = CompanyProfileContacts
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CompanyProfileContactsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

CompanyProfileContactsFormSet = inlineformset_factory(CompanyProfile, CompanyProfileContacts ,form=CompanyProfileContactsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Company Profile

######### Prices Levels

class PriceLevelsForm(BSModalForm):
    class Meta:
        model = PriceLevels
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Prices Levels


######### Payment Tearm

class PaymentsTearmsForm(BSModalForm):
    class Meta:
        model = PaymentsTearms
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Payment Tearm

######### Cash Discounts Roles
class CashDiscountsRolesForm(forms.ModelForm):

    class Meta:
        model = CashDiscountsRoles
        exclude = ()
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(CashDiscountsRolesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()


class CashDiscountsRolesLineForm(forms.ModelForm):

    ledid = forms.IntegerField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right'}), required=False,disabled=False )
    custid = forms.IntegerField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right'}), required=False,disabled=False )


    class Meta:
        model = CashDiscountsRolesLine
        exclude = []
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CashDiscountsRolesLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


CashDiscountsRolesLineFormSet = inlineformset_factory(CashDiscountsRoles, CashDiscountsRolesLine ,form=CashDiscountsRolesLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Customers Journal


