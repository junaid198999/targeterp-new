from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from sy.models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from djangoformsetjs.utils import formset_media_js
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field

def index(request):
    return render(request, 'gl/index.html')

######### Customers Categories

class CustomersCategoriesForm(BSModalForm):
    class Meta:
        model = CustomersCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Customers Categories


######### Customers Classes

class CustomersClassesForm(BSModalForm):
    class Meta:
        model = CustomersClasses
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Customers Classes


######### Customers

class CustomersForm(forms.ModelForm):
    startbusinessdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    statusdate= forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False ,disabled=True)
    statuschangedby =forms.IntegerField (widget=forms.TextInput(attrs={'type': 'text'}), required=False ,disabled=True)

    class Meta:
        model = Customers
        exclude = ()


class CustomersAddressesForm(forms.ModelForm):
    class Meta:
        model = CustomersAddresses
        exclude = ()
        widgets = {
        }

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CustomersAddressesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


CustomersAddressesFormSet = inlineformset_factory(Customers, CustomersAddresses, form=CustomersAddressesForm, extra=0,
                                                min_num=1, validate_min=True, can_delete=True)


class CustomersContactsForm(forms.ModelForm):
    class Meta:
        model = CustomersContacts
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CustomersContactsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

CustomersContactsFormSet = inlineformset_factory(Customers, CustomersContacts ,form=CustomersContactsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Customers

######### Customers Journal
class CustomersJourForm(forms.ModelForm):
    statusdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','readonly':'readonly'}), required=False,disabled=True,label="Status Date")

    class Meta:
        model = CustomersJour
        exclude = ()
        widgets = {
            #'transtype': Select2Widget,
        }



    def __init__(self, *args, **kwargs):
        super(CustomersJourForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['status'].disabled = True

        if self.instance.transtype_id == None:
            self.fields['transtype'].disabled = False
        else:
            self.fields['transtype'].disabled = True




class CustomersJourLineForm(forms.ModelForm):

    ledid = forms.IntegerField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right'}), required=False,disabled=False )
    custid = forms.IntegerField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right'}), required=False,disabled=False )


    class Meta:
        model = CustomersJourLine
        exclude = []
        widgets = {
            #'ledger': Select2Widget,
            #'costcenter1': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CustomersJourLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


        self.ledid= self.instance.ledger_id
        print(self.ledid)
        self.custid = self.instance.customer_id
        print(self.custid)
    #
    #
    #
    # def save(self, *args, **kwargs):
    #     self.ledger_id= self.instance.ledger_id
    #     self.customer_id = self.instance.customer_id
    #
    #
    #
    #     print(self.customer_id)






CustomersJourLineFormSet = inlineformset_factory(CustomersJour, CustomersJourLine ,form=CustomersJourLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Customers Journal

######### Customers Payments
class CustomersPaymentsForm(BSModalForm):
    paymentdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False )
    class Meta:
        model = CustomersPayments
        exclude = ('transtype','number','paymentdate','ledger','costcenter1','costcenter2','costcenter3','costcenter3','amount')



class CustomersPaymentsLineForm(forms.ModelForm):
    class Meta:
        model = CustomersPaymentsLine
        exclude = ()
        widgets = {
           # 'ledger': Select2Widget,
            #'costcenter1': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CustomersPaymentsLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


CustomersPaymentsLineFormSet = inlineformset_factory(CustomersPayments, CustomersPaymentsLine ,form=CustomersPaymentsLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Ledger Payments


######### Collections
class CollectionsForm(forms.ModelForm):

    collectiondate = forms.DateField(widget=forms.DateInput (attrs={'type': 'date','readonly':'readonly'}), required=False , disabled=True,initial=datetime.now().date() )
    statusdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','readonly':'readonly'}), required=False,disabled=True,label="Status Date")
    duedate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False,disabled=False,label="Due Date")

    number = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )
    customer = Customers.objects.filter(allowaccountentry=True).values()

    class Meta:
        model = Collections
        exclude = ()
        widgets = {
        }


    def __init__(self, *args, **kwargs):
        super(CollectionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['status'].disabled = True
        self.fields['statusdate'].disabled = True
        #self.fields['collector'].disabled = True
        self.helper.layout = Layout(


            )

class CollectionsDuePaymentsForm(forms.ModelForm):
    class Meta:
        model = CollectionsDuePayments
        exclude = []
        widgets = {

        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CollectionsDuePaymentsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['customerpaymentschedule'].widget.attrs['readonly'] = True
        self.fields['operationnumber'].widget.attrs['readonly'] = True
        self.fields['duedate'].widget.attrs['readonly'] = True
        self.fields['dueamount'].widget.attrs['readonly'] = True


CollectionsDuePaymentsFormSet = inlineformset_factory(Collections, CollectionsDuePayments ,form=CollectionsDuePaymentsForm, extra=0, min_num=1, validate_min=True, can_delete=True)
######### End  Collections

######### Salesmans Groups

class SalesmansGroupsForm(BSModalForm):
    class Meta:
        model = SalesmansGroups
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Salesmans Groups



######### Salesmans

class SalesmansForm(BSModalForm):
    class Meta:
        model = Salesmans
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Salesmans
