from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from djangoformsetjs.utils import formset_media_js
from gl.models import *


class LedgerSOAListForm(BSModalForm):
    class Meta:
        model = LedgerTrans
        exclude = ['timestamp']


######### Reports Groups

class ReportsGroupsForm(BSModalForm):
    class Meta:
        model = ReportsGroups
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Reports Groups


######### Reports
class VendorsForm(forms.ModelForm):
    class Meta:
        model = Reports
        exclude = ()

class ReportsParametersForm(forms.ModelForm):
    class Meta:
        model = ReportsParameters
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(ReportsParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

ReportsParametersFormSet = inlineformset_factory(Reports, ReportsParameters ,form=ReportsParametersForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### Report run
class ReportsRunForm(forms.ModelForm):
    class Meta:
        model = ReportsParameters
        exclude = ['']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End Report run


######### Report Param view
class reportparamForm(BSModalForm):
    class Meta:
        model = ReportsParameters
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End Report Param view
