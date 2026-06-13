from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency
from sy.models import PaymentsMethods,LookUp
from django.utils.translation import get_language





class LedgersTypes(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class LedgersCategories(models.Model):
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
class LedgersClasses(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    glledger = models.IntegerField(blank=True, null=True,verbose_name=_("Ledger Account"))
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



class Ledger(models.Model):
    code = models.CharField( max_length=50, unique=True, verbose_name=_("Code"))
    segment1 = models.CharField(max_length=50, unique=False, blank=False, null=False,verbose_name=_("segment 1"))
    segment2 = models.CharField(max_length=50, unique=False, blank=True, null=True,verbose_name=_("segment 2"))
    segment3 = models.CharField(max_length=50, unique=False, blank=True, null=True,verbose_name=_("segment 3"))
    segment4 = models.CharField(max_length=50, unique=False, blank=True, null=True,verbose_name=_("segment 4"))
    segment5 = models.CharField(max_length=50, unique=False, blank=True, null=True,verbose_name=_("segment 5"))
    segment6 = models.CharField(max_length=50, unique=False, blank=True, null=True,verbose_name=_("segment 6"))
    engname = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    ledgertype = models.ForeignKey(LedgersTypes,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Ledger Type"))
    ledgercategory = models.ForeignKey(LedgersCategories, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger Category"))
    ledgerclass = models.ForeignKey(LedgersClasses , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger Classes"))
    allowaccountentry = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Account Entry"))
    currency = models.ForeignKey(Currency, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    budgetenabled = models.BooleanField(verbose_name=_("Budget Enabled"))
    checkbudget = models.BooleanField(verbose_name=_("Check Budget"))
    inactive = models.BooleanField(verbose_name=_("InActive"))
    inactivereason = models.CharField(blank=True, null=True,max_length=100, verbose_name=_("InActive Reason"))
    debitbalance = models.BooleanField(verbose_name=_("Is Debit Balance"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))
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
    created_by = models.ForeignKey(User, related_name='ledger_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='ledger_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""






class CostCategories(models.Model):
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
    created_by = models.ForeignKey(User, related_name='costcategories_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(blank=True, null=True,auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='costcategories_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""


class CostCentersLevels(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    length = models.IntegerField(blank=True, null=True,verbose_name=_("Length"))
    rank = models.IntegerField(blank=True, null=True,verbose_name=_("Rank"))

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
    created_by = models.ForeignKey(User, related_name='costcenterslevels_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(blank=True, null=True,auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='costcenterslevels_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""


class CostCenters(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    costcenterlevel = models.ForeignKey(CostCentersLevels, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost Center Level"))
    costcentercategory = models.ForeignKey(CostCategories, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost Category"))
    allowaccountentry = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Account Entry"))
    remarks = models.CharField(blank=True, null=True,max_length=100, unique=False, verbose_name=_("Remarks"))

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
    created_by = models.ForeignKey(User, related_name='costcenters_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='costcenters_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""

class TransTypes(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    transkind = models.ForeignKey(LookUp,related_name='TransTypes_TransKind', limit_choices_to={'keyname': 'TransKind'}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Kind"))
    sign = models.ForeignKey(LookUp,related_name='TransTypes_Sign', limit_choices_to={'keyname': 'Sign'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Sign"))
    paymentmethod= models.ForeignKey(PaymentsMethods,related_name='TransTypes_PaymentMethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    paymentdirection = models.ForeignKey(LookUp,related_name='TransTypes_PaymentDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Direction"))

    isreceipt = models.BooleanField(blank=False, null=False, verbose_name=_("Is Receipt"))
    alloweditdate = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Edit Date"))
    alloweditnumber = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Edit Number"))
    ismanual = models.BooleanField(blank=False, null=False, verbose_name=_("Is Manual"))
    iscash = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Cash"))
    ischeck = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Check"))
    iscreditcard = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Credit Card"))
    iscollectorneeded = models.BooleanField(blank=False, null=False, verbose_name=_("Is Collector Needed"))
    useref1 = models.BooleanField(blank=False, null=False, verbose_name=_("Use Ref 1"))
    ref1engcaption = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Ref1 Eng Caption"))
    ref1arbcaption = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Ref1 Arb Caption"))
    useref2 = models.BooleanField(blank=False, null=False, verbose_name=_("Use Ref2"))
    ref2engcaption = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Ref2 Eng Caption"))
    ref2arbcaption = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Ref2 Arb Caption"))
    iscashdisc = models.BooleanField(blank=False, null=False, verbose_name=_("Is Cash Discount"))
    istaxtrans = models.BooleanField(blank=False, null=False, verbose_name=_("Is Tax Trans"))
    isautoposttogl = models.BooleanField(blank=False, null=False, verbose_name=_("Is Auto Post To GL"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
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
    created_by = models.ForeignKey(User, related_name='TransTypes_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='TransTypes_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""

class LedgerJour(models.Model):
    transtype = models.ForeignKey(TransTypes, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    journalnumber = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name =_("Journal Number"))
    journaldate = models.DateField(blank=True, null=True,verbose_name=_("Journal Date"))
    journalyear = models.CharField(max_length=4, blank=True, null=True, verbose_name=_("Journal Year"))
    journalmonth = models.CharField(max_length=2, blank=True, null=True, verbose_name=_("Journal Month"))
    sequence = models.IntegerField( blank=True, null=True, verbose_name=_("Sequence"))
    reference = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference"))
    reference1 = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference1"))
    reference2 = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Reference1"))
    confirmdate = models.DateField(blank=True, null=True,verbose_name=_("Confirm Date"))
    postdate = models.DateField(blank=True, null=True,verbose_name=_("Post Date"))
    islocked = models.BooleanField(default=False,blank=True, verbose_name=_("Is Locked"))
    totalamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total Amount"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    vendorjournal = models.IntegerField( blank=True, null=True, verbose_name=_("Vendor Journal"))
    customerjournal = models.IntegerField( blank=True, null=True, verbose_name=_("Customer Journal"))
    itemtranshead = models.IntegerField( blank=True, null=True, verbose_name=_("Item Trans Head"))
    assetstranshead = models.IntegerField( blank=True, null=True, verbose_name=_("Assets Trans Head"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    fiscalyearperiod = models.IntegerField( blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    # created_by = models.ForeignKey(User, blank=False, null=True,related_name='LedgerJour_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    paymentid = models.IntegerField( blank=True, null=True,  verbose_name=_("Ledger Payment ID"))
    status = models.ForeignKey(LookUp,related_name='LedgerJour_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    created_date = models.DateField(blank=True, null=True,verbose_name=_("Created Date"))
    operation = models.ForeignKey('inv.operations', blank = True, null = True, related_name = 'LedgerJour_operation', on_delete = models.PROTECT, verbose_name = _("Operation"))
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


class LedgerJourLine(models.Model):
    ledgerjour = models.ForeignKey(LedgerJour, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger Jour"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='LedgerJourLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='LedgerJourLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='LedgerJourLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='LedgerJourLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))
    qty = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("qty"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    reverse = models.IntegerField( blank=True, null=True,  verbose_name =_("Reverse"))
    customer = models.IntegerField( blank=True, null=True,  verbose_name =_("Customer"))
    vendor = models.IntegerField( blank=True, null=True,  verbose_name =_("Vendor"))
    debitamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Debit Amount"))
    creditamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Credit Amount"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount (Debit - Credit)"))
    remarks = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.ledger



class Treasuries(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("User"))
    #employee = models.ForeignKey(Employees, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("employee"))
    employee = models.IntegerField( blank=True, null=True,  verbose_name =_("employee"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    ledgerdiff = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': 'True'},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Differences Ledger"))
    requiredreceiptno = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("RequiredReceiptNo"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))

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
    created_by = models.ForeignKey(User, related_name='costcenters_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Modified Date"))
    modified_by = models.ForeignKey(User, related_name='costcenters_modified_by',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Modified By"))

"""


# treasury Details 1
class TreasuriesAccounts(models.Model):
    treasury = models.ForeignKey(Treasuries, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("treasury"))
    engdesc = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Desc"))
    arbdesc = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Desc"))
    isbank = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("isbank"))
    #bank = models.ForeignKey(Banks, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Bank"))
    bank = models.IntegerField( blank=True, null=True,  verbose_name =_("bank"))
    ledger = models.ForeignKey(Ledger, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("ledger"))
    isdefault = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("Is Default"))

    costcenter1 = models.ForeignKey(CostCenters,related_name='TreasuriesAccounts_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='TreasuriesAccounts_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='TreasuriesAccounts_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='TreasuriesAccounts_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


# treasury Details 2
class TreasuriesTransTypes(models.Model):
    treasury = models.ForeignKey(Treasuries, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("treasury"))
    transtype = models.ForeignKey(TransTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    #accounttype = models.ForeignKey(LookUp, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    accounttype = models.IntegerField( blank=True, null=True,  verbose_name =_("Account Type"))
    #paymentdirection = models.ForeignKey(LookUp, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Direction"))
    paymentdirection = models.IntegerField( blank=True, null=True,  verbose_name =_("Payment Direction"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk

"""
class PaymentMethod(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    iscash = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("Is Cash"))
    iscredit = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("Is Credit"))
    iscreditcard = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("Is Credit Card"))
    ischeck = models.BooleanField(default=False,  blank=False, null=False, verbose_name=_("Is Check"))
    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk

"""

class TreasuriesOrders(models.Model):
    treasury = models.ForeignKey(Treasuries, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("treasury"))
    treasuryledger = models.ForeignKey(Ledger,related_name='TreasuriesLedger', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Ledger"))
    treasurycenter1 = models.ForeignKey(CostCenters,related_name='TLTreasuriesOrders_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Cost center 1"))
    treasurycenter2 = models.ForeignKey(CostCenters,related_name='TLTreasuriesOrders_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Cost center 2"))
    treasurycenter3 = models.ForeignKey(CostCenters,related_name='TLTreasuriesOrders_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Cost center 3"))
    treasurycenter4 = models.ForeignKey(CostCenters,related_name='TLTreasuriesOrders_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Cost center 4"))
    paymentdirection = models.ForeignKey(LookUp,related_name='TreasuriesOrders_PayDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Direction"))
    paymentmethod = models.ForeignKey(PaymentsMethods, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    referencerecord = models.IntegerField( blank=True, null=True,  verbose_name =_("Reference Record Key"))
    referenceobjectname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Reference Object Name"))
    orderdate = models.DateField(blank=True, null=True,verbose_name =_("Order Date"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=False, null=False, verbose_name =_("Amount"))
    currency = models.ForeignKey(Currency, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    engdesc = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Desc"))
    arbdesc = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Desc"))
    accounttype = models.ForeignKey(LookUp,related_name='TreasuriesOrders_AccountType', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    #account = models.IntegerField( blank=True, null=True,  verbose_name =_("Account Key"))

    ledger = models.ForeignKey(Ledger, limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger"))
    customer = models.ForeignKey('ar.Customers', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Customers"))
    vendor = models.ForeignKey('ap.vendors', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Vendors"))
    #employee = models.ForeignKey(Employees, limit_choices_to={'allowaccountentry': True}, blank=False, null=False,on_delete=models.PROTECT, verbose_name=_("Employees"))


    transtype =  models.ForeignKey(TransTypes,blank=False, null=True,limit_choices_to={'isreceipt': True},  on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    fiscalyearperiod = models.IntegerField( blank=True, null=True,  verbose_name =_("Fiscal Year Period"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='TreasuriesOrders_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='TreasuriesOrders_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='TreasuriesOrders_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='TreasuriesOrders_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    approvaldate = models.DateTimeField(blank=True, null=True,verbose_name =_("Approval Date"))
    approvalby = models.ForeignKey(User, blank=True, null=True,related_name='TreasuriesOrders_approvalby', on_delete=models.CASCADE, verbose_name =_("Approval By"))
    receipt = models.IntegerField( blank=True, null=True,  verbose_name =_("Receipt Key"))
    finishdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Finish Date"))
    isfinish = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is finish"))
    referencepayment = models.IntegerField( blank=True, null=True,  verbose_name =_("Reference Payment Key"))
    refpaymentid = models.IntegerField( blank=True, null=True,  verbose_name =_("Payment Reference ID"))
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





class LedgerCostBalances(models.Model):
    serial = models.IntegerField(blank=True, null=True,unique=True,  verbose_name=_("serial"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    ledger = models.ForeignKey(Ledger, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='LedgerCostBalances_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='LedgerCostBalances_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='LedgerCostBalances_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='LedgerCostBalances_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    dramount = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Debit Amount"))
    cramount = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Credit Amount"))
    dramountfc = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Debit Amount FC"))
    cramountfc = models.DecimalField(decimal_places=3, max_digits=30, blank=True, null=True, verbose_name =_("Credit Amount FC"))
    lastledgertrans = models.IntegerField(blank=True, null=True,verbose_name=_("Last Ledger Trans"))
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


class LedgerPayments(models.Model):
    transtype = models.ForeignKey(TransTypes  , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    number = models.IntegerField(blank=True, null=True,unique=True,  verbose_name=_("Payment Number"))
    paymentdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Payment Date"))
    status = models.ForeignKey(LookUp,related_name='LedgerPayments_Status', limit_choices_to={'keyname': 'PaymentStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    treasuryorder=models.ForeignKey(TreasuriesOrders, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury Order"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True,verbose_name=_("Fiscal Year Period"))
    ledger = models.ForeignKey(Ledger, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='LedgerPayments_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='LedgerPayments_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='LedgerPayments_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='LedgerPayments_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    isposted = models.BooleanField(blank=False, null=False, verbose_name=_("Is Posted"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    paymentdirection = models.ForeignKey(LookUp,related_name='LedgerPayments_PaymentDirection', limit_choices_to={'keyname': 'PaymentDirection'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Status"))
    paymentmethod = models.ForeignKey(PaymentsMethods,related_name='LedgerPayments_Paymethod', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Payment Method"))
    currency = models.ForeignKey(Currency,related_name='LedgerPayments_Currency', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    created_by = models.ForeignKey(User,blank=False, null=True, related_name='LedgerPayments_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
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


class LedgerPaymentsLine(models.Model):
    ledgerpayment= models.ForeignKey(LedgerPayments, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger Payment"))
    rank = models.IntegerField( blank=True, null=True, verbose_name =_("Rank"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='LedgerPaymentsLine_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='LedgerPaymentsLine_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='LedgerPaymentsLine_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='LedgerPaymentsLine_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount FC"))
    accounttype = models.ForeignKey(LookUp,related_name='LedgerPaymentsLine_accounttype', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    account = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True} ,related_name='LedgerPaymentsLine_account', blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    engdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Eng Description"))
    arbdesc = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Arb Description"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.ledger




class LedgerTrans(models.Model):

    transtype =  models.ForeignKey(TransTypes,blank=False, null=True,  on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    ledger = models.ForeignKey(Ledger,related_name='TransLedger_Ledger', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='TransLedger_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='TransLedger_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='TransLedger_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='TransLedger_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    transdate = models.DateField(blank=True, null=True,verbose_name =_("Trans Date"))
    docnumber = models.CharField(max_length=50, blank=False, null=False, verbose_name =_("Doc Number"))
    ledgerjour = models.ForeignKey(LedgerJour,related_name='TransLedger_LedgerJour', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger Jour"))
    customerjour = models.IntegerField( blank=True, null=True,  verbose_name=_("Customer Jour"))
    vendorjour = models.IntegerField( blank=True, null=True,  verbose_name=_("Vendor Jour"))
    customertrans = models.IntegerField( blank=True, null=True, verbose_name=_("Customer Trans"))
    vendortrans = models.IntegerField( blank=True, null=True,  verbose_name=_("Vendor Trans"))
    payment = models.ForeignKey(LedgerPayments, blank=True, null=True, on_delete=models.PROTECT,  verbose_name =_("Ledger Payment Key"))
    engdesc = models.CharField(max_length=100, blank=False, null=False, verbose_name =_("Eng Desc"))
    arbdesc = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Desc"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=False, null=False, verbose_name =_("Amount"))
    amountfc = models.DecimalField(decimal_places=1, max_digits=12, blank=False, null=False, verbose_name =_("Amount FC"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currency"))
    currencyrate = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Currenct Rate"))
    duedate = models.DateField(blank=True, null=True,verbose_name =_("Due Date"))
    closedate = models.DateField(blank=True, null=True,verbose_name =_("Close Date"))
    approvaldate = models.DateTimeField(blank=True, null=True,verbose_name =_("Approval Date"))
    approvalby = models.ForeignKey(User, blank=True, null=True,related_name='LedgerTrans_approvalby', on_delete=models.CASCADE, verbose_name =_("Approval By"))
    postdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Post Date"))
    postby = models.ForeignKey(User, blank=True, null=True,related_name='LedgerTrans_PostBy', on_delete=models.CASCADE, verbose_name =_("Post By"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    created_by = models.ForeignKey(User,blank=False, null=True, related_name='LedgerTrans_created_by', on_delete=models.CASCADE, verbose_name =_("Created By"))
    remarks = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Remarks"))
    settleamount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Settlement Amount"))
    operation = models.ForeignKey('inv.operations', blank = True, null = True, related_name = 'CustomersTrans_operation', on_delete = models.PROTECT, verbose_name = _("Operation"))
    created_date = models.DateField(blank=True, null=True,verbose_name=_("Created Date"))
    lastsettledate = models.DateTimeField(blank=True, null=True,verbose_name =_("Last Settle Date"))

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


class TaxesTrans(models.Model):
    transtype = models.ForeignKey(TransTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    sourcetablename = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Source Table Name"))
    sourcerecid = models.IntegerField( blank=True, null=True,  verbose_name =_("Source Record ID"))
    transdate = models.DateTimeField(blank=True, null=True,verbose_name =_("Trans Date"))
    tax = models.ForeignKey('sy.Taxes',related_name='TaxesTrans_tax', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax"))
    taxbaseamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Tax Base Amount"))
    taxpercent = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Tax Percent"))
    taxamount = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True, verbose_name =_("Tax Amount"))
    taxregnumber = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Tax Registeration Number"))
    taxaccountname = models.CharField(max_length=100, blank=True, null=True, unique=False, verbose_name=_("Tax Account Name"))
    remarks = models.CharField(max_length=200, blank=True, null=True, unique=False, verbose_name=_("Remarks"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='TaxesTrans_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='TaxesTrans_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='TaxesTrans_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='TaxesTrans_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    duedate = models.DateTimeField(blank=True, null=True,verbose_name =_("Due Date"))
    fiscalyearperiod = models.IntegerField(blank=True, null=True, verbose_name=_("Fiscal Year Period"))
    closed = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Closed"))
    closeddate = models.DateTimeField(blank=True, null=True,verbose_name =_("Closed Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



