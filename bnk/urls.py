from django.urls import path
from . import views

app_name = "bnk"


urlpatterns = [

#Banks Groups
    path("banksgroups/", views.BanksGroupsListView.as_view(), name="list-banksgroups"),
    path("banksgroups/create/", views.BanksGroupsCreateView.as_view(), name="create_banksgroups"),
    path("banksgroups/update/<int:pk>", views.BanksGroupsUpdateView.as_view(), name="edit_banksgroups"),
    path("banksgroups/<int:pk>/delete/", views.BanksGroupsDeleteView.as_view(), name="delete_banksgroups"),


#Banks
    path("banks/", views.BanksListView.as_view(), name="list-banks"),
    path("banks/create/", views.BanksCreateView.as_view(), name="create_banks"),
    path("banks/update/<int:pk>", views.BanksUpdateView.as_view(), name="edit_banks"),
    path("banks/<int:pk>/delete/", views.BanksDeleteView.as_view(), name="delete_banks"),


#Banks
    path("banksdocumentsunderprocess/", views.BanksDocumentsUnderProcessListView.as_view(), name="list-banksdocumentsunderprocess"),
    path("banksdocumentsunderprocess/update/<int:pk>", views.BanksDocumentsUnderProcessUpdateView.as_view(), name="edit_banksdocumentsunderprocess"),
    path("banksdocumentsunderprocess/<int:pk>/delete/", views.BanksDocumentsUnderProcessDeleteView.as_view(), name="delete_banksdocumentsunderprocess"),


    ]