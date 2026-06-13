from django.urls import path
from . import views

app_name = "gl"

urlpatterns = [
    path('', views.index, name ='index'),
#Ledgers Types
    path("ledgerstypes/", views.LedgersTypesListView.as_view(), name = "list-ledgerstypes"),
    path("ledgerstypes/create/", views.LedgersTypesCreateView.as_view(), name="create_ledgerstypes"),
    path("ledgerstypes/update/<int:pk>", views.LedgersTypesUpdateView.as_view(), name="edit_ledgerstypes"),
    path("ledgerstypes/<int:pk>/delete/", views.LedgersTypesDeleteView.as_view(), name="delete_ledgerstypes"),
#ledger Categories
    path("ledgerscategories/", views.LedgersCategoriesListView.as_view(), name="list-ledgerscategories"),
    path("ledgerscategories/create/", views.LedgersCategoriesCreateView.as_view(), name="create_ledgerscategories"),
    path("ledgerscategories/update/<int:pk>", views.LedgersCategoriesUpdateView.as_view(), name="edit_ledgerscategories"),
    path("ledgerscategories/<int:pk>/delete/", views.LedgersCategoriesDeleteView.as_view(), name="delete_ledgerscategories"),

#Ledger
    path("ledger/", views.LedgerListView.as_view(), name="list-ledger"),
    path("ledger/create/", views.LedgerCreateView.as_view(), name="create_ledger"),
    path("ledger/update/<int:pk>", views.LedgerUpdateView.as_view(),name="edit_ledger"),
    path("ledger/<int:pk>/delete/", views.LedgerDeleteView.as_view(),name="delete_ledger"),


#Cost Categories
    path("costcategories/", views.CostCategoriesListView.as_view(), name="list-costcategories"),
    path("costcategories/create/", views.CostCategoriesCreateView.as_view(), name="create_costcategories"),
    path("costcategories/update/<int:pk>", views.CostCategoriesUpdateView.as_view(), name="edit_costcategories"),
    path("costcategories/<int:pk>/delete/", views.CostCategoriesDeleteView.as_view(), name="delete_costcategories"),


#Cost Centers Levels

    path("costcenterslevels/", views.CostCentersLevelsListView.as_view(), name="list-costcenterslevels"),
    path("costcenterslevels/create/", views.CostCentersLevelsCreateView.as_view(), name="create_costcenterslevels"),
    path("costcenterslevels/update/<int:pk>", views.CostCentersLevelsUpdateView.as_view(), name="edit_costcenterslevels"),
    path("costcenterslevels/<int:pk>/delete/", views.CostCentersLevelsDeleteView.as_view(), name="delete_costcenterslevels"),


#Cost Centers

    path("costcenters/", views.CostCentersListView.as_view(), name="list-costcenters"),
    path("costcenters/create/", views.CostCentersCreateView.as_view(), name="create_costcenters"),
    path("costcenters/update/<int:pk>", views.CostCentersUpdateView.as_view(), name="edit_costcenters"),
    path("costcenters/<int:pk>/delete/", views.CostCentersDeleteView.as_view(), name="delete_costcenters"),


#Trans Types

    path("transtypes/", views.TransTypesListView.as_view(), name="list-transtypes"),
    path("transtypes/create/", views.TransTypesCreateView.as_view(), name="create_transtypes"),
    path("transtypes/update/<int:pk>", views.TransTypesUpdateView.as_view(), name="edit_transtypes"),
    path("transtypes/<int:pk>/delete/", views.TransTypesDeleteView.as_view(), name="delete_transtypes"),

# Load Data
    path("ajax/load-transtypes/", views.load_transtypes, name="ajax_load_transtypes"),

#Ledger journal

    path("ledgerjour/", views.LedgerJourListView.as_view(), name="list-ledgerjour"),
    path("ledgerjour/create/", views.LedgerJourCreateView.as_view(), name="create_ledgerjour"),
    path("ledgerjour/update/<int:pk>", views.LedgerJourUpdateView.as_view(), name="edit_ledgerjour"),
    path("ledgerjour/<int:pk>/delete/", views.LedgerJourDeleteView.as_view(), name="delete_ledgerjour"),


#Treasuries

    path("treasuries/", views.TreasuriesListView.as_view(), name="list-treasuries"),
    path("treasuries/create/", views.TreasuriesCreateView.as_view(), name="create_treasuries"),
    path("treasuries/update/<int:pk>", views.TreasuriesUpdateView.as_view(), name="edit_treasuries"),
    path("treasuries/<int:pk>/delete/", views.TreasuriesDeleteView.as_view(), name="delete_treasuries"),

#Treasuries Orders

    path("treasuriesorders/", views.TreasuriesOrdersListView.as_view(), name="list-treasuriesorders"),
    path("treasuriesorders/create/", views.TreasuriesOrdersCreateView.as_view(), name="create_treasuriesorders"),
    path("treasuriesorders/update/<int:pk>", views.TreasuriesOrdersUpdateView.as_view(), name="edit_treasuriesorders"),
    path("treasuriesorders/<int:pk>/delete/", views.TreasuriesOrdersDeleteView.as_view(), name="delete_treasuriesorders"),


#Treasuries Orders Approval

    path("treasuriesordersapproval/", views.TreasuriesOrdersApprovalListView.as_view(), name="list-treasuriesordersapproval"),
    path("treasuriesordersapproval/update/<int:pk>", views.TreasuriesOrdersApprovalUpdateView.as_view(), name="edit_treasuriesordersapproval"),


# Ledger Payment

    path("ledgerpayments/", views.LedgerPaymentsListView.as_view(), name="list-ledgerpayments"),
    path("ledgerpayments/update/<int:pk>", views.LedgerPaymentsUpdateView.as_view(), name="edit_ledgerpayments"),



]

