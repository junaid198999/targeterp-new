from django.conf.urls import url
from django.urls import include, path, re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, base_name='users')
router.register('permissions', views.PermissionViewSet, base_name='permissions')
router.register('groups', views.GroupViewSet, base_name='groups')


router.register('countries', views.CountryViewSet, base_name='countries')
router.register('areas', views.AreaViewSet, base_name='areas')
router.register('cities', views.CityViewSet, base_name='cities')
router.register('channels', views.ChannelViewSet, base_name='channels')
router.register('salesmen', views.SalesmanViewSet, base_name='salesmen')
router.register('products', views.ProductViewSet, base_name='products')
router.register('categories', views.CategoryViewSet, base_name='categories')
router.register('customers', views.CustomerViewSet, base_name='customers')
router.register('login', views.LoginViewSet, base_name='login')

router.register('accounts', views.AccountViewSet, base_name='accounts')
router.register('warehouses', views.WarehouseViewSet, base_name='warehouses')

router.register('salesorders', views.SalesOrderViewSet, base_name='salesorders')
router.register('salesproducts', views.SalesProductViewSet, base_name='salesproducts')
router.register('salesreturnorders', views.SalesReturnOrderViewSet, base_name='salesreturnorders')
router.register('salesreturnproducts', views.SalesReturnProductViewSet, base_name='salesreturnproducts')
router.register('collections', views.CollectionViewSet, base_name='collections')

router.register('transactions', views.TransactionsViewSet, base_name='sransactions')
router.register('targettrans', views.TargetTransactionsViewSet, base_name='targettrans')

router.register('financialyears', views.FinancialYearViewSet, base_name='financialyears')
router.register('company', views.CompanyViewSet, base_name='company')
router.register('unitsname', views.UnitsNameViewSet, base_name='unitsname')
router.register('currencies', views.CurrencyViewSet, base_name='currencies')
router.register('notifications', views.NotificationViewSet, base_name='notifications')
router.register('servername', views.ServerNameViewSet, base_name='servername')

app_name ="crm"

urlpatterns = [
    # path('api/countries/', views.country_list),
    # path('api/countries/', views.CountryAPIView.as_view()),
    # path('api/g/countries/<int:id>/', views.CountryGenericAPIView.as_view()),

    # path('api/countries/<int:pk>/', views.country_details),
    # path('api/countries/<int:id>/', views.CountryDetails.as_view()),
    path('api/leads', views.LeadViewSet.as_view()),

    path('api/todos', views.TodosViewSet.as_view()),
    path('api/todosdone', views.TodosDoneViewSet.as_view()),

    path('api/salesrep/', views.SalesRepView.as_view()),
    path('api/catsalesrep/', views.CatSalesRepView.as_view()),
    path('api/areasalesrep/', views.AreaSalesRepView.as_view()),
    path('api/customersalesrep/', views.CustomerSalesRepView.as_view()),
    path('api/salesmansalesrep/', views.SalesmanSalesRepView.as_view()),
    path('api/productsalesrep/', views.ProductSalesRepView.as_view()),
    path('api/collectionsrep/', views.CollectionRepView.as_view()),

    path('api/cattargetrep/', views.CatTargetRepView.as_view()),
    path('api/chatargetrep/', views.ChaTargetRepView.as_view()),
    path('api/areatargetrep/', views.AreaTargetRepView.as_view()),
    path('api/custtargetrep/', views.CustTargetRepView.as_view()),

    path('api/salesmantargetrep/', views.SalesmanTargetRepView.as_view()),
    path('api/producttargetrep/', views.ProductTargetRepView.as_view()),
    path('api/storageanalysisrep/', views.StorageAnalysisRepRepView.as_view()),

    path('api/dashboard/', views.DashboardView.as_view()),

    path('api/', include(router.urls)),
    path('api/<int:pk>/', include(router.urls)),

    path('api/customer-list/', views.CustomerListView.as_view()),

    path('api/transections-list-create/', views.AccTransactionDetailListView.as_view()),
    path('api/transections-rud/<int:pk>', views.AccTransactionDetailURDView.as_view()),

    path('api/deposit-accounts/', views.ListDepositAccountsView.as_view()),
    path('api/split-accounts/', views.ListSplitAccountsView.as_view()),

    path('api/vendors-list/', views.VendorsListView.as_view()),

    path('api/reconciliation-accounts/', views.ListReconciliationAccountsView.as_view()),
    path('api/reconciliation-create', views.CreateReconciliationView.as_view()),
    path('api/reconciliation-rud/<int:pk>', views.UpdateReconciliationView.as_view()),

]