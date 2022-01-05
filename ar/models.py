from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency,Salesman
from gl.models import Ledger,TransTypes,CostCenters,TreasuriesOrders,Treasuries
from sy.models import *


# from inv.models import Operations

#PaymentsMethods,LookUp,Languages,AgingStyles,PaymentsTearms,BusinessActivitiesTypes ,AddressesTypes,ContactsTypes
from django.utils.translation import get_language
from django.db.models import Q


class SalesmansGroups(models.Model):
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

class Salesmans(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(blank=True, null=True,max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    email = models.EmailField(max_length=100, blank=True,null=True, verbose_name =_("Email"))
    reportingto = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='Salesmans_ReportingTo', verbose_name =_("Reporting To"))
    treasurylink = models.ForeignKey(Treasuries, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Link"))
    user = models.ForeignKey(User,blank=False,null=True, on_delete=models.PROTECT, verbose_name =_("User"))
    iscashier = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Cashier"))
    iscollector = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Collector"))
    status = models.ForeignKey(LookUp,related_name='Salesmans_status',limit_choices_to={'keyname': 'AccountStatus'}, blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,related_name='Salesmans_statuschangedby',blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    ledgerdiff = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Differences Ledger"))
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name =_("Mobile"))
    noofvisitperday = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("No Of Visit Per Day"))
    salesmangroup = models.ForeignKey(SalesmansGroups,blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Salesman Group"))
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

class CustomersCategories(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
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
class CustomersClasses(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    isdefault = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Default"))
    salesperson = models.ForeignKey(Salesmans,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Salesman"))
    currency = models.ForeignKey(Currency,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Currency"))
    paymenttearm = models.ForeignKey(PaymentsTearms,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Payments Tearms"))
    language = models.ForeignKey(Languages,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Language"))
    agingstyle = models.ForeignKey(AgingStyles,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Aging Style"))
    arledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("AR. Ledger"))
    creditlimit = models.DecimalField(decimal_places=12, max_digits=30,blank=False, null=True, verbose_name =_("Credit Limit"))
    creditdays = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Credit Days"))
    allowchaneged = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Change Class info"))
    pricelevel = models.ForeignKey(PriceLevels,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Price level"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

# Class = Channel
class VisitsClasses(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    noofvisit = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("No Of Visits"))
    visitperiodminute= models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Visits Period Per minute"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Customers(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    shortengname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Short Eng Name"))
    shortarbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Short Arb Name"))
    parent = models.ForeignKey('self',blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Parent Customer"))
    startbusinessdate = models.DateField(blank=True, null=True, verbose_name =_("Start Business Date"))
    status = models.ForeignKey(LookUp,related_name='customer_status',limit_choices_to={'keyname': 'AccountStatus'}, blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    customercategory = models.ForeignKey(CustomersCategories,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Customer Category"))
    customerclass = models.ForeignKey(CustomersClasses,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Customer Channel"))
    visitclass = models.ForeignKey(VisitsClasses,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Visit Class"))
    currency = models.ForeignKey(Currency,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Currency"))
    salesperson = models.ForeignKey(Salesmans,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Salesman"))
    paymenttearm = models.ForeignKey(PaymentsTearms,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Payments Tearms"))
    agingstyle = models.ForeignKey(AgingStyles,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Aging Style"))
    creditlimit = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Credit Limit"))
    creditdays = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Credit Days"))
    mandatorycreditlimit = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Mandatory Credit Limit"))
    allowtarget = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Allow Target"))
    noofemployees = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("No Of Employees"))
    vatgroup = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("VAT Group"))
    vatregnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("VAT Registration Number"))
    iscash = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Cash Customer"))
    iscredit = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Credit Customer"))
    language = models.ForeignKey(Languages,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Language"))
    arledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("AR. Ledger"))
    accountsize = models.ForeignKey(LookUp,blank=True,limit_choices_to={'keyname': 'AccountSize'},related_name='customer_accountsize', null=True,  on_delete=models.PROTECT, verbose_name=_("Account Size"))
    businessactivitytype = models.ForeignKey(BusinessActivitiesTypes,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Business Activity Type"))
    allowaccountentry = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Account Entry"))
    cashdiscount = models.ForeignKey(CashDiscountsRoles,blank=True,related_name='customer_cashdiscount', null=True,  on_delete=models.PROTECT, verbose_name=_("Cash Discount"))
    allowcashdiscount = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Cash Discount"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class CustomersAddresses(models.Model):
    customer =models.ForeignKey(Customers, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
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


class CustomersContacts(models.Model):
    customer = models.ForeignKey(Customers, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
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



class CustomersJour(models.Model):
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
    totalamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Total Amount"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    paymentid = models.IntegerField( blank=True, null=True,  verbose_name=_("Customer Payment ID"))
    fiscalyearperiod = models.IntegerField( blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    confirmdate = models.DateField(blank=True, null=True,verbose_name=_("Confirm Date"))
    postdate = models.DateField(blank=True, null=True,verbose_name=_("Post Date"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='CustomersJour_created_by', on_delete=models.PROTECT, verbose_name =_("Created By"))
    status = models.ForeignKey(LookUp,related_name='CustomersJour_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    operation = models.ForeignKey('inv.operations', blank = True, null = True, related_name = 'CustomersJour_operation', on_delete = models.PROTECT, verbose_name = _("Operation"))
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

class CustomersJourLine(models.Model):
    customerjour = models.ForeignKey(CustomersJour, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer Jour"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    accounttype = models.ForeignKey(LookUp,related_name='CustomersJourLine_AccountType', limit_choices_to=Q(keyid= 90001) | Q(keyid=90003), blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Ledger"))
    customer = models.ForeignKey(Customers,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='CustomersJourLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='CustomersJourLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='CustomersJourLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='CustomersJourLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))
    qty = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("qty"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    reverse = models.IntegerField( blank=True, null=True,  verbose_name =_("Reverse"))
    debitamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Debit Amount"))
    creditamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Credit Amount"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount (Debit - Credit)"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




class CustomerCostBalances(models.Model):
    serial = models.IntegerField(blank=True, null=True,unique=True,  verbose_name=_("serial"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    customer = models.ForeignKey(Customers, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='CustomersCostBalances_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='CustomersCostBalances_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='CustomersCostBalances_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='CustomersCostBalances_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    dramount = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Debit Amount"))
    cramount = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Credit Amount"))
    dramountfc = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Debit Amount FC"))
    cramountfc = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Credit Amount FC"))
    lastcustomertrans = models.IntegerField(blank=True, null=True,verbose_name=_("Last Customer Trans"))
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

class CustomersPaymentsSchedule(models.Model):
    paymenttearm =  models.ForeignKey(PaymentsTearms,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Payment Tearm"))
    customer = models.ForeignKey(Customers,related_name='CustomersPaymentsSchedule_Customer', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    operation = models.ForeignKey('inv.Operations', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    operationdate = models.DateField(blank=True, null=True,verbose_name =_("Operation Date"))
    operationamount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Operation Amount"))
    operationamountfc = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Operation Amount FC"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    dueamount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Due Amount"))
    dueamountfc = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Due Amount FC"))
    paidamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Paid Amount"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    parent = models.ForeignKey('self',related_name='CustomersPaymentsSchedule_parent', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent Rec ID"))
    isclose = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Close"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='CustomersPaymentsSchedule_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    created_date = models.DateTimeField(blank=True, null=True,verbose_name =_("Created Date"))
    # status = models.ForeignKey(LookUp,related_name='CustomersPaymentsSchedule_status',limit_choices_to={'keyname': 'AccountStatus'}, blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Status"))
    # statusdate = models.DateField(blank=True, null=True,verbose_name =_("Status Date"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return str(self.pk)



class Collections(models.Model):
    number =models.CharField(max_length=20, blank=True, null=True,unique=True, verbose_name=_("Collection Number"))
    collectiondate = models.DateField(blank=True, null=True,verbose_name =_("Collection Date"))
    status = models.ForeignKey(LookUp,related_name='Collections_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Collection Status"))
    statusdate = models.DateField(blank=True, null=True,verbose_name =_("status Date"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    collector = models.ForeignKey(Salesmans, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Collector"))
    paymentmethod = models.ForeignKey(PaymentsMethods,related_name='Collections_Paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    customer = models.ForeignKey(Customers, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='Collections_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='Collections_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='Collections_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='Collections_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount"))
    currency = models.ForeignKey(Currency,related_name='Collections_Currency', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))

    chequenumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Cheque Number"))
    chequebankname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Cheque Bank Name"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    beneficiaryname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Beneficiary Name"))
    bankchequedestination  = models.ForeignKey('bnk.Banks',related_name='Collections_bankchequedestination', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Cheque Destination"))

    remittanceno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remittance NUmber"))
    fromaccountno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("From Account NUmber"))
    frombankname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("From Bank Name"))
    remittancedate = models.DateField(blank=True, null=True,verbose_name =_("Remittance Date"))
    bankdestination  = models.ForeignKey('bnk.Banks',related_name='Collections_bankdestination', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Remittance Destination"))

    creditcardtype  = models.ForeignKey(CreditCardsTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Credit Card Type"))
    creditcardnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Credit Card Number"))
    cvnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("CV Number"))
    expiredate = models.DateField(blank=True, null=True,verbose_name =_("Expire Date"))

    bankrefno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Bank Reference Number"))
    bankrefdate= models.DateField(blank=True, null=True,verbose_name =_("Bank Reference Date"))

    bankdocunderprocess  = models.ForeignKey('bnk.BanksDocumentsUnderProcess', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Doc. Under Process"))
    isclose = models.BooleanField(default=False,blank=True, null=False, verbose_name=_("Is Close"))
    islocked = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is IsLocked"))

    created_by = models.ForeignKey(User,blank=True, null=True, related_name='Collections_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return str(self.pk)

class CollectionsDuePayments(models.Model):
    collection = models.ForeignKey(Collections, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Collection"))
    customerpaymentschedule = models.ForeignKey(CustomersPaymentsSchedule, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Due Payment"))
    operationnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Number"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    dueamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Due Amount"))
    paidamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Paid Amount"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return str(self.pk)

class CustomersPayments(models.Model):
    transtype = models.ForeignKey(TransTypes  , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    number = models.CharField(max_length=20,blank=True, null=True,unique=True,  verbose_name=_("Payment Number"))
    paymentdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Payment Date"))
    status = models.ForeignKey(LookUp,related_name='CustomersPayments_Status', limit_choices_to={'keyname': 'PaymentStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    treasuryorder=models.ForeignKey(TreasuriesOrders, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Order"))
    collection=models.ForeignKey(Collections, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Collection"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    customer = models.ForeignKey(Customers, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='CustomersPayments_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='CustomersPayments_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='CustomersPayments_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='CustomersPayments_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount"))
    isposted = models.BooleanField(blank=False, null=False, verbose_name=_("Is Posted"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    paymentdirection = models.ForeignKey(LookUp,related_name='CustomersPayments_PaymentDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    paymentmethod = models.ForeignKey(PaymentsMethods,related_name='CustomersPayments_Paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    currency = models.ForeignKey(Currency,related_name='CustomersPayments_Currency', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='CustomersPayments_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))

    chequenumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Cheque Number"))
    chequebankname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Cheque Bank Name"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    beneficiaryname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Beneficiary Name"))

    remittanceno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remittance NUmber"))
    fromaccountno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("From Account NUmber"))
    frombankname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("From Bank Name"))
    remittancedate = models.DateField(blank=True, null=True,verbose_name =_("Remittance Date"))
    bankdestination  = models.ForeignKey('bnk.Banks', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank Destination"))

    creditcardtype  = models.ForeignKey(CreditCardsTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Credit Card Type"))
    creditcardnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Credit Card Number"))
    cvnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("CV Number"))
    expiredate = models.DateField(blank=True, null=True,verbose_name =_("Expire Date"))

    bankrefno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Bank Reference Number"))
    bankrefdate= models.DateField(blank=True, null=True,verbose_name =_("Bank Reference Date"))


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


class CustomersPaymentsLine(models.Model):
    customerpayment= models.ForeignKey(CustomersPayments, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer Payment"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    customer = models.ForeignKey(Customers,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='CustomersPaymentsLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='CustomersPaymentsLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='CustomersPaymentsLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='CustomersPaymentsLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Amount FC"))
    accounttype = models.ForeignKey(LookUp,related_name='CustomersPaymentsLine_accounttype', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True} ,related_name='CustomersPaymentsLine_account', blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.ledger




class CustomersTrans(models.Model):

    transtype =  models.ForeignKey(TransTypes,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    customer = models.ForeignKey(Customers,related_name='CustomersTrans_Customer', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customer"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='CustomersTrans_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='CustomersTrans_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='CustomersTrans_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='CustomersTrans_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    transdate = models.DateField(blank=True, null=True,verbose_name =_("Trans Date"))
    docnumber = models.CharField(max_length=50, blank=False, null=False, verbose_name =_("Doc Number"))
    customerjour = models.ForeignKey(CustomersJour,related_name='CustomersTrans_LedgerJour', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Customers Jour"))
    vendortrans = models.IntegerField( blank=True, null=True,  verbose_name=_("Vendor Trans"))
    operationid = models.IntegerField( blank=True, null=True, verbose_name=_("Operation ID"))
    customertrans = models.IntegerField( blank=True, null=True, verbose_name=_("Customer Trans"))
    payment = models.ForeignKey(CustomersPayments, blank=True, null=True, on_delete=models.PROTECT,  verbose_name =_("Customers Payment Key"))
    engdesc = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Desc"))
    arbdesc = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Desc"))
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Amount FC"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    closedate = models.DateField(blank=True, null=True,verbose_name =_("Close Date"))
    approvaldate = models.DateTimeField(blank=True, null=True,verbose_name =_("Approval Date"))
    approvalby = models.ForeignKey(User, blank=True, null=True,related_name='CustomersTrans_approvalby', on_delete=models.CASCADE, verbose_name =_("Approval By"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    postby = models.ForeignKey(User, blank=True, null=True,related_name='CustomersTrans_PostBy', on_delete=models.CASCADE, verbose_name =_("Post By"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='CustomersTrans_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))
    settleamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Settlement Amount"))
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
class DrawersLogClose(models.Model):
    treasury = models.ForeignKey(Treasuries,blank=True, null=True, related_name='DrawersLogClose_treasury', on_delete=models.CASCADE, verbose_name =_("Treasury"))
    user = models.ForeignKey(User,blank=True, null=True, related_name='DrawersLogClose_user', on_delete=models.CASCADE, verbose_name =_("User "))
    closedate = models.DateField(blank=True, null=True,verbose_name =_("Close Date"))
    closetime = models.TimeField(blank=True, null=True,verbose_name =_("Close Time"))
    todrawerlog = models.IntegerField( blank=True, null=True, verbose_name=_("Last ID Close from Drawer Log"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='DrawersLogClose_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk

class DrawersLogCloseline(models.Model):
    drawerlogclose = models.ForeignKey(DrawersLogClose,blank=True, null=True, related_name='DrawersLogCloseline_drawerlogclose', on_delete=models.CASCADE, verbose_name =_("Drawer Log Close"))
    paymethod = models.ForeignKey(PaymentsMethods,related_name='DrawersLogCloseline_paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    calcamount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Calculated Amount"))
    actamount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Actual Amount"))
    diffamount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Diff. Amount"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




class DrawersLog(models.Model):
    sourcename = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Source Name"))  #Source  Table Name
    sourcerecid = models.IntegerField( blank=True, null=True, verbose_name=_("Source Record ID"))  # Source Record ID From Source Table
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Currenct Rate"))
    user = models.ForeignKey(User,blank=True, null=True, related_name='DrawersLog_user', on_delete=models.CASCADE, verbose_name =_("User "))
    salesman = models.ForeignKey(Salesmans,related_name='DrawersLog_salesman', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Salesman"))
    paymethod = models.ForeignKey(PaymentsMethods,related_name='DrawersLog_paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    actioncode = models.CharField(max_length=20, blank=False, null=False, verbose_name =_("Action Code"))  #Action Code (ADD,OUT,CLOSE)
    amount = models.DecimalField(decimal_places=12, max_digits=30, blank=False, null=False, verbose_name =_("Amount"))
    actiondate = models.CharField(max_length=10,blank=True, null=True,verbose_name =_("Action Date"))
    actiontime = models.CharField(max_length=8,blank=True, null=True,verbose_name =_("Action Time"))
    drawerlogclose = models.ForeignKey(DrawersLogClose, blank=True, null=True, on_delete=models.PROTECT,  verbose_name =_("Drawer Log Close"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    created_by = models.ForeignKey(User, related_name='DrawersLog_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




