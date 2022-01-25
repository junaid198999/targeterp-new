from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from djangoformsetjs.utils import formset_media_js


######### Ledgers Types

class LedgersTypesForm(BSModalForm):
    class Meta:
        model = LedgersTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Ledgers Types

######### Ledgers Categories

class LedgersCategoriesForm(BSModalForm):
    class Meta:
        model = LedgersCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Ledgers Categories

######### Ledgers

class LedgerForm(BSModalForm):
    class Meta:
        model = Ledger
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Ledgers

######### Cost Categories

class CostCategoriesForm(BSModalForm):
    class Meta:
        model = CostCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Cost Categories

######### Cost Centers Levels

class CostCentersLevelsForm(BSModalForm):
    class Meta:
        model = CostCentersLevels
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Cost  Centers Levels

######### Cost Centers
class CostCentersForm(BSModalForm):
    class Meta:
        model = CostCenters
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Cost  Centers

######### Trans Types
class TransTypesForm(BSModalForm):
    class Meta:
        model = TransTypes
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Trans Types


######### Ledger Journal
class LedgerJourForm(forms.ModelForm):
    statusdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','readonly':'readonly'}), required=False,disabled=True,label="Status Date")
    class Meta:
        model = LedgerJour
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(LedgerJourForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['status'].disabled = False

        if self.instance.transtype_id == None:
            self.fields['transtype'].disabled = False
        else:
            self.fields['transtype'].disabled = True


#    def __init__(self, *args, **kwargs):
 #       super().__init__(*args, **kwargs)

class LedgerJourLineForm(forms.ModelForm):
    class Meta:
        model = LedgerJourLine
        exclude = ()
        widgets = {
            #'ledger': Select2Widget,
            #'costcenter1': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(LedgerJourLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


LedgerJourLineFormSet = inlineformset_factory(LedgerJour, LedgerJourLine ,form=LedgerJourLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Ledger Journal

######### Treasuries
class TreasuriesForm(BSModalForm):
    class Meta:
        model = Treasuries
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

######### End Treasuries

######### Treasuries Orders
class TreasuriesOrdersForm(BSModalForm):
    orderdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    approvaldate = forms.DateField(widget=forms.DateInput (attrs={'type': 'date'}), required=False,disabled=True)

    class Meta:
        model = TreasuriesOrders
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Treasuries Orders


######### Treasuries Orders Approval
class TreasuriesOrdersApprovalForm(BSModalForm):
    orderdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False )
    class Meta:
        model = TreasuriesOrders
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Treasuries Orders Approval


######### Ledger Payments
class LedgerPaymentsForm(BSModalForm):
    paymentdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False )
    class Meta:
        model = LedgerPayments
        exclude = ('transtype','number','paymentdate','ledger','costcenter1','costcenter2','costcenter3','costcenter3','amount')



class LedgerPaymentsLineForm(forms.ModelForm):
    class Meta:
        model = LedgerPaymentsLine
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
        super(LedgerPaymentsLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


LedgerPaymentsLineFormSet = inlineformset_factory(LedgerPayments, LedgerPaymentsLine ,form=LedgerPaymentsLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


######### End Ledger Payments
