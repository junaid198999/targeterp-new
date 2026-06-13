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

def index(request):
    return render(request, 'gl/index.html')

######### Vendors Categories

class VendorsCategoriesForm(BSModalForm):
    class Meta:
        model = VendorsCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Vendors Categories


######### Vendors Classes

class VendorsClassesForm(BSModalForm):
    class Meta:
        model = VendorsClasses
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Vendors Classes


######### Vendors
class VendorsForm(forms.ModelForm):
    class Meta:
        model = Vendors
        exclude = ()

class VendorsAddressesForm(forms.ModelForm):
    class Meta:
        model = VendorsAddresses
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(VendorsAddressesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

VendorsAddressesFormSet = inlineformset_factory(Vendors, VendorsAddresses ,form=VendorsAddressesForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class VendorsContactsForm(forms.ModelForm):
    class Meta:
        model = VendorsContacts
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(VendorsContactsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

VendorsContactsFormSet = inlineformset_factory(Vendors, VendorsContacts ,form=VendorsContactsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Vendors

######### Buyers Groups

class BuyersGroupsForm(BSModalForm):
    class Meta:
        model = BuyersGroups
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Buyers Groups


######### Buyers

class BuyersForm(BSModalForm):
    class Meta:
        model = Buyers
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Buyers



######### Vendors Jour
class VendorsJourForm(forms.ModelForm):
    class Meta:
        model = Vendors
        exclude = ()

class VendorsJourLineForm(forms.ModelForm):
    class Meta:
        model = VendorsAddresses
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(VendorsJourLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

VendorsJourLineFormSet = inlineformset_factory(VendorsJour, VendorsJourLine ,form=VendorsJourLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Vendors Jour
