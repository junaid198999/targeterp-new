from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Q
import datetime

from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _

from TARGET.crm.models import current_year

from sy.models import PaymentsMethods,LookUp
from django.utils.translation import get_language
from gl.models import *
from sy.models import *
from ar.models import Customers ,  CustomersClasses ,Salesmans
from ap.models import *


from datetime import datetime


#from django.db import models


class Units(models.Model):
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
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class Warehouses(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class StorageMethodsTypes(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))


    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class InventoriesLocationsTypes(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))


    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class InventoriesLocations(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name=_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    invlocationtype = models.ForeignKey(InventoriesLocationsTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventry Location Type"))
    branch = models.ForeignKey(Branches, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Branch"))
    warehouse = models.ForeignKey(Warehouses, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Warehouse Related Cost Price"))
    country = models.ForeignKey(Countries, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Country"))
    city = models.ForeignKey(Cities, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("City"))
    district = models.ForeignKey(Districts, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("District"))
    address1 = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Address 1"))
    address2 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Address 2"))
    address3 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("address 3"))
    street = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Street"))
    isecommerce = models.BooleanField(blank=False, null=False, verbose_name=_("Is E Commerce"))
    istransit = models.BooleanField(blank=False, null=False, verbose_name=_("Is Transit"))
    isassets = models.BooleanField(blank=False, null=False, verbose_name=_("Is Assets Inventory Location"))
    isdamage = models.BooleanField(blank=False, null=False, verbose_name=_("Is Damaged Inventory Location"))
    invledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_invled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Ledger"))
    adjledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_adjled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Adjustment Ledger"))
    slsledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_slsled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Sales Ledger"))
    rslsledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_rslsled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Refund Sales Ledger"))
    costsalesledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_costsalesled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost Of Sales Sales Ledger"))
    purledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_purledger',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Purchase Ledger"))
    rpurledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_rpurledger',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Refund Purchase Ledger"))
    settleledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_settleled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Settlement Ledger"))
    expenseledger = models.ForeignKey(Ledger,related_name='InventoriesLocations_expenseled',limit_choices_to={'allowaccountentry': 'True'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Expenses Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='InventoriesLocations_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='InventoriesLocations_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='InventoriesLocations_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='InventoriesLocations_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))
    storekeeper = models.IntegerField( blank=True, null=True,  verbose_name =_("Store Keeper"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))


    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return str(self.code + ' - ' + self.arbname)
        else:
            return str(self.code + ' - ' + self.engname)


class InventoriesBinLocations(models.Model):
    inventlocation = models.ForeignKey(InventoriesLocations, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    code = models.CharField(max_length=100,unique=True, verbose_name=_("Auto Code Concat(L+F+Z+T+S+B)"))
    barcode = models.CharField(max_length=100,unique=True, verbose_name=_("Barode"))
    floor = models.CharField(max_length=50,  verbose_name=_("Floor"))
    zone = models.CharField(max_length=100, blank=False, null=True, verbose_name=_("Zone"))
    track = models.CharField(max_length=100, blank=False, null=True, verbose_name=_("Track"))
    shelf = models.CharField(max_length=100, blank=False, null=True, verbose_name=_("Shelf"))
    bin = models.CharField(max_length=100, blank=False, null=True, verbose_name=_("Bin"))
    storagemethod = models.ForeignKey(StorageMethodsTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventry Storage Method"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
            return str(self.code)



class ItemsTypes(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    iskit = models.BooleanField(blank=False, null=False, verbose_name=_("Is Kit Item"))
    isservice = models.BooleanField(blank=False, null=False, verbose_name=_("Is Service Item"))
    isasset = models.BooleanField(blank=False, null=False, verbose_name=_("Is Asset Item"))
    alloweditname = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Edit Name"))
    allowsellingzeroqty = models.BooleanField(blank=False, null=False, verbose_name=_("Allow Selling Zero Qty"))
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


class ItemsCategories(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self',related_name='ItemsCategories_Parent', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent Category"))
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


class ItemsGroups(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self',related_name='ItemsGroups_Parent', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent Group"))
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


class ItemsBrands(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self',related_name='ItemsBrands_Parent', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
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



class GenericNamesCategories(models.Model):
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
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class GenericNames(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    genericcategory = models.ForeignKey(GenericNamesCategories, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Generic Category"))
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



class ItemsClasses(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    itemtrack = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'ItemTracking'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Tracking"))
    autobarcode = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Auto Barcode"))
    barcodelength = models.IntegerField( blank=True, null=True,  verbose_name =_("Barcode Length"))
    quantitydecimal = models.IntegerField( blank=True, null=True,  verbose_name =_("Quantity Decimal"))
    expensesledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Expenses Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='ItemsClasses_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='ItemsClasses_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='ItemsClasses_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='ItemsClasses_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))


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


class Items(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    shortengname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Short Eng Name"))
    shortarbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Short Arb Name"))
    barcode = models.CharField(max_length=100,blank=False, null=False, verbose_name=_("Barcode Global Trade Item Number (GTIN)"))
    quantitydecimal = models.IntegerField(default=0, blank=False, null=False,  verbose_name =_("Quantity Decimal"))
    itemtype = models.ForeignKey(ItemsTypes , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item Type"))
    itemclass = models.ForeignKey(ItemsClasses , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item Class"))
    itemcategory = models.ForeignKey(ItemsCategories , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Category"))
    itemgroup = models.ForeignKey(ItemsGroups  , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Group"))
    itembrand = models.ForeignKey(ItemsBrands  , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Brand"))
    storagemethod = models.ForeignKey(StorageMethodsTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Storage Method"))
    baseunit = models.ForeignKey(Units, blank=False, null=False,related_name='Items_BaseUnit', on_delete=models.PROTECT, verbose_name=_("Base Unit"))
    baseuom = models.ForeignKey('ItemsUOM', blank=True, null=True,related_name='Items_BaseUOM', on_delete=models.PROTECT, verbose_name=_("Base UOM"))
    noofpiece = models.IntegerField(default=1, blank=True, null=True,  verbose_name =_("No Of Piece"))
    weight =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Weight"))
    weightunit = models.ForeignKey(Units, blank=True, null=True,related_name='Items_WeightUnit', on_delete=models.PROTECT, verbose_name=_("Weight Unit"))

    status = models.ForeignKey(LookUp,related_name='Items_Status', limit_choices_to={'keyname': 'ItemStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))
    alertexpiredays = models.IntegerField( blank=True, null=True,  verbose_name =_("Alter Expiration Date Days"))
    abccode = models.CharField(max_length=1,blank=True, null=True, verbose_name=_("ABC Code"))
    allowecommerce = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow E Commerce"))
    taxgroupsale= models.ForeignKey(TaxesGroups,related_name='Items_taxgroupheadsale',blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Tax Group Head Sale"))
    taxgroupsaleincludedprice = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Tax Included sale Price"))
    taxgroupPurchase= models.ForeignKey(TaxesGroups,related_name='Items_taxgroupheadPurchase',blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Tax Group Head Purchase"))
    taxgroupPurchaseincludedprice = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Tax Included Purchase Price"))

    image = ImageField(upload_to='images/', max_length=255, blank=True, null=True, verbose_name =_("Item Image"))
    ti = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("TI"))
    hi = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("HI"))

    shelflife = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Shelf Life Month"))
    safetystock = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Safety Stock Month"))

    sfdaregno = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("SFDA Registration Number"))
    genericname = models.ForeignKey(GenericNames  , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Generic Name"))
    lasa = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Look-Alike/Sound-Alike"))
    highalter = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("High Alter"))
    controlled = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Controlled"))
    aso = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Administrative Services Only"))
    prescribed = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Prescribed"))
    multidosage = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Multi Dosage"))
    dosageform = models.CharField(max_length=200,blank=True, null=True, verbose_name=_("Dosage Form"))
    strength = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Strength"))
    instruction = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Instruction"))
    routeofadministration = models.IntegerField( blank=True, null=True,  verbose_name =_("route of administration"))

    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    created_date = models.DateField(auto_now_add=True, auto_now=False, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


""" Insert into next table One record for Base unit and factor is 1 to make relation direct with Item Identifier"""
class ItemsUOM(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    unit = models.ForeignKey(Units, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit"))
    baseunitfactor = models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Base Unit Factor"))
    barcode = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Barcode Global Trade Item Number (GTIN)"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return   self.unit.code + ' - ' + str(int(self.baseunitfactor)) + ' - ' + self.barcode



class ItemsInventoriesLocations(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    invlocation = models.ForeignKey(InventoriesLocations, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    binlocation = models.ForeignKey(InventoriesBinLocations  ,max_length=100,blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Bin Location"))
    status = models.ForeignKey(LookUp,related_name='ItemsInventoriesLocations_Status', limit_choices_to={'keyname': 'ItemStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.invlocation


class ItemsSeasonality(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    area = models.ForeignKey(Areas, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Area "))
    quotapercent = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Quota Percent"))
    m1 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M1"))
    m2 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M2"))
    m3 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M3"))
    m4 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M4"))
    m5 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M5"))
    m6 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M6"))
    m7 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M7"))
    m8 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.33, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M8"))
    m9 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.34, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M9"))
    m10 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.34, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M10"))
    m11 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.34, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M11"))
    m12 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12, default=8.34, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("M12"))
    m_total = models.PositiveIntegerField(default=100, validators=[MinValueValidator(100),MaxValueValidator(100)], verbose_name =_("Total"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')



    def __str__(self):
        return self.pk


class ItemsPricesLevels(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    pricelevel = models.ForeignKey(PriceLevels , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Price Level"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pricelevel


class ItemsPricesLists(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Item UOM"))
    pricelevel = models.ForeignKey(PriceLevels , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Price Level"))
    invlocation = models.ForeignKey(InventoriesLocations, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    unit = models.ForeignKey(Units, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Unit"))
    price =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Price"))
    #barcode = models.CharField(max_length=100,blank=False, null=False,unique=True, verbose_name=_("Barcode Global Trade Item Number (GTIN)"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return str(self.price)


class ItemsIdentifiers(models.Model):
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=False,related_name='ItemsIdentifiers_itemuom', on_delete=models.PROTECT, verbose_name=_("Item UOM"))
    baseitemuom = models.ForeignKey(ItemsUOM, blank=False, null=True,related_name='ItemsIdentifiers_baseitemuom', on_delete=models.PROTECT, verbose_name=_("Base Item UOM"))
    barcode = models.CharField(max_length=100,blank=False, null=False,unique=True, verbose_name=_("New Barcode with Attribute (Auto Generation)"))
    expiredate = models.DateField(blank=True, null=True, verbose_name =_("Expire Date"))
    batchnumber = models.CharField(max_length=50,blank=True, null=True,unique=True, verbose_name=_("Batch Number"))
    lotdate = models.DateField(blank=True, null=True, verbose_name =_("Lot Date"))
    lotnumber = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Lot Number"))
    serialnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Serial Number"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')
        unique_together = ['item', 'itemuom','barcode','expiredate','batchnumber','lotdate','lotnumber','serialnumber']


    def __str__(self):
        return self.barcode


class WFActionsStatus(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Action Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Action Arb Name"))
    statusengname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Status Eng Name"))
    statusarbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Arb Name"))
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


class ExpensesTypes(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Action Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Action Arb Name"))
    ledger = models.ForeignKey(Ledger, limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='ExpensesType_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='ExpensesType_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='ExpensesType_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='ExpensesType_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))

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


class Agencies(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Action Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Action Arb Name"))
    accounttype = models.ForeignKey(LookUp,related_name='Agencies_AccountType', limit_choices_to=Q(keyid= 90001) | Q(keyid=90002), blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger,limit_choices_to={'allowaccountentry': True},blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Ledger"))
    vendor = models.ForeignKey(Vendors,limit_choices_to={'allowaccountentry': True}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Vendor"))
    costcenter1 = models.ForeignKey(CostCenters,related_name='Agencies_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='Agencies_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='Agencies_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='Agencies_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))

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

class AgenciesExpensesLine(models.Model):
    agency = models.ForeignKey(Agencies,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Agency"))
    expenstype = models.ForeignKey(ExpensesTypes,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Expense Type"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class OperationsTypes(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    operationkind = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'OperationsKinds'},related_name='OperationsTypes_operationkind', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Operation Kind"))
    pricelevel = models.ForeignKey(PriceLevels,related_name='OperationsTypes_pricelevel', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Price Level"))
    effectcostprice = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Iseffecting Item Cost Price"))
    viewlocationqty = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("View Qty In All Locations"))
    accounttype = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'AccountType'},related_name='OperationsTypes_accounttype', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    viewaccountbalance = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("View Account Balance"))
    allowrevise = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Revise"))
    allowadditem = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Add New Item"))
    allowdeleteitem = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Delete Item"))
    allowadjustqty = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Adjust Original Qty"))
    usepaymethod = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Pay Methods"))
    defaultqty = models.IntegerField( blank=True, null=True,  verbose_name =_("Default Quantity"))
    defaultdiscounttype = models.IntegerField(default=False, blank=True, null=True,  verbose_name =_("Default Discount Type"))
    useshipping = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Shipping"))
    isinventory = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Inventory Transaction"))
    usedepartment = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Department"))
    usecostcenter1 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Cost Center 1"))
    usecostcenter2 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Cost Center 2"))
    usecostcenter3 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Cost Center 3"))
    usecostcenter4 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Cost Center 4"))
    usesaleperson = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Sales Person"))
    useexpense = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Expense"))
    usedisc1 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Discount 1"))
    usedisc2 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Discount 2"))
    usedisc3 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Use Discount 3"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    transtype = models.ForeignKey(TransTypes ,related_name='OperationsTypes_transtype',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Trans Type"))
    ledgerdisc1 = models.ForeignKey(Ledger,related_name='OperationsTypes_ledgerdisc1', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger Disc1"))
    ledgerdisc2 = models.ForeignKey(Ledger,related_name='OperationsTypes_ledgerdisc2', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger Disc2"))
    ledgerdisc3 = models.ForeignKey(Ledger,related_name='OperationsTypes_ledgerdisc3', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("LedgerDisc3"))
    useref1 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Reference 1"))
    useref2 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Reference 2"))
    useref3 = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Reference 3"))
    viewparent = models.BooleanField(default=False, verbose_name =_("Load Parent"))
    #possibleparent = models.CharField(max_length=450,blank=True, null=True, verbose_name=_("Parent Possible"))
    possibleparent = models.ManyToManyField('self',verbose_name=_("Parent Possible"))

    ledgergoodsonway = models.ForeignKey(Ledger,related_name='OperationsTypes_ledgergoodsonway', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger Goods On The Way"))
    allowchangeprice = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Allow Item Change Price"))
    allowcashdiscount = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Allow Cash Discount"))


    viewitem = models.BooleanField(default=False, verbose_name =_("Item"))
    viewitemidentifier = models.BooleanField(default=False, verbose_name =_("Item Identifier"))
    viewitemengdesc = models.BooleanField(default=False, verbose_name =_("Item Eng Description"))
    viewitemarbdesc = models.BooleanField(default=False, verbose_name =_("Item Arb Description"))
    viewinvbinlocation = models.BooleanField(default=False, verbose_name =_("Inventory Bin Location"))
    viewquantity = models.BooleanField(default=False, verbose_name =_("Quantity"))
    viewquantitycount = models.BooleanField(default=False, verbose_name =_("Quantity Count"))
    viewisbonus = models.BooleanField(default=False, verbose_name =_("Is Bonus Quantity"))
    viewitemuom = models.BooleanField(default=False, verbose_name =_("Unit Of Measurement"))
    viewunit = models.BooleanField(default=False, verbose_name =_("Unit"))
    viewbaseunitfactor = models.BooleanField(default=False, verbose_name =_("Base Unit Factor"))
    viewbaseequivalentquantity = models.BooleanField(default=False, verbose_name =_("Base Equivalent Quantity"))
    viewbaseunit = models.BooleanField(default=False, verbose_name =_("Base Unit"))
    viewprice = models.BooleanField(default=False, verbose_name =_("Price"))
    viewpricelist = models.BooleanField(default=False, verbose_name =_("Price List"))
    vieworiginalprice = models.BooleanField(default=False, verbose_name =_("Original Price"))
    viewcostprice = models.BooleanField(default=False, verbose_name =_("Cost Price"))
    viewlastdi = models.BooleanField(default=False, verbose_name =_("Last DI Factor"))
    viewdiscper1 = models.BooleanField(default=False, verbose_name =_("Discount 1 %"))
    viewdiscper2 = models.BooleanField(default=False, verbose_name =_("Discount 2 %"))
    viewdiscper3 = models.BooleanField(default=False, verbose_name =_("Discount 3 %"))
    viewdiscamt1 = models.BooleanField(default=False, verbose_name =_("Discount 1 #"))
    viewdiscamt2 = models.BooleanField(default=False, verbose_name =_("Discount 2 #"))
    viewdiscamt3 = models.BooleanField(default=False, verbose_name =_("Discount 3 #"))
    viewbarcode = models.BooleanField(default=False, verbose_name =_("Barcode"))
    viewexpiredate = models.BooleanField(default=False, verbose_name =_("Expire Date"))
    viewbatchnumber = models.BooleanField(default=False, verbose_name =_("Batch Number"))
    viewlotdate = models.BooleanField(default=False, verbose_name =_("Lot Date"))
    viewlotnumber = models.BooleanField(default=False, verbose_name =_("Lot Number"))
    viewserialnumber = models.BooleanField(default=False, verbose_name =_("Serial Number"))
    viewlinetotal = models.BooleanField(default=False, verbose_name =_("Line Total"))
    viewtaxpercent = models.BooleanField(default=False, verbose_name =_("Tax Percent"))
    viewtaxamount = models.BooleanField(default=False, verbose_name =_("Tax Amount"))


    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname

class OperationsTypesExpensesLine(models.Model):
    operationtype = models.ForeignKey(OperationsTypes ,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Operation Type"))
    expenstype = models.ForeignKey(ExpensesTypes,blank=True, null=True,  on_delete=models.PROTECT, verbose_name=_("Expense Type"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class OperationsTypesLineViews(models.Model):
    operationtype = models.OneToOneField(OperationsTypes,related_name='OperationsTypesLineViews_Operatoiontype', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Operation Type"))
    viewitem = models.BooleanField(default=False, verbose_name =_("Auto Approved"))
    viewitemidentifier = models.BooleanField(default=False, verbose_name =_("Item Identifier"))
    viewitemengdesc = models.BooleanField(default=False, verbose_name =_("Item Eng Description"))
    viewitemarbdesc = models.BooleanField(default=False, verbose_name =_("Item Arb Description"))
    viewinvbinlocation = models.BooleanField(default=False, verbose_name =_("Inventory Bin Location"))
    viewquantity = models.BooleanField(default=False, verbose_name =_("Quantity"))
    viewquantitycount = models.BooleanField(default=False, verbose_name =_("Quantity Count"))
    viewisbonus = models.BooleanField(default=False, verbose_name =_("Is Bonus Quantity"))
    viewitemuom = models.BooleanField(default=False, verbose_name =_("Unit Of Measurement"))
    viewunit = models.BooleanField(default=False, verbose_name =_("Unit"))
    viewbaseunitfactor = models.BooleanField(default=False, verbose_name =_("Base Unit Factor"))
    viewbaseequivalentquantity = models.BooleanField(default=False, verbose_name =_("Base Equivalent Quantity"))
    viewbaseunit = models.BooleanField(default=False, verbose_name =_("Base Unit"))
    viewprice = models.BooleanField(default=False, verbose_name =_("Price"))
    viewpricelist = models.BooleanField(default=False, verbose_name =_("Price List"))
    vieworiginalprice = models.BooleanField(default=False, verbose_name =_("Original Price"))
    viewcostprice = models.BooleanField(default=False, verbose_name =_("Cost Price"))
    viewlastdi = models.BooleanField(default=False, verbose_name =_("Last DI Factor"))
    viewdiscper1 = models.BooleanField(default=False, verbose_name =_("Discount 1 %"))
    viewdiscper2 = models.BooleanField(default=False, verbose_name =_("Discount 2 %"))
    viewdiscper3 = models.BooleanField(default=False, verbose_name =_("Discount 3 %"))
    viewdiscamt1 = models.BooleanField(default=False, verbose_name =_("Discount 1 #"))
    viewdiscamt2 = models.BooleanField(default=False, verbose_name =_("Discount 2 #"))
    viewdiscamt3 = models.BooleanField(default=False, verbose_name =_("Discount 3 #"))
    viewbarcode = models.BooleanField(default=False, verbose_name =_("Barcode"))
    viewexpiredate = models.BooleanField(default=False, verbose_name =_("Expire Date"))
    viewbatchnumber = models.BooleanField(default=False, verbose_name =_("Batch Number"))
    viewlotdate = models.BooleanField(default=False, verbose_name =_("Lot Date"))
    viewlotnumber = models.BooleanField(default=False, verbose_name =_("Lot Number"))
    viewserialnumber = models.BooleanField(default=False, verbose_name =_("Serial Number"))
    viewlinetotal = models.BooleanField(default=False, verbose_name =_("Line Total"))
    viewtaxpercent = models.BooleanField(default=False, verbose_name =_("Tax Percent"))
    viewtaxamount = models.BooleanField(default=False, verbose_name =_("Tax Amount"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class Operations(models.Model):
    operationtype = models.ForeignKey(OperationsTypes,related_name='Operations_Operatoiontype' ,db_index = True, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Operation Type"))
    number = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Operation Number"))
    subject = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Subject"))
    operationdate = models.DateField(blank=True, null=True, verbose_name =_("Operation Date"))
    fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Fiscal Year Period"))
    accounttype = models.ForeignKey(LookUp,related_name='Operations_AccountType', limit_choices_to={'keyname': 'AccountType'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Account Type"))
    ledger = models.ForeignKey(Ledger, limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Ledger"))
    customer = models.ForeignKey('ar.Customers', limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Customers"))
    vendor = models.ForeignKey(Vendors, limit_choices_to={'allowaccountentry': True}, blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Vendors"))
    #employee = models.ForeignKey(Employees, limit_choices_to={'allowaccountentry': True}, blank=False, null=False,on_delete=models.PROTECT, verbose_name=_("Employees"))
    invlocation = models.ForeignKey(InventoriesLocations,related_name='Operations_invlocation',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    sourceinvlocation = models.ForeignKey(InventoriesLocations,related_name='Operations_sourceinvlocation',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("source Inventory Location"))
    destinationinvlocation = models.ForeignKey(InventoriesLocations,related_name='Operations_destinationinvlocation',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Destination Inventory Location"))
    currency = models.ForeignKey(Currency,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Currency"))
    salesperson = models.ForeignKey(Salesmans,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Salesman"))
    department = models.ForeignKey(Departments,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Department"))
    parent = models.ForeignKey('self',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Parent"))
    discper1 =models.DecimalField(decimal_places=2, max_digits=12,blank=True, null=True, verbose_name =_("Discount 1 %"))
    discper2 =models.DecimalField(decimal_places=2, max_digits=12,blank=True, null=True, verbose_name =_("Discount 2 %"))
    discper3 =models.DecimalField(decimal_places=2, max_digits=12,blank=True, null=True, verbose_name =_("Discount 3 %"))
    discamt1 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 1 #"))
    discamt2 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 2 #"))
    discamt3 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 3 #"))

    expenseamount =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Expense Amount"))
    grossamount =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Gross Amount"))
    taxamount =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Tax Amount"))
    netamount =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Net Amount"))
    totalcost =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Total Cost"))

    costcenter1 = models.ForeignKey(CostCenters,related_name='Operations_cc1', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 1"))
    costcenter2 = models.ForeignKey(CostCenters,related_name='Operations_cc2', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 2"))
    costcenter3 = models.ForeignKey(CostCenters,related_name='Operations_cc3', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 3"))
    costcenter4 = models.ForeignKey(CostCenters,related_name='Operations_cc4', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Cost center 4"))

    status = models.ForeignKey(LookUp,related_name='Operations_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Rec. Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Rec. Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Rec. Status Reason"))
    statuschangedby = models.ForeignKey(User,related_name='Operations_statuschangedby',blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Rec. Status Changed By"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    reference1 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Reference 1"))
    reference2 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Reference 2"))
    reference3 = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Reference 3"))
    islocked = models.BooleanField(blank=False, null=False, verbose_name=_("Is IsLocked"))

    rdstatus = models.ForeignKey(LookUp,related_name='Operations_rdStatus', limit_choices_to={'keyname': 'ReceiveDeliveryStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Receive & Delivery Status"))
    rdstatusdate = models.DateField(blank=True, null=True, verbose_name =_("Receive Delivery. Date"))
    rdstatusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Receive Delivery. Reason"))
    rdstatuschangedby = models.ForeignKey(User,related_name='ReceiveDelivery_statuschangedby',blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Receive Delivery. Changed By"))


    amountstatus = models.ForeignKey(LookUp,related_name='Operations_amountstatus', limit_choices_to={'keyname': 'AmountStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Amount Status"))
    amountstatusdate = models.DateField(blank=True, null=True, verbose_name =_("Amount Pay Date"))
    amountstatusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Amount Status Reason"))
    amountstatuschangedby = models.ForeignKey(User,related_name='Payment_amountchangedby',blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Amount Pay By"))


    wfstatus = models.ForeignKey('inv.WFActionsStatus' ,related_name='Operations_WFStatus', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("W. F. Status"))
    wfstatusdate = models.DateField(blank=True, null=True, verbose_name =_("W. F. Status Date"))
    wfstatusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("W. F. Status Reason"))
    wfstatuschangedby = models.ForeignKey(User,related_name='Operations_wfstatuschangedby',blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("W. F. Status Changed By"))

    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if str(self.customer ) != None :
            acc = str(self.customer )
        elif str(self.vendor ) != None :
            acc = str(self.vendor )

        elif str(self.ledger) != None:
            acc = str(self.ledger )
        else:
            acc=''
        return str(self.pk) + ' - ' + str(self.number) +  ' - ' + str(self.operationdate)  +  ' - ' +   acc


class OperationsLine(models.Model):
    operation = models.ForeignKey(Operations, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    item = models.ForeignKey(Items, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Item"))
    itemidentifier = models.ForeignKey(ItemsIdentifiers, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Identifier"))
    itemengdesc = models.CharField(max_length=100,blank=True, null=True,unique=True, verbose_name=_("Item Eng Description"))
    itemarbdesc = models.CharField(max_length=100,blank=True, null=True,unique=True, verbose_name=_("Item Arb Description"))
    invbinlocation=models.ForeignKey(InventoriesBinLocations, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Inventory Bin Location"))
    quantity =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Quantity"))
    quantitycount =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Quantity Count"))
    isbonus = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Bonus Quantity"))
    itemuom = models.ForeignKey(ItemsUOM, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    unit = models.ForeignKey(Units, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit"))
    baseunitfactor =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Base Unit Factor"))
    baseequivalentquantity =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Base Equivalent Quantity"))
    baseunit = models.ForeignKey(Units, blank=True, null=True,related_name='Operations_baseunit', on_delete=models.PROTECT, verbose_name=_("Base Unit"))
    baseuom = models.ForeignKey(ItemsUOM, blank=True, null=True,related_name='Operations_baseuom', on_delete=models.PROTECT, verbose_name=_("Base U.O.M."))
    price =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Price"))
    pricelist = models.ForeignKey(ItemsPricesLists , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Price List"))
    originalprice =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Original Price"))
    costprice =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Cost Price"))
    lastdi =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Last DI Factor"))
    discper1 =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Discount 1 %"))
    discper2 =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Discount 2 %"))
    discper3 =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Discount 3 %"))
    discamt1 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 1 #"))
    discamt2 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 2 #"))
    discamt3 =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Discount 3 #"))
    barcode = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Barcode"))
    expiredate = models.DateField(blank=True, null=True, verbose_name =_("Expire Date"))
    batchnumber = models.CharField(max_length=50,blank=True, null=True,unique=True, verbose_name=_("Batch Number"))
    lotdate = models.DateField(blank=True, null=True, verbose_name =_("Lot Date"))
    lotnumber = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Lot Number"))
    serialnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Serial Number"))
    linetotal =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Line Total"))
    taxpercent =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Tax Percent"))
    taxamount =models.DecimalField(decimal_places=6, max_digits=30,blank=True, null=True, verbose_name =_("Tax Amount"))
    tax = models.ForeignKey(Taxes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax"))
    parent = models.IntegerField( blank=True, null=True, verbose_name=_("Parent"))
    newcostprice = models.DecimalField(decimal_places=12, max_digits=30, blank=True, null=True,verbose_name=_("New Cost Price"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __int__(self):
        return self.pk

class OperationsExpensesLine(models.Model):
    operation = models.ForeignKey(Operations, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    agency = models.ForeignKey(Agencies, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Agency"))
    serviceexpense = models.ForeignKey(ExpensesTypes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Service Expense"))
    documentno = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Doc. Number"))
    documentdate = models.DateField(blank=True, null=True, verbose_name =_("Doc. Date"))
    remarks = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Remarks"))
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Currenct"))
    currencyrate =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Currency Rate"))
    amount =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Amount"))
    exptaxpercent =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Tax Percent"))
    exptaxamount =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Tax Amount"))
    explinetotal =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Line Total"))
    exptax = models.ForeignKey(Taxes, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Tax"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class OperationsStatusLog(models.Model):
    operation = models.ForeignKey(Operations , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    status = models.ForeignKey(LookUp,related_name='OperationsStatusLog_Status', limit_choices_to={'keyname': 'RecordStatus'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("Status Date"))
    statusreason = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Status Reason"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Status Changed By"))

    class Meta:
        ordering = ['-pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class ItemsCosts(models.Model):

    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    unit = models.ForeignKey(Units, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Unit"))
    itemuom = models.ForeignKey(ItemsUOM, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit"))
    warehouse = models.ForeignKey(Warehouses, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Warehouse"))
    transdate = models.DateField(blank=False, null=True, verbose_name =_("Transaction Date"))
    costprice =models.DecimalField(max_digits=30, decimal_places=12, blank=True, null=True, verbose_name =_("Cost Price"))
    itemtransid = models.IntegerField( blank=True, null=True,  verbose_name =_("Item Trans ID"))
    itemtranslineid = models.IntegerField( blank=True, null=True,  verbose_name =_("Item Trans ID"))


    class Meta:
        ordering = ['-pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.costprice

class ItemsTrans(models.Model):

    operationtype = models.ForeignKey(OperationsTypes, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation Type"))
    operation = models.ForeignKey(Operations, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    transdate = models.DateField(blank=False, null=False, verbose_name =_("Transaction Date"))
    number = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Operation Number"))
    invlocation = models.ForeignKey(InventoriesLocations,related_name='ItemsTrans_invlocation',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Fiscal Year Period"))
    parent = models.ForeignKey('self',related_name='ItemsTrans_Parent',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Parent"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk

class ItemsTransLine(models.Model):
    itemtrans = models.ForeignKey(ItemsTrans, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item Trans"))
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    itemidentifier = models.ForeignKey(ItemsIdentifiers, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Item Identifier"))
    invbinlocation=models.ForeignKey(InventoriesBinLocations, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Inventory Bin Location"))
    quantity =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Quantity"))
    quantitycount =models.DecimalField(decimal_places=3, max_digits=130,blank=True, null=True, verbose_name =_("Quantity Count"))
    isbonus = models.BooleanField(blank=False, null=False, verbose_name=_("Is Bonus Quantity"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    unit = models.ForeignKey(Units, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit"))
    baseunitfactor =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Base Unit Factor"))
    baseequivalentquantity =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Base Equivalent Quantity"))
    baseunit = models.ForeignKey(Units, blank=True, null=True,related_name='ItemsTransLine_baseunit', on_delete=models.PROTECT, verbose_name=_("Base Unit"))
    baseuom = models.ForeignKey(ItemsUOM, blank=True, null=True,related_name='ItemsTransLine_baseuom', on_delete=models.PROTECT, verbose_name=_("Base U.O.M."))
    price =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Price"))
    pricelist = models.ForeignKey(ItemsPricesLists , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Price List"))
    originalprice =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Original Price"))
    costprice =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Cost Price"))
    newcostprice =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("New Cost Price"))
    lastdi =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Last DI Factor"))
    expiredate = models.DateField(blank=True, null=True, verbose_name =_("Expire Date"))
    batchnumber = models.CharField(max_length=50,blank=True, null=True,unique=True, verbose_name=_("Batch Number"))
    lotdate = models.DateField(blank=True, null=True, verbose_name =_("Lot Date"))
    lotnumber = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("Lot Number"))
    serialnumber = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Serial Number"))
    linetotal =models.DecimalField(decimal_places=12, max_digits=30,blank=True, null=True, verbose_name =_("Line Total"))
    operationlineid = models.IntegerField( blank=True, null=True, verbose_name=_("Operation Line ID"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class Inventory(models.Model):
    invlocation = models.ForeignKey(InventoriesLocations,related_name='Inventory_invlocation',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Inventory Location"))
    invbinlocation=models.ForeignKey(InventoriesBinLocations, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Inventory Bin Location"))
    itemidentifier = models.ForeignKey(ItemsIdentifiers, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Item Identifier"))
    item = models.ForeignKey(Items, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    changedate = models.DateField(blank=False, null=False, verbose_name =_("Change Date"))
    perviouschangedate = models.DateField(blank=False, null=True, verbose_name =_("Pervious Change Date"))
    changeqty =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Change Quantity"))
    previousqtybalance =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Previous Quantity Balance"))
    qtybalance =models.DecimalField(decimal_places=3, max_digits=30,blank=True, null=True, verbose_name =_("Quantity Balance"))
    fiscalyearperiod = models.ForeignKey(FiscalYearsPeriods,  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Fiscal Year Period"))
    lastitemtrans = models.ForeignKey(ItemsTrans, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Last Item Trans"))
    lastitemtransline = models.ForeignKey(ItemsTransLine , blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Last Item Trans Line"))
    isopenbal = models.BooleanField(blank=False, null=False, verbose_name=_("Is Open Balance"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')
        unique_together = ['invlocation', 'invbinlocation','itemidentifier','item','changedate','itemuom']


    def __str__(self):
        return self.pk





class WFGroups(models.Model):
    code = models.CharField(max_length=20,blank=True, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Action Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Action Arb Name"))
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

class WFGroupsUsers(models.Model):
    group=models.ForeignKey(WFGroups, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Group"))
    user=models.ForeignKey(User , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("User"))
    levelrank = models.IntegerField( blank=False, null=False,  verbose_name =_("Level Rank"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))
    #created_date = models.DateTimeField(blank=True,auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk




class WFOperationsCycles(models.Model):
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
            return self.code + ' - ' + self.arbname
        else:
            return self.code + ' - ' + self.engname


class WFOperationsCyclesLine(models.Model):
    operationcycle = models.ForeignKey(WFOperationsCycles,related_name='WFOperationsCyclesLine_operationcycle',  blank=True, null=True,on_delete=models.PROTECT, verbose_name=_("Operation Cycle"))
    sequence = models.IntegerField( blank=False, null=False,  verbose_name =_("Sequence Rank"))
    fromoperationtype=models.ForeignKey(OperationsTypes,related_name='WFOperationsCyclesLine_fromoperationtype', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("From Operation Type"))
    tooperationtype=models.ForeignKey(OperationsTypes,related_name='WFOperationsCyclesLine_tooperationtype', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("To Operation Type"))
    actionstatus=models.ForeignKey(WFActionsStatus,related_name='WFOperationsCyclesLine_actionstatus', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Action & Status"))
    direction = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'WFDirectionsTypes'}, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Directions Types"))
    wfgroups=models.ForeignKey(WFGroups ,related_name='WFOperationsCyclesLine_wfgroups', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Workflow Group"))
    notifyapplicant = models.BooleanField(blank=False, null=False, verbose_name=_("Notify Applicant"))
    notifyrecipient = models.BooleanField(blank=False, null=False, verbose_name=_("Notify Recipient"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk



class WFOperationsStatusLog(models.Model):
    operation = models.ForeignKey(Operations , blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Operation"))
    status = models.ForeignKey(WFActionsStatus , blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("W. F. Status"))
    statusdate = models.DateField(blank=True, null=True, verbose_name =_("W. F. Status Date"))
    statuschangedby = models.ForeignKey(User,blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("W. F. Status Changed By"))

    class Meta:
        ordering = ['-pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


#---------- SATRT TARGET TABLES

class TargetBuildingBlocks(models.Model):
    code = models.CharField(max_length=20,blank=False, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    item = models.OneToOneField(Items, on_delete=models.PROTECT, verbose_name =_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    yearly_qty = models.PositiveIntegerField(blank=False, null=False)
    c_total = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100),MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.item

class TargetBuildingBlocksItems(models.Model):     #TargetBuildingBlocksProducts
    channel = models.ForeignKey(CustomersClasses, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Channel"))
    contribution = models.PositiveIntegerField(blank=False, null=False, verbose_name =_("Contribution"))
    small = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Small"))
    medium = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Medium"))
    large = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Large"))
    s_total = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100),MaxValueValidator(100)], verbose_name =_("Total %"))
    changed = models.PositiveSmallIntegerField(default=0,blank=True, null=True)
    targetbuildingblocks = models.ForeignKey(TargetBuildingBlocks, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.channel

class TargetBuildingBlocksExeption(models.Model):
    account = models.ForeignKey(Customers, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Account"))
    targetbuildingblocks = models.ForeignKey(TargetBuildingBlocks, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.account

class TargetBuildingBlocksAccounts(models.Model):
    code = models.CharField(max_length=20,blank=False, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    channel = models.ForeignKey(CustomersClasses, on_delete=models.PROTECT, verbose_name =_("Channel"))
    account = models.ForeignKey(Customers, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Account"))
    customer_size = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'AccountSize'}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer Size"))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('channel', 'account', 'customer_size', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.account

class TargetBuildingBlocksAccountsItems(models.Model):   #TargetBuildingBlocksAccountsProducts
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=False, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    small = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Small"))
    medium = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Medium"))
    large = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Large"))
    monthly_target = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("Monthly Target"))
    targetbuildingblocksaccounts = models.ForeignKey(TargetBuildingBlocksAccounts, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('targetbuildingblocksaccounts', 'item','year'),  )
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.item

class TargetBuildingBlocksChannels(models.Model):
    code = models.CharField(max_length=20,blank=False, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    channel = models.ForeignKey(CustomersClasses, on_delete=models.PROTECT, verbose_name =_("Channel"))
    customer_size = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'AccountSize'}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer Size"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('channel', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.pk

class TargetBuildingBlocksChannelsItems(models.Model):  #TargetBuildingBlocksChannelsProducts
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=False, null=True, verbose_name =_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    small = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Small"))
    medium = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Medium"))
    large = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Large"))
    targetbuildingblockschannels = models.ForeignKey(TargetBuildingBlocksChannels, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('targetbuildingblockschannels', 'item', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.item


class TargetTransactions(models.Model):
    code = models.CharField(max_length=20,blank=False, null=True, verbose_name =_("Code"))
    engname = models.CharField(max_length=100,blank=False, null=True, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    channel = models.ForeignKey(CustomersClasses, on_delete=models.PROTECT)
    account = models.ForeignKey(Customers,related_name='TargetTransactions_account', on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customers ,related_name='TargetTransactions_customer', on_delete=models.PROTECT, blank=True, null=True)
    customer_size = models.ForeignKey(LookUp,limit_choices_to={'keyname': 'AccountSize'}, blank=False, null=True, on_delete=models.PROTECT, verbose_name=_("Customer Size"))
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Item"))
    itemuom = models.ForeignKey(ItemsUOM, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Unit Of Measurement"))
    price = models.DecimalField(decimal_places=3, max_digits=12,blank=True, null=True)
    yearly_target = models.IntegerField(blank=True, null=True)
    m1 = models.IntegerField(blank=True, null=True)
    m2 = models.IntegerField(blank=True, null=True)
    m3 = models.IntegerField(blank=True, null=True)
    m4 = models.IntegerField(blank=True, null=True)
    m5 = models.IntegerField(blank=True, null=True)
    m6 = models.IntegerField(blank=True, null=True)
    m7 = models.IntegerField(blank=True, null=True)
    m8 = models.IntegerField(blank=True, null=True)
    m9 = models.IntegerField(blank=True, null=True)
    m10 = models.IntegerField(blank=True, null=True)
    m11 = models.IntegerField(blank=True, null=True)
    m12 = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    source = models.CharField(max_length=50, blank=True)
    source_id = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Countries,blank=True, null=True, on_delete=models.PROTECT)
    area = models.ForeignKey(Areas,blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(Cities,blank=True, null=True, on_delete=models.PROTECT)
    #salesman = models.ForeignKey('crm.Salesman', on_delete=models.PROTECT)
    #category = models.ForeignKey(Category, on_delete=models.PROTECT)
    isautoseasonality = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Auto Seasonality %"))

    class Meta:
        ordering = ['source_id']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.source


#---------- END TARGET TABLES

