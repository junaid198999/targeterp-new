from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.forms.models import inlineformset_factory, HiddenInput
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from django_select2.forms import Select2MultipleWidget
from djangoformsetjs.utils import formset_media_js
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field

######### Units

class UnitsForm(BSModalForm):
    class Meta:
        model = Units
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Units

######### Warehouses

class WarehousesForm(BSModalForm):
    class Meta:
        model = Warehouses
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End Warehouses


######### StorageMethodsTypes

class StorageMethodsTypesForm(BSModalForm):
    class Meta:
        model = StorageMethodsTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End StorageMethodsTypes

######### InventoriesLocationsTypes

class InventoriesLocationsTypesForm(BSModalForm):
    class Meta:
        model = InventoriesLocationsTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End InventoriesLocationsTypes

######### InventoriesLocations

class InventoriesLocationsForm(BSModalForm):
    class Meta:
        model = InventoriesLocations
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End InventoriesLocations

######### InventoriesBinLocations

class InventoriesBinLocationsForm(BSModalForm):
    class Meta:
        model = InventoriesBinLocations
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End InventoriesLocations


######### ItemsTypes

class ItemsTypesForm(BSModalForm):
    class Meta:
        model = ItemsTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End ItemsTypes


######### ItemsCategories

class ItemsCategoriesForm(BSModalForm):
    class Meta:
        model = ItemsCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End ItemsCategories


######### ItemsGroups

class ItemsGroupsForm(BSModalForm):
    class Meta:
        model = ItemsGroups
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End ItemsGroups

######### ItemsBrands
class ItemsBrandsForm(BSModalForm):
    class Meta:
        model = ItemsBrands
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End ItemsBrands

######### GenericNamesCategories
class GenericNamesCategoriesForm(BSModalForm):
    class Meta:
        model = GenericNamesCategories
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End GenericNamesCategories


######### GenericNames
class GenericNamesForm(BSModalForm):
    class Meta:
        model = GenericNames
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End GenericNames

######### ItemsClasses
class ItemsClassesForm(BSModalForm):

    class Meta:
        model = ItemsClasses
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End ItemsClasses

######### Items
class ItemsForm(forms.ModelForm):
    #baseuom =forms.IntegerField (widget=forms.TextInput(), required=False ,disabled=True)

    class Meta:
        model = Items
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['baseuom'].disabled = True
        self.helper.layout = Layout(


            )



class ItemsUOMForm(forms.ModelForm):
    class Meta:
        model = ItemsUOM
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(ItemsUOMForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

ItemsUOMFormSet = inlineformset_factory(Items, ItemsUOM ,form=ItemsUOMForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class ItemsInventoriesLocationsForm(forms.ModelForm):
    class Meta:
        model = ItemsInventoriesLocations
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(ItemsInventoriesLocationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

ItemsInventoriesLocationsFormSet = inlineformset_factory(Items, ItemsInventoriesLocations ,form=ItemsInventoriesLocationsForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class ItemsSeasonalityForm(forms.ModelForm):
    class Meta:
        model = ItemsSeasonality
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(ItemsSeasonalityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

ItemsSeasonalityFormSet = inlineformset_factory(Items, ItemsSeasonality ,form=ItemsSeasonalityForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Items

######### ExpensesTypes
class ExpensesTypesForm(BSModalForm):
    class Meta:
        model = ExpensesTypes
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
######### End ExpensesTypes

######### Agencies  Form
class AgenciesForm(forms.ModelForm):
    class Meta:
        model = Agencies
        exclude = []

class AgenciesExpensesLineForm(forms.ModelForm):
    class Meta:
        model = AgenciesExpensesLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(AgenciesExpensesLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

AgenciesExpensesLineFormSet = inlineformset_factory(Agencies, AgenciesExpensesLine  ,form=AgenciesExpensesLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Agencies  Form




######### OperationsTypes
class OperationsTypesForm(forms.ModelForm):

    possibleparent = forms.ModelMultipleChoiceField(queryset=OperationsTypes.objects.all(), widget=Select2MultipleWidget ,required=False )


    class Meta:
        model = OperationsTypes
        exclude = ()
        widgets = {
            #'ledgergoodsonway': Select2Widget,
            #'customer': Select2Widget,

        }


class OperationsTypesExpensesLineForm(forms.ModelForm):
    class Meta:
        model = OperationsTypesExpensesLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(OperationsTypesExpensesLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

OperationsTypesExpensesLineFormSet = inlineformset_factory(OperationsTypes, OperationsTypesExpensesLine ,form=OperationsTypesExpensesLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)

class OperationsTypesLineViewsForm(forms.ModelForm):
    class Meta:
        model = OperationsTypesLineViews
        exclude = ('operationtype',)
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(OperationsTypesLineViewsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


OperationsTypesLineViewsFormSet = inlineformset_factory(OperationsTypes, OperationsTypesLineViews ,form=OperationsTypesLineViewsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End OperationsTypes


######### Operations
class OperationsForm(forms.ModelForm):

    operationdate = forms.DateField(widget=forms.DateInput (attrs={'type': 'date','readonly':'readonly'}), required=False , disabled=True,initial=datetime.now().date() )
    statusdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date','readonly':'readonly'}), required=False,disabled=True,label="Status Date")
    number = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )


    netamount = forms.DecimalField (widget=forms.TextInput (attrs={'style': 'text-align:right;'}), required=False,disabled =True )
    taxamount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )
    grossamount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )
    expenseamount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )

    discamt1 = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )
    discamt2 = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )
    discamt3 = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=False )


    class Meta:
        model = Operations
        exclude = ()
        widgets = {
            #'ledger': Select2Widget,
            #'customer': Select2Widget,

        }


    def __init__(self, *args, **kwargs):
        super(OperationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['status'].disabled = True
        self.helper.layout = Layout(


            )
        #self.fields["status"].widget.attrs["disabled"] = "true"

        #self.fields["operationtype"].widget.attrs["hidden"] = "true"
        #self.helper.form_show_labels = False

class OperationsLineForm(forms.ModelForm):
    linetotal = forms.DecimalField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right','readonly':'readonly'}), required=False )
    price = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    originalprice = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right'}), required=False,disabled=True )
    quantity = forms.IntegerField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right'}), required=True,disabled=False )

    baseunitfactor = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    baseeequivalentquantity = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    baseunit = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    costprice = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    barcode = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )

    taxpercent = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    taxamount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )

    pricelist = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )
    unit = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )
    itemidentifier = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False,disabled =False )

    expiredate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'} ) , required=False )

    lotdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False )
    tax = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )

    print('form')
    class Meta:
        model = OperationsLine
        exclude = []
        widgets = {

        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        print('form __init__')
        super(OperationsLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.fields['price'].widget.attrs['readonly'] = False


OperationsLineFormSet = inlineformset_factory(Operations, OperationsLine ,form=OperationsLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)




class OperationsExpensesLineForm(forms.ModelForm):
    explinetotal = forms.DecimalField (widget=forms.TextInput(attrs={'type': 'number','class': 'text-right','readonly':'readonly'}), required=False )
    exptaxpercent = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    exptaxamount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'currency','class': 'text-right','readonly':'readonly'}), required=False,disabled =False )
    documentdate = forms.DateField(widget=forms.TextInput( attrs={'type': 'date'})  , required=False  )


    class Meta:
        model = OperationsExpensesLine
        exclude = []
        widgets = {

        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(OperationsExpensesLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False



OperationsExpensesLineFormSet = inlineformset_factory(Operations, OperationsExpensesLine ,form=OperationsExpensesLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Operations


######### Items Price List
class ItemsPLForm(forms.ModelForm):


    class Meta:
        model = Items
        fields = ('code', 'engname', 'arbname')
        exclude = ['']



class ItemsPriceListForm(forms.ModelForm):
    price = forms.DecimalField(widget=forms.TextInput(attrs={'style': 'text-align:right;'}), required=False)

    class Meta:
        model = ItemsPricesLists
        exclude = ('unit','item')
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            kwargs['instance'].price = kwargs['instance'].price.quantize(Decimal('0.01'))

        super(ItemsPriceListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['invlocation'].disabled = True
        self.fields['itemuom'].disabled = True
        self.fields['pricelevel'].disabled = True
        self.fields['invlocation'].initial = self.instance.invlocation
        self.fields['itemuom'].initial = self.instance.itemuom
        self.fields['pricelevel'].initial = self.instance.pricelevel



        #self.fields['price'].widget.attrs['class'] = 'price'
        #self.fields['price'].decimal_places = 2
        #self.fields['invlocation'].widget.attrs['disabled'] = True


ItemsPriceListFormSet = inlineformset_factory(Items, ItemsPricesLists  ,form=ItemsPriceListForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End Items Price List

######### WF Groups Form
class WFGroupsForm(forms.ModelForm):
    class Meta:
        model = WFGroups
        exclude = []

class WFGroupsUsersForm(forms.ModelForm):
    class Meta:
        model = WFGroupsUsers
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(WFGroupsUsersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

WFGroupsUsersFormSet = inlineformset_factory(WFGroups, WFGroupsUsers  ,form=WFGroupsUsersForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End WF Groups Form

######### WFActions Status

class WFActionsStatusForm(BSModalForm):
    class Meta:
        model = WFActionsStatus
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


######### End WFActions Status

######### WF Operations Cycles
class WFOperationsCyclesForm(forms.ModelForm):
    class Meta:
        model = WFOperationsCycles
        exclude = []

class WFOperationsCyclesLineForm(forms.ModelForm):
    class Meta:
        model = WFOperationsCyclesLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(WFOperationsCyclesLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

WFOperationsCyclesLineFormSet = inlineformset_factory(WFOperationsCycles, WFOperationsCyclesLine  ,form=WFOperationsCyclesLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)

######### End WF Operations Cycles


##-------- START TARGET FORMS
class TargetBuildingBlocksForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocks
        exclude = ()

class TargetBuildingBlocksItemsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksItems
        exclude = ()
        widgets = {
            #'channel': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksItemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['s_total'].widget.attrs['readonly'] = True

TargetBuildingBlocksItemsFormSet = inlineformset_factory(TargetBuildingBlocks, TargetBuildingBlocksItems,form=TargetBuildingBlocksItemsForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksExpetionForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksExeption
        exclude = ()

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksExpetionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetBuildingBlocksExceptFormSet = inlineformset_factory(TargetBuildingBlocks, TargetBuildingBlocksExeption,form=TargetBuildingBlocksExpetionForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksAccountsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksAccounts
        exclude = ()

class TargetBuildingBlocksAccountsItemsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksAccountsItems
        exclude = ()
        widgets = {
            #'item': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksAccountsItemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetBuildingBlocksAccountsItemsFormSet = inlineformset_factory(TargetBuildingBlocksAccounts, TargetBuildingBlocksAccountsItems,form=TargetBuildingBlocksAccountsItemsForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksChannelsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksChannels
        exclude = ()

class TargetBuildingBlocksChannelsItemsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksChannelsItems
        exclude = ()
        widgets = {
            #'item': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksChannelsItemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetBuildingBlocksChannelsItemsFormSet = inlineformset_factory(TargetBuildingBlocksChannels, TargetBuildingBlocksChannelsItems,form=TargetBuildingBlocksChannelsItemsForm, extra=0, min_num=1, validate_min=True)

##-------- END TARGET FORMS