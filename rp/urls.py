from django.urls import path
from . import views

app_name = "rp"

urlpatterns = [
    path('', views.index, name ='index'),

# Reports Settings

# Reports Groups
    path("reportsgroups/", views.ReportsGroupsListView.as_view(), name="list-reportsgroups"),
    path("reportsgroups/create/", views.ReportsGroupsCreateView.as_view(),name="create_reportsgroups"),
    path("reportsgroups/update/<int:pk>", views.ReportsGroupsUpdateView.as_view(),name="edit_reportsgroups"),
    path("reportsgroups/<int:pk>/delete/", views.ReportsGroupsDeleteView.as_view(),name="delete_reportsgroups"),
    path('reportsgroups/delete/',views.deletereportsgroups, name="delete_reportsgroups"),

# Reports
    path("reports/", views.ReportsListView.as_view(), name="list-reports"),
    path("reports/create/", views.ReportsCreateView.as_view(), name="create_reports"),
    path("reports/update/<int:pk>", views.ReportsUpdateView.as_view(), name="edit_reports"),
    path("reports/<int:pk>/delete/", views.ReportsDeleteView.as_view(), name="delete_reports"),
    path('reports/delete/',views.deletereports, name="delete_reports"),

# Reports Viewer
    path("reportsrun/<int:pk>", views.ReportsRunView.as_view(), name="reportsrun"),

    path("reportcontainerview/<int:id>", views.ReportsContainerView.as_view(), name="view-reportcontainerview"),
    path("reportparam/<int:id>", views.ReportsParamView.as_view(), name="view-reportparam"),
    path("reportview/", views.ReportView.as_view(), name="view_reportview"),

    path("dashboardview/<int:id>", views.DashboardViewerView.as_view(), name="view-dashboardview"),

    # Load Reports

    path("ajax/load_reports/", views.load_reports, name="ajax_load_reports"),
    path("ajax/load_bashboards/", views.load_reports, name="ajax_load_bashboards"),

    #path("ajax/load_reports/", views.load_reports, name="ajax_load_reports"),

    path("reportsmenu/", views.ReportsMenuListView.as_view(), name="list-reportsmenu"),

    path("ledgersoa/", views.LedgerSOAListView.as_view(), name="list-ledgersoa"),


]