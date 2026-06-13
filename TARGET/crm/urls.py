from django.urls import path, include

from . import views
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static



app_name = "crm"
urlpatterns = [
    path('', include('TARGET.crm.api.urls')),
    path("pages/", views.Error500View, name="error500"),

    path('backups/', include('dbbackup_ui.urls'), name="backups"),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^tinymce/', include('tinymce.urls')),
    path("languages/", views.languages, name="languages"),

    path("ajax/set_currency/", views.Set_Currency, name="ajax_change_currency"),

    path("setting/financialyears/", views.FinancialYearListView.as_view(), name="financialyears"),
    path("setting/financialyears/update/<int:pk>", views.FinancialYearUpdateView.as_view(), name="edit_financialyears"),

    path("setting/productunits/", views.ProductUnitsListView.as_view(), name="productunits"),
    path("setting/productunits/update/<int:pk>", views.ProductUnitsUpdateView.as_view(), name="edit_productunits"),

    path('select2/', include('django_select2.urls')),

    path("accounts/", views.AccountListView.as_view(), name="accounts"),
    path("accounts/create/", views.AccountCreateView.as_view(), name="create_account"),
    path("accounts/<int:pk>/delete/", views.AccountDeleteView.as_view(), name="delete_account"),
    path("accounts/update/<int:pk>", views.AccountUpdateView.as_view(), name="edit_account"),

    path("calendar/", views.CalendarListView.as_view(), name="calendar"),
    path("calendar_visit/", views.CalendarVisitListView.as_view(), name="calendar_visit"),
    path("calendar_visit/create/", views.CalendarVisitCreateView.as_view(), name="create_visit"),
    path("calendar_visit/delete/", views.CalendarVisitDeleteView.as_view(), name="delete_visit"),
    path("calendar_print/", views.CalendarVisitPrintView.as_view(), name="print_visit"),

    path("actual_visits/", views.ActualVisitListView.as_view(), name="actualvisits"),
    path("actual_visits/create/", views.ActualVisitCreateView.as_view(), name="create_actualvisit"),
    path("actual_visits/update/<int:pk>", views.ActualVisitUpdateView.as_view(), name="edit_actualvisit"),
    path("actual_visits/<int:pk>/delete/", views.ActualVisitDeleteView.as_view(), name="delete_actualvisit"),

    path("documents/", views.DocumentListView.as_view(), name="documents"),
    path("documents/create/", views.DocumentCreateView.as_view(), name="create_document"),
    path("documents/update/<int:pk>", views.DocumentUpdateView.as_view(), name="edit_document"),
    path("documents/<int:pk>/delete/", views.DocumentDeleteView.as_view(), name="delete_document"),

    path("questionanswers/", views.QuestionAnswersListView.as_view(), name="questionanswers"),
    path("questionanswers/update/<int:pk>", views.QuestionAnswersUpdateView.as_view(), name="edit_questionanswer"),
    path("questionanswers/<int:pk>/delete/", views.QuestionAnswersDeleteView.as_view(), name="delete_questionanswer"),

    path("questions/", views.QuestionsListView.as_view(), name="questions"),
    path("questions/<int:pk>/", views.QuestionsDetailView.as_view(), name="detail_question"),
    path("questions/create/", views.QuestionsCreateView.as_view(), name="create_question"),
    path("questions/update/<int:pk>", views.QuestionsUpdateView.as_view(), name="edit_question"),
    path("questions/<int:pk>/delete/", views.QuestionsDeleteView.as_view(), name="delete_question"),

    path("questionfields/update/<int:pk>", views.QuestionFieldsUpdateView.as_view(), name="edit_questionfields"),

    path("company/", views.CompanyListView.as_view(), name="company"),
    path("company/update/<int:pk>", views.CompanyUpdateView.as_view(), name="edit_company"),

    path("customers/", views.CustomerListView.as_view(), name="customers"),
    path("customers/create/", views.CustomerCreateView.as_view(), name="create_customer"),
    path("customers/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name="delete_customer"),
    path("customers/update/<int:pk>", views.CustomerUpdateView.as_view(), name="edit_customer"),
    path("customers/read/<int:pk>", views.CustomerDetailView.as_view(), name="read_customer"),

    path("product_customer/", views.products_list, name="product_customer"),
    path("ajax/create-customer-order/", views.create_customer_order, name="ajax_create_customer_order"),
    path("salecustomersorder/update/<int:pk>", views.SalesCustomerOrderUpdateView.as_view(), name="edit_salescustomerorder"),
    path("salecustomersorder/view/<int:pk>", views.SalesCustomerOrderViewView.as_view(), name="view_salescustomerorder"),
    path("salecustomersorder/invoice/<int:pk>", views.SalesCustomerOrderInvoiceView.as_view(), name="salescustomerorder_invoice"),
    path("salescustomerorder/", views.SalesCustomerOrderListView.as_view(), name="salescustomerorder"),

    path("doctors/", views.DoctorListView.as_view(), name="doctors"),
    path("doctors/create/", views.DoctorCreateView.as_view(), name="create_doctor"),
    path("doctors/<int:pk>/delete/", views.DoctorDeleteView.as_view(), name="delete_doctor"),
    path("doctors/update/<int:pk>", views.DoctorUpdateView.as_view(), name="edit_doctor"),
    path("doctors/approve/<int:pk>", views.DoctorApproveView.as_view(), name="approve_doctor"),

    path("ajax/save-visits/", views.save_visits, name="ajax_save_visits"),
    path("ajax/check-visits-count/", views.check_visits_count, name="ajax_check_visits_count"),
    path("ajax/save-visits-true/", views.save_visits_true, name="ajax_save_visits_true"),
    path("ajax/delete-visits/", views.delete_visits, name="ajax_delete_visits"),
    path("ajax/save-dates/", views.save_dates, name="ajax_save_dates"),

    path("ajax/retrieve-visits/", views.retrieve_visits, name="retrieve_visits"),

    path("classes/", views.ClassListView.as_view(), name="classes"),
    path("classes/create/", views.ClassCreateView.as_view(), name="create_class"),
    path("classes/<int:pk>/delete/", views.ClassDeleteView.as_view(), name="delete_class"),
    path("classes/update/<int:pk>", views.ClassUpdateView.as_view(), name="edit_class"),

    path("doctor_specialties/", views.SpecialtyListView.as_view(), name="specialties"),
    path("doctor_specialties/create/", views.SpecialtyCreateView.as_view(), name="create_specialty"),
    path("doctor_specialties/<int:pk>/delete/", views.SpecialtyDeleteView.as_view(), name="delete_specialty"),
    path("doctor_specialties/update/<int:pk>", views.SpecialtyUpdateView.as_view(), name="edit_specialty"),

    path("pharmacies/", views.PharmacyListView.as_view(), name="pharmacies"),
    path("pharmacies/create/", views.PharmacyCreateView.as_view(), name="create_pharmacy"),
    path("pharmacies/<int:pk>/delete/", views.PharmacyDeleteView.as_view(), name="delete_pharmacy"),
    path("pharmacies/update/<int:pk>", views.PharmacyUpdateView.as_view(), name="edit_pharmacy"),
    path("pharmacies/approve/<int:pk>", views.PharmacyApproveView.as_view(), name="approve_pharmacy"),

    path("pharmacy_categories/", views.PharmacyCategoryListView.as_view(), name="pharmacycategories"),
    path("pharmacy_categories/create/", views.PharmacyCategoryCreateView.as_view(), name="create_pharmacycategory"),
    path("pharmacy_categories/<int:pk>/delete/", views.PharmacyCategoryDeleteView.as_view(), name="delete_pharmacycategory"),
    path("pharmacy_categories/update/<int:pk>", views.PharmacyCategoryUpdateView.as_view(), name="edit_pharmacycategory"),

    path("vendors/", views.VendorListView.as_view(), name="vendors"),
    path("vendors/create/", views.VendorCreateView.as_view(), name="create_vendor"),
    path("vendors/<int:pk>/delete/", views.VendorDeleteView.as_view(), name="delete_vendor"),
    path("vendors/update/<int:pk>", views.VendorUpdateView.as_view(), name="edit_vendor"),

    path("notifications/", views.NotificationListView.as_view(), name="notifications"),
    path("notifications/create/", views.NotificationCreateView.as_view(), name="create_notification"),
    path("notifications/update/<int:pk>", views.NotificationUpdateView.as_view(), name="edit_notification"),
    path("notifications/reply/<int:pk>", views.NotificationReplyView.as_view(), name="reply_notification"),
    path("notifications/send_whatsapp/<int:pk>", views.NotificationWhatsAppView.as_view(), name="send_whatsapp"),
    path("notifications/<int:pk>/delete/", views.NotificationDeleteView.as_view(), name="delete_notification"),
    path("notifications/read/", views.note_read, name="note_read"),
    path("notifications/read/", views.note_read_top, name="note_read_top"),
    path("notifications/clearall/", views.note_clear_all, name="note_clear_all"),
    path('notifications/delete/',views.deletenotifications, name="delete_notifications"),

    path("todolist/add/", views.todo_add, name="todo_add"),
    path("todolist/save/", views.todo_save, name="todo_save"),
    path("todolist/done/", views.todo_done, name="todo_done"),
    path("todolist/edit/", views.todo_edit, name="todo_edit"),
    path("todolist/filter/", views.todo_filter, name="todo_filter"),

    path("notifications/status/", views.note_status, name="note_status"),
    path("notifications/tour/", views.tour_status, name="tour_status"),
    path("notifications/dark/", views.dark_status, name="dark_status"),
    path("notifications/color/", views.theme_color, name="theme_color"),

    path("branches/", views.BranchListView.as_view(), name="branches"),
    path("branches/create/", views.BranchCreateView.as_view(), name="create_branch"),
    path("branches/<int:pk>/delete/", views.BranchDeleteView.as_view(), name="delete_branch"),
    path("branches/update/<int:pk>", views.BranchUpdateView.as_view(), name="edit_branch"),

    path("setting/uoms/", views.UomListView.as_view(), name="uoms"),
    path("setting/uoms/create/", views.UomCreateView.as_view(), name="create_uom"),
    path("setting/uoms/<int:pk>/delete/", views.UomDeleteView.as_view(), name="delete_uom"),
    path("setting/uoms/update/<int:pk>", views.UomUpdateView.as_view(), name="edit_uom"),

    path("setting/countries/", views.CountryListView.as_view(), name="countries"),
    path("setting/countries/create/", views.CountryCreateView.as_view(), name="create_country"),
    path("setting/countries/<int:pk>/delete/", views.CountryDeleteView.as_view(), name="delete_country"),
    path("setting/countries/update/<int:pk>", views.CountryUpdateView.as_view(), name="edit_country"),

    path("setting/warehouses/", views.WarehouseListView.as_view(), name="warehouses"),
    path("setting/warehouses/create/", views.WarehouseCreateView.as_view(), name="create_warehouse"),
    path("setting/warehouses/<int:pk>/delete/", views.WarehouseDeleteView.as_view(), name="delete_warehouse"),
    path("setting/warehouses/update/<int:pk>", views.WarehouseUpdateView.as_view(), name="edit_warehouse"),

    path("setting/warehousetypes/", views.WarehouseTypeListView.as_view(), name="warehousetypes"),
    path("setting/warehousetypes/create/", views.WarehouseTypeCreateView.as_view(), name="create_warehousetype"),
    path("setting/warehousetypes/<int:pk>/delete/", views.WarehouseTypeDeleteView.as_view(), name="delete_warehousetype"),
    path("setting/warehousetypes/update/<int:pk>", views.WarehouseTypeUpdateView.as_view(), name="edit_warehousetype"),

    path("setting/areas/", views.AreaListView.as_view(), name="areas"),
    path("setting/areas/create/", views.AreaCreateView.as_view(), name="create_area"),
    path("setting/areas/<int:pk>/delete/", views.AreaDeleteView.as_view(), name="delete_area"),
    path("setting/areas/update/<int:pk>", views.AreaUpdateView.as_view(), name="edit_area"),

    path("setting/cities/", views.CityListView.as_view(), name="cities"),
    path("setting/cities/create/", views.CityCreateView.as_view(), name="create_city"),
    path("setting/cities/<int:pk>/delete/", views.CityDeleteView.as_view(), name="delete_city"),
    path("setting/cities/update/<int:pk>", views.CityUpdateView.as_view(), name="edit_city"),

    path("users/", views.UserListView.as_view(), name="users"),
    path("users/create/", views.UserCreateView.as_view(), name="create_user"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete_user"),
    path("users/update/<int:pk>", views.UserUpdateView.as_view(), name="edit_user"),
    path('users/delete/',views.deleteusers, name="delete_users"),

    path("groups/", views.GroupListView.as_view(), name="groups"),
    path("groups/create/", views.GroupCreateView.as_view(), name="create_group"),
    path("groups/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="delete_group"),
    path("groups/update/<int:pk>", views.GroupUpdateView.as_view(), name="edit_group"),
    path('groups/delete/',views.deletegroups, name="delete_groups"),
    
    path("group_permission/update/<int:pk>", views.GroupPermissionUpdateView.as_view(), name="edit_group_permission"),

    path("users_permission/update/<int:pk>", views.UserPermissionUpdateView.as_view(), name="edit_user_permission"),
    

    path("channels/", views.ChannelListView.as_view(), name="channels"),
    path("channels/create/", views.ChannelCreateView.as_view(), name="create_channel"),
    path("channels/<int:pk>/delete/", views.ChannelDeleteView.as_view(), name="delete_channel"),
    path("channels/update/<int:pk>", views.ChannelUpdateView.as_view(), name="edit_channel"),

    path("expensetypes/", views.ExpenseTypeListView.as_view(), name="expensetypes"),
    path("expensetypes/create/", views.ExpenseTypeCreateView.as_view(), name="create_expensetype"),
    path("expensetypes/<int:pk>/delete/", views.ExpenseTypeDeleteView.as_view(), name="delete_expensetype"),
    path("expensetypes/update/<int:pk>", views.ExpenseTypeUpdateView.as_view(), name="edit_expensetype"),

    path("expenses/", views.ExpenseListView.as_view(), name="expenses"),
    path("expenses/create/", views.ExpenseCreateView.as_view(), name="create_expense"),
    path("expenses/<int:pk>/delete/", views.ExpenseDeleteView.as_view(), name="delete_expense"),
    path("expenses/approve/<int:pk>", views.ExpenseApproveView.as_view(), name="approve_expense"),
    path("expenses/update/<int:pk>", views.ExpenseUpdateView.as_view(), name="edit_expense"),

    #salesman
    path("salesmans/", views.SalesmanListView.as_view(), name="salesmans"),
    path("salesmans/create/", views.SalesmanCreateView.as_view(), name="create_salesman"),
    path("salesmans/<int:pk>/delete/", views.SalesmanDeleteView.as_view(), name="delete_salesman"),
    path("salesmans/update/<int:pk>", views.SalesmanUpdateView.as_view(), name="edit_salesman"),
    path('salesmans/delete/',views.deletesalesmans, name="delete_salesmans"),

    #salesmangroup
    path("salesmangroups/", views.SalesmanGroupsListView.as_view(), name="salesmangroups"),
    path("salesmangroups/create/", views.SalesmanGroupsCreateView.as_view(), name="create_salesmangroup"),
    path("salesmangroups/<int:pk>/delete/", views.SalesmanGroupsDeleteView.as_view(), name="delete_salesmangroup"),
    path("salesmangroups/update/<int:pk>", views.SalesmanGroupsUpdateView.as_view(), name="edit_salesmangroup"),
    path('salesmangroups/delete/',views.deletesalesmangroups, name="delete_salesmangroups"),


    path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),
    path("ajax/load-Country-cities/", views.load_country_cities, name="ajax_load_country_cities"),
    path("ajax/load-areas/", views.load_areas, name="ajax_load_areas"),

    path("ajax/load-cust-visit-feedback/", views.load_cust_visit_feedback, name="ajax_load_cust_visit_feedback"),
    path("ajax/load-doct-visit-feedback/", views.load_doct_visit_feedback, name="ajax_load_doct_visit_feedback"),

    path("ajax/load-accounts/", views.load_accounts, name="ajax_load_accounts"),
    path("ajax/load-customers/", views.load_payment_terms, name="ajax_load_customers"),
    path("ajax/load-salesorders/", views.load_salesorders, name="ajax_load_salesorders"),
    path("ajax/load-salesorders-salesman/", views.load_salesorders_salesman, name="ajax_load_salesorders_salesman"),
    path("ajax/load-salesorders-warehouse/", views.load_salesorders_warehouse, name="ajax_load_salesorders_warehouse"),
    path("ajax/load-salesorders-product/", views.load_salesorders_product, name="ajax_load_salesorders_product"),
    path("ajax/load-salesorders-product-count/", views.load_salesorders_product_count, name="ajax_load_salesorders_product_count"),

    path("ajax/load-days/", views.load_payment_days, name="ajax_load_days"),
    path("ajax/load-total/", views.load_salesorder_total, name="ajax_load_total"),
    path("ajax/load-sr-total/", views.load_salesreturnorder_total, name="ajax_load_sr_total"),
    path("ajax/load-collection-total/", views.load_collection_total, name="ajax_load_collection_total"),
    path("ajax/load-net-total/", views.load_salesorder_net_total, name="ajax_load_net_total"),
    path("ajax/load-unitprice/", views.load_unitprice, name="ajax_load_unitprice"),
    path("ajax/load-unitprice-float/", views.load_unitprice_float, name="ajax_load_unitprice_float"),
    path("ajax/load-duedate/", views.load_duedate, name="ajax_load_duedate"),

    path("ajax/check-lead/", views.check_lead, name="ajax_check_lead"),
    path("ajax/get-questionanswer-id/", views.get_questionanswer_id, name="ajax_get_questionanswer_id"),

    path("ajax/check-sales-status/", views.check_sales_status, name="check_sales_status"),

    path("ajax/ajax-select-customer/", views.ajax_select_customer, name="ajax_select_customer"),

    path("ajax/load-saleman/", views.load_saleman, name="ajax_load_saleman"),
    path("ajax/load-salesorder/", views.load_salesorder, name="ajax_load_salesorder"),
    path("ajax/load-uom/", views.load_uom, name="ajax_load_uom"),
    path("ajax/save-calender/", views.save_calendar, name="ajax_save_calendar"),
    path("ajax/save-calender-visit/", views.save_calendar_visit, name="ajax_save_calendar_visit"),
    path("ajax/create-event/", views.create_event, name="ajax_create_event"),
    path("ajax/update-event/", views.update_event, name="ajax_update_event"),

    path("price/<int:pk>", views.fetch_price, name="fetch_price"),

    path("accounts/logout/", views.logout_view.as_view(), name="logout"),
    # path("accounts/lock/", views.changepassword_view, name="lock"),
    path("accounts/login/", views.login_view.as_view(), name="login"),

    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="create_category"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="delete_category"),
    path("categories/update/<int:pk>", views.CategoryUpdateView.as_view(), name="edit_category"),

    path("brands/", views.BrandListView.as_view(), name="brands"),
    path("brands/create/", views.BrandCreateView.as_view(), name="create_brand"),
    path("brands/<int:pk>/delete/", views.BrandDeleteView.as_view(), name="delete_brand"),
    path("brands/update/<int:pk>", views.BrandUpdateView.as_view(), name="edit_brand"),

    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/create/", views.ProductCreateView.as_view(), name="create_product"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("products/update/<int:pk>", views.ProductUpdateView.as_view(), name="edit_product"),

    path("purchaseorder/", views.PuchaseOrderListView.as_view(), name="purchaseorder"),
    path("purchaseorder/create/", views.PurchaseProductCreate.as_view(), name="create_purchaseorder"),
    path("purchaseorder/view/<int:pk>", views.PurchaseOrderUpdateView.as_view(), name="edit_purchaseorder"),
    path("purchaseorder/invoice/<int:pk>", views.PuchaseOrderInvoiceView.as_view(), name="purchaseorder_invoice"),

    path("purchasereturnorder/", views.PuchaseReturnOrderListView.as_view(), name="purchasereturnorder"),
    path("purchasereturnorder/create/", views.PurchaseReturnProductCreate.as_view(), name="create_purchasereturnorder"),
    path("purchasereturnorder/view/<int:pk>", views.PurchaseReturnOrderUpdateView.as_view(), name="edit_purchasereturnorder"),
    path("purchasereturnorder/invoice/<int:pk>", views.PuchaseReturnOrderInvoiceView.as_view(), name="purchasereturnorder_invoice"),

    path("contract/", views.ContractListView.as_view(), name="contract"),
    path("contract/create/", views.ContractProductCreate.as_view(), name="create_contract"),
    path("contract/view/<int:pk>", views.ContractUpdateView.as_view(), name="edit_contract"),
    path("contract/update/<int:pk>", views.ContractChangeView.as_view(), name="change_contract"),
    path("contract/invoice/<int:pk>", views.ContractInvoiceView.as_view(), name="contract_invoice"),
    path("contract/<int:pk>/approve/", views.ApproveContractView.as_view(), name="approve_contract"),

    path("salesorder/", views.SalesOrderListView.as_view(), name="salesorder"),
    path("salesorder/create/", views.SalesProductCreate.as_view(), name="create_salesorder"),
    path("salesorder/view/<int:pk>", views.SalesOrderUpdateView.as_view(), name="edit_salesorder"),
    path("salesorder/update/<int:pk>", views.SalesOrderChangeView.as_view(), name="change_salesorder"),
    path("salesreturn/update/<int:pk>", views.SalesReturnUpdateView.as_view(), name="edit_salesreturn"),
    path("salesorder/invoice/<int:pk>", views.SalesOrderInvoiceView.as_view(), name="salesorder_invoice"),
    path("salesorder/<int:pk>/approve/", views.ApproveSalesOrderView.as_view(), name="approve_sales"),

    path("sampleorder/", views.SampleOrderListView.as_view(), name="sampleorder"),
    path("sampleorder/create/", views.SampleProductCreate.as_view(), name="create_sampleorder"),
    path("sampleorder/view/<int:pk>", views.SampleOrderUpdateView.as_view(), name="edit_sampleorder"),
    path("sampleorder/update/<int:pk>", views.SampleOrderChangeView.as_view(), name="change_sampleorder"),
    path("samplereturnorder/update/<int:pk>", views.SampleReturnUpdateView.as_view(), name="edit_samplereturn"),
    path("sampleorder/invoice/<int:pk>", views.SampleOrderInvoiceView.as_view(), name="sampleorder_invoice"),
    path("sampleorder/<int:pk>/approve/", views.ApproveSampleOrderView.as_view(), name="approve_sample"),
    path("acctransactions/", views.AccTransactionsListView, name="acctransactions"),

    path("acctransactions/create/", views.AccTransactionsCreate.as_view(), name="create_acctransactions"),
    path("acctransactions/update/<int:pk>", views.AccTransactionsChangeView.as_view(), name="change_acctransactions"),
    path("acctransactions/invoice/<int:pk>", views.AccTransactionsInvoiceView.as_view(), name="acctransactions_invoice"),

    path("reconciliation/", views.AccReconciliationListView, name="reconciliation"),

    path("salesreturnorder/", views.SalesReturnOrderListView.as_view(), name="salesreturnorder"),
    path("salesreturnorder/create/", views.SalesReturnProductCreate.as_view(), name="create_salesreturnorder"),
    path("salesreturnorder/view/<int:pk>", views.SalesReturnOrderUpdateView.as_view(),name="edit_salesreturnorder"),
    path("salesreturnorder/invoice/<int:pk>", views.SalesReturnOrderInvoiceView.as_view(), name="salesreturnorder_invoice"),

    path("chartofaccounts/", views.ChartOfAccountsListView, name="chartofaccounts"),
    path("chartofaccounts/update/<int:pk>", views.ChartOfAccountsEditView.as_view(), name="edit_chartofaccounts"),
    path("chartofaccounts/create/", views.ChartOfAccountsCreateView.as_view(), name="create_chartofaccounts"),
    path("chartofaccounts/createall/", views.ChartOfAccountsCreateAllView.as_view(), name="create_all_chartofaccounts"),
    path("chartofaccounts/upload/", views.ChartOfAccounts_upload, name="chartofaccounts_upload"),

    path("transferorder/", views.TransferOrderListView.as_view(), name="transferorder"),
    path("transferorder/create/", views.TransferProductCreate.as_view(), name="create_transferorder"),
    path("transferorder/update/<int:pk>", views.TransferOrderUpdateView.as_view(), name="edit_transferorder"),

    path("targetbuildingblocks/", views.TargetBildingBlocksListView.as_view(), name="targetbuildingblocks"),
    path("targetbuildingblocks/create/", views.TargetBuildingBlocksCreateView.as_view(), name="create_targetbuildingblocks"),
    path("targetbuildingblocks/update/<int:pk>", views.TargetBuildingBlocksUpdateView.as_view(), name="edit_targetbuildingblocks"),
    path("targetbuildingblocks/rebuild/", views.TargetBuildingBlocksRebuildView.as_view(), name="rebuild_targetbuildingblocks"),

    path("targetbuildingblocksaccounts/", views.TargetBuildingBlocksAccountsListView.as_view(), name="targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/create/", views.TargetBuildingBlocksAccountsCreateView.as_view(),
         name="create_targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/update/<int:pk>", views.TargetBuildingBlocksAccountsUpdateView.as_view(),
         name="edit_targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/rebuild/", views.TargetBuildingBlocksAccountsRebuildView.as_view(),
         name="rebuild_targetbuildingblocksaccounts"),

    path("targetbuildingblockschannels/", views.TargetBuildingBlocksChannelsListView.as_view(),
         name="targetbuildingblockschannels"),
    path("targetbuildingblockschannels/create/", views.TargetBuildingBlocksChannelsCreateView.as_view(),
         name="create_targetbuildingblockschannels"),
    path("targetbuildingblockschannels/update/<int:pk>", views.TargetBuildingBlocksChannelsUpdateView.as_view(),
         name="edit_targetbuildingblockschannels"),
    path("targetbuildingblockschannels/rebuild/", views.TargetBuildingBlocksChannelsRebuildView.as_view(),
         name="rebuild_targetbuildingblockschannels"),

    path("targetcategorychannels/", views.TargetCategoryChannelsListView.as_view(),
         name="targetcategorychannels"),
    path("targetcategorychannels/create/", views.TargetCategoryChannelsCreateView.as_view(),
         name="create_targetcategorychannels"),
    path("targetcategorychannels/update/<int:pk>", views.TargetCategoryChannelsUpdateView.as_view(),
         name="edit_targetcategorychannels"),
    path("targetcategorychannels/rebuild/", views.TargetCategoryChannelsRebuildView.as_view(),
         name="rebuild_targetcategorychannels"),
    path('targetcategorychannels/delete/',views.deletetargetcategorychannels, name="delete_targetcategorychannels"),
    # Reports
    path("ajax/load-cities-r/", views.load_cities_r, name="ajax_load_cities_r"),
    path("salesrep/", views.SalesRepView.as_view(), name="salesrep"),
    path("catsalesrep/", views.CatSalesRepView.as_view(), name="catsalesrep"),
    path("areasalesrep/", views.AreaSalesRepView.as_view(), name="areasalesrep"),
    path("customersalesrep/", views.CustomerSalesRepView.as_view(), name="customersalesrep"),
    path("salesmansalesrep/", views.SalesmanSalesRepView.as_view(), name="salesmansalesrep"),
    path("productsalesrep/", views.ProductSalesRepView.as_view(), name="productsalesrep"),
    path("collectionsrep/", views.CollectionRepView.as_view(), name="collectionsrep"),
    path("commissionrep/", views.CommissionRepView.as_view(), name="commissionrep"),

    path("cattargetrep/", views.CatTargetRepView.as_view(), name="cattargetrep"),
    path("chatargetrep/", views.ChaTargetRepView.as_view(), name="chatargetrep"),
    path("areatargetrep/", views.AreaTargetRepView.as_view(), name="areatargetrep"),
    path("custtargetrep/", views.CustTargetRepView.as_view(), name="custtargetrep"),
    path("salesmantargetrep/", views.SalesmanTargetRepView.as_view(), name="salesmantargetrep"),
    path("producttargetrep/", views.ProductTargetRepView.as_view(), name="producttargetrep"),
    path("storageanalysisrep/", views.StorageAnalysisRepRepView.as_view(), name="storageanalysisrep"),

    path("expenserep/", views.ExpensePrintView.as_view(), name="expenserep"),
    path("samplesrep/", views.SamplesRepView.as_view(), name="samplesrep"),

    path("salesmanvisitsrep/", views.SalesmanVisitsRepView.as_view(), name="salesmanvisitsrep"),
    path("salesmancoveragesrep/", views.SalesmanCoverageRepView.as_view(), name="salesmancoveragesrep"),

    path("collections/", views.CollectionListView.as_view(), name="collections"),
    path("collections/create/", views.CollectionCreateView.as_view(), name="create_collection"),
    path("collections/<int:pk>/delete/", views.CollectionDeleteView.as_view(), name="delete_collection"),
    path("collections/update/<int:pk>", views.CollectionUpdateView.as_view(), name="edit_collection"),
    path("collections/invoice/<int:pk>", views.CollectionInvoiceView.as_view(), name="collection_invoice"),

    path("currencies/", views.CurrencyListView.as_view(), name="currencies"),
    path("currencies/create/", views.CurrencyCreateView.as_view(), name="create_currency"),
    path("currencies/<int:pk>/delete/", views.CurrencyDeleteView.as_view(), name="delete_currency"),
    path("currencies/update/<int:pk>", views.CurrencyUpdateView.as_view(), name="edit_currency"),
    path('currencies/delete/',views.deletecurrencies, name="delete_currencies"),

    path("import/", views.Import, name="import"),
    path("export/", views.Export, name="export"),

    path("newsubdomain/", views.SubDomainListView.as_view(), name="newsubdomain"),
    path("newsubdomain/login", views.SubDomainLoginView, name="login_newsubdomain"),
    path("newsubdomain/create", views.SubDomainCreateView, name="create_newsubdomain"),
    path("newsubdomain/<int:pk>/delete/", views.SubDomainDeleteView.as_view(), name="delete_demoaccounts"),
    path("newsubdomain/stop/<int:pk>", views.SubDomainStopView.as_view(), name="stop_demoaccounts"),
    path("newsubdomain/activate/<int:pk>", views.SubDomainActiveView.as_view(), name="activate_demoaccounts"),
    path('newsubdomain/delete/',views.deletenewsubdomain, name="delete_newsubdomain"),

    path("leads/", views.LeadListView.as_view(), name="leads"),
    path("leads/upload/", views.contact_upload, name="contact_upload"),
    path("leads/create/", views.LeadCreateView.as_view(), name="create_lead"),
    path("leads/<int:pk>/delete/", views.LeadDeleteView.as_view(), name="delete_lead"),
    path("leads/<int:pk>/convert/", views.LeadConvertView.as_view(), name="convert_lead"),
    path("leads/update/<int:pk>", views.LeadUpdateView.as_view(), name="edit_lead"),

    path("opportunities/", views.OpportunityListView.as_view(), name="opportunities"),
    path("opportunities/create/", views.OpportunityCreateView.as_view(), name="create_opportunity"),
    path("opportunities/<int:pk>/delete/", views.OpportunityDeleteView.as_view(), name="delete_opportunity"),
    path("opportunities/update/<int:pk>", views.OpportunityUpdateView.as_view(), name="edit_opportunity"),
    path("opportunities/<int:pk>/convert/", views.OpportunityConvertView.as_view(), name="convert_opportunity"),

    path("activities/", views.ActivityListView.as_view(), name="activities"),
    path("activities/create/", views.ActivityCreateView.as_view(), name="create_activity"),
    path("activities/<int:pk>/delete/", views.ActivityDeleteView.as_view(), name="delete_activity"),
    path("activities/update/<int:pk>", views.ActivityUpdateView.as_view(), name="edit_activity"),

    path("commissions/", views.CommissionListView.as_view(), name="commissions"),
    path("commissions/create/", views.CommissionCreateView.as_view(), name="create_commission"),
    path("commissions/update/<int:pk>", views.CommissionUpdateView.as_view(), name="edit_commission"),
    path('commissions/delete/',views.deletecommissions, name="delete_commissions"),

    path("commissions_calc/", views.Commission_CalcListView.as_view(), name="commissions_calc"),
    path("commissions_calc/calc", views.CommissionCreate_Calc, name="create_commission_calc"),
    path("commissions_calc/update/<int:pk>", views.CommissionUpdateView.as_view(), name="edit_commission_calc"),
    path("commissions_calc/<int:pk>/delete/", views.CommissionDeleteView.as_view(), name="delete_commission_calc"),

    path("creditnotes/", views.CreditNoteListView.as_view(), name="creditnotes"),
    path("creditnotes/create/", views.CreditNoteCreateView.as_view(), name="create_creditnote"),
    path("creditnotes/<int:pk>/delete/", views.CreditNoteDeleteView.as_view(), name="delete_creditnote"),
    path("creditnotes/update/<int:pk>", views.CreditNoteUpdateView.as_view(), name="edit_creditnote"),
    path("creditnotes/invoice/<int:pk>", views.CreditNoteInvoiceView.as_view(),name="creditnote_invoice"),


#------------------khaldoun
    path("ajax/load-salesundeliveredorders-product/", views.load_salesundeliveredorders_product,name="ajax_load_salesundeliveredorders_product"),
    path("ajax/load_salesundeliveredorders-product-count/", views.load_salesundeliveredorders_product_count,name="ajax_load_salesundeliveredorders_product_count"),

    path("salesdelivery/", views.SalesDeliveryListView.as_view(), name="salesdelivery"),
    path("salesdelivery/create/<int:pk>", views.SalesDeliveryProductCreate.as_view(),name="create_salesdelivery"),
    #path("salesorder/update/<int:pk>", views.SalesOrderChangeView.as_view(), name="change_salesorder"),

    path("salesdelivery/view/<int:pk>", views.SalesDeliveryUpdateView.as_view(),name="edit_salesdelivery"),
    #path("salesreturnorder/invoice/<int:pk>", views.SalesReturnOrderInvoiceView.as_view(),name="salesreturnorder_invoice"),

    path("salesreturndelivery/", views.SalesReturnDeliveryListView.as_view(), name="salesreturndelivery"),

    path("useradditionalprofile/", views.UserAdditionalProfileListView.as_view(), name="useradditionalprofile"),
    path("useradditionalprofile/create/", views.UserAdditionalProfileCreateView.as_view(), name="create_useradditionalprofile"),
    path("useradditionalprofile/<int:pk>/delete/", views.UserAdditionalProfileDeleteView.as_view(), name="delete_useradditionalprofile"),
    path("useradditionalprofile/update/<int:pk>", views.UserAdditionalProfileUpdateView.as_view(), name="edit_useradditionalprofile"),
    path('useradditionalprofile/delete/',views.deleteuseradditionalprofile, name="delete_useradditionalprofile"),

    path("userbusinessroles/", views.UserBusinessRolesListView.as_view(),name="list-userbusinessroles"),
    path("userbusinessroles/create/", views.UserBusinessRolesCreateView.as_view(),name="create_userbusinessroles"),
    path("userbusinessroles/update/<int:pk>", views.UserBusinessRolesUpdateView.as_view(),name="edit_userbusinessroles"),
    path("userbusinessroles/<int:pk>/delete/", views.UserBusinessRolesDeleteView.as_view(),name="delete_userbusinessroles"),
    path('userbusinessroles/delete/',views.deleteuserbusinessroles, name="delete_userbusinessroles"),
                  #---------------------End khaldoun



    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
