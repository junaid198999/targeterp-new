from django.db import models
from django.db.models import ImageField
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_pgviews import view as pg
from django.utils.translation import get_language
from datetime import datetime
import django.contrib.auth.models as auth_models



class Modules(models.Model):
    code = models.CharField(max_length=5,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    isregistered = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Registered"))
    isfydependant = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Fiscal Year Dependant"))
    isgl = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is General Ledger"))
    isar = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Account Receivable"))
    isap = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Account Payable"))
    isfa = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Fixed Assets"))
    isin = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Inventory"))
    ishr = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Human Resources"))
    isfc = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Manufacturing"))
    ispm = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Projects Management"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class LUPeriodsTypes(models.Manager):
    def get_queryset(self):
        return super(LUPeriodsTypes, self).get_queryset().filter(keyname='PeriodType')


class LUGenders(models.Manager):
    def get_queryset(self):
        return super(LUGenders, self).get_queryset().filter(keyname='Gender')


class LookUp(models.Model):
    keyid = models.IntegerField(blank=False, null=False ,unique=True, verbose_name=_("Key ID"))
    keyname = models.CharField(max_length=100,blank=False, null=False , verbose_name =_("Key Name"))
    code = models.CharField(max_length=20, verbose_name =_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True,null=True, verbose_name=_("Arb Name"))
    value = models.CharField(max_length=200, blank=True,null=True,verbose_name=_("Value"))
    remarks = models.CharField(max_length=500, blank=True,null=True,verbose_name=_("Remarks"))

    objects = models.Manager()
    periodtype = LUPeriodsTypes()
    Gender = LUGenders()


    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')


    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class vwPeriodsTypes(pg.View):
    projection = ['sy.LookUp.*',]
    sql = """SELECT * FROM sy_LookUp WHERE keyname='PeriodType' ;"""

    class Meta:
      managed = False


class FiscalYears(models.Model):
    code = models.CharField(max_length=10,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class FiscalYearsPeriods(models.Model):
    code = models.CharField(max_length=10,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    fiscalyear = models.ForeignKey(FiscalYears, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Fiscal Year"))
    fromdate = models.DateField(blank=False, null=False, verbose_name =_("From Date"))
    todate = models.DateField(blank=False, null=False, verbose_name =_("To Date"))
    rank = models.IntegerField(blank=True, null=True , verbose_name=_("Rank"))
    periodtype = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'PeriodType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Period  Type"))

    #periodtype= LUPeriodsTypes()

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname




class FiscalYearsPeriodsModules(models.Model):

    fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Fiscal Year Period"))
    module = models.ForeignKey(Modules, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Module"))
    opendate = models.DateField(blank=True, null=True, verbose_name =_("From Date"))
    closedate = models.DateField(blank=True, null=True, verbose_name =_("To Date"))


    class Meta:
        ordering = ['-pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




class PaymentsMethods(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    iscash = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Cash"))
    iscreditcard = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Credit Card"))
    ischeck = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Check"))
    iscredit = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Credit"))
    isremittance = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Is Remittance"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class CreditCardsTypes(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Languages(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Nationalities(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class Regions(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class Countries(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    region = models.ForeignKey(Regions,blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Regions"))
    nationality = models.ForeignKey(Nationalities,blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Nationality"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class Areas(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, verbose_name =_("Country"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class Cities(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    area = models.ForeignKey(Areas,blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Area"))
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, verbose_name =_("Country"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Districts(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Arb Name"))
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name =_("Cities"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class AddressesTypes(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class ContactsTypes(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class DocumentsTypes(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class BusinessActivitiesTypes(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname



class AgingStyles(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    module = models.ForeignKey(Modules,  on_delete=models.PROTECT, verbose_name=_("Module"))
    isdefault = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Default"))
    useduedate = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Use Due Date"))
    remarks = models.CharField(max_length=100, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class AgingStylesLines(models.Model):
    agingstyle = models.ForeignKey(AgingStyles,  on_delete=models.PROTECT, verbose_name=_("Module"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    periodvalue = models.IntegerField( blank=True, null=True, verbose_name=_("Period Value Per Days"))
    rank = models.IntegerField( blank=True, null=True, verbose_name=_("Rank"))
    class Meta:
        ordering = ['rank']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class PaymentsTearms(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True ,verbose_name=_("Arb Name"))
    accounttype = models.ForeignKey(LookUp,related_name='PaymentsTearms_AccountType', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    noofpayment = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("No Of Payments"))
    #minpercentpayment = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Minimum Percent Per Payment"))
    creditlimit = models.DecimalField(decimal_places=12, max_digits=30,blank=False, null=True, verbose_name =_("Credit Limit"))
    creditdays = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Credit Days"))
    paymentintervalday = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Payment Interval Per Day"))
    allowcashdiscount = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Allow cash Discount Role"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    isperiod = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Is Period Begin Month"))
    perioddays = models.PositiveIntegerField( blank=True, null=True, verbose_name=_("Period Days"))
    accountcheck = models.ForeignKey(LookUp,related_name='PaymentsTearms_accountcheck', limit_choices_to={'keyname': 'AccountCheck'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Checking Type"))


    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class CashDiscountsRoles(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    accounttype = models.ForeignKey(LookUp,related_name='CashDiscountsRoles_AccountType', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey('gl.Ledger', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class CashDiscountsRolesLine(models.Model):
    cashdiscountrole = models.ForeignKey(CashDiscountsRoles, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cash Discount Role"))
    # paymentmethod = models.ForeignKey(PaymentsMethods,  on_delete=models.PROTECT, verbose_name=_("Payment Methods"))
    lessthanpercent = models.IntegerField( blank=True, null=True, verbose_name=_("Less Than Pecent From Credit Period"))
    discountpercent = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount Percent"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class CompanyProfile(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    prefix = models.CharField(max_length=50, verbose_name=_("Prefix"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Arb Name"))
    ishijri = models.BooleanField(default=False, verbose_name =_("Is Hijri Date"))
    logo = ImageField(upload_to='images/', max_length=255, blank=True, null=True, verbose_name =_("Company Logo"))
    #logo = models.BinaryField(null=True, verbose_name =_("Company Logo"))
    defaultcurrency = models.ForeignKey(Currency, related_name='compayprofile_currency', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Default Curency"))
    capitalledger = models.ForeignKey('gl.Ledger',limit_choices_to={'allowaccountentry': 'True'}, related_name='compayprofile_capitalledger', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Capital Ledger"))
    plledger = models.ForeignKey('gl.Ledger',limit_choices_to={'allowaccountentry': 'True'}, related_name='compayprofile_plledger', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("P & L Ledger"))
    taxregisterno = models.CharField(max_length=50, verbose_name =_("Tax Register Number"))
    allowed_users = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("users"))
    usecostcenter1 = models.BooleanField(default=False, verbose_name =_("User Cost Center 1"))
    usecostcenter2 = models.BooleanField(default=False, verbose_name =_("User Cost Center 2"))
    usecostcenter3 = models.BooleanField(default=False, verbose_name =_("User Cost Center 3"))
    usecostcenter4 = models.BooleanField(default=False, verbose_name =_("User Cost Center 4"))



    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class CompanyProfileAddresses(models.Model):
    company =models.ForeignKey(CompanyProfile , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Company"))
    addresstype = models.ForeignKey(AddressesTypes, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Address Type"))
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


class CompanyProfileContacts(models.Model):
    company = models.ForeignKey(CompanyProfile , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Company"))
    contacttype = models.ForeignKey(ContactsTypes, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Contact Type"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    value = models.CharField(max_length=300, verbose_name =_("Value"))
    inactive = models.BooleanField(blank=False, null=False, verbose_name=_("Inactive"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class CompanyProfileDocuments(models.Model):
    company = models.ForeignKey(CompanyProfile , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Company"))
    documenttype = models.ForeignKey(DocumentsTypes, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Document Type"))
    documentnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Document Number"))
    issuedate = models.DateField(blank=True, null=True, verbose_name =_("Issue Date"))
    expiredate = models.DateField(blank=True, null=True, verbose_name =_("Expire Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class Branches(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Arb Name"))
    company =models.ForeignKey(CompanyProfile , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Company"))
    parent =models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    isheadoffice = models.BooleanField(default=False, verbose_name =_("Is Head Office"))
    treasury =models.ForeignKey('gl.Treasuries', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Treasury"))
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

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class BranchesContacts(models.Model):
    branch = models.ForeignKey(CompanyProfile , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Branch"))
    contacttype = models.ForeignKey(ContactsTypes, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Contact Type"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    value = models.CharField(max_length=300, verbose_name =_("Value"))
    inactive = models.BooleanField(blank=False, null=False, verbose_name=_("Inactive"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class Departments(models.Model):
    code = models.CharField(max_length=20,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Arb Name"))
    parent =models.ForeignKey('self', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Parent"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class BranchesDepartments(models.Model):
    department =models.ForeignKey(Departments, blank=False, null=False,related_name='BranchesDepartments_Department', on_delete=models.PROTECT, verbose_name=_("Department"))
    branch =models.ForeignKey(Departments, blank=False, null=False,related_name='BranchesDepartments_Branch', on_delete=models.PROTECT, verbose_name=_("Branch"))



class PriceLevels(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    module = models.ForeignKey(Modules, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Module"))
    inactive = models.BooleanField(blank=False, null=False, verbose_name=_("Inactive"))
    isminprice = models.BooleanField(blank=False, null=False, verbose_name=_("Is Minimum Price"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Taxes(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    taxledger = models.ForeignKey('gl.Ledger',related_name='Taxes_taxledger', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Tax Ledger"))
    taxsettledledger = models.ForeignKey('gl.Ledger',related_name='Taxes_taxsettledledger', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Tax Settled Ledger"))

    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class TaxesLine(models.Model):
    tax = models.ForeignKey(Taxes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax"))
    value = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Tax Value Percent"))
    limitmin = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Tax Limit Min"))
    limitmax = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Tax Limit Max"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class TaxesGroups(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return str(self.code) + ' - ' + str(self.arbname)
        else:
            return str(self.code) + ' - ' + str(self.engname)


class TaxesGroupsLine(models.Model):
    taxgroup = models.ForeignKey(TaxesGroups, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax Group"))
    tax = models.ForeignKey(Taxes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax"))
    #value = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax Value Percent"))
    fromdate = models.DateField(blank=True, null=True, verbose_name =_("From Date"))
    todate = models.DateField(blank=True, null=True, verbose_name =_("To Date"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.value



class StatusLog(models.Model):
    tablename = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Table Name"))
    recordid = models.IntegerField( blank=True, null=True,  verbose_name =_("Record ID"))
    status = models.ForeignKey(LookUp,related_name='StatusLog_Status', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk
