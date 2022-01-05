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


######### BanksGroups

class BanksGroupsForm(BSModalForm):
    class Meta:
        model = BanksGroups
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End BanksGroups


######### Banks

class BanksForm(forms.ModelForm):
    # statusdate= forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False ,disabled=True)
    # statuschangedby =forms.IntegerField (widget=forms.TextInput(attrs={'type': 'text'}), required=False ,disabled=True)

    class Meta:
        model = Banks
        exclude = ()


class BanksAddressesForm(forms.ModelForm):
    class Meta:
        model = BanksAddresses
        exclude = ()
        widgets = {
        }

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(BanksAddressesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


BanksAddressesFormSet = inlineformset_factory(Banks, BanksAddresses, form=BanksAddressesForm, extra=0,
                                                min_num=1, validate_min=True, can_delete=True)


class BanksContactsForm(forms.ModelForm):
    class Meta:
        model = BanksContacts
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(BanksContactsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

BanksContactsFormSet = inlineformset_factory(Banks, BanksContacts ,form=BanksContactsForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class BanksCreditCardsTypesForm(forms.ModelForm):
    class Meta:
        model = BanksCreditCardsTypes
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(BanksCreditCardsTypesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

BanksCreditCardsTypesFormSet = inlineformset_factory(Banks, BanksCreditCardsTypes ,form=BanksCreditCardsTypesForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Banks


######### BanksDocumentsUnderProcess

class BanksDocumentsUnderProcessForm(BSModalForm):
    bankrefdate= forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False ,disabled=False)
    bankrefno= forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}), required=False ,disabled=False)
    sourcename= forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}), required=False ,disabled=True)
    sourceid= forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}), required=False ,disabled=True)


    class Meta:
        model = BanksDocumentsUnderProcess
        exclude = ['created_date','created_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End BanksDocumentsUnderProcess
