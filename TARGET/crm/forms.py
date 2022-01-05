from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from django import forms
from django_select2.forms import Select2Widget
from djangoformsetjs.utils import formset_media_js

from .models import *

from bootstrap_modal_forms.forms import BSModalForm
from TARGET.users.models import User
from django.contrib.auth.models import Permission, Group
from TARGET.users.forms import UserCreationForm, UserChangeForm
from django.forms.models import BaseInlineFormSet

from .utils.forms import is_form_persisted, is_empty_form
from django_select2.forms import Select2MultipleWidget

from inv.models import InventoriesLocations , OperationsTypes
from gl.models import TransTypes
class ExtendUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'picture' )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ExtendUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','thumb', 'picture' )

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user

class ExtendGroupCreationForm(UserCreationForm):
    class Meta:
        model = Group
        fields = ('name','id')

    def save(self, commit=True):
        group = super().save(commit=False)

        group.name = self.cleaned_data['name']

        if commit:
            group.save()
        return group

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SalesmanForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = '__all__'

class SalesmanEditForm(BSModalForm):
    class Meta:
        model = Salesman
        fields = '__all__'



class ChannelForm(BSModalForm):
    class Meta:
        model = Channel
        exclude = ['timestamp']

class ExpenseTypeForm(BSModalForm):
    class Meta:
        model = ExpenseType
        exclude = ['timestamp']

class ExpenseForm(BSModalForm):
    class Meta:
        model = Expense
        exclude = ['timestamp']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'picture')

class UserPermissions(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),
                                                      widget=FilteredSelectMultiple("user_permissions",
                                                                                    is_stacked=True))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                                      widget=FilteredSelectMultiple("groups",
                                                                                    is_stacked=True))

    class Meta:
        model = User
        fields = ('username', 'user_permissions','groups', 'is_superuser')


class GroupPermissions(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('permissions','name')

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name','id')




class UserPermissionForm(BSModalForm):
    class Meta:
        model = Permission
        exclude = ['timestamp']



class WarehouseTypeForm(BSModalForm):
    class Meta:
        model = WarehouseType
        exclude = ['timestamp']


class WarehouseForm(BSModalForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False )
    class Meta:
        model = Warehouse
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class CountryForm(BSModalForm):
    class Meta:
        model = Country
        exclude = ['timestamp']


class UomForm(BSModalForm):
    class Meta:
        model = Uom

        exclude = ['timestamp']


class AreaForm(BSModalForm):
    class Meta:
        model = Area
        exclude = ['timestamp']


class CityForm(BSModalForm):
    class Meta:
        model = City
        exclude = ['timestamp']


class CustomerForm(BSModalForm):
    class Meta:
        model = Customer
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['area'].queryset = Area.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.country.area_set.order_by('name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'city' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['city'].queryset = City.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty District queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.area.city_set.order_by('name')

class SpecialtyForm(BSModalForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False )
    class Meta:
        model = Specialty
        exclude = ['timestamp']

class DoctorForm(BSModalForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False )
    class Meta:
        model = Doctor
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account1'].queryset = Customer.objects.filter(status=1)
        self.fields['account2'].queryset = Customer.objects.filter(status=1)

class VisitForm(BSModalForm):

    class Meta:
        model = DoctorVisits
        exclude = ['timestamp']

class ClassForm(BSModalForm):
    class Meta:
        model = Class
        exclude = ['timestamp']

class PharmacyCategoryForm(BSModalForm):
    class Meta:
        model = PharmacyCategory
        exclude = ['timestamp']

class PharmacyForm(BSModalForm):
    class Meta:
        model = Pharmacy
        exclude = ['timestamp']

class BranchForm(BSModalForm):
    class Meta:
        model = Branch
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['area'].queryset = Area.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.country.area_set.order_by('name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'city' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['city'].queryset = City.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty District queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.area.city_set.order_by('name')


class CategoryForm(BSModalForm):
    class Meta:
        model = Category
        exclude = ['timestamp']

class BrandForm(BSModalForm):
    class Meta:
        model = Brand
        exclude = ['timestamp']


class ProductForm(BSModalForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}), required=False)

    class Meta:
        model = Product
        exclude = ['timestamp']


class AccountForm(BSModalForm):
    class Meta:
        model = Account
        exclude = ['timestamp']


class CalenderForm(BSModalForm):
    class Meta:
        model = Calender
        exclude = ['timestamp']

class CompanyForm(BSModalForm):
    class Meta:
        model = Company
        exclude = ['timestamp']

class AccountingChildForm(BSModalForm):
    class Meta:
        model = AccountingChild
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super(AccountingChildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False)


class VendorForm(BSModalForm):
    class Meta:
        model = Vendor
        exclude = ['timestamp']

class NotificationForm(BSModalForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False)

    class Meta:
        model = Notification
        exclude = ['created_date']

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['from_user'].widget.attrs['readonly'] = True

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        exclude = ()

class PurchaseOrderProductsForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True

PurchaseOrderProductsFormSet = inlineformset_factory(PurchaseOrder, PurchaseProduct,form=PurchaseOrderProductsForm, extra=0, min_num=1, validate_min=True)


class PurchaseReturnOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturnOrder
        exclude = ()

class PurchaseReturnOrderProductsForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturnProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(PurchaseReturnOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True

PurchaseReturnOrderProductsFormSet = inlineformset_factory(PurchaseReturnOrder, PurchaseReturnProduct,form=PurchaseReturnOrderProductsForm, extra=0, min_num=1, validate_min=True)


class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ()


class SalesOrderProductsForm(forms.ModelForm):
    class Meta:
        model = SalesProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(SalesOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True


SalesOrderProductsFormSet = inlineformset_factory(SalesOrder, SalesProduct,form=SalesOrderProductsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ()


class ContractProductsForm(forms.ModelForm):
    class Meta:
        model = ContractProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'p_bonus_uint': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(ContractProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


ContractProductsFormSet = inlineformset_factory(Contract, ContractProduct,form=ContractProductsForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class AccTransactionsForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ()

class AccTransactionsDetailsForm(forms.ModelForm):
    class Meta:
        model = AccTransactions
        exclude = ()

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(AccTransactionsDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


AccTransactionsDetailsFormSet = inlineformset_factory(AccTransactions, AccTransactionsDetails,form=AccTransactionsDetailsForm, extra=0, min_num=1, validate_min=True, can_delete=True)



class SalesReturnOrderForm(forms.ModelForm):
    class Meta:
        model = SalesReturnOrder
        exclude = ()

class SalesReturnOrderProductsForm(forms.ModelForm):
    class Meta:
        model = SalesReturnProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(SalesReturnOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['discount'].widget.attrs['readonly'] = True

SalesReturnOrderProductsFormSet = inlineformset_factory(SalesReturnOrder, SalesReturnProduct,form=SalesReturnOrderProductsForm, extra=0, min_num=1, validate_min=True)




class TransferOrderForm(forms.ModelForm):
    class Meta:
        model = TransferOrder
        exclude = ()

class TransferOrderProductsForm(forms.ModelForm):
    class Meta:
        model = TransferProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'from_warehouse': Select2Widget,
            'to_warehouse': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TransferOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TransferOrderProductsFormSet = inlineformset_factory(TransferOrder, TransferProduct,form=TransferOrderProductsForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksold
        exclude = ()

class TargetBuildingBlocksProductsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksProducts
        exclude = ()
        widgets = {
            'channel': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['s_total'].widget.attrs['readonly'] = True

TargetBuildingBlocksProductsFormSet = inlineformset_factory(TargetBuildingBlocksold, TargetBuildingBlocksProducts,form=TargetBuildingBlocksProductsForm, extra=0, min_num=1, validate_min=True)

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

TargetBuildingBlocksExceptFormSet = inlineformset_factory(TargetBuildingBlocksold, TargetBuildingBlocksExeption,form=TargetBuildingBlocksExpetionForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksAccountsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksAccounts
        exclude = ()

class TargetBuildingBlocksAccountsProductsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksAccountsProducts
        exclude = ()
        widgets = {
            'product': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksAccountsProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetBuildingBlocksAccountsProductsFormSet = inlineformset_factory(TargetBuildingBlocksAccounts, TargetBuildingBlocksAccountsProducts,form=TargetBuildingBlocksAccountsProductsForm, extra=0, min_num=1, validate_min=True)

class TargetBuildingBlocksChannelsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksChannels
        exclude = ()

class TargetBuildingBlocksChannelsProductsForm(forms.ModelForm):
    class Meta:
        model = TargetBuildingBlocksChannelsProducts
        exclude = ()
        widgets = {
            'product': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetBuildingBlocksChannelsProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetBuildingBlocksChannelsProductsFormSet = inlineformset_factory(TargetBuildingBlocksChannels, TargetBuildingBlocksChannelsProducts,form=TargetBuildingBlocksChannelsProductsForm, extra=0, min_num=1, validate_min=True)

class TargetCategoryChannelsForm(forms.ModelForm):
    class Meta:
        model = TargetCategoryChannels
        exclude = ()

class TargetCategoryChannelsProductsForm(forms.ModelForm):
    class Meta:
        model = TargetCategoryChannelsProducts
        exclude = ()
        widgets = {
            'category': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(TargetCategoryChannelsProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

TargetCategoryChannelsProductsFormSet = inlineformset_factory(TargetCategoryChannels, TargetCategoryChannelsProducts,form=TargetCategoryChannelsProductsForm, extra=0, min_num=1, validate_min=True)

class FinancialYearForm(BSModalForm):
    class Meta:
        model = FinancialYear
        exclude = ['timestamp']

class TransactionsForm(BSModalForm):
    class Meta:
        model = Transactions
        exclude = ['timestamp']

class ProductUnitsForm(BSModalForm):
    class Meta:
        model = UnitsName
        exclude = ['timestamp']

class CollectionForm(BSModalForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False)

    class Meta:
        model = Collection
        exclude = ['timestamp']

class CreditNoteForm(BSModalForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), required=False)

    class Meta:
        model = CreditNote
        exclude = ['timestamp']

class CurrencyForm(BSModalForm):

    class Meta:
        model = Currency
        exclude = ['timestamp']


class LeadForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    status_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    lead_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)

    class Meta:
        model = Lead
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class OpportunityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)

    class Meta:
        model = Opportunity
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class OpportunityProductsForm(forms.ModelForm):
    class Meta:
        model = SalesProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(OpportunityProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True

OpportunityProductsFormSet = inlineformset_factory(Opportunity, OpportunityProduct,form=OpportunityProductsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

class ActualVisitForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)

    class Meta:
        model = ActualVisit
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ActualVisitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class ActivityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)

    class Meta:
        model = Activities
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ()

class CommissionDetailsForm(forms.ModelForm):
    class Meta:
        model = Commission_Details
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(CommissionDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

CommissionDetailsFormFormSet = inlineformset_factory(Commission, Commission_Details,form=CommissionDetailsForm, extra=0, min_num=1, validate_min=True)

class Commission_CalcForm(forms.ModelForm):
    class Meta:
        model = Commission_Calc
        exclude = ()

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class QuestionForm(BSModalForm):
    class Meta:
        model = Question
        exclude = ['timestamp']

class QuestionFieldsForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(QuestionFieldsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class QuestionFieldsChildForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(QuestionFieldsChildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

QuestionFieldsFormFormSet = inlineformset_factory(
    QuestionFields,
    QuestionFieldChild,
    fields=('title',),
    form=QuestionFieldsForm,
    extra=1)

class BaseQuestionFieldChildFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested = QuestionFieldsFormFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='questionfieldchild-%s-%s' % (
                form.prefix,
                QuestionFieldsFormFormSet.get_default_prefix()),
        )

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('You are trying to add image(s) to a book which '
                            'does not yet exist. Please add information '
                            'about the book and choose the image file(s) again.'))

    def save(self, commit=True):

        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Images to a new Book whose data we haven't entered?
        """
        if not hasattr(form, 'nested'):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


QuestionWithFieldChildFormset = inlineformset_factory(
    Question,
    QuestionFields,
    formset= BaseQuestionFieldChildFormset,
    fields=('title', 'type', ),
    extra=1,
)

class QuestionAnswersForm(forms.ModelForm):
    class Meta:
        model = QuestionA
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(QuestionAnswersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

QuestionAnswersFormSet = inlineformset_factory(
    QuestionAFields,
    QuestionAnswers,
    fields=('answer','questionfieldchilds_title','id'),
    form=QuestionFieldsForm,
    extra=0)

class BaseQuestionAnswersFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested = QuestionAnswersFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='question_fields_answer-%s-%s' % (
                form.prefix,
                QuestionAnswersFormSet.get_default_prefix()),
        )

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('You are trying to add image(s) to a book which '
                            'does not yet exist. Please add information '
                            'about the book and choose the image file(s) again.'))

    def save(self, commit=True):
        result = super().save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        if not hasattr(form, 'nested'):
            return False

        if is_form_persisted(form):
            return False

        if not is_empty_form(form):
            return False

        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


QuestionWithAnswersFormset = inlineformset_factory(
    QuestionA,
    QuestionAFields,
    formset= BaseQuestionAnswersFormset,
    fields=('title', 'type', ),
    extra=0,
)

class SalesmanGroupsForm(BSModalForm):
    class Meta:
        model = SalesmanGroups
        exclude = ['timestamp']

class SampleOrderForm(forms.ModelForm):
    class Meta:
        model = SampleOrder
        exclude = ()

class SampleOrderProductsForm(forms.ModelForm):
    class Meta:
        model = SampleProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(SampleOrderProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['product'].queryset = Product.objects.filter(Q(price=0) | Q(price=None))


SampleOrderProductsFormSet = inlineformset_factory(SampleOrder, SampleProduct,form=SampleOrderProductsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

class CustomerSalesOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerSalesOrder
        exclude = ()


class CustomerSalesProductsForm(forms.ModelForm):
    class Meta:
        model = CustomerSalesProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(CustomerSalesProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['subtotal'].widget.attrs['readonly'] = True


CustomerSalesProductFormSet = inlineformset_factory(CustomerSalesOrder, CustomerSalesProduct,form=CustomerSalesProductsForm, extra=0, min_num=1, validate_min=True, can_delete=True)

class SubDomainForm(BSModalForm):
    class Meta:
        model = DemoAccounts
        exclude = ()


###----------------------------- Form  khaldoun



class SalesDeliveryForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ()

class SalesDeliveryProductsForm(forms.ModelForm):
    class Meta:
        model = SalesProduct
        exclude = ()
        widgets = {
            'product': Select2Widget,
            'uom': Select2Widget,
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(SalesDeliveryProductsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
#        self.fields['subtotal'].widget.attrs['readonly'] = True
 #       self.fields['discount'].widget.attrs['readonly'] = True

SalesDeliveryProductsFormSet = inlineformset_factory(SalesDelivery, SalesDeliveryProduct,form=SalesDeliveryProductsForm, extra=0, min_num=1, validate_min=True)



class UserAdditionalProfileForm(forms.ModelForm):
    class Meta:
        model = UserAdditionalProfile
        exclude = ['timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



######### UserBusinessRoles
class UserBusinessRolesForm(forms.ModelForm):
    invlocation = forms.ModelMultipleChoiceField(queryset= InventoriesLocations.objects.all(), widget=Select2MultipleWidget ,required=False )
    class Meta:
        model = UserBusinessRoles
        exclude = ()

class UserBusinessRolesOTLineForm(forms.ModelForm):
    class Meta:
        model = UserBusinessRolesOTLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(UserBusinessRolesOTLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


UserBusinessRolesOTLineFormSet = inlineformset_factory(UserBusinessRoles, UserBusinessRolesOTLine ,form=UserBusinessRolesOTLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)


class UserBusinessRolesTTLineForm(forms.ModelForm):
    class Meta:
        model = UserBusinessRolesTTLine
        exclude = ()
        widgets = {
        }
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    def __init__(self, *args, **kwargs):
        super(UserBusinessRolesTTLineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


UserBusinessRolesTTLineFormSet = inlineformset_factory(UserBusinessRoles, UserBusinessRolesTTLine ,form=UserBusinessRolesTTLineForm, extra=0, min_num=1, validate_min=True, can_delete=True)



######### End UserBusinessRoles




class SalesRetrunDeliveryForm(forms.ModelForm):
    class Meta:
        model = SalesDelivery
        exclude = ()
