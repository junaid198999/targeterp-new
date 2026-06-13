from django.contrib import admin
from .models import Product, AccountingType, AccountingChild, AccountingParent, Question

admin.site.register(Product)
admin.site.register(AccountingChild)
admin.site.register(AccountingType)
admin.site.register(AccountingParent)

# Register your models here.
