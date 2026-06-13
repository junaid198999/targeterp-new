from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ImageField
from datetime import datetime
from decimal import Decimal
import datetime

from django.urls import reverse

from TARGET.users.models import User

from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from tinymce.models import HTMLField
from django.contrib.auth.models import Permission, Group

def current_year():
    return datetime.date.today().year

class Commission(models.Model):
    title = models.CharField(max_length=50, verbose_name =_("Commission Title"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('title', 'year'))
        default_permissions = ('add', 'change', 'delete', 'view', 'view_commissions_calculation', 'recalculate')

    def __str__(self):
        return self.title

class Commission_Details(models.Model):
    SALES = 1
    COLLECTION = 2
    TYPE = (
        (SALES , 'Sales'),
        (COLLECTION , 'Collection'),
    )

    AMOUNT = 1
    AMOUNTPERCENTAGE = 2
    QTY = 3
    QTYPERCENTAGE = 4
    ONWHAT = (
        (AMOUNT, "Amount"),
        (AMOUNTPERCENTAGE, "Amount %"),
        (QTY, "Quantity"),
        (QTYPERCENTAGE, "Quantity %"),
    )

    AMOUNT = 1
    PERCENTAGE = 2
    ON = (
        (AMOUNT, "Amount"),
        (PERCENTAGE, "Percentage"),
    )

    MONTHLY = 1
    QUARTELY = 2
    YEARLY = 3
    DURATION = (
        (MONTHLY, "Monthly"),
        (QUARTELY, "Quarterly"),
        (YEARLY, "Yearly"),
    )


    description = models.CharField(max_length=100, verbose_name =_("Description"))
    commission_type = models.PositiveSmallIntegerField(choices=TYPE, blank=False, default=1, verbose_name =_("Type"))
    type_value = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Value"))
    on_what = models.PositiveSmallIntegerField(choices=ONWHAT, blank=False, default=1, verbose_name =_("On"))
    onvalue = models.DecimalField(decimal_places=2, max_digits=12,blank=True, null=True, verbose_name =_("Value"))
    commission_on = models.PositiveSmallIntegerField(choices=ON, blank=False, default=1, verbose_name =_("Commission"))
    commission_value = models.DecimalField(decimal_places=3, max_digits=12,blank=True, null=True, verbose_name =_("Commission Value"))
    calculation = models.PositiveSmallIntegerField(choices=DURATION, blank=False, default=1, verbose_name =_("Calculation"))
    comission_id = models.ForeignKey(Commission, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.type

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class SalesmanGroups(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Salesman(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    email = models.EmailField(max_length=100, blank=True,null=True, verbose_name =_("Email"))
    report_to = models.ForeignKey("self", on_delete=models.PROTECT, blank=False, null=True, verbose_name =_("Report To"))
    reporting_to = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=True, related_name='reporting_to', verbose_name =_("Reporting To"))
    user = models.ForeignKey(User,null=True, on_delete=models.PROTECT, verbose_name =_("User"))
    allowed_discount = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True, verbose_name =_("Allowed Discount"))
    commission = models.ForeignKey(Commission, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Commission"))
    noofvisitperday = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("No Of Visit Per Day"))
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name =_("Mobile"))
    salesmangroups = models.ForeignKey(SalesmanGroups, null=True, on_delete=models.PROTECT, verbose_name =_("Salesmen Group"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Commission_Calc(models.Model):
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    description = models.CharField(max_length=100, verbose_name =_("Description"))
    target = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Target"))
    sales = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Sales"))
    sales_return = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Sales Return"))
    collection = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Collection"))
    commission = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Commission"))
    paid_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Paid Amount"))
    paid = models.BooleanField(default=False, verbose_name =_("Paid"))
    comission_id = models.ForeignKey(Commission, on_delete=models.PROTECT)
    from_date = models.DateField(blank=True, null=True, verbose_name =_("From Date"))
    to_date = models.DateField(blank=True, null=True, verbose_name =_("To Date"))
    month = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Month"))
    calc_desc = models.CharField(blank=True,max_length=100)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.salesman

class Channel(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    parent_channel_id = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Parent Channel"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

    # @property
    # def owner(self):
    #     return 'admin'
    #
    # def get_api_url(self, request=None):
    #     return api_reverse("crm:api-channel:channel-rud", kwargs={'pk': self.pk}, request=request)

class Notification(models.Model):
    NORMAL = 0
    URGENT = 1
    PRIORITY = (
        (NORMAL, 'Normal'),
        (URGENT, 'Urgent'),
    )
    source = models.CharField(max_length=50, verbose_name =_("Task"))
    source_id = models.IntegerField(blank=True, null=True, verbose_name =_("Source ID"))
    message = models.CharField(max_length=1024, blank=True, verbose_name =_("Message"))
    from_user = models.ForeignKey(User, related_name='user1', on_delete=models.PROTECT, verbose_name =_("From User"))
    to_user = models.ForeignKey(User, related_name='user2', on_delete=models.PROTECT, verbose_name =_("To User"))
    read = models.BooleanField(default=False, verbose_name =_("Read"))
    urgent = models.PositiveSmallIntegerField(choices=PRIORITY, default=0, verbose_name =_("Priority"))
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name =_("URL"))
    attachment = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name =_("Attachment"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['read','created_date']
        default_permissions = ('add', 'change', 'delete', 'view', 'reply')

    def __str__(self):
        return self.source

class UnitsName(models.Model):
    unit_1 = models.CharField(max_length=30, verbose_name =_("Unit 1"))
    unit_2 = models.CharField(max_length=30, verbose_name =_("Unit 2"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    def __str__(self):
        return self.unit_1

class Uom(models.Model):
    name = models.CharField(max_length=30, verbose_name =_("Unit"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=30, verbose_name =_("Name"))
    name_l2 = models.CharField(max_length=30, blank=True, verbose_name =_("Name Language 2"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.name_l2
        else:
            return self.name

class Area(models.Model):
    name = models.CharField(max_length=30, verbose_name =_("Name"))
    name_l2 = models.CharField(max_length=30, blank=True, verbose_name =_("Name Language 2"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.name_l2
        else:
            return self.name

class City(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name =_("Area"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    name = models.CharField(max_length=30, verbose_name =_("Name"))
    name_l2 = models.CharField(max_length=30, blank=True, verbose_name =_("Name Language 2"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        if get_language() == 'ar':
            return self.name_l2
        else:
            return self.name

class WarehouseType(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=30, verbose_name =_("Name"))
    address = models.CharField(max_length=1024, blank=True, verbose_name =_("Address"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    warehousetype = models.ForeignKey(WarehouseType, on_delete=models.PROTECT, verbose_name =_("Warehouse Type"))
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name =_("Area"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name =_("City"))
    size = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Size"))
    capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Capacity"))
    shelves = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Shelves"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=30, verbose_name =_("Name"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Contract(models.Model):
    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),

    )
    ACTIVE = 1
    INACTIVE = 2
    HOLD = 3
    CANCELED = 4
    STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (HOLD, 'Hold'),
        (CANCELED, 'Canceled'),
    )
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    contract_number = models.CharField(max_length=50, blank=True, verbose_name =_("CO No"))
    startdate = models.DateField(blank=True, null=True, verbose_name =_("Start Date"))
    enddate = models.DateField(blank=True, null=True, verbose_name =_("End Date"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))
    target1_discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Target 1 Discount"))
    target2_discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Target 2 Discount"))
    target3_discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Target 3 Discount"))
    payment_terms = models.PositiveSmallIntegerField(choices=PAY_TERM, verbose_name =_("Payment Terms"))

    inv_dis1 = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Invoice Discount 1"))
    inv_dis2 = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Invoice Discount 2"))
    bonus = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Bonus %"))
    bonus_uint = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Bonus Unit"))
    rebate = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Rebate %"))
    marketing_support = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Marketing Support"))
    scientific_support = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Scientific Support"))
    training = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Training"))

    approved = models.BooleanField(default=False, verbose_name =_("Approved"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'print', 'details')

    def __str__(self):
        return str(self.name)

class Class(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    visits = models.PositiveIntegerField(null=True, verbose_name =_("Visits"))
    doctor_c = models.BooleanField(default=False, verbose_name =_("Doctor"))
    pharmacy_c = models.BooleanField(default=False, verbose_name =_("Pharmacy"))
    customer_c = models.BooleanField(default=False, verbose_name =_("Customer"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Customer(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )

    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),

    )

    ACTIVE = 1
    INACTIVE = 0
    STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'In Active'),

    )
    SUPERMARKET = 1
    DOCTOR = 2
    PHARMACY = 3
    CUS_TYPE = (
        (SUPERMARKET, 'FMCG'),
        (DOCTOR, 'Doctor'),
        (PHARMACY, 'Pharmacy'),

    )
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"), related_name='channels')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Account"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    customer_size = models.PositiveSmallIntegerField(default=NONE, choices=CUST_SIZE, verbose_name =_("Customer Size"))
    branches = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Branches"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name =_("Area"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name =_("City"))
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name =_("Address"))
    credit_limit = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Credit Limit"))
    payment_terms = models.PositiveSmallIntegerField(choices=PAY_TERM, verbose_name =_("Payment Terms"))
    customer_type = models.PositiveSmallIntegerField(default=1, choices=CUS_TYPE, verbose_name =_("Customer Type"))
    payment_days = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Due Days"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    libility = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Libility"))
    contact1_name = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 1 Name"))
    contact1_title = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 1 Title"))
    contact1_mobile = models.CharField(max_length=32, blank=True, null=True, verbose_name =_("Contact 1 Mobile #"))
    contact2_name = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 2 Name"))
    contact2_title = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 2 Title"))
    contact2_mobile = models.CharField(max_length=32, blank=True, null=True, verbose_name =_("Contact 2 Mobile #"))
    contact3_name = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 3 Name"))
    contact3_title = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Contact 3 Title"))
    contact3_mobile = models.CharField(max_length=32, blank=True, null=True, verbose_name =_("Contact 3 Mobile #"))
    contract1 = models.ForeignKey(Contract, blank=True, null=True, related_name='contract1', on_delete=models.PROTECT, verbose_name =_("Contract 1"))
    contract2 = models.ForeignKey(Contract, blank=True, null=True, related_name='contract2', on_delete=models.PROTECT, verbose_name =_("Contract 2"))
    contract3 = models.ForeignKey(Contract, blank=True, null=True, related_name='contract3', on_delete=models.PROTECT, verbose_name =_("Contract 3"))

    store_code = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Store Code"))
    retail_brand_name = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Retail Brand Name"))
    store_format = models.CharField(max_length=50, blank=True, null=True, verbose_name =_("Store Format"))
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS, verbose_name =_("Status"))
    customer_class = models.ForeignKey(Class, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Class"))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("User"))
    timestamp = models.DateField(auto_now_add=True, blank=True, auto_now=False, verbose_name =_("Created Date"))

    @cached_property
    def duedate(self):
        if self.payment_days == None:
            paymentdays = 0
        else:
            paymentdays = self.payment_days
        return datetime.date.today() + datetime.timedelta(paymentdays)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    dgree = models.CharField(max_length=50, null=True, verbose_name =_("Degree"))
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, verbose_name =_("Specialty"))
    account1 = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Customer 1"))
    account2 = models.ForeignKey(Customer, related_name='account2', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Customer 2"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    mobile = models.CharField(max_length=32, blank=True, null=True, verbose_name =_("Contact #"))
    doctor_category = models.ForeignKey(Class, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Class"))
    monthly_target = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Monthly Sales Target"))
    note = models.CharField(max_length=1000, null=True, verbose_name =_("Note"))
    approved = models.BooleanField(default=False, verbose_name =_("Approved"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve')

    def __str__(self):
        return self.pk

class DoctorVisits(models.Model):
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Doctor"))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    date_p = models.DateField(blank=True, null=True, verbose_name =_("Date"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))
    added = models.BooleanField(default=False, verbose_name =_("Added"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'print')

    def __str__(self):
        return self.pk

class DoctorDates(models.Model):
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.PROTECT, verbose_name =_("Doctor"))
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    date_p = models.DateField(blank=True, null=True, verbose_name =_("Date"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))
    added = models.BooleanField(default=False, verbose_name =_("Added"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk


class PharmacyCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    visits = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Visits"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Pharmacy(Customer):
    pharmacy_description = models.CharField(max_length=1024, blank=True, verbose_name =_("Pharmacy Description"))
    pharmacy_category = models.ForeignKey(PharmacyCategory, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Category"))
    approved = models.BooleanField(default=False, verbose_name =_("Approved"))

    class Meta:
        ordering = ['pharmacy_description']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pharmacy_description

class Branch(models.Model):
    SMALL = 1
    MEDIUM = 2
    BIG = 3
    BRNCH_SIZE = (
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    branch_size = models.PositiveSmallIntegerField(choices=BRNCH_SIZE, verbose_name =_("Branch Size"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    area = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name =_("Area"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name =_("City"))
    address = models.CharField(max_length=1024, blank=True, verbose_name =_("Address"))
    timestamp = models.DateField(auto_now_add=True, auto_now=False, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    parent_category = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Parent Category"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    parent_brand = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Parent Brand"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name =_("Name"))
    sku = models.CharField(max_length=50,blank=True, verbose_name =_("SKU"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name =_("Category"))
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Brand"))
    cost = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True, verbose_name =_("Cost Price"))
    price = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True, verbose_name =_("Price 1"))
    barcode = models.CharField(max_length=50,blank=True, verbose_name =_("Barcode"))
    unit_1 = models.PositiveIntegerField(blank=False, null=False, default=1, verbose_name =_("Unit 1"))
    unit_2 = models.PositiveIntegerField(blank=True, null=True, default=12, verbose_name =_("Unit 2"))
    price_2 = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True, verbose_name =_("Price 2"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, blank=True, null=True, related_name = 'uomone', default=1)
    uom2 = models.ForeignKey(Uom, on_delete=models.PROTECT, blank=True, null=True, related_name = 'uomtwo', default=2)
    packing = models.PositiveIntegerField(blank=True, null=True, default=12, verbose_name =_("Packing"))
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Weight"))
    monthly_safety_stock = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Safety Stock / M"))
    image = ImageField(upload_to='images/', max_length=255, blank=True, null=True, verbose_name =_("Product Image"))
    ti = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("TI"))
    hi = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("HI"))
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

    timestamp = models.DateField(auto_now_add=True, auto_now=False, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

    # @property
    # def owner(self):
    #     return 'admin'
    #
    # def get_api_url(self, request=None):
    #     return api_reverse("crm:api-product:post-rud", kwargs={'pk': self.pk}, request=request)

class ActualVisit(models.Model):

    DOCTOR = 1
    CUSTOMER = 2
    SOURCE = (
        (DOCTOR, "Doctor"),
        (CUSTOMER, "Customer"),
    )

    source = models.PositiveSmallIntegerField(choices=SOURCE, blank=True, null=True, verbose_name =_("Source"))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Doctor"))
    feedback = models.CharField(max_length=1024, verbose_name =_("Feed Back"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Assigned to"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    conv_salesorder_id = models.IntegerField(blank=True, null=True, verbose_name =_("Sales Order"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view', 'convert_salesorder')

    def __str__(self):
        return self.customer

class ContractProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    retail_price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Retail Price"))
    distributor_price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Distributor Price"))
    inv_discount1 = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Invoice Discount 1"))
    inv_discount2 = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Invoice Discount 2"))
    p_bonus = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Bonus %"))
    p_bonus_uint = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Bonus units"))
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))

    class Meta:
        ordering = ['contract']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class Vendor(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    contact_person = models.CharField(max_length=100, blank=True, verbose_name =_("Contact Person"))
    mobile = models.CharField(max_length=32, blank=True, verbose_name =_("Mobile"))
    office_phone = models.CharField(max_length=32, blank=True, verbose_name =_("Office Phone"))
    email = models.EmailField(max_length=100, blank=True, verbose_name =_("Email"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name =_("Country"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name =_("City"))
    address = models.CharField(max_length=1024, blank=True, verbose_name =_("Address"))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("User"))
    timestamp = models.DateField(auto_now_add=True, auto_now=False, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    purchaseorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("PO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name =_("Vendor"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    payment_terms = models.CharField(max_length=50,blank=True, verbose_name =_("Payment Terms"))
    total = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Total"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject

class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Subtotal"))
    purchaseorder = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['purchaseorder']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class PurchaseReturnOrder(models.Model):
    purchasreturneorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("PRO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name =_("Vendor"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    payment_terms = models.CharField(max_length=50,blank=True, verbose_name =_("Payment Terms"))
    total = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Total"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject

class PurchaseReturnProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Subtotal"))
    purchaseorder = models.ForeignKey(PurchaseReturnOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['purchaseorder']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class SalesOrder(models.Model):
    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),

    )

    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    )
    salesorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    payment_terms = models.PositiveSmallIntegerField(choices=PAY_TERM, verbose_name =_("Payment Terms"))
    payment_days = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Due Days"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    paid = models.BooleanField(default=False, verbose_name =_("Paid"))
    returned = models.BooleanField(default=False, verbose_name =_("Returned"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject

class SalesProduct(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),

    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Subtotal"))
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    salesorder = models.ForeignKey(SalesOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['salesorder']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class CustomerSalesOrder(models.Model):
    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),

    )

    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    )
    salesorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SO No"))
    sales_id = models.IntegerField(blank=True, null=True, verbose_name =_("Sales Order Id"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    payment_terms = models.PositiveSmallIntegerField(choices=PAY_TERM, verbose_name =_("Payment Terms"))
    payment_days = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Due Days"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    paid = models.BooleanField(default=False, verbose_name =_("Paid"))
    returned = models.BooleanField(default=False, verbose_name =_("Returned"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'view_ecommerce', 'approve', 'print')

    def __str__(self):
        return self.subject

class CustomerSalesProduct(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),

    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Subtotal"))
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    salesorder = models.ForeignKey(CustomerSalesOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['salesorder']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class SalesReturnOrder(models.Model):
    salesreturnorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SRO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    payment_terms = models.CharField(max_length=50,blank=True, verbose_name =_("Payment Terms"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Net Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    salesorderid = models.IntegerField(blank=True, null=True, verbose_name =_("Sales Order Id"))

    def save(self, *args, **kwargs):
        companies = Company.objects.all().values()
        try:
            maxsoid = int(SalesReturnOrder.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        if companies[0]['sales_return_prefix'] == None:
            salesreturn_prefix = "SRO-"
        else:
            salesreturn_prefix = companies[0]['sales_return_prefix']

        self.salesreturnorder_number = salesreturn_prefix + str(maxsoid)
        return super(SalesReturnOrder, self).save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject

class SalesReturnProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Subtotal"))
    salesorder = models.ForeignKey(SalesReturnOrder, on_delete=models.PROTECT)
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class TransferOrder(models.Model):
    transferorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("TO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['subject']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.pk

class TransferProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.IntegerField(blank=True, null=True, verbose_name =_("Qty"))
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("From Warehouse"))
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='WarehouseB', verbose_name =_("To Warehouse"))
    transferorder = models.ForeignKey(TransferOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['product']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.pk

class TargetBuildingBlocksold(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    product = models.OneToOneField(Product, on_delete=models.PROTECT, verbose_name =_("Product"))
    yearly_qty = models.PositiveIntegerField(blank=False, null=False)
    c_total = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100),MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.product

class TargetBuildingBlocksProducts(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Channel"))
    contribution = models.PositiveIntegerField(blank=False, null=False, verbose_name =_("Contribution"))
    small = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Small"))
    medium = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Medium"))
    large = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Large"))
    s_total = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100),MaxValueValidator(100)], verbose_name =_("Total %"))
    changed = models.PositiveSmallIntegerField(default=0,blank=True, null=True)
    targetbuildingblocks = models.ForeignKey(TargetBuildingBlocksold, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.channel

class TargetBuildingBlocksExeption(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Account"))
    targetbuildingblocks = models.ForeignKey(TargetBuildingBlocksold, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.account

class TargetBuildingBlocksAccounts(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Account"))
    customer_size = models.PositiveSmallIntegerField(choices=CUST_SIZE, verbose_name =_("Customer Size"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('channel', 'account', 'customer_size', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.customer

class TargetBuildingBlocksAccountsProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    monthly_target = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("Monthly Target"))
    targetbuildingblocksaccounts = models.ForeignKey(TargetBuildingBlocksAccounts, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('targetbuildingblocksaccounts', 'product','year'),  )
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class TargetBuildingBlocksChannels(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    customer_size = models.PositiveSmallIntegerField(choices=CUST_SIZE, verbose_name =_("Customer Size"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('channel', 'customer_size', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.customer

class TargetBuildingBlocksChannelsProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    monthly_target = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("Monthly Target"))
    targetbuildingblockschannels = models.ForeignKey(TargetBuildingBlocksChannels, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('targetbuildingblockschannels', 'product', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class TargetCategoryChannels(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    customer_size = models.PositiveSmallIntegerField(choices=CUST_SIZE, verbose_name =_("Customer Size"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('channel', 'customer_size', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'rebuild')

    def __str__(self):
        return self.customer

class TargetCategoryChannelsProducts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Category"))
    monthly_target = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("Monthly Target"))
    targetcategorychannels = models.ForeignKey(TargetCategoryChannels, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    year = models.IntegerField(default=current_year, verbose_name =_("Year"))

    class Meta:
        ordering = ['pk']
        unique_together = (('targetcategorychannels', 'category', 'year'),)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.category

class Transactions(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    source = models.CharField(max_length=50, blank=True)
    source_id = models.CharField(max_length=50, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    ctrqty = models.DecimalField(decimal_places=2, max_digits=12)
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True)
    tax = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True)
    nettotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, blank=True, null=True)
    customer_size = models.PositiveSmallIntegerField(choices=CUST_SIZE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['source_id']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.source

class TargetTransactions(models.Model):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    CUST_SIZE = (
        (NONE, 'None'),
        (SMALL, 'Small Business'),
        (MEDIUM, 'Medium Business'),
        (BIG, 'Larg Business'),
    )
    name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    customer_size = models.PositiveSmallIntegerField(choices=CUST_SIZE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    price = models.PositiveIntegerField(blank=True, null=True)
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
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['source_id']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.source

class FinancialYear(models.Model):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12
    MONTH = (
        (JAN, 'JAN'),
        (FEB, 'FEB'),
        (MAR, 'MAR'),
        (APR, 'APR'),
        (MAY, 'MAY'),
        (JUN, 'JUN'),
        (JUL, 'JUL'),
        (AUG, 'AUG'),
        (SEP, 'SEP'),
        (OCT, 'OCT'),
        (NOV, 'NOV'),
        (DEC, 'DEC'),
    )
    m1 = models.PositiveSmallIntegerField(choices=MONTH)
    m2 = models.PositiveSmallIntegerField(choices=MONTH)
    m3 = models.PositiveSmallIntegerField(choices=MONTH)
    m4 = models.PositiveSmallIntegerField(choices=MONTH)
    m5 = models.PositiveSmallIntegerField(choices=MONTH)
    m6 = models.PositiveSmallIntegerField(choices=MONTH)
    m7 = models.PositiveSmallIntegerField(choices=MONTH)
    m8 = models.PositiveSmallIntegerField(choices=MONTH)
    m9 = models.PositiveSmallIntegerField(choices=MONTH)
    m10 = models.PositiveSmallIntegerField(choices=MONTH)
    m11 = models.PositiveSmallIntegerField(choices=MONTH)
    m12 = models.PositiveSmallIntegerField(choices=MONTH)

    class Meta:
        ordering = ['m1']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.source

class Collection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Customer"))
    salesorder = models.IntegerField(blank=False, null=True, verbose_name =_("Sales Order"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'print')

    def __str__(self):
        return self.customer

class Currency(models.Model):
    code = models.CharField(max_length=3, verbose_name =_("Code"))
    name = models.CharField(max_length=50, blank=True, verbose_name =_("Name"))
    symbol = models.CharField(max_length=3, blank=False, verbose_name =_("Symbol"))
    rate = models.DecimalField(decimal_places=8, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))], verbose_name =_("rate"))
    default = models.BooleanField(default=False, verbose_name =_("Default"))
    active = models.BooleanField(default=False, verbose_name =_("Active"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.code

class Calender(models.Model):
    NORMAL = 0
    URGENT = 1
    PRIORITY = (
        (NORMAL, 'Normal'),
        (URGENT, 'Urgent'),
    )
    source = models.CharField(max_length=50, verbose_name =_("Task"))
    salesman = models.ForeignKey(Salesman, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    source_id = models.IntegerField(blank=True, null=True, verbose_name =_("Source ID"))
    message = models.CharField(max_length=1024, blank=True, verbose_name =_("Message"))
    from_user = models.ForeignKey(User, related_name='c_user1', on_delete=models.PROTECT, verbose_name =_("From User"))
    to_user = models.ForeignKey(User, related_name='c_user2', on_delete=models.PROTECT, verbose_name =_("To User"))
    urgent = models.PositiveSmallIntegerField(choices=PRIORITY, default=0, verbose_name =_("Priority"))
    start = models.DateField(blank=True, null=True, verbose_name =_("Start Date"))
    end = models.DateField(blank=True, null=True, verbose_name =_("End Date"))
    classname = models.CharField(blank=True, null=True, max_length=50, verbose_name =_("Class"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.source

class Events(models.Model):
    title = models.CharField(max_length=1024, blank=True, verbose_name =_("Title"))
    user = models.ForeignKey(User, related_name='event_user', on_delete=models.PROTECT, verbose_name =_("User"))
    classname = models.CharField(blank=True, null=True, max_length=50, verbose_name =_("Class"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.message


class Lead(models.Model):
    NEW = 1
    ASSIGNED = 2
    IN_PROCESS = 3
    CONVERTED = 4
    RECYCLED = 5
    DEAD = 6
    STATUS = (
        (NEW, 'New'),
        (ASSIGNED, 'Assigned'),
        (IN_PROCESS, 'In Process'),
        (CONVERTED, 'Converted'),
        (RECYCLED, 'Recycled'),
        (DEAD, 'Dead'),
    )

    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),
    )

    COLD_CALL = 1
    EXISTING_CUSTOMER = 2
    SELF_GENERATED = 3
    EMPLOYEE = 4
    PARTNER = 5
    PUBLIC_RELATION = 6
    DIRECT_MAIL = 7
    CONFERENCE = 8
    TRADE_SHOW = 9
    WEB_SITE = 10
    WORD_OF_MOUTH = 11
    EMAIL = 12
    CAMPAIGN = 13
    OTHER = 14
    LEAD_SOURCE = (
        (COLD_CALL, "Cold Call"),
        (EXISTING_CUSTOMER, "Existing Customer"),
        (SELF_GENERATED, "Self Generated"),
        (EMPLOYEE, "Employee"),
        (PARTNER, "Partner"),
        (PUBLIC_RELATION, "Public Relation"),
        (DIRECT_MAIL, "Direct Mail"),
        (CONFERENCE, "Conference"),
        (TRADE_SHOW, "Trade Show"),
        (WEB_SITE, "Web Site"),
        (WORD_OF_MOUTH, "Word of Mouth"),
        (EMAIL, "Email"),
        (CAMPAIGN, "Campaign"),
        (OTHER, "Other")
    )

    name = models.CharField(max_length=50, verbose_name =_("Name"))
    office_phone = models.CharField(max_length=32, blank=True, verbose_name =_("Office Phone"))
    title = models.CharField(max_length=50, blank=True, verbose_name =_("Title"))
    mobile = models.CharField(max_length=32, blank=True, verbose_name =_("Mobile"))
    department = models.CharField(max_length=50, blank=True, verbose_name =_("Department"))
    fax = models.CharField(max_length=32, blank=True, verbose_name =_("Fax"))
    account_name = models.CharField(max_length=50, blank=True, verbose_name =_("Account Name"))
    website = models.CharField(max_length=100, blank=True, verbose_name =_("Website"))
    address = models.CharField(max_length=1024, blank=True, verbose_name =_("Address"))
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Country"))
    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Area"))
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("City"))
    postal_code = models.CharField(max_length=100, blank=True, verbose_name =_("Postal Code"))
    other_address = models.CharField(max_length=1024, blank=True, verbose_name =_("Other Address"))
    other_country = models.ForeignKey(Country, blank=True, null=True, related_name='other_country', on_delete=models.PROTECT, verbose_name =_("Country"))
    other_area = models.ForeignKey(Area, blank=True, null=True, related_name='other_area', on_delete=models.PROTECT, verbose_name =_("Area"))
    other_city = models.ForeignKey(City, blank=True, null=True, related_name='other_city', on_delete=models.PROTECT, verbose_name =_("City"))
    other_postal_code = models.CharField(max_length=100, blank=True, verbose_name =_("Postal Code"))
    email = models.EmailField(max_length=100, blank=True, verbose_name =_("Email Address"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name =_("Status"))
    status_description = models.CharField(max_length=1024, blank=True, verbose_name =_("Status Description"))
    opportunity_name = models.CharField(max_length=1024, blank=True, verbose_name =_("Opportunity Name"))
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Opportunity Amount"))
    lead_Source = models.PositiveSmallIntegerField(choices=LEAD_SOURCE, verbose_name =_("Lead Source"))
    lead_description = models.CharField(max_length=1024, blank=True, verbose_name =_("Status Source Description"))
    referred_by = models.CharField(max_length=100, blank=True, verbose_name =_("Referred By"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Assigned to"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    donotcall = models.BooleanField(default=False, verbose_name =_("Do Not Call"))
    converted = models.BooleanField(default=False, verbose_name =_("Converted"))
    conv_customer_id = models.IntegerField(blank=True, null=True, verbose_name =_("Customer Id"))
    conv_date = models.DateField(blank=True, null=True, verbose_name =_("Converted Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view', 'import', 'convert')

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    PROSPECTING = 1
    QUALIFICATION = 2
    NEEDS_ANALYSIS = 4
    VALUE_PROPOSITION = 6
    IDENTIFYING_DECISION_MAKERS = 9
    PERCEPTION_ANALYSIS = 11
    PROPOSAL_PRICE_QUOTE = 13
    NEGOTIATION_REVIEW = 14
    CLOSED_WON = 16
    CLOSEDL_OST = 18


    STAGE = (
        (PROSPECTING , 'Prospecting'),
        (QUALIFICATION , 'Qualification'),
        (NEEDS_ANALYSIS , 'Needs Analysis'),
        (VALUE_PROPOSITION , 'Value Proposition'),
        (IDENTIFYING_DECISION_MAKERS , 'Identifying Decision Makers'),
        (PERCEPTION_ANALYSIS , 'Perception Analysis'),
        (PROPOSAL_PRICE_QUOTE , 'Proposal/Price Quote'),
        (NEGOTIATION_REVIEW , 'Negotiation/Review'),
        (CLOSED_WON , 'Closed Won'),
        (CLOSEDL_OST , 'Closed Lost')
    )

    COLD_CALL = 1
    EXISTING_CUSTOMER = 2
    SELF_GENERATED = 3
    EMPLOYEE = 4
    PARTNER = 5
    PUBLIC_RELATION = 6
    DIRECT_MAIL = 7
    CONFERENCE = 8
    TRADE_SHOW = 9
    WEB_SITE = 10
    WORD_OF_MOUTH = 11
    EMAIL = 12
    CAMPAIGN = 13
    OTHER = 14
    LEAD_SOURCE = (
        (COLD_CALL, "Cold Call"),
        (EXISTING_CUSTOMER, "Existing Customer"),
        (SELF_GENERATED, "Self Generated"),
        (EMPLOYEE, "Employee"),
        (PARTNER, "Partner"),
        (PUBLIC_RELATION, "Public Relation"),
        (DIRECT_MAIL, "Direct Mail"),
        (CONFERENCE, "Conference"),
        (TRADE_SHOW, "Trade Show"),
        (WEB_SITE, "Web Site"),
        (WORD_OF_MOUTH, "Word of Mouth"),
        (EMAIL, "Email"),
        (CAMPAIGN, "Campaign"),
        (OTHER, "Other")
    )

    LEAD = 1
    CUSTOMER = 2
    SOURCE = (
        (LEAD, "Lead"),
        (CUSTOMER, "Customer"),
    )

    EXISTING_BUSINESS = 1
    NEW_BUSINESS = 2
    TYPE = (
        (EXISTING_BUSINESS, "Existing Business"),
        (NEW_BUSINESS, "New Business")

    )

    name = models.CharField(max_length=50, verbose_name =_("Opportunity Name"))
    source = models.PositiveSmallIntegerField(choices=SOURCE, blank=True, null=True, verbose_name =_("Source"))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    lead = models.ForeignKey(Lead, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Lead"))
    closedate = models.DateField(blank=True, null=True, verbose_name =_("Expected Close Date"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Opportunity Amount"))
    stage = models.PositiveSmallIntegerField(choices=STAGE, blank=False, default=0, verbose_name =_("Sales Stage"))
    type = models.PositiveSmallIntegerField(choices=TYPE, verbose_name =_("Type"))
    lead_Source = models.PositiveSmallIntegerField(choices=LEAD_SOURCE, verbose_name =_("Lead Source"))
    probability = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Probability"))
    campaign = models.CharField(max_length=100, blank=True, verbose_name =_("Campaign"))
    next_step = models.CharField(max_length=100, blank=True, verbose_name =_("Next Step"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Assigned to"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    converted = models.BooleanField(default=False, verbose_name =_("Converted"))
    conv_salesorder_id = models.IntegerField(blank=True, null=True, verbose_name =_("Sales Order"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    conv_date = models.DateField(blank=True, null=True, verbose_name =_("Converted Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view', 'convert')

    def __str__(self):
        return self.name

class OpportunityProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Subtotal"))
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    opportunity_id = models.ForeignKey(Opportunity, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))

    class Meta:
        ordering = ['opportunity_id']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class Activities(models.Model):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    PENDING_INPUT = 4
    DEFERRED = 5
    STATUS = (
        (NOT_STARTED , 'Not Started'),
        (IN_PROGRESS , 'In Progress'),
        (COMPLETED , 'Completed'),
        (PENDING_INPUT , 'Pending Input'),
        (DEFERRED , 'Deferred'),
    )

    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    )

    LEAD = 1
    CUSTOMER = 2
    OPPORTUNITY = 3
    SOURCE = (
        (LEAD, "Lead"),
        (CUSTOMER, "Customer"),
        (OPPORTUNITY, "Opportunity"),
    )


    subject = models.CharField(max_length=50, verbose_name =_("Subject"))
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=False, default=0, verbose_name =_("Status"))
    source = models.PositiveSmallIntegerField(choices=SOURCE, blank=True, null=True, verbose_name =_("Source"))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    lead = models.ForeignKey(Lead, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Lead"))
    opportunity = models.ForeignKey(Opportunity, blank=True, null=True, on_delete=models.PROTECT, verbose_name =_("Opportunity"))
    startdate = models.DateField(blank=True, null=True, verbose_name =_("Start Date"))
    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, blank=False, default=0, verbose_name =_("Priority"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Assigned to"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['subject']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.subject

class AccountingChild(models.Model):
    number = models.IntegerField(blank=True, null=True, verbose_name =_("Account Nubmber"))
    parent = models.IntegerField(blank=True, null=True, verbose_name =_("Parent"))
    name = models.CharField(max_length=100, verbose_name =_("Account Name"))
    description = models.CharField(max_length=2000, verbose_name =_("Description"))
    created_date = models.DateField(auto_now_add=True, verbose_name =_("Created Date"))
    active = models.BooleanField(default=False, verbose_name =_("Active"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))

    def __str__(self):
        return self.name

class AccountingParent(models.Model):
    number = models.IntegerField(blank=True, null=True, verbose_name =_("Account Nubmber"))
    name = models.CharField(max_length=100, verbose_name =_("Account Name"))
    description = models.CharField(blank=True, null=True, max_length=2000, verbose_name =_("Description"))
    created_date = models.DateField(auto_now_add=True, verbose_name =_("Created Date"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))
    active = models.BooleanField(default=True, verbose_name =_("Active"))
    accounting_child = models.ManyToManyField(AccountingChild, blank=True, verbose_name =_("Child Account"))

    def __str__(self):
        return self.name

class AccountingType(models.Model):
    name = models.CharField(max_length=100, verbose_name =_("Name"))
    description = models.CharField(blank=True, null=True, max_length=2000, verbose_name =_("Description"))
    accounting_parent = models.ManyToManyField(AccountingParent, blank=True, verbose_name =_("Parent Account"))

    def __str__(self):
        return self.name

class AccTransactions(models.Model):
    description = models.CharField(max_length=100, verbose_name =_("Description"))
    note = models.CharField(max_length=1000, verbose_name =_("Note"))
    Total = models.IntegerField(blank=True, null=True, verbose_name =_("Total"))
    reviewd = models.BooleanField(default=False, verbose_name =_("Reviewd"))
    last_modified = models.DateField(auto_now=True, verbose_name =_("Last Modified"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    def __str__(self):
        return self.description

class AccTransactionsDetails(models.Model):
    debits = models.IntegerField(blank=True, null=True, verbose_name =_("Debit"))
    d_acc = models.ForeignKey(AccountingChild, related_name='DebitAccount',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Debit Acc"))
    d_desc = models.CharField(max_length=100, verbose_name =_("Debit Description"))
    credits = models.IntegerField(blank=True, null=True, verbose_name =_("Credit"))
    c_acc = models.ForeignKey(AccountingChild, related_name='CreditAccount',blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Credit Acc"))
    c_desc = models.CharField(max_length=100, verbose_name =_("Credit Description"))
    balance = models.IntegerField(blank=True, null=True, verbose_name =_("Balance"))
    customer = models.ForeignKey(Customer,blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Customer"))
    vendor = models.ForeignKey(Vendor,blank=True, null=True, on_delete=models.CASCADE, verbose_name =_("Vendor"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name =_("User"))
    acc_trans_id = models.ForeignKey(AccTransactions, on_delete=models.PROTECT)
    last_modified = models.DateField(auto_now=True, verbose_name =_("Last Modified"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    def __str__(self):
        return self.d_desc

class Document(models.Model):
    title = models.CharField(max_length=50, verbose_name =_("Title"))
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    note = HTMLField()
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name =_("URL"))
    attachment = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name =_("Attachment"))
    active = models.BooleanField(default=True, verbose_name =_("Active"))
    version = models.CharField(blank=True, null=True, max_length=50, verbose_name =_("Version"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=100, verbose_name =_("Title"))
    active = models.BooleanField(default=True, verbose_name =_("Active"))
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, verbose_name =_("Channel"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('crm:detail_question', kwargs={'pk': self.pk})

class QuestionFields(models.Model):
    TEXT = 1
    CHECKBOX = 3
    CHOICE = 4
    DROPDOWN = 5
    TYPE = (
        (TEXT, "Text & Number"),
        (CHECKBOX, "Checkbox"),
        (CHOICE, "Multiple Choice"),
        (DROPDOWN, "DropDown List"),
    )
    title = models.CharField(max_length=100, verbose_name =_("Title"))
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='question_fields')
    type = models.PositiveSmallIntegerField(choices=TYPE, blank=True, null=True, verbose_name =_("Answer Type"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.title

class QuestionFieldChild(models.Model):
    title = models.CharField(max_length=100, verbose_name =_("Title"))
    value = models.CharField(max_length=50, verbose_name =_("value"))
    questionfields = models.ForeignKey(QuestionFields, on_delete=models.PROTECT, related_name='question_fields_chiled')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

class QuestionA(models.Model):
    title = models.CharField(max_length=100, verbose_name =_("Title"))
    question_id = models.IntegerField(blank=True, null=True, verbose_name =_("Question ID"))
    active = models.BooleanField(default=True, verbose_name =_("Active"))
    actualvisit = models.ForeignKey(ActualVisit, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.title

class QuestionAFields(models.Model):
    TEXT = 1
    CHECKBOX = 3
    CHOICE = 4
    DROPDOWN = 5
    TYPE = (
        (TEXT, "Text & Number"),
        (CHECKBOX, "Checkbox"),
        (CHOICE, "Multiple Choice"),
        (DROPDOWN, "DropDown List"),
    )
    title = models.CharField(max_length=100, verbose_name =_("Title"))
    question = models.ForeignKey(QuestionA, on_delete=models.PROTECT, related_name='question_fields')
    type = models.PositiveSmallIntegerField(choices=TYPE, blank=True, null=True, verbose_name =_("Answer Type"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.title

class QuestionAnswers(models.Model):
    question_title = models.CharField(max_length=100, verbose_name =_("Question Title"))
    question_id = models.IntegerField(blank=True, null=True, verbose_name =_("Question ID"))
    questionfields_title = models.CharField(max_length=100, verbose_name =_("Title"))
    questionfields = models.ForeignKey(QuestionAFields, on_delete=models.PROTECT, related_name='question_fields_answer')
    questionfields_type = models.IntegerField(blank=True, null=True, verbose_name =_("Field Type"))
    questionfieldchilds_title = models.CharField(blank=True,null=True, max_length=100, verbose_name =_("Title"))
    questionfieldchilds_id = models.IntegerField(blank=True, null=True, verbose_name =_("Child ID"))
    answer = models.CharField(blank=True, null=True, max_length=50, verbose_name =_("Answer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

class Reconciliation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    account = models.ForeignKey(AccountingChild, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date',)
        default_permissions = ('add', 'change', 'delete', 'view')


class CreditDebit(models.Model):
    TYPE = (
        ('1', 'debit'),
        ('2', 'credit'),
    )
    category = models.ForeignKey(AccountingChild, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    type = models.CharField(max_length=1, choices=TYPE)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')


class AccTransactionDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TYPE = (
        ('1', 'Deposit'),
        ('2', 'Withdrawal'),
        ('3', 'Journal')
    )

    type = models.CharField(max_length=1, choices=TYPE)

    credit_debit = models.ManyToManyField(CreditDebit)

    notes = models.CharField(max_length=250, null=True, blank=True)
    reviewed = models.BooleanField(default=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateField()

    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

class ServerName(models.Model):
    link = models.CharField(blank=True, null=True, max_length=100, verbose_name =_("Link"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

class SampleOrder(models.Model):
    CASH = 1
    CREDIT = 2
    PAY_TERM = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit'),

    )

    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    )
    sampleorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SMO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    paid = models.BooleanField(default=False, verbose_name =_("Paid"))
    returned = models.BooleanField(default=False, verbose_name =_("Returned"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'details', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject

class SampleProduct(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),

    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Subtotal"))
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    sampleorder = models.ForeignKey(SampleOrder, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))

    class Meta:
        ordering = ['sampleorder']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class SampleReturnOrder(models.Model):
    samplereturnorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SMRO No"))
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Net Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    sampleorderid = models.IntegerField(blank=True, null=True, verbose_name =_("Sample Order Id"))

    def save(self, *args, **kwargs):
        companies = Company.objects.all().values()
        try:
            maxsoid = int(SalesReturnOrder.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        if companies[0]['sample_return_prefix'] == None:
            samplereturn_prefix = "SMRO-"
        else:
            samplereturn_prefix = companies[0]['sample_return_prefix']

        self.samplereturnorder_number = samplereturn_prefix + str(maxsoid)
        return super(SampleReturnOrder, self).save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.subject

class SampleReturnProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Subtotal"))
    sampleorder = models.ForeignKey(SalesReturnOrder, on_delete=models.PROTECT)
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class ExpenseType(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    description = models.CharField(max_length=1024, blank=True, verbose_name =_("Description"))
    parent_expense_id = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Parent Expense"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class Expense(models.Model):
    description = models.CharField(max_length=50, verbose_name =_("Description"))
    expensetype = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, verbose_name =_("Expense Type"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT, verbose_name =_("Customer"))
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Amount"))
    approved = models.BooleanField(default=False, verbose_name =_("Approved"))
    image = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name =_("Document"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-created_date']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve')

    def __str__(self):
        return self.description

class ToDoList(models.Model):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )
    task = models.CharField(max_length=100, blank=True, verbose_name =_("Task"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name =_("User"))
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.PROTECT, verbose_name =_("To User"))
    done = models.BooleanField(default=False, verbose_name =_("Done"))
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=0, verbose_name =_("Priority"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['-priority']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.task

class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    email = models.EmailField(max_length=100, blank=True, verbose_name =_("Email"))
    phone_number = models.CharField(max_length=32, blank=True, verbose_name =_("Phone Number"))
    tax = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Tax"))
    logo = ImageField(upload_to='images/', max_length=255, blank=True, null=True, verbose_name =_("Company Logo"))
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Default Curency"))
    tax_number = models.CharField(max_length=50, verbose_name =_("Tax Number"))
    sales_prefix = models.CharField(max_length=10, default='SO-', verbose_name =_("Sales Prefix"))
    sales_return_prefix = models.CharField(max_length=10, default='SRO-', verbose_name =_("Sales Return Prefix"))
    sample_prefix = models.CharField(max_length=10, default='SMO-', verbose_name =_("Sample Prefix"))
    sample_return_prefix = models.CharField(max_length=10, default='SMRO-', verbose_name =_("Sample Return Prefix"))
    purchase_prefix = models.CharField(max_length=10, default='PO-', verbose_name =_("Purchase Prefix"))
    purchase_return_prefix = models.CharField(max_length=10, default='PRO-', verbose_name =_("Purchase Return Prefix"))
    transfer_prefix = models.CharField(max_length=10, default='TO-', verbose_name =_("Transfer Prefix"))
    actualvisit_prefix = models.CharField(max_length=10, default='AV-', verbose_name =_("Visit Prefix"))

    sales_delivery_prefix = models.CharField(max_length=10, default='del-', verbose_name =_("Sales Delivery Prefix"))

    sales_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Sales Header"))
    sales_return_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Sales Return Header"))
    sample_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Sample Header"))
    sample_return_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Sample Return Header"))
    purchase_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Purchase Header"))
    purchase_return_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Purchase Return Header"))
    collection_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Collection Header"))

    sales_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Sales Footer"))
    sales_return_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Sales Return Footer"))
    sample_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Sample Footer"))
    sample_return_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Sample Return Footer"))
    purchase_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Purchase Footer"))
    purchase_return_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Purchase Return Footer"))
    collection_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Collection Footer"))

    address = models.CharField(max_length=1024, blank=True, verbose_name =_("Address"))
    sales_auto = models.BooleanField(default=False, verbose_name =_("Auto Approved"))
    sample_auto = models.BooleanField(default=False, verbose_name =_("Auto Approved"))
    allowed_users = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("users"))

    cash_account = models.ForeignKey(AccountingParent, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Cash Account"))
    bank_account = models.ForeignKey(AccountingParent, related_name='bank_account', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Bank Account"))
    customer_account = models.ForeignKey(AccountingChild, related_name='customer_account', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Customer Account"))
    creditnote_header = models.CharField(max_length=1024, blank=True, verbose_name =_("Credit Note Header"))
    creditnote_footer = models.CharField(max_length=1024, blank=True, verbose_name =_("Credit Note Footer"))

    #created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))


    class Meta:
        ordering = ['name']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.name

class CreditNote(models.Model):
    CASH = 1
    TRANSFER = 2
    ACCOUNT = 3
    PAYMENTTYPE = (
        (CASH, 'Cash'),
        (TRANSFER, 'Transfer'),
        (ACCOUNT, 'Account'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Customer"))
    amount = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Amount"))
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENTTYPE, default=0, verbose_name =_("Payment Type"))
    bank_account = models.ForeignKey(AccountingChild, on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Bank Account"))
    cashaccount = models.ForeignKey(AccountingChild, related_name='cashaccount', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Cash Account"))
    customeraccount = models.ForeignKey(AccountingChild, related_name='customeraccount', on_delete=models.PROTECT, blank=True, null=True, verbose_name =_("Customer Account"))
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name =_("Description"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.customer

class DemoAccounts(models.Model):
    username = models.CharField(max_length=50, verbose_name =_("Name"))
    email = models.EmailField(max_length=100, blank=True, verbose_name =_("Email"))
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name =_("Company Name"))
    expiry_date = models.DateField(verbose_name =_("Expiry Date"))
    active = models.BooleanField(default=True, verbose_name =_("Active"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        ordering = ['expiry_date']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.username

class Accounting(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view', 'view_chart_of_account', 'view_customer_statement', 'print', 'view_transactions', 'view_reconciliation', 'view_reports')

    def __str__(self):
        return self.pk

class ReportsOld(models.Model):
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        default_permissions = ('view', 'view_salesman_visits', 'view_salesman_coverage', 'view_sample', 'view_sales', 'view_channel_sales', 'view_area_sales',
                               'view_customer_sales', 'view_product_sales', 'view_category_target', 'view_channel_target', 'view_area_target', 'view_customer_target',
                               'view_salesman_target', 'view_product_target', 'view_storage', 'view_expense', 'view_calender')

    def __str__(self):
        return self.pk

class Logs(models.Model):
    ADD = 1
    CHANGE = 2
    DELETE = 3
    APPROVE = 4
    TRANSTYPE = (
        (ADD, 'Add'),
        (CHANGE, 'Change'),
        (DELETE, 'Delete'),
        (APPROVE, 'Approve'),
    )
    name = models.CharField(max_length=50, verbose_name =_("Name"))
    trans_type = models.PositiveSmallIntegerField(choices=TRANSTYPE, default=0, verbose_name =_("Transaction Type"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name =_("User"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view', 'print')

    def __str__(self):
        return self.pk

#---------------Model--khaldoun

class SalesDelivery(models.Model):
    PENDING = 1
    APPROVED = 2
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    )


    salesdelivery_number = models.CharField(max_length=50, blank=True, verbose_name =_("SO No"))
    salesorder = models.ForeignKey(SalesOrder, on_delete=models.PROTECT)
    subject = models.CharField(max_length=50, blank=True, verbose_name =_("Subject"))
    deliverydate = models.DateField(blank=True, null=True, verbose_name =_("Delivery Date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name =_("Customer"))
    salesman = models.ForeignKey(Salesman, on_delete=models.PROTECT, verbose_name =_("Salesman"))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name =_("Warehouse"))
    drivername = models.CharField(max_length=50, blank=True, verbose_name =_("drivername"))
    platenumber = models.CharField(max_length=50, blank=True, verbose_name =_("platenumber"))

    duedate = models.DateField(blank=True, null=True, verbose_name =_("Due Date"))
    payment_terms = models.CharField(max_length=50,blank=True, verbose_name =_("Payment Terms"))
    total = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Total"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Net Total"))
    so_tax = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Tax"))
    tax_number = models.CharField(max_length=50,blank=True, null=True, verbose_name =_("Tax Number"))
    salesorderid = models.IntegerField(blank=True, null=True, verbose_name =_("Sales Order Id"))
    payment_days = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Due Days"))
    paid = models.BooleanField(default=False, verbose_name =_("Paid"))
    returned = models.BooleanField(default=False, verbose_name =_("Returned"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))
    salesorder_number = models.CharField(max_length=50, blank=True, verbose_name =_("SO No"))



    def save(self, *args, **kwargs):
        companies = Company.objects.all().values()
        try:
            maxsoid = int(SalesDelivery.objects.latest('pk').pk) + 1
        except:
            maxsoid = 1
        if companies[0]['sales_delivery_prefix'] == None:
            salesdelivery_prefix = "DEL-"
        else:
            salesdelivery_prefix = companies[0]['sales_delivery_prefix']

        self.salesdelivery_number = salesdelivery_prefix + str(maxsoid)
        return super(SalesDelivery, self).save(*args, **kwargs)

    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view', 'approve', 'print')

    def __str__(self):
        return self.subject




class SalesDeliveryProduct(models.Model):
    PENDING = 1
    APPROVED = 2

    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),

    )

    salesorderdelivery = models.ForeignKey(SalesDelivery, on_delete=models.PROTECT)
    #salesorderproduct = models.ForeignKey(SalesOrderproduct, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name =_("Product"))
    qty = models.PositiveIntegerField(blank=False, null=True, verbose_name =_("Qty"))
    uom = models.ForeignKey(Uom, on_delete=models.PROTECT, verbose_name =_("Unit"))

    price = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Price"))
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name =_("Discount"))
    tax = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Tax"))
    subtotal = models.DecimalField(decimal_places=1, max_digits=12, blank=True, null=True, verbose_name =_("Subtotal"))
    salesorder = models.ForeignKey(SalesOrder, on_delete=models.PROTECT)
    bt_total = models.DecimalField(decimal_places=1, max_digits=12,blank=True, null=True, verbose_name =_("Net Total"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name =_("Created Date"))

    deleted = models.BooleanField(default=False, verbose_name =_("Deleted"))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name =_("Status"))



    class Meta:
        ordering = ['pk']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return self.product

class UserAdditionalProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    defaultwarehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)


class UserBusinessRoles(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT,blank=True,null=True ,verbose_name =_("User"))
    group = models.OneToOneField(Group, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Users Groups"))
    invlocation = models.ManyToManyField('inv.InventoriesLocations',blank=True, verbose_name =_("Inventory Locations"))
    colcancreate = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Create Collection"))
    colcanedit = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Edit Collection"))
    colcanview = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can View Collection"))
    colcansubmit = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Submit Collection"))
    colcanapprove = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Approve Collection"))
    colcanpost = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Post Collection"))
    colcanrejct = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Reject Collection"))
    colcancancel = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Cancel Collection"))




class UserBusinessRolesOTLine(models.Model):
    userbusinessrole = models.ForeignKey(UserBusinessRoles, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_("Users Business Rols"))
    operationstype = models.ForeignKey('inv.OperationsTypes', on_delete=models.PROTECT,blank=True, verbose_name =_("Operations Types"))
    cancreate = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Create"))
    canedit = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Edit"))
    canview = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can View"))
    cansubmit = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Submit"))
    canapprove = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Approve"))
    canpost = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Post"))
    canrejct = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Reject"))
    cancancel = models.BooleanField(default=False,  blank=True, null=False, verbose_name=_("Can Cancel"))

class UserBusinessRolesTTLine(models.Model):
    userbusinessrole = models.ForeignKey(UserBusinessRoles, blank=True, null=True, on_delete=models.PROTECT,verbose_name=_("Users Business Rols"))
    transtype = models.ForeignKey('gl.TransTypes', on_delete=models.PROTECT, blank=True, verbose_name=_("Transactions Types"))
    canview = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can View"))
    cancreate = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Create"))
    canedit = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Edit"))
    cansubmit = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Submit"))
    canapprove = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Approve"))
    canpost = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Post"))
    canrejct = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Reject"))
    cancancel = models.BooleanField(default=False, blank=True, null=False, verbose_name=_("Can Cancel"))


#-------------khaldoun

import TARGET.crm.signals


