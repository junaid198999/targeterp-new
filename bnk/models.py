from django.db import models

# Create your models here.
from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency,Salesman
from gl.models import Ledger,TransTypes,CostCenters,TreasuriesOrders
from sy.models import *
from ar.models import Customers
from ap.models import Vendors
from django.db.models import Q

#PaymentsMethods,LookUp,Languages,AgingStyles,PaymentsTearms,BusinessActivitiesTypes ,AddressesTypes,ContactsTypes
from django.utils.translation import get_language
from django.db.models import Q

# Bank Groups
class BanksGroups(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

# Bank Groups

class Banks(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    shortengname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Short Eng Name"))
    shortarbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Short Arb Name"))
    bankgroup = models.ForeignKey(BanksGroups,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Bank Group"))
    accountnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Bank Account Number"))
    iban = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("IBAN Number"))
    status = models.ForeignKey(LookUp,related_name='Bank_Status', limit_choices_to={'keyname': 'BankStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Status"))
    reconciliationenabled = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Reconciliation Enabled"))
    bankledger = models.ForeignKey(Ledger,related_name='Banks_bankledger',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Account Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='Banks_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='Banks_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='Banks_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='Banks_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    commissionledger = models.ForeignKey(Ledger,related_name='Banks_commissionledger',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Commission Ledger"))
    commissioncostcenter1 = models.ForeignKey(CostCenters,related_name='Banks_Commissioncc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Commission Cost center 1"))
    commissioncostcenter2 = models.ForeignKey(CostCenters,related_name='Banks_Commissioncc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Commission Cost center 2"))
    commissioncostcenter3 = models.ForeignKey(CostCenters,related_name='Banks_Commissioncc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Commission Cost center 3"))
    commissioncostcenter4 = models.ForeignKey(CostCenters,related_name='Banks_Commissioncc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Commission Cost center 4"))
    currency = models.ForeignKey(Currency,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Currency"))
    prefixchequeno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Prefix Cheque Number"))
    suffixchequeno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Suffix Cheque Number"))

    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class BanksAddresses(models.Model):
    bank =models.ForeignKey(Banks, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Bank"))
    addresstype = models.ForeignKey(AddressesTypes, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Address Type"))
    country = models.ForeignKey(Countries, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Country"))
    city = models.ForeignKey(Cities, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("City"))
    district = models.ForeignKey(Districts, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("District"))
    address1 = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Address 1"))
    address2 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Address 2"))
    address3 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("address 3"))
    street = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Street"))
    latitudes = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Latitudes"))
    longitudes = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Longitudes"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class BanksContacts(models.Model):
    bank = models.ForeignKey(Banks, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    contacttype = models.ForeignKey(ContactsTypes, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Contact Type"))
    value = models.CharField(max_length=300, verbose_name =_("Value"))
    inactive = models.BooleanField(blank=False, null=False, verbose_name=_("Inactive"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class BanksCreditCardsTypes(models.Model):
    bank = models.ForeignKey(Banks, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank"))
    creditcardtype = models.ForeignKey(CreditCardsTypes, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Credit Cards Type"))
    commissionpercent = models.DecimalField(decimal_places=4, max_digits=22, blank=True, null=True, verbose_name =_("Commission Percent"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class BanksCheques(models.Model):
    bank = models.ForeignKey(Banks, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank"))
    chequebooknum = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Cheque Book Num"))
    chequenum = models.CharField(max_length=300,blank=True, null=True, verbose_name =_("Cheque Num"))
    chequeserial = models.PositiveIntegerField( blank=True, null=True,  verbose_name=_("Cheque Serial"))
    status = models.ForeignKey(LookUp,related_name='BanksCheques_Status', limit_choices_to={'keyname': 'ChequeStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cheque Status"))
    statusdate = models.DateField(blank=True, null=True,verbose_name=_("Status Date"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    beneficiaryname= models.CharField(max_length=300,blank=True, null=True, verbose_name =_("Beneficiary Name"))
    beneficiarycompanyname= models.CharField(max_length=300,blank=True, null=True, verbose_name =_("Beneficiary Company Name"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount Foreign Currency"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    chequedate = models.DateField(blank=True, null=True,verbose_name=_("Cheque Date"))
    chequeduedate = models.DateField(blank=True, null=True,verbose_name=_("Cheque Due Date"))
    accounttype = models.ForeignKey(LookUp,related_name='BanksCheques_AccountType', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Ledger"))
    customer = models.ForeignKey(Customers,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    vendor = models.ForeignKey(Vendors,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    refpaymentid = models.IntegerField( blank=True, null=True,  verbose_name=_("Reference Payment ID"))
    created_date = models.DateField(blank=True, null=True,verbose_name=_("Created Date"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='BanksCheques_created_by', on_delete=models.PROTECT, verbose_name =_("Created By"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class BanksDocumentsUnderProcess(models.Model):
    sourcename = models.CharField(max_length=300,blank=True, null=True, verbose_name =_("Source Table Name"))
    sourceid = models.PositiveIntegerField( blank=True, null=True,  verbose_name=_("Source ID"))
    bankrefno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Bank Reference Number"))
    bankrefdate = models.DateField(blank=True, null=True,verbose_name =_("Bank Reference Date"))
    isclose = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Close"))
    created_date = models.DateField(auto_now_add=True,blank=True, null=True,verbose_name=_("Created Date"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='BanksDocumentsUnderProcess_created_by', on_delete=models.PROTECT, verbose_name =_("Created By"))
    updated_date = models.DateField(auto_now_add=True,blank=True, null=True,verbose_name=_("Updated Date"))
    updated_by = models.ForeignKey(User,blank=True, null=True, related_name='BanksDocumentsUnderProcess_updated_by', on_delete=models.PROTECT, verbose_name =_("Updated_by By"))
    paymentmethod = models.ForeignKey(PaymentsMethods,related_name='BanksDocumentsUnderProcess_Paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    paymentdirection = models.ForeignKey(LookUp,related_name='BanksDocumentsUnderProcess_PaymentDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))

    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


