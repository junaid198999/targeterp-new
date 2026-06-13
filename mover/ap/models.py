from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency,Salesman
from gl.models import Ledger,TransTypes,CostCenters,TreasuriesOrders
from sy.models import *
#PaymentsMethods,LookUp,Languages,AgingStyles,PaymentsTearms,BusinessActivitiesTypes ,AddressesTypes,ContactsTypes
from django.utils.translation import get_language
from django.db.models import Q

class VendorsCategories(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(blank=True, null=True,max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

"""
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='ledgerscategories_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(blank=True, null=True,auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='ledgerscategories_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""

# Class = Channel
class VendorsClasses(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    isdefault = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Default"))
    buyer = models.ForeignKey(User,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Buyer"))
    currency = models.ForeignKey(Currency,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Currency"))
    paymenttearm = models.ForeignKey(PaymentsTearms,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Payments Tearms"))
    language = models.ForeignKey(Languages,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Language"))
    agingstyle = models.ForeignKey(AgingStyles,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Aging Style"))
    apledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("AP. Ledger"))
    creditlimit = models.DecimalField(decimal_places=1, max_digits=12,blank=False, null=True, verbose_name =_("Credit Limit"))
    creditdays = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Credit Days"))
    allowchaneged = models.BooleanField(default=False,blank=True, null=False, verbose_name=_("Allow Change Class info"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class BuyersGroups(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(blank=True, null=True,max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname




class Buyers(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(blank=True, null=True,max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    email = models.EmailField(max_length=100, blank=True,null=True, verbose_name =_("Email"))
    reportingto = models.ForeignKey('self', on_delete=models.PROTECT, blank=False, null=True, related_name='Buyers_ReportingTo', verbose_name =_("Reporting To"))
    user = models.ForeignKey(User,blank=False,null=True, on_delete=models.PROTECT, verbose_name =_("User"))
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name =_("Mobile"))
    buyergroup = models.ForeignKey(BuyersGroups,blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Buyer Group"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))


    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



# Vendors
class Vendors(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    shortengname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Short Eng Name"))
    shortarbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Short Arb Name"))
    parent = models.ForeignKey('self',blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Parent vendor"))
    startbusinessdate = models.DateField(blank=True, null=True, verbose_name =_("Start Business Date"))
    status = models.ForeignKey(LookUp,related_name='vendor_status',limit_choices_to={'keyname': 'AccountStatus'}, blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    vendorcategory = models.ForeignKey(VendorsCategories,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("vendor Category"))
    vendorclass = models.ForeignKey(VendorsClasses,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("vendor Class"))
    currency = models.ForeignKey(Currency,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Currency"))
    buyer = models.ForeignKey(Buyers,related_name='Vendors_Buyer',blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Buyer"))
    paymenttearm = models.ForeignKey(PaymentsTearms,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Payments Tearms"))
    agingstyle = models.ForeignKey(AgingStyles,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Aging Style"))
    creditlimit = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Credit Limit"))
    creditdays = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Credit Days"))
    mandatorycreditlimit = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Mandatory Credit Limit"))
    allowtarget = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Allow Target"))
    noofemployees = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("No Of Employees"))
    vatgroup = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("VAT Group"))
    vatregnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("VAT Registration Number"))
    iscash = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Cash vendor"))
    iscredit = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Credit vendor"))
    language = models.ForeignKey(Languages,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Language"))
    apledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("AP. Ledger"))
    accountsize = models.ForeignKey(LookUp,blank=True,limit_choices_to={'keyname': 'AccountSize'},related_name='vendor_accountsize', null=True,  on_delete=models.PROTECT, verbose_name=_("Account Size"))
    businessactivitytype = models.ForeignKey(BusinessActivitiesTypes,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Business Activity Type"))
    allowaccountentry = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Account Entry"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class VendorsAddresses(models.Model):
    vendor =models.ForeignKey(Vendors, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("vendor"))
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


class VendorsContacts(models.Model):
    vendor = models.ForeignKey(Vendors, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("vendor"))
    #contacttype = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Contact Type"))
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


class VendorsJour(models.Model):
    transtype = models.ForeignKey(TransTypes, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    journalnumber = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name =_("Journal Number"))
    journaldate = models.DateField(blank=True, null=True,verbose_name=_("Journal Date"))
    journalyear = models.CharField(max_length=4, blank=True, null=True, verbose_name=_("Journal Year"))
    journalmonth = models.CharField(max_length=2, blank=True, null=True, verbose_name=_("Journal Month"))
    sequence = models.IntegerField( blank=True, null=True, verbose_name=_("Sequence"))
    reference = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference"))
    reference1 = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference1"))
    reference2 = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference1"))
    islocked = models.BooleanField(default=False,blank=True, verbose_name=_("Is Locked"))
    totalamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total Amount"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    paymentid = models.IntegerField( blank=True, null=True,  verbose_name=_("Vendor Payment ID"))
    fiscalyearperiod = models.IntegerField( blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    confirmdate = models.DateField(blank=True, null=True,verbose_name=_("Confirm Date"))
    postdate = models.DateField(blank=True, null=True,verbose_name=_("Post Date"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='VendorsJour_created_by', on_delete=models.PROTECT, verbose_name =_("Created By"))
    status = models.ForeignKey(LookUp,related_name='VendorsJour_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    operation = models.ForeignKey('inv.operations', blank = True, null = True, related_name = 'VendorsJour_operation', on_delete = models.PROTECT, verbose_name = _("Operation"))
    created_date = models.DateField(blank=True, null=True,verbose_name=_("Created Date"))
    itemtransid = models.IntegerField( blank=True, null=True,  verbose_name=_("Item Trans ID"))


    class Meta:
        ordering = ['journalnumber']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.journalnumber
"""
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='TransTypes_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='TransTypes_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""

class VendorsJourLine(models.Model):
    vendorjour = models.ForeignKey(VendorsJour, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor Jour"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    accounttype = models.ForeignKey(LookUp,related_name='VendorsJourLine_AccountType', limit_choices_to=Q(keyid= 90001) | Q(keyid=90002), blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Ledger"))
    vendor = models.ForeignKey(Vendors,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='VendorsJourLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='VendorsJourLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='VendorsJourLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='VendorsJourLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))
    qty = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("qty"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    reverse = models.IntegerField( blank=True, null=True,  verbose_name =_("Reverse"))
    debitamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Debit Amount"))
    creditamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Credit Amount"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount (Debit - Credit)"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




class VendorCostBalances(models.Model):
    serial = models.IntegerField(blank=True, null=True,unique=True,  verbose_name=_("serial"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    vendor = models.ForeignKey(Vendors, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='VendorsCostBalances_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='VendorsCostBalances_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='VendorsCostBalances_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='VendorsCostBalances_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    dramount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Debit Amount"))
    cramount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Credit Amount"))
    dramountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Debit Amount FC"))
    cramountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Credit Amount FC"))
    lastvendortrans = models.IntegerField(blank=True, null=True,verbose_name=_("Last Vendor Trans"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk
"""
    #fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("FiscalYearsPeriods"))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='TransTypes_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='TransTypes_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""


class VendorsPayments(models.Model):
    transtype = models.ForeignKey(TransTypes  , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    number = models.IntegerField(blank=True, null=True,unique=True,  verbose_name=_("Payment Number"))
    paymentdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Payment Date"))
    status = models.ForeignKey(LookUp,related_name='VendorsPayments_Status', limit_choices_to={'keyname': 'PaymentStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    treasuryorder=models.ForeignKey(TreasuriesOrders, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Order"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    vendor = models.ForeignKey(Vendors, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='VendorsPayments_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='VendorsPayments_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='VendorsPayments_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='VendorsPayments_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    isposted = models.BooleanField(blank=False, null=False, verbose_name=_("Is Posted"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    paymentdirection = models.ForeignKey(LookUp,related_name='VendorsPayments_PaymentDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    paymentmethod = models.ForeignKey(PaymentsMethods,related_name='VendorsPayments_Paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    currency = models.ForeignKey(Currency,related_name='VendorsPayments_Currency', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    created_by = models.ForeignKey(User, blank=True, null=True,related_name='VendorsPayments_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.number
"""
    #fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("FiscalYearsPeriods"))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='TransTypes_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='TransTypes_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""


class VendorsPaymentsLine(models.Model):
    vendorpayment= models.ForeignKey(VendorsPayments, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor Payment"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    vendor = models.ForeignKey(Vendors,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='VendorsPaymentsLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='VendorsPaymentsLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='VendorsPaymentsLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='VendorsPaymentsLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount FC"))
    accounttype = models.ForeignKey(LookUp,related_name='VendorsPaymentsLine_accounttype', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True} ,related_name='VendorsPaymentsLine_account', blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.ledger




class VendorsTrans(models.Model):

    transtype =  models.ForeignKey(TransTypes,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    vendor = models.ForeignKey(Vendors,related_name='VendorsTrans_vendor', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='VendorsTrans_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='VendorsTrans_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='VendorsTrans_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='VendorsTrans_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    transdate = models.DateField(blank=True, null=True,verbose_name =_("Trans Date"))
    docnumber = models.CharField(max_length=50, blank=False, null=False, verbose_name =_("Doc Number"))
    vendorjour = models.ForeignKey(VendorsJour,related_name='VendorsTrans_LedgerJour', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendors Jour"))
    vendortrans = models.IntegerField( blank=True, null=True,  verbose_name=_("Vendor Trans"))
    operationid = models.IntegerField( blank=True, null=True, verbose_name=_("Operation ID"))
    payment = models.ForeignKey(VendorsPayments, blank=True, null=True, on_delete=models.PROTECT,  verbose_name =_("Vendors Payment Key"))
    engdesc = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Desc"))
    arbdesc = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Desc"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=False, null=False, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=False, null=False, verbose_name =_("Amount FC"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    closedate = models.DateField(blank=True, null=True,verbose_name =_("Close Date"))
    approvaldate = models.DateTimeField(blank=True, null=True,verbose_name =_("Approval Date"))
    approvalby = models.ForeignKey(User, blank=True, null=True,related_name='VendorsTrans_approvalby', on_delete=models.CASCADE, verbose_name =_("Approval By"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    postby = models.ForeignKey(User, blank=True, null=True,related_name='VendorsTrans_PostBy', on_delete=models.CASCADE, verbose_name =_("Post By"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='VendorsTrans_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))
    settleamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Settlement Amount"))
    lastsettledate = models.DateTimeField(blank=True, null=True,verbose_name =_("Last Settle Date"))
    created_date = models.DateTimeField(blank=True, null=True,verbose_name =_("Created Date"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk
"""
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='costcenters_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='costcenters_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""




