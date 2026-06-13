from django.urls import path
from . import views

app_name = "ap"

urlpatterns = [
#vendors Categories
    path("vendorscategories/", views.VendorsCategoriesListView.as_view(), name="list-vendorscategories"),
    path("vendorscategories/create/", views.VendorsCategoriesCreateView.as_view(), name="create_vendorscategories"),
    path("vendorscategories/update/<int:pk>", views.VendorsCategoriesUpdateView.as_view(), name="edit_vendorscategories"),
    path("vendorscategories/<int:pk>/delete/", views.VendorsCategoriesDeleteView.as_view(), name="delete_vendorscategories"),



#vendors Classes
    path("vendorsclasses/", views.VendorsClassesListView.as_view(), name="list-vendorsclasses"),
    path("vendorsclasses/create/", views.VendorsClassesCreateView.as_view(), name="create_vendorsclasses"),
    path("vendorsclasses/update/<int:pk>", views.VendorsClassesUpdateView.as_view(), name="edit_vendorsclasses"),
    path("vendorsclasses/<int:pk>/delete/", views.VendorsClassesDeleteView.as_view(), name="delete_vendorsclasses"),


#Vendor
    path("vendors/", views.VendorsListView.as_view(), name="list-vendors"),
    path("vendors/create/", views.VendorsCreateView.as_view(), name="create_vendors"),
    path("vendors/update/<int:pk>", views.VendorsUpdateView.as_view(),name="edit_vendors"),
    path("vendors/<int:pk>/delete/", views.VendorsDeleteView.as_view(),name="delete_vendors"),


#buyersgroups
    path("buyersgroups/", views.BuyersGroupsListView.as_view(), name="list-buyersgroups"),
    path("buyersgroups/create/", views.BuyersGroupsCreateView.as_view(), name="create_buyersgroups"),
    path("buyersgroups/update/<int:pk>", views.BuyersGroupsUpdateView.as_view(),name="edit_buyersgroups"),
    path("buyersgroups/<int:pk>/delete/", views.BuyersGroupsDeleteView.as_view(),name="delete_buyersgroups"),

#buyers
    path("buyers/", views.BuyersListView.as_view(), name="list-buyers"),
    path("buyers/create/", views.BuyersCreateView.as_view(), name="create_buyers"),
    path("buyers/update/<int:pk>", views.BuyersUpdateView.as_view(),name="edit_buyers"),
    path("buyers/<int:pk>/delete/", views.BuyersDeleteView.as_view(),name="delete_buyers"),





#Vendor Jour
    path("vendorsjour/", views.VendorsJourListView.as_view(), name="list-vendorsjour"),
    path("vendorsjour/create/", views.VendorsJourCreateView.as_view(), name="create_vendorsjour"),
    path("vendorsjour/update/<int:pk>", views.VendorsJourUpdateView.as_view(),name="edit_vendorsjour"),
    path("vendorsjour/<int:pk>/delete/", views.VendorsJourDeleteView.as_view(),name="delete_vendorsjour"),


]