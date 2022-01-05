import datetime
import json
from rest_framework import serializers
from django.contrib.auth.models import Permission, Group
from TARGET.crm.models import *


class ServerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerName
        fields = ["id", "link"]


# -------------------------------------------------------
class ReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconciliation
        fields = "__all__"


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


class AccountingChildReconciliationSerializer(serializers.ModelSerializer):
    credit_debit = serializers.SerializerMethodField()
    reconciliation_list = serializers.SerializerMethodField()

    class Meta:
        model = AccountingChild
        fields = "__all__"

    def get_credit_debit(self, obj):
        credit_debit = (CreditDebit.objects.filter(category=obj).values("amount", "category", "type",
                                                                               "acctransactiondetail__date"))
        return json.dumps(list(credit_debit),
                          sort_keys=True,
                          indent=1,
                          default=default)

    def get_reconciliation_list(self, obj):
        user = User.objects.get(id=obj.user.id)
        reconciliation_list = (
            Reconciliation.objects.filter(user=user, account=obj).values("amount", "date", "account",
                                                                                "date_created", "id"))

        return json.dumps(list(reconciliation_list),
                          sort_keys=True,
                          indent=1,
                          default=default)


# --------------------------------------------------------

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name"]


# -------------------------------------------------------
class CustomerAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name"]


# -------------------------------------------------------

class AccountingChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingChild
        fields = "__all__"


class CreditDebitSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = CreditDebit
        fields = "__all__"


class AccTransactionDetailSerializer(serializers.ModelSerializer):
    credit_debit = CreditDebitSerializer(many=True)

    class Meta:
        model = AccTransactionDetail
        fields = ["id", "description",
                  "date", "type",
                  "credit_debit",
                  "notes", "reviewed",
                  "user"]

    def create(self, validated_data):
        credit_debit = False
        if "credit_debit" in validated_data:
            credit_debit = validated_data.pop("credit_debit")

        instance = AccTransactionDetail.objects.create(**validated_data)

        if credit_debit:
            for c in credit_debit:
                temp = {}
                for key, value in c.items():
                    temp[key] = value
                credit_debit = CreditDebit.objects.create(**temp)
                instance.credit_debit.add(credit_debit)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        credit_debit = False
        if "credit_debit" in validated_data:
            credit_debit = validated_data.pop("credit_debit")
        print(instance.id)
        AccTransactionDetail.objects.filter(id=instance.id).update(**validated_data)
        instance_updated = AccTransactionDetail.objects.get(id=instance.id)
        CreditDebit.objects.filter(acctransactiondetail=instance.id).delete()

        if credit_debit:
            for c in credit_debit:
                temp = {}
                for key, value in c.items():
                    temp[key] = value
                credit_debit = CreditDebit.objects.create(**temp)
                instance_updated.credit_debit.add(credit_debit)
            instance_updated.save()
        return instance_updated


# ------------------------------------------------------------
class ListDepositAccountChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingChild
        fields = "__all__"


class ListDepositAccountsSerializer(serializers.ModelSerializer):
    accounting_child = ListDepositAccountChildrenSerializer(many=True)

    class Meta:
        model = AccountingParent
        fields = "__all__"

# ---------------------------------------------------------------------------------------

class LeadSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Lead
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = ToDoList
        fields = '__all__'
        depth = 1


class CountrySerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Country
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Area
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = City
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Channel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class UserLoginSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

class PermissionSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Group
        fields = '__all__'

class SalesmanSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Salesman
        fields = '__all__'

class UomSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Uom
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Category
        fields = '__all__'

class CustomerCreateSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1

class AccountSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Account
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Warehouse
        fields = '__all__'

class SalesProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = SalesProduct
        fields = '__all__'

class SalesOrderSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = SalesOrder
        fields = '__all__'

class SalesOrderProdSerializer(serializers.ModelSerializer):  # create class to serializer model
    salesorder = SalesProductSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = '__all__'

    def create(self, validated_data):
        choice_validated_data = validated_data.pop('salesorder')
        salesorders = SalesOrder.objects.create(**validated_data)
        choice_set_serializer = self.fields['salesorder']
        for each in choice_validated_data:
            each['salesorder'] = salesorders
        salesproducts = choice_set_serializer.create(choice_validated_data)
        return salesorders

class SalesReturnProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = SalesReturnProduct
        fields = '__all__'

class SalesReturnOrderSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = SalesReturnOrder
        fields = '__all__'

class SalesReturnOrderProdSerializer(serializers.ModelSerializer):  # create class to serializer model
    salesorder = SalesReturnProductSerializer(many=True)

    class Meta:
        model = SalesReturnOrder
        fields = '__all__'

    def create(self, validated_data):
        choice_validated_data = validated_data.pop('salesorder')
        salesreturnorders = SalesReturnOrder.objects.create(**validated_data)
        choice_set_serializer = self.fields['salesorder']
        for each in choice_validated_data:
            each['salesorder'] = salesreturnorders
        salesreturnproducts = choice_set_serializer.create(choice_validated_data)
        return salesreturnorders


class CollectionSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Collection
        fields = '__all__'

class TransactionsSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Transactions
        fields = '__all__'

class TargetTransactionsSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = TargetTransactions
        fields = '__all__'

class FinancialYearSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = FinancialYear
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Currency
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Company
        fields = '__all__'

class UnitsNameSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = UnitsName
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Notification
        fields = '__all__'
