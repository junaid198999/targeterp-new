# generic
import calendar
from django.db.models import Sum, Q, IntegerField, F
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from TARGET.crm.api.serializers import *
from TARGET.crm.models import *

class SalesOrderViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            salesorders = SalesOrder.objects.filter(salesman__in=salesmanid)
        else:
            salesorders = SalesOrder.objects.all()

        serializer = SalesOrderSerializer(salesorders, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = SalesOrderProdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = SalesOrder.objects.all()
        salesorders = get_object_or_404(queryset, pk=pk)
        serializer = SalesOrderSerializer(salesorders)
        return Response(serializer.data)

    def update(self, request, pk=None):
        salesorders = SalesOrder.objects.get(pk=pk)
        serializer = SalesOrderSerializer(salesorders, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        salesorders = SalesOrder.objects.get(pk=pk)
        try:
            salesorders.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class SalesProductViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        salesproducts = SalesProduct.objects.all()
        serializer = SalesProductSerializer(salesproducts, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = SalesProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = SalesProduct.objects.all()
        salesproducts = get_object_or_404(queryset, pk=pk)
        serializer = SalesProductSerializer(salesproducts)
        return Response(serializer.data)

    def update(self, request, pk=None):
        salesproducts = SalesProduct.objects.get(pk=pk)
        serializer = SalesProductSerializer(salesproducts, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        salesproducts = SalesProduct.objects.get(pk=pk)
        try:
            salesproducts.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class SalesReturnOrderViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            salesreturnorders = SalesReturnOrder.objects.filter(salesman__in=salesmanid)
        else:
            salesreturnorders = SalesReturnOrder.objects.all()

        serializer = SalesReturnOrderSerializer(salesreturnorders, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = SalesReturnOrderProdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = SalesReturnOrder.objects.all()
        salesreturnorders = get_object_or_404(queryset, pk=pk)
        serializer = SalesReturnOrderSerializer(salesreturnorders)
        return Response(serializer.data)

    def update(self, request, pk=None):
        salesreturnorders = SalesReturnOrder.objects.get(pk=pk)
        serializer = SalesReturnOrderSerializer(salesreturnorders, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        salesreturnorders = SalesReturnOrder.objects.get(pk=pk)
        try:
            salesreturnorders.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class SalesReturnProductViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        salesreturnproducts = SalesReturnProduct.objects.all()
        serializer = SalesReturnProductSerializer(salesreturnproducts, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = SalesReturnProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = SalesReturnProduct.objects.all()
        salesreturnproducts = get_object_or_404(queryset, pk=pk)
        serializer = SalesReturnProductSerializer(salesreturnproducts)
        return Response(serializer.data)

    def update(self, request, pk=None):
        salesreturnproducts = SalesReturnProduct.objects.get(pk=pk)
        serializer = SalesReturnProductSerializer(salesreturnproducts, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        salesreturnproducts = SalesReturnProduct.objects.get(pk=pk)
        try:
            salesreturnproducts.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class CollectionViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()


        collections = Collection.objects.filter(customer_id__in=customers)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Collection.objects.all()
        collections = get_object_or_404(queryset, pk=pk)
        serializer = CollectionSerializer(collections)
        return Response(serializer.data)

    def update(self, request, pk=None):
        collections = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collections, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        collections = Collection.objects.get(pk=pk)
        try:
            collections.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()
    serializer_class = CitySerializer

class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class SalesmanViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        users = User.objects.get(pk=user_id)

        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        if users.is_superuser:
            salesmans = Salesman.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmans = Salesman.objects.filter(user=user_id)
            elif salesmanid.count() > 0:
                salesmans = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

        serializer = SalesmanSerializer(salesmans, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

class UomViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Uom.objects.all()
    serializer_class = UomSerializer

class ProductViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        products = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    def update(self, request, pk=None):
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        products = Product.objects.get(pk=pk)
        try:
            products.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class CategoryViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        categories = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(categories)
        return Response(serializer.data)

    def update(self, request, pk=None):
        categories = Category.objects.get(pk=pk)
        serializer = CategorySerializer(categories, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        categories = Category.objects.get(pk=pk)
        try:
            categories.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class CustomerViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Customer.objects.all()
        customers = get_object_or_404(queryset, pk=pk)
        serializer = CustomerSerializer(customers)
        return Response(serializer.data)

    def update(self, request, pk=None):
        customers = Customer.objects.get(pk=pk)
        serializer = CustomerCreateSerializer(customers, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        customers = Customer.objects.get(pk=pk)
        try:
            customers.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class LoginViewSetold(viewsets.ViewSet):
    def list(self, request):
        pass

    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        users = User.objects.get(email=username)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            Old_Token = Token.objects.filter(user=users.pk)
            if Old_Token.count() > 0:
                Old_Token.delete()
        except:
            pass

        token = Token.objects.create(user=users)
        user_data = User.objects.all().filter(email=username)
        serializer = UserLoginSerializer(user_data, many=True)
        return Response({'token': token.key, 'user': serializer.data})

    def retrieve(self, request, pk=None):
        queryset = Customer.objects.all()
        customers = get_object_or_404(queryset, pk=pk)
        serializer = CustomerSerializer(customers)
        return Response(serializer.data)
class LoginViewSet(viewsets.ViewSet):
    def list(self, request):
        pass

    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.get(email=username)

            try:
                Old_Token = Token.objects.filter(user=users.pk).values()
            except:
                pass

            Old_Token = Token.objects.filter(user=users.pk).values()
            if Old_Token.count() == 0:
                token = Token.objects.create(user=users)
                token_key = token.key
            else:
                token = Old_Token
                token_key = Old_Token[0]['key']
            user_data = User.objects.all().filter(email=username)
            serializer = UserLoginSerializer(user_data, many=True)
        return Response({'token': token_key, 'user': serializer.data})

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        users = get_object_or_404(queryset, pk=pk)
        serializer = UserLoginSerializer(users)
        return Response(serializer.data)

class AccountViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        accounts = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(accounts)
        return Response(serializer.data)

    def update(self, request, pk=None):
        accounts = Account.objects.get(pk=pk)
        serializer = AccountSerializer(accounts, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        accounts = Account.objects.get(pk=pk)
        try:
            accounts.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class WarehouseViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Warehouse.objects.all()
        warehouses = get_object_or_404(queryset, pk=pk)
        serializer = WarehouseSerializer(warehouses)
        return Response(serializer.data)

    def update(self, request, pk=None):
        warehouses = Warehouse.objects.get(pk=pk)
        serializer = WarehouseSerializer(warehouses, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        warehouses = Warehouse.objects.get(pk=pk)
        try:
            warehouses.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

class TransactionsViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            transactions = Transactions.objects.filter(salesman__in=salesmanid)
        else:
            transactions = Transactions.objects.all()

        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

class TargetTransactionsViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            target_transactions = TargetTransactions.objects.filter(salesman__in=salesmanid)
        else:
            target_transactions = TargetTransactions.objects.all()

        serializer = TargetTransactionsSerializer(target_transactions, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

class FinancialYearViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        currencies = Currency.objects.all()

        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class UnitsNameViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        units = UnitsName.objects.all()

        serializer = UnitsNameSerializer(units, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

class LeadViewSet(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def paginate_queryset(self, queryset, view=None):
        # couldn't find a better solution
        return None

class TodosViewSet(generics.ListAPIView):
    queryset = ToDoList.objects.all().filter(done=0)
    serializer_class = TodoSerializer

    def paginate_queryset(self, queryset, view=None):
        # couldn't find a better solution
        return None

class TodosDoneViewSet(generics.ListAPIView):
    queryset = ToDoList.objects.all().filter(done=1)
    serializer_class = TodoSerializer

    def paginate_queryset(self, queryset, view=None):
        # couldn't find a better solution
        return None

class NotificationViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser:
            notifications = Notification.objects.all().order_by('read', '-created_date')
        else:
            if salesmanid.count() == 0:
                notifications = Notification.objects.filter(to_user=users.id).order_by('read', '-created_date')
            elif salesmanid.count() > 0:
                notifications = Notification.objects.filter(Q(to_user__in=salesmanid) | Q(to_user=users.id)).order_by('read', '-created_date')


        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Notification.objects.all()
        notifications = get_object_or_404(queryset, pk=pk)
        serializer = NotificationSerializer(notifications)
        return Response(serializer.data)

    def update(self, request, pk=None):
        notifications = Notification.objects.get(pk=pk)
        serializer = NotificationSerializer(notifications, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        notifications = Notification.objects.get(pk=pk)
        try:
            notifications.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)


class SalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channels_id = int(request.GET.get('channel'))
        except:
            channels_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channelar = []
        channels = Channel.objects.all()
        channel_serializer = ChannelSerializer(channels, many=True)

        if channels_id != 9898989998 :
            channel_name = channels.filter(pk=channels_id).values('name')
            channelname = channel_name[0]['name']
        else:
            channelname =''

        areas = Area.objects.all()
        area_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        city_serializer = CitySerializer(citiylist, many=True)

        parent_ch = channels.filter(parent_channel_id=channels_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channels_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channels_id).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:

            if areas_id != 9898989998 and channels_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channels_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channels_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        totalqty = queryavailablestock.aggregate(qty=Sum('ctrqty'))



        salesorders = SalesOrder.objects.all()
        queryset = SalesOrder.objects.all()
        serializer_class = SalesOrderSerializer

        m=1
        totalmonthlytargets = 0
        totalmonthlytargetsqty = 0
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        tablear = []
        temonth = int(monthn)
        customers = Customer.objects.all().filter(salesman__in=salesmanid)
        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        while m <= 12 :
            monthss = "m" + str(m)

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0

            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0

            queryyearlytarget = targettransactions.annotate(total=Sum(F(monthss) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear)
            totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
            try:
                totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
            except:
                totalmonthlytargets = 0

            querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear)
            totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
            try:
                totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
            except:
                totalmonthlytargetsqty = 0


            if city_id != 9898989998 or areas_id != 9898989998 or channels_id != 9898989998:
                querymonthlycustomers = transactions.values('customer_id')
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=m).filter(customer_id__in=querymonthlycustomers)
            else:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=m)

            collectionamount = collections.aggregate(total=Sum('amount'))
            collectamount = collectionamount['total']
            if collectamount is None:
                collectamount = 0

            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=m).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0
            if achievedqtym > 0:
                try:
                    achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
                except:
                    achievedqtylasty = 0.0
            else:
                achievedqtylasty = 0.0


            if achievedpercm > 0:
                try:
                    achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
                except:
                    achievedtotallasty = 0.0
            else:
                achievedtotallasty = 0.0

            mname = calendar.month_name[m]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                tablear.append({'month': mname, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': m,
                                'collectamount': collectamount,

                                })
            m += 1


        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'data': tablear,
            'channels': channel_serializer.data,
            'cities': city_serializer.data,
            'areas': area_serializer.data,
            'channels_id': channels_id,
            'channelname': channelname,
            'areas_id': areas_id,
            'city_id': city_id,
            'temonth': temonth,
        }
        return Response(context, content_type="text/html; charset=utf-8")

class CatSalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        area_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)
            customers = Customer.objects.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))



        salesorders = SalesOrder.objects.all()
        salesorders_serializer = SalesOrderSerializer(salesorders, many=True)


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)
        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        for channel in channels :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(channel_id = channel.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlycustomers = customers.filter(channel_id = channel.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act

            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(channel_id = channel.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(channel_id = channel.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'channel': channel.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })


        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'data': channelear,
            'categories': categories_serializer.data,
            'areas': area_serializer.data,
            'cities': cities_serializer.data,
            'categories_id': categories_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class AreaSalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()

        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        cities_serializer = CitySerializer(citiylist, many=True)

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))
            customers = Customer.objects.filter(salesman__in=salesmanid)

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))



        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        for area in areas :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(area_id = area.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(area_id = area.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlycustomers = customers.filter(area_id = area.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(area_id = area.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(area_id = area.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'area': area.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })

        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets


        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class CustomerSalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()

        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

        if users.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()
            salesmanid = Salesman.objects.all()

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)


        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))



        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        totalmonthlytargets = 0
        totalmonthlytargetsqty = 0
        mname = calendar.month_name[thismonth]
        for customer in customers :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(customer_id = customer.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(customer_id = customer.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(customer_id = customer.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1

            collections = qcollections.values('customer').order_by('customer') \
                .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(customer_id=customer.id)
            collectionamount = collections.aggregate(total=Sum('amount'))
            collectamount = collectionamount['total']
            if collectamount is None:
                collectamount = 0

            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(customer_id = customer.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(customer_id = customer.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'customer': customer.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount':collectamount,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets

        if num_customers is None or num_customers == 0:
            activecustomersper = 0
        else:
            activecustomersper = round(activecustomers / num_customers * 100)


        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class SalesmanSalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)
        if users.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        salesmans = Salesman.objects.all()
        salesmans_serializer = SalesmanSerializer(salesmans, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        for salesman in salesmans :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1

            querymonthlycustomers = customers.filter(salesman_id = salesman.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]


            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'salesman': salesman.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets
        if num_customers > 0:
            activecustomersper = round(activecustomers / num_customers * 100)
        else:
            activecustomersper = 0

        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'salesmans': salesmans_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class ProductSalesRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        if users.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id).filter(category_id=categories_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id).filter(category_id__in=parent_cat)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)
        for product in products :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(product_id = product.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(product_id = product.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(product_id = product.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(product_id = product.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]

            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'product': product.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets
        if num_customers > 0:
            activecustomersper = round(activecustomers / num_customers * 100)
        else:
            activecustomersper = 0

        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'products': products_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'categories_id':categories_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class CollectionRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998
        salesmanid = Salesman.objects.all().filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 365

        from datetime import datetime
        today = datetime.today()
        currentYear = timezone.now().year

        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        qcustomers = Customer.objects.all().filter(payment_terms=2)
        customers_serializer = CustomerSerializer(qcustomers, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
            else:
                customers = qcustomers
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                customers = qcustomers.filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                customers = qcustomers.filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                customers = qcustomers

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            customers = customers.filter(salesman__in=salesmanid)

            customers_serializer = CustomerSerializer(customers, many=True)

        salesorders = SalesOrder.objects.all().filter(payment_terms=2)
        salesreturns = SalesReturnOrder.objects.all().filter(salesorderid__in = salesorders)

        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        currentday = timezone.now()

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all()
        else:
            qcollections = Collection.objects.all().filter(customer_id__in=customers)

        now = datetime.today()
        if month_id != 9898989998 and month_id != 0 and month_id != 365:
            dayslater = timezone.now() + timezone.timedelta(days=month_id)
        elif month_id == 0:
            dayslater = str('2010') + "-01-01"
        elif month_id == 365:
            daysstart = str('2010') + "-01-01"
            dayslater = str(currentYear) + "-12-31"
        else:
            dayslater = str(currentYear) + "-12-31"
            # month_id = (datetime.strptime(dayslater, "%Y-%m-%d") - now).days
        totalsalesorderv = 0
        for customer in customers :
            if month_id != 9898989998 and month_id != 0 and month_id != 365:
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(now, dayslater))
                totalsalesorder = qsalesorder.aggregate(Sum('total'))
            elif month_id != 9898989998 and month_id == 0 :
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(dayslater, now))
                totalsalesorder = qsalesorder.aggregate(Sum('total'))
            elif month_id == 365 :
                qsalesorder = salesorders.annotate(totalso=Sum('total')).filter(customer_id = customer.id).filter(duedate__range=(daysstart, dayslater))
                totalsalesorder = qsalesorder.aggregate(Sum('total'))
            if totalsalesorder['total__sum'] is None:
                totalsalesorderv = 0
            else:
                totalsalesorderv = totalsalesorder['total__sum']

            salesorderid = qsalesorder.values('pk')
            qsalesreturn = salesreturns.annotate(totalrs=Sum('total')).filter(customer_id = customer.id)
            totalsalesreturn = qsalesreturn.aggregate(Sum('total'))

            if totalsalesreturn['total__sum'] is None:
                totalsalesreturnv = 0
            else:
                totalsalesreturnv = totalsalesreturn['total__sum']

            netsales = totalsalesorderv - totalsalesreturnv
            collections = qcollections \
                .annotate(total=Sum('amount')).filter(customer_id=customer.id).filter(~Q(description__contains='auto created from Sales')).filter(salesorder__in = salesorderid)
            collectionamount = collections.aggregate(total=Sum('amount'))
            collectamount = collectionamount['total']
            if collectamount is None:
                collectamount = 0

            balance = netsales - collectamount
            if netsales != 0:
                salesmanname = customer.salesman.name
                channelear.append({'customer': customer.name, 'salesman': salesmanname, 'totalamount': netsales,
                                'amount': collectamount,
                                'balance': balance,


                                   })

        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'month_id': month_id

        }
        return Response(context, content_type="text/html; charset=utf-8")

class CatTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

        if users.is_superuser is False:
            targettransactions = targettransactions.filter(salesman__in=salesmanid)


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        for category in categories :
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id = category.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0


            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(total=Sum(F(montht)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(category_id=category.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0



                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(created_date__year=currentYear).filter(category_id=category.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'category': category.name,'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 !=0 and t2 !=0 and t3 !=0 and t4 !=0 and t5 !=0 and t6 !=0 and t7 !=0 and t8 !=0 and t9 !=0 and t10 !=0 and t11 !=0 and t12 !=0 :
                channelear.append({'category': category.name,
                                't1': t1,'t2': t2,'t3': t3,'t4': t4,'t5': t5,'t6': t6,'t7': t7,'t8': t8,'t9': t9,'t10': t10,'t11': t11,'t12': t12,
                                'q1': q1,'q2': q2,'q3': q3,'q4': q4,'q5': q5,'q6': q6,'q7': q7,'q8': q8,'q9': q9,'q10': q10,'q11': q11,'q12': q12,
                                'monthint': thismonth,

                                })



        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class ChaTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            category_id = int(request.GET.get('category'))
        except:
            category_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Category.objects.all().filter(parent_category=category_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and category_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif category_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=category_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id=category_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=category_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id=category_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and category_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif category_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and category_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(category_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()


        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        for channel in channels :
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12')*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id = channel.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0


            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(total=Sum(F(montht)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(channel_id=channel.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0



                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(created_date__year=currentYear).filter(channel_id=channel.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'channel': channel.name,'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 !=0 and t2 !=0 and t3 !=0 and t4 !=0 and t5 !=0 and t6 !=0 and t7 !=0 and t8 !=0 and t9 !=0 and t10 !=0 and t11 !=0 and t12 !=0 :
                channelear.append({'channel': channel.name,
                                't1': t1,'t2': t2,'t3': t3,'t4': t4,'t5': t5,'t6': t6,'t7': t7,'t8': t8,'t9': t9,'t10': t10,'t11': t11,'t12': t12,
                                'q1': q1,'q2': q2,'q3': q3,'q4': q4,'q5': q5,'q6': q6,'q7': q7,'q8': q8,'q9': q9,'q10': q10,'q11': q11,'q12': q12,
                                'monthint': thismonth,

                                })



        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'category_id': category_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class AreaTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)
        qcollections = Collection.objects.all()
        for area in areas:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(area_id=area.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(area_id=area.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0

                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(area_id=area.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'area': area.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'area': area.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class CustTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        customers = Customer.objects.all()

        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        for customer in customers:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'customer': customer.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'customer': customer.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'cities': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class SalesmanTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        salesmans = Salesman.objects.all()
        salesmans_serializer = SalesmanSerializer(salesmans, many=True)

        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id=channel_id).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    channel_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    channel_id__in=parent_cat).filter(city_id=city_id)

            else:
                targettransactions = TargetTransactions.objects.all()


        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        for salesman in salesmans:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(salesman_id=salesman.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(salesman_id=salesman.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(salesman_id=salesman.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'salesman': salesman.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'salesman': salesman.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })


        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'citiylist': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class ProductTargetRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        salesmanid = Salesman.objects.filter(reporting_to=user_id).values('reporting_to')
        users = User.objects.get(pk=user_id)

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            categories_id = int(request.GET.get('category'))
        except:
            categories_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        products = Product.objects.all()

        channels = Channel.objects.all()
        channels_serializer = ChannelSerializer(channels, many=True)

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        parent_cat = Category.objects.all().filter(parent_category=categories_id)
        if parent_cat.count() == 0:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    category_id=categories_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(
                    category_id=categories_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id).filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id).filter(
                    city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id=categories_id).filter(
                    area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id=categories_id).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif categories_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                    category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id == 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id__in=parent_cat)
            elif city_id == 9898989998 and areas_id != 9898989998 and categories_id == 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id == 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id).filter(
                    category_id__in=parent_cat)
            elif city_id != 9898989998 and areas_id != 9898989998 and categories_id != 9898989998 and channel_id != 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                    category_id__in=parent_cat).filter(city_id=city_id).filter(channel_id=channel_id)
            else:
                targettransactions = TargetTransactions.objects.all()
            if areas_id != 9898989998 and categories_id == 9898989998 and city_id == 9898989998:
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)

        if users.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=users.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=users.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)


        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)
        for product in products:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(product_id=product.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(product_id=product.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(product_id=product.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'product': product.name, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'product': product.name,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })


        context = {
            'data': channelear,
            'channels': channels_serializer.data,
            'categories': categories_serializer.data,
            'areas': areas_serializer.data,
            'citiylist': cities_serializer.data,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'categories_id': categories_id,
            'city_id': city_id,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return Response(context, content_type="text/html; charset=utf-8")

class StorageAnalysisRepRepView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]

        products = Product.objects.all()

        areas = Area.objects.all()
        areas_serializer = AreaSerializer(areas, many=True)

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        cities_serializer = CitySerializer(citiylist, many=True)

        if areas_id != 9898989998 and city_id == 9898989998:
            transactions = Transactions.objects.all().filter(area_id=areas_id)
            targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            warehouses = Warehouse.objects.all().filter(area_id=areas_id)
        elif city_id != 9898989998 and areas_id == 9898989998:
            transactions = Transactions.objects.all().filter(city_id=city_id)
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            warehouses = Warehouse.objects.all().filter(city_id=city_id)
        elif city_id != 9898989998 and areas_id != 9898989998:
            transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            warehouses = Warehouse.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
        else:
            transactions = Transactions.objects.all()
            targettransactions = TargetTransactions.objects.all()
            warehouses = Warehouse.objects.all()

        catear = []

        totalactual = 0
        totaltarget = 0
        diffperc = 0
        for product in products:
            qproduct = products.annotate(total=Sum(F('ti')*F('hi'))).filter(pk=product.id)
            msafetys = qproduct.aggregate(Sum('total'))
            try:
                msafetystock = msafetys['total__sum']
            except:
                msafetystock = 0
            if msafetystock == None:
                msafetystock = 0

            qproduct = products.values('monthly_safety_stock').filter(pk=product.id)
            try:
                sstock = qproduct[0]['monthly_safety_stock']
            except:
                sstock = 0
            if sstock == None:
                sstock = 0

            qproductactual = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder'))
            qqproductactual = qproductactual.aggregate(total = Sum('ctrqty'))
            try:
                productactual = qqproductactual['total']
            except:
                productactual = 0
            if productactual == None:
                productactual = 0

            qproductpur = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(
                Q(source='PurchaseOrder') | Q(source='PurchaseReturnOrder'))
            qqproductpur = qproductpur.aggregate(total=Sum('ctrqty'))
            try:
                productpurchase = qqproductpur['total']
            except:
                productpurchase = 0
            if productpurchase == None:
                productpurchase = 0

            qtransferin = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(source='TransferIn').filter(created_date__year=currentYear)
            qqtransferin = qtransferin.aggregate(total=Sum('ctrqty'))
            try:
                transferin = qqtransferin['total']
            except:
                transferin = 0
            if transferin == None:
                transferin = 0

            qtransferout = transactions.annotate(Sum('ctrqty')).filter(product_id=product.id).filter(source='TransferOut').filter(created_date__year=currentYear)
            qqtransferout = qtransferout.aggregate(total=Sum('ctrqty'))
            try:
                qtransferout = qqtransferout['total']
            except:
                qtransferout = 0
            if qtransferout == None:
                qtransferout = 0

            netstock = productpurchase - productactual + qtransferout + transferin

            if productactual != 0 and msafetystock != 0:
                totalactual = totalactual + round(netstock /  msafetystock)


            qsproduct = products.filter(pk=product.id).values('monthly_safety_stock')
            msafetys = qsproduct[0]['monthly_safety_stock']
            if msafetys == None:
                msafetys = 0


            qproducttarget = targettransactions.annotate(total=Sum(F('m1')+F('m2')+F('m3')+F('m4')+F('m5')+F('m6')+F('m7')+F('m8')+F('m9')+F('m10')+F('m11')+F('m12'), output_field=IntegerField()))\
                .filter(product_id=product.id).filter(created_date__year=currentYear)
            qqproducttarget = qproducttarget.aggregate(Sum('total'))

            if qqproducttarget['total__sum'] != None:
                producttarget = qqproducttarget['total__sum']
                avgproducttarget = qqproducttarget['total__sum'] / 12
            else:
                producttarget = 0
                avgproducttarget = 0

            if producttarget != 0 and msafetystock != 0:
                totaltarget = totaltarget +  producttarget / 12 * msafetys / msafetystock
            else:
                totaltarget = totaltarget

            if avgproducttarget != 0:
                reservestock = avgproducttarget * sstock
            else:
                reservestock = 0
            catear.append({'product': product.name, 'diff': round(netstock)-round(reservestock), 'reservestock': round(reservestock), 'available': netstock})

        qwarehouse = warehouses.annotate(Sum('capacity')).values('capacity')
        warhouseqty = qwarehouse.aggregate(qty=Sum('capacity'))
        if warhouseqty['qty'] != None:
            warehousecap = warhouseqty['qty']
        else:
            warehousecap = 0


        if netstock > 0 and reservestock > 0:
            diffperc = round((round(warehousecap) - round(totaltarget)) / warehousecap * 100,1)


        context = {
            'data': catear,
            'areas': areas_serializer.data,
            'citiylist': cities_serializer.data,
            'areas_id': areas_id,
            'city_id': city_id,
            'TIHITotal': msafetystock,
            'recom': totaltarget,
            'ssize': warehousecap,
            'occupied': totalactual,
            'recommend': round(totaltarget,1),
            'notes': diffperc,


        }
        return Response(context, content_type="text/html; charset=utf-8")

class DashboardView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_id = int(request.GET.get('user'))
        except:
            user_id = 9898989998

        users = User.objects.get(pk=user_id)

        today = datetime.date.today()
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']

        try:
            year_id = int(self.request.GET.get('year'))
        except:
            year_id = timezone.now().year
        try:
            date_id = int(self.request.GET.get('month'))
            if date_id == 111:
                date_id = 9999999
        except:
            current_month1 = months[today.month]
            current_month = int(current_month1)
            date_id = current_month

        financialyears = FinancialYear.objects.all()
        current_month1 = months[today.month]
        if date_id != 44 and date_id != 55 and date_id != 66 and date_id != 77 and date_id != 9999999 and date_id != 88 and date_id != 99:
            current_month = date_id
        else:
            current_month = int(current_month1)

        for financialyear in financialyears:
            Quarter1 = [financialyear.m1, financialyear.m2, financialyear.m3]
            Quarter2 = [financialyear.m4, financialyear.m5, financialyear.m6]
            Quarter3 = [financialyear.m7, financialyear.m8, financialyear.m9]
            Quarter4 = [financialyear.m10, financialyear.m11, financialyear.m12]
            FirstHalf = [financialyear.m1, financialyear.m2, financialyear.m3, financialyear.m4, financialyear.m5, financialyear.m6]
            SecondHalf = [financialyear.m7, financialyear.m8, financialyear.m9, financialyear.m10, financialyear.m11, financialyear.m12]
            numberofdaysQ1 = 31+28+31
            numberofdaysQ2 = 30+31+30 + numberofdaysQ1
            numberofdaysQ3 = 31+31+30 + numberofdaysQ2
            numberofdaysQ4 = 31+30+31 + numberofdaysQ3

            numberofdaysAQ1 = 31+28+31
            numberofdaysAQ2 = 30+31+30
            numberofdaysAQ3 = 31+31+30
            numberofdaysAQ4 = 31+30+31

            numberofdaysFH = 31+28+31+30+31+30
            numberofdaysSH = 31+31+30+31+30+31
            numberofdaysFY = 31+28+31+30+31+30+31+31+30+31+30+31
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31

        currentY = timezone.now().year
        lastYear = timezone.now().year - 1
        print('jjnjj' , date_id)
        if year_id == lastYear and date_id == 9999999:
            monthn = [1,2,3,4,5,6,7,8,9,10,11,12]
            Quarter = "None"
            numberofdays = numberofdaysFY
            numberofdaysA = numberofdaysFY
        elif year_id == currentY and date_id == 9999999:
            monthn = [1,2,3,4,5,6,7,8,9,10,11,12]
            Quarter = "None"
            numberofdays = numberofdaysFY
            numberofdaysA = numberofdaysFY
        elif date_id == 44:
            Quarter = Quarter1
            cmonth1 = 'm1'
            cmonth2 = 'm2'
            cmonth3 = 'm3'
            numberofdays = numberofdaysQ1
            numberofdaysA = numberofdaysAQ1
        elif date_id == 55:
            Quarter = Quarter2
            cmonth1 = 'm4'
            cmonth2 = 'm5'
            cmonth3 = 'm6'
            numberofdays = numberofdaysQ2
            numberofdaysA = numberofdaysAQ2
        elif date_id == 66:
            Quarter = Quarter3
            cmonth1 = 'm7'
            cmonth2 = 'm8'
            cmonth3 = 'm9'
            numberofdays = numberofdaysQ3
            numberofdaysA = numberofdaysAQ3
        elif date_id == 77:
            Quarter = Quarter4
            cmonth1 = 'm10'
            cmonth2 = 'm11'
            cmonth3 = 'm12'
            numberofdays = numberofdaysQ4
            numberofdaysA = numberofdaysAQ4
        elif date_id == 88:
            Quarter = FirstHalf
            cmonth1 = 'm1'
            cmonth2 = 'm2'
            cmonth3 = 'm3'
            cmonth4 = 'm4'
            cmonth5 = 'm5'
            cmonth6 = 'm6'
            numberofdays = numberofdaysFH
            numberofdaysA = numberofdaysFH
        elif date_id == 99:
            Quarter = SecondHalf
            cmonth1 = 'm7'
            cmonth2 = 'm8'
            cmonth3 = 'm9'
            cmonth4 = 'm10'
            cmonth5 = 'm1'
            cmonth6 = 'm12'
            numberofdays = numberofdaysSH
            numberofdaysA = numberofdaysSH
        else:
            Quarter = "None"
            monthn = int(monthn)

        currentYear = year_id
        print('currentYear', year_id)
        yearsq = Transactions.objects.dates('created_date', 'year')
        yearlist = []
        if yearsq.count() > 0:
            for Years in yearsq:
                yearlist.append({'Year': Years.year })
        else:
            yearlist.append({'Year': currentY})



        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querysourcetotal = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
            querysourcetotalp = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            queryavailablestock = Transactions.objects.annotate(totalq=Sum('ctrqty')).values('ctrqty').filter(
                created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:

            querysourcetotal = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear)
            querysourcetotalp = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear)

            queryavailablestock = Transactions.objects.annotate(totalq=Sum('ctrqty')).values('ctrqty').filter(
                created_date__year=currentYear)

        qproductactual = Transactions.objects.annotate(Sum('ctrqty')).filter(
            Q(source='SalesOrder') | Q(source='SalesReturnOrder') | Q(source='TransferOut') | Q(
                source='TransferIn'))

        salesmanncount = 0

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
                salesmanncount = 0
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                salesmanncount = salesmanid.count()

            querysourcetotal = querysourcetotal.filter(salesman__in=salesmanid)


        totalqty = queryavailablestock.aggregate(Sum('ctrqty'))
        qqproductactual = qproductactual.aggregate(total=Sum('ctrqty'))
        try:
            productactual = qqproductactual['total']
        except:
            productactual = 0
        if productactual == None:
            productactual = 0

        qproductpur = Transactions.objects.annotate(Sum('ctrqty')).filter(
            Q(source='PurchaseOrder') | Q(source='PurchaseReturnOrder'))
        qqproductpur = qproductpur.aggregate(total=Sum('ctrqty'))
        try:
            productpurchase = qqproductpur['total']
        except:
            productpurchase = 0
        if productpurchase == None:
            productpurchase = 0

        netstock = productpurchase - productactual

        ctrqty = round(netstock)

        custcount = Customer.objects.all().count()
        chcount = Channel.objects.all().count()
        citycount = City.objects.all().count()


        if self.request.user.is_superuser:
            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
                targettransactions = TargetTransactions.objects.all().filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            else:
                targettransactions = TargetTransactions.objects.all().filter(created_date__year=currentYear)
        else:
            if Quarter is not "None":
                targettransactions = TargetTransactions.objects.all().filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter)).filter(salesman__in=salesmanid)
            else:
                targettransactions = TargetTransactions.objects.all().filter(created_date__year=currentYear).filter(salesman__in=salesmanid)

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalpurchase = querysourcetotal.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalpurchasereturn = querysourcetotal.filter(source='PurchaseReturnOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3))  * F('price'), output_field=IntegerField()))
            elif date_id == 88 or date_id == 99:
                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6))  * F('price'), output_field=IntegerField()))

            querymonthlysales = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))


        else:

            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalpurchase = querysourcetotalp.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month=monthn))

                querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month=monthn))


                querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalpurchasereturn = querysourcetotalp.filter(source='PurchaseReturnOrder').values('total').filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querymonthlytarget = targettransactions.annotate(
                    total=Sum(F(cmonths) * F('price'),
                              output_field=IntegerField())).filter(created_date__year=currentYear)
                querymonthlysales = Transactions.objects.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month=monthn).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total')


            else:

                querytotalpurchase = querysourcetotalp.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(
                    created_date__month__in=monthn)
                querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalpurchasereturn = querysourcetotalp.filter(source='PurchaseReturnOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                              output_field=IntegerField()))
                querymonthlysales = Transactions.objects.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(
                    created_date__year=currentYear)


        totalpurchase = querytotalpurchase.aggregate(Sum('total'))
        totalsales = querytotalsales.aggregate(Sum('total'))
        totalsalesreturn = querytotalsalesreturn.aggregate(Sum('total'))
        totalpurchasereturn = querytotalpurchasereturn.aggregate(Sum('total'))
        if totalpurchasereturn['total__sum'] is not None and totalpurchase['total__sum'] is not None:
            netpurchase = round(totalpurchase['total__sum'] + totalpurchasereturn['total__sum'])
        elif totalpurchase['total__sum'] is not None:
            netpurchase = round(totalpurchase['total__sum'])
        else:
            netpurchase = 0
        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99 or date_id == 9999999:
            if date_id != 9999999 and date_id != 88 and date_id != 99:
                print( Quarter[0])
                if len(str(Quarter[0])) == 1:
                    currentQ = "0" + str(Quarter[0])
                else:
                    currentQ = str(Quarter[0])

                startdateformat = str(currentYear) + "-" + currentQ + "-01"
                print(startdateformat)
                currday = timezone.now().date()
                startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                print(currday)
                currentday = (currday - startday).days
                print(currentday)
                print(numberofdaysA)
                daysspent = round(currentday / numberofdaysA * 100)
                if int(current_month1) not in Quarter:
                    print('yes')
                    daysspent = 100
            else:
                startdateformat = str(currentYear) + "-01-01"
                currday = timezone.now().date()
                startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                currentday = (currday - startday).days
                daysspent = round(currentday / numberofdays * 100)
                if Quarter != "None":
                    if int(current_month1) not in Quarter and (date_id == 88 or date_id == 99) and date_id != 9999999:
                        daysspent = 100
                    elif date_id == 88 or date_id == 99 and date_id != 9999999:
                        if len(str(Quarter[0])) == 1:
                            currentQ = "0" + str(Quarter[0])
                        else:
                            currentQ = str(Quarter[0])

                        startdateformat = str(currentYear) + "-" + currentQ + "-01"
                        print(startdateformat)
                        currday = timezone.now().date()
                        startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                        currentday = (currday - startday).days
                        print(currentday)
                        print(numberofdays)
                        daysspent = round(currentday / numberofdays * 100)

        elif date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
            currentday = timezone.now().day
            daysspent = 100
            print(date_id)
            print(numberofdays)
            if int(current_month1) == int(date_id):
                daysspent = round(currentday / numberofdays * 100)
                print(daysspent)

        totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
        totalmonthlytargets = totalmonthlytarget['total__sum']


        if self.request.user.is_superuser is False:
            querymonthlysales = querymonthlysales.filter(salesman__in=salesmanid)

        totalmonthlysaless = querymonthlysales.aggregate(Sum('total'))
        try:
            totalmonthlysaless = round(int(totalmonthlysaless['total__sum']), 1)
        except:
            totalmonthlysaless = 0


        # Sales vs Target - Monthly view
        allmonthsales = []

        mc = 0
        allmonthsales = []
        while mc < 12:
            salesmonths = 'm' + str(mc + 1)

            monthfinancialyear = financialyears.values(salesmonths)

            queryallmonthsales = Transactions.objects.annotate(month=ExtractMonth('created_date')).values(
                'month').order_by(
                'month').filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month=monthfinancialyear[0][salesmonths]) \
                .annotate(total=Sum('total')).values('month', 'total').filter(created_date__year=currentYear)

            if self.request.user.is_superuser is False:
                queryallmonthsales = queryallmonthsales.filter(salesman__in=salesmanid)

            queryallmonthtarget = targettransactions.annotate(
                total=Sum(F(salesmonths) * F('price'), output_field=IntegerField())).order_by('total')
            totalallmonthtarget = queryallmonthtarget.aggregate(Sum('total'))
            try:
                ee = queryallmonthsales[0]['total']
                if totalallmonthtarget['total__sum'] is not None:
                    allmonthsales.append(
                        {'month': monthfinancialyear[0][salesmonths], 'sales': int(round(queryallmonthsales[0]['total'])),
                         'target': round(totalallmonthtarget['total__sum'])})
                else:
                    allmonthsales.append(
                        {'month': monthfinancialyear[0][salesmonths], 'sales': int(round(queryallmonthsales[0]['total'])),
                         'target': 0})
            except:
                if totalallmonthtarget['total__sum'] is not None:
                    allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                          'target': int(round(totalallmonthtarget['total__sum']))})

                else:
                    allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                          'target': 0})

            mc += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescustomer = Transactions.objects.values('customer') \
            .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
            '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total')
            elif date_id == 88 or date_id == 99:
                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'), output_field=IntegerField())).order_by('-total')

        else:
            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum(F(cmonths) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(created_date__year=currentYear)
                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum(F(cmonths) * F('price'),
                                        output_field=IntegerField())).order_by('-total')
            else:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(created_date__year=currentYear)
                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                        output_field=IntegerField())).order_by('-total')


        if self.request.user.is_superuser is False:
            querytotalsaleschannel = querytotalsaleschannel.filter(salesman__in=salesmanid)
            querytotaltargetchannel = querytotaltargetchannel.filter(salesman__in=salesmanid)

        channelcount = int(querytotalsaleschannel.count())
        channelTotal = []
        channelLabel = ''
        channelLabels = []
        channelsales = []
        c = 0
        if channelcount == 0 :
            channelsales.append(
                {'channel': '',
                 'sales': 0,
                 'salest': 0,
                 'target': 0,
                 'targetFull': 0
                 }
            )

        while c < channelcount:
            channelLabel1 = Channel.objects.filter(pk=querytotalsaleschannel[c]['channel']).values('name')
            channeltargettotalq = querytotaltargetchannel.filter(channel=querytotalsaleschannel[c]['channel'])

            channeltargettotalqv = 0
            querytotalsaleschannelv = 0
            try:
                channeltargettotalqv = round(int(channeltargettotalq[0]['total']))
            except:
                channeltargettotalqv = 0

            try:
                querytotalsaleschannelv = round(int(querytotalsaleschannel[c]['total']))
            except:
                querytotalsaleschannelv = 0

            targetotal = channeltargettotalqv - querytotalsaleschannelv
            if targetotal < 0:
                targetotal = 0

            try:
                temp = querytotaltargetchannel[c]['total']
                if totalmonthlysaless != 0:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) / totalmonthlysaless * 100),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetchannel[c]['total']))
                         }
                    )
                else:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) ),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetchannel[c]['total']))
                         }
                    )
            except:
                if totalmonthlysaless != 0:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) / totalmonthlysaless * 100),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': 0
                         }
                    )
                else:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) ),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': 0
                         }
                    )

            c += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescustomer = Transactions.objects.values('customer') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total')
            elif date_id == 88 or date_id == 99:
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total')

        else:

            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total')
            else:
                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total')


        if self.request.user.is_superuser is False:
            querytotalsalesarea = querytotalsalesarea.filter(salesman__in=salesmanid)
            querytotaltargetarea = querytotaltargetarea.filter(salesman__in=salesmanid)

        arealcount = int(querytotalsalesarea.count())
        areaTotal = []
        areaLabel = ''
        areaLabels = []
        areasales = []
        c = 0
        if arealcount == 0:
            areasales.append(
                {'area': '',
                 'sales': 0,
                 'salest': 0,
                 'target': 0,
                 'targetFull': 0
                 }
            )

        while c < arealcount:
            areaLabel1 = Area.objects.filter(pk=querytotalsalesarea[c]['area']).values('name')
            areatargettotalq = querytotaltargetarea.filter(area=querytotalsalesarea[c]['area'])
            try:
                targetotal = round(int(areatargettotalq[0]['total'])) - round(
                         int(querytotalsalesarea[c]['total']))
            except:
                targetotal = 0

            if targetotal < 0:
                targetotal = 0
            try:
                temp = querytotaltargetarea[c]['total']
                if totalmonthlysaless != 0:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) / totalmonthlysaless * 100, 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetarea[c]['total']))
                         }
                    )
                else:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) , 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetarea[c]['total']))
                         }
                    )

            except:
                if totalmonthlysaless != 0:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) / totalmonthlysaless * 100, 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': 0
                         }
                    )
                else:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) , 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': 0
                         }
                    )

            c += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalessalesman = Transactions.objects.values('salesman') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            elif date_id == 88 or date_id == 99:
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:


            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
                querytotalsalessalesman = Transactions.objects.values('salesman') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)
            else:
                querytotalsalessalesman = Transactions.objects.values('salesman') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)

        if self.request.user.is_superuser is False:
            querytotalsalessalesman = querytotalsalessalesman.filter(salesman__in=salesmanid)
            querymonthlytargetsalesman = querymonthlytargetsalesman.filter(salesman__in=salesmanid)

        salesmancount = int(querytotalsalessalesman.count())
        salesmanTotal = []
        salesmanLabel = ''
        salesmanLabels = []
        salesmantargetLabels = []
        salesmantargettotal = []
        s = 0
        if salesmancount == 0 :
            salesmanTotal.append(
                {
                    'salesman': '',
                    'total': 0,
                    'target': 0
                }
            )

        while s < salesmancount:
            salesmanLabel = Salesman.objects.filter(pk=querytotalsalessalesman[s]['salesman']).values('name')
            salesmantargettotalq = querymonthlytargetsalesman.filter(salesman=querytotalsalessalesman[s]['salesman'])
            if salesmantargettotalq.count() > 0:
                salesmantargetLabel = Salesman.objects.filter(pk=salesmantargettotalq[0]['salesman']).values('name')
                targetotal = round(int(salesmantargettotalq[0]['total']), 1) - round(
                            int(querytotalsalessalesman[s]['total']), 1)
                if targetotal < 0:
                    targetotal = 0
                salesmanTotal.append(
                    {
                        'salesman': salesmanLabel[0]['name'],
                        'total': round(int(querytotalsalessalesman[s]['total']), 1),
                        'target': targetotal
                    }
                )
            else:
                salesmanTotal.append(
                    {'salesman': salesmanLabel[0]['name'], 'total': round(int(querytotalsalessalesman[s]['total']), 1),
                     'target': 0})
            s += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescategory = Transactions.objects.values('category') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            elif date_id == 88 or date_id == 99:
                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total').filter(
                                        created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:
            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
                querytotalsalescategory = Transactions.objects.values('category') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)
            else:
                querytotalsalescategory = Transactions.objects.values('category') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)

        if self.request.user.is_superuser is False:
            querytotalsalescategory = querytotalsalescategory.filter(salesman__in=salesmanid)
            querymonthlytargetcategory = querymonthlytargetcategory.filter(salesman__in=salesmanid)

        categorycount = int(querytotalsalescategory.count())
        categoryLabel = ''
        categorytargetLabels = []
        categorytargettotal = []
        categorysalesTotal = []
        categorytargettotal = []
        cat = 0
        if categorycount == 0 :
            categorysalesTotal.append(
                {'category': '',
                 'sales': 0,
                 'target': 0}
            )

        while cat < categorycount:
            categoryLabel = Category.objects.filter(pk=querytotalsalescategory[cat]['category']).values('name')
            categorytargettotalq = querymonthlytargetcategory.filter(category=querytotalsalescategory[cat]['category'])
            try:
                categorytargettotalqv = categorytargettotalq[0]['total']
            except:
                categorytargettotalqv = 0

            try:
                querytotalsalescategoryv = querytotalsalescategory[cat]['total']
            except:
                querytotalsalescategoryv = 0

            targetotal = round(int(categorytargettotalqv), 1) - round(
                         int(querytotalsalescategoryv), 1)
            if targetotal < 0:
                targetotal = 0

            if categorytargettotalq.count() > 0:
                categorytargetLabel = Category.objects.filter(pk=categorytargettotalq[0]['category']).values('name')
                categorysalesTotal.append(
                    {'category': categoryLabel[0]['name'],
                     'sales': round(int(querytotalsalescategory[cat]['total']), 1),
                     'target': targetotal})
            else:
                categorysalesTotal.append(
                    {'category': categoryLabel[0]['name'],
                     'sales': round(int(querytotalsalescategory[cat]['total']), 1), 'target': 0})
                categorytargetLabels.append('')
                categorytargettotal.append(0)
            cat += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
        elif date_id == 9999999:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month__in=monthn).filter(created_date__year=currentYear)
        else:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month=monthn).filter(created_date__year=currentYear)


        if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                or date_id == 10 or date_id == 11 or date_id == 12:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel').annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year=currentYear)
            querytotalsales = Transactions.objects.annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year=currentYear)

            querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                .annotate(totals=Sum(F(cmonths) * F('price'), output_field=IntegerField())).values('totals').filter(
                created_date__year=currentYear)
            querymonthlytarget = TargetTransactions.objects \
                .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).values('total').filter(
                created_date__year=currentYear)
        elif date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
            querytotalsales = Transactions.objects \
                .annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=Quarter).filter(created_date__year=currentYear)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                    .annotate(totals=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                         output_field=IntegerField())).values('totals').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
                querymonthlytarget = TargetTransactions.objects \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                        output_field=IntegerField())).values('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)

            elif date_id == 88 or date_id == 99:
                querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                    .annotate(totals=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                         output_field=IntegerField())).values('totals').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)
                querymonthlytarget = TargetTransactions.objects \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).values('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)


        else:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
            querytotalsales = Transactions.objects \
                .annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

            querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                .annotate(totals=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                    output_field=IntegerField())).values('totals').filter(
                created_date__year=currentYear)
            querymonthlytarget = TargetTransactions.objects \
                .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                    output_field=IntegerField())).values('total').filter(created_date__year=currentYear)

        querytotalsalesv = querytotalsales.aggregate(total=Sum('total'))

        if querytotalsalesv['total'] is None:
            totalsalesv = 0
        else:
            totalsalesv = int(querytotalsalesv['total'])

        try:
            totaltargetv = int(querymonthlytarget[0]['total'])
        except:
            totaltargetv = 0


        if totaltargetv != 0:
            acheivedv = (totalsalesv / totaltargetv) * 100
        else:
            acheivedv = 0

        chcount = int(qtotchsm1.count())
        chsm1 = 0
        chsmqs1 = []
        while chsm1 < chcount:


            qtotsm = querytotalsalessalesman.values('salesman', 'total').order_by('-total').filter(
                channel_id=qtotchsm1[chsm1]['channel'])

            ttotsm = querymonthlytargetsalesman.values('salesman', 'totals').order_by('-totals').filter(
                channel_id=qtotchsm1[chsm1]['channel'])
            if qtotsm.count() > 0:
                try:
                    chsalesv = int(qtotsm[0]['total'])
                except:
                    chsalesv = 0

                try:
                    chtargetv = int(ttotsm[0]['totals'])
                except:
                    chtargetv = 0

                try:
                    chsalesp = int((chsalesv / totalsalesv) * 100)
                except:
                    chsalesp = 0

                try:
                    acheivedv = (chsalesv / chtargetv) * 100
                except:
                    chtargetp = 0

                try:
                    chtargetp = (chtargetv / totaltargetv) * 100
                except:
                    chtargetp = 0


                chsmLabel = Channel.objects.filter(pk=qtotchsm1[chsm1]['channel']).values('name')

                chsmsalesmanLabel = Salesman.objects.filter(pk=qtotsm[0]['salesman']).values('name')

                chsmqs1.append({'channel': chsmLabel[0]['name'], 'salesman': chsmsalesmanLabel[0]['name'],
                                'total': chsalesv,
                                'salesp': round(acheivedv)})
            chsm1 += 1

        ch1 = 0
        chq1 = []
        while ch1 < chcount:
            qtot = qtotchsm1.values('customer', 'total').order_by('-total').filter(channel_id=qtotchsm1[ch1]['channel'])
            chLabel = Channel.objects.filter(pk=qtotchsm1[ch1]['channel']).values('name')
            chLabels = Customer.objects.filter(pk=qtot[0]['customer']).values('name')
            if qtot[0]['total'] is None:
                totalqq = 0
            else:
                totalqq = round(int(qtot[0]['total']), 1)
            chq1.append({'customer': chLabels[0]['name'], 'channel': chLabel[0]['name'],
                         'total': totalqq})
            ch1 += 1

        if totalmonthlysaless is None:
            totalmonthlysaless = 0
        if totalmonthlytargets is None:
            totalmonthlytargets = 0
        if chcount is None:
            chcount = 0
        targetvsactual = totalmonthlysaless - totalmonthlytargets
        if totalmonthlysaless > totalmonthlytargets:
            if totalmonthlysaless > 0:
                totalmonthlysalessperc = round(((((totalmonthlysaless - totalmonthlytargets) / totalmonthlysaless)) * 100))
            else:
                totalmonthlysalessperc = 0
            totalmonthlytargetsperc = 0
        else:
            if totalmonthlytargets != 0 or  totalmonthlysaless !=0:
                totalmonthlytargetsperc = round(((totalmonthlysaless / totalmonthlytargets) * 100))
            else:
                totalmonthlytargetsperc = 0
            totalmonthlysalessperc = 0

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all()
        else:
            customers = Customer.objects.all().filter(salesman__in=salesmanid)
            qcollections = Collection.objects.all().filter(customer_id__in=customers)

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            qqcollections = qcollections.values('customer').order_by('customer') \
                .annotate(total=Sum('amount')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
        elif date_id == 9999999:
            qqcollections = qcollections.values('customer').order_by('customer') \
                .annotate(total=Sum('amount')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
        else:
            qqcollections = qcollections.values('customer').order_by('customer') \
                .annotate(total=Sum('amount')).filter(created_date__month=monthn).filter(created_date__year=currentYear)

        collectionamount = qqcollections.aggregate(total=Sum('amount'))
        collectamount = collectionamount['total']
        if collectamount is None:
            collectamount = 0
        else:
            collectamount = round(collectionamount['total'])

        context = {
            'netpurchase': netpurchase,
            'ctrqty': ctrqty,
            'totalmonthlytargets': totalmonthlytargets,
            'totalmonthlysaless': totalmonthlysaless,
            'totalmonthlytargetsperc': totalmonthlytargetsperc,
            'totalmonthlysalessperc': totalmonthlysalessperc,
            'daysspent': daysspent,
            'salesmanTotal': salesmanTotal,
            'chsmqs1': chsmqs1,
            'chq1': chq1,
            'channelsales': channelsales,
            'categorysalesTotal': categorysalesTotal,
            'allmonthsales': allmonthsales,
            'channelsales': channelsales,
            'areasales': areasales,
            'collectamount': collectamount,
            'salesmanncount': salesmanncount,
            'date_id': date_id,
            'yearlist': yearlist,
            'thismonth': date_id,
            'CurrentYY': year_id,

        }
        return Response(context, content_type="text/html; charset=utf-8")


class ServerNameViewSet(viewsets.ModelViewSet):

    def list(self, request):
        servers = ServerName.objects.all()
        serializer = ServerNameSerializer(servers, many=True)
        return Response(serializer.data, content_type="text/html; charset=utf-8")

    def create(self, request):
        servers = ServerName.objects.all().values()
        serializer = ServerNameSerializer(data=request.data)
        if servers.count() == 0:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            valid = {"id": servers[0]['id'], "link": servers[0]['link']}
            return Response(valid, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = ServerName.objects.all()
        servers = get_object_or_404(queryset, pk=pk)
        serializer = ServerNameSerializer(servers)
        return Response(serializer.data)

    def update(self, request, pk=None):
        servers = ServerName.objects.get(pk=pk)
        serializer = ServerNameSerializer(servers, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        servers = ServerName.objects.get(pk=pk)
        try:
            servers.delete()
            delete_status =  {"success":True}
        except:
            delete_status =  {"error":"The transaction is referenced by other transaction"}
        return Response(delete_status)

# ACCOUNT TRANSECTION DETAIL APIS

class AccTransactionDetailListView(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        return AccTransactionDetail.objects.filter(user=self.request.query_params.get('user')).order_by("-id")

    serializer_class = AccTransactionDetailSerializer


class AccTransactionDetailURDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccTransactionDetailSerializer
    queryset = AccTransactionDetail.objects.all()


class ListDepositAccountsView(generics.ListAPIView):
    pagination_class = None

    def get_queryset(self):
        print(self.request.query_params.get('user'))
        return AccountingParent.objects.filter((Q(accountingtype__name='Assets') |
                                                       Q(accountingtype__name='Liabilities') |
                                                       Q(accountingtype__name='Equity')),
                                                      accounting_child__isnull=False,
                                                      accounting_child__user__id=self.request.query_params.get('user')).distinct()

    serializer_class = ListDepositAccountsSerializer


class ListSplitAccountsView(generics.ListAPIView):
    pagination_class = None

    def get_queryset(self):
        print(self.request.query_params.get('user'))
        return AccountingParent.objects.filter((Q(accountingtype__name='Assets') |
                                                       Q(accountingtype__name='Liabilities') |
                                                       Q(accountingtype__name='Equity') |
                                                       Q(accountingtype__name='Expenses')),
                                                      accounting_child__isnull=False,
                                                      accounting_child__user__id=self.request.query_params.get('user')).distinct()

    serializer_class = ListDepositAccountsSerializer


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    pagination_class = None

    def get_queryset(self):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.query_params.get('user')).values(
            'reporting_to')
        if self.request.user.is_superuser:
            return Customer.objects.all()
        else:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.query_params.get('user'))
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(
                    Q(reporting_to__in=salesmanid) | Q(user=self.request.query_params.get('user')))

            return Customer.objects.filter(salesman__in=salesmanid).filter(status=1)

    serializer_class = CustomerAccountsSerializer


class VendorsListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = None


class ListReconciliationAccountsView(generics.ListAPIView):
    pagination_class = None

    def get_queryset(self):
        print(self.request.query_params.get('user'))
        return AccountingChild.objects.filter(user__id=self.request.query_params.get('user'))

    serializer_class = AccountingChildReconciliationSerializer

class CreateReconciliationView(generics.CreateAPIView):
    serializer_class = ReconciliationSerializer
    queryset = Reconciliation.objects.all()

class UpdateReconciliationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReconciliationSerializer
    queryset = Reconciliation.objects.all()
