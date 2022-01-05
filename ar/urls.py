from django.urls import path
from . import views

app_name = "ar"

urlpatterns = [
# Drop Down
    path("ajax/load-duepayment-lines/", views.load_duepayment_line, name="ajax_load-duepayment-lines"),
    path("ajax/load-duepayment-lines-count/", views.load_duepayment_line_count, name="ajax_load-duepayment-lines-count"),

#Customers Categories
    path("customerscategories/", views.CustomersCategoriesListView.as_view(), name="list-customerscategories"),
    path("customerscategories/create/", views.CustomersCategoriesCreateView.as_view(), name="create_customerscategories"),
    path("customerscategories/update/<int:pk>", views.CustomersCategoriesUpdateView.as_view(), name="edit_customerscategories"),
    path("customerscategories/<int:pk>/delete/", views.CustomersCategoriesDeleteView.as_view(), name="delete_customerscategories"),



#Customers Classes
    path("customersclasses/", views.CustomersClassesListView.as_view(), name="list-customersclasses"),
    path("customersclasses/create/", views.CustomersClassesCreateView.as_view(), name="create_customersclasses"),
    path("customersclasses/update/<int:pk>", views.CustomersClassesUpdateView.as_view(), name="edit_customersclasses"),
    path("customersclasses/<int:pk>/delete/", views.CustomersClassesDeleteView.as_view(), name="delete_customersclasses"),


#Customer
    path("customers/", views.CustomersListView.as_view(), name="list-customers"),
    path("customers/create/", views.CustomersCreateView.as_view(), name="create_customers"),
    path("customers/update/<int:pk>", views.CustomersUpdateView.as_view(),name="edit_customers"),
    path("customers/<int:pk>/delete/", views.CustomersDeleteView.as_view(),name="delete_customers"),


#Customers journal

    path("customersjour/", views.CustomersJourListView.as_view(), name="list-customersjour"),
    path("customersjour/create/", views.CustomersJourCreateView.as_view(), name="create_customersjour"),
    path("customersjour/update/<int:pk>", views.CustomersJourUpdateView.as_view(), name="edit_customersjour"),
    path("customersjour/<int:pk>/delete/", views.CustomersJourDeleteView.as_view(), name="delete_customersjour"),

# Csutomers Payments

    path("customerspayments/", views.CustomersPaymentsListView.as_view(), name="list-customerspayments"),
    path("customerspayments/update/<int:pk>", views.CustomersPaymentsUpdateView.as_view(), name="edit_customerspayments"),


#Collections

    path("collections/", views.CollectionsListView.as_view(), name="list-collections"),
    path("collections/create/", views.CollectionsCreateView.as_view(), name="create_collections"),
    path("collections/update/<int:pk>", views.CollectionsUpdateView.as_view(), name="edit_collections"),
    path("collections/<int:pk>/delete/", views.CollectionsDeleteView.as_view(), name="delete_collections"),


#Salesmans Groups
    path("salesmansgroups/", views.SalesmansGroupsListView.as_view(), name="list-salesmansgroups"),
    path("salesmansgroups/create/", views.SalesmansGroupsCreateView.as_view(), name="create_salesmansgroups"),
    path("salesmansgroups/update/<int:pk>", views.SalesmansGroupsUpdateView.as_view(), name="edit_salesmansgroups"),
    path("salesmansgroups/<int:pk>/delete/", views.SalesmansGroupsDeleteView.as_view(), name="delete_salesmansgroups"),


#Salesmans
    path("salesmans/", views.SalesmansListView.as_view(), name="list-salesmans"),
    path("salesmans/create/", views.SalesmansCreateView.as_view(), name="create_salesmans"),
    path("salesmans/update/<int:pk>", views.SalesmansUpdateView.as_view(), name="edit_salesmans"),
    path("salesmans/<int:pk>/delete/", views.SalesmansDeleteView.as_view(), name="delete_salesmans"),


]