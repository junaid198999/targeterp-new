from django.db import models
from TARGET.users.models import User
from django.utils.translation import gettext_lazy as _
from TARGET.crm.models import Currency
from sy.models import PaymentsMethods,LookUp

class ReportsGroups(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100, verbose_name=_("Arb Name"))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Parent"))
    rank = models.IntegerField(blank=True, null=True,verbose_name=_("Rank"))
    remarks = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Remarks"))

    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.code + ' - ' + self.engname



class Reports(models.Model):
    code = models.CharField(max_length=50,unique=True, verbose_name=_("Code"))
    engname = models.CharField(blank=False, null=True,max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(blank=False, null=True,max_length=100, verbose_name=_("Arb Name"))
    reportgroup = models.ForeignKey(ReportsGroups, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Report Group"))
    rank = models.IntegerField(blank=True, null=True,verbose_name=_("Rank"))
    datasource = models.CharField(blank=False, null=True,max_length=100, verbose_name=_("Data Source"))
    isprocedure = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Stored Procedure"))
    isdashboard = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Dashboard"))
    josndesign = models.CharField(blank=False, null=True,max_length=1000000, verbose_name=_("JOSN Design"))



    class Meta:
        ordering = ['code']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.code + ' - ' + self.engname



class ReportsParameters(models.Model):
    fieldname = models.CharField(max_length=60, verbose_name=_("Code"))
    engname = models.CharField(blank=False, null=True,max_length=100, verbose_name =_("Eng Name"))
    arbname = models.CharField(max_length=100,blank=True, null=True, verbose_name=_("Arb Name"))
    report = models.ForeignKey(Reports, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Report"))
    rank = models.IntegerField(blank=True, null=True,verbose_name=_("Rank"))
    datatype = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Data Type"))
    controltype = models.CharField(max_length=100,blank=True, null=True, verbose_name =_("Control Type"))
    isdisable = models.BooleanField(default=False,blank=False, null=False, verbose_name=_("Is Disable"))
    isvisible = models.BooleanField(default=True,blank=False, null=False, verbose_name=_("Is Visible"))
    canprint = models.BooleanField(default=False, blank=False, null=False, verbose_name=_("Can Print"))
    defaultvalue = models.CharField(max_length=1000,default='%',blank=True, null=True, verbose_name =_("Default Value"))


    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')
        unique_together = ['fieldname', 'report']
    def __str__(self):
        return self.engname


