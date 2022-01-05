from django.urls import path

#from TARGET.crm.views import (dashboard2_view, )
from .views import (dashboard_view, )

app_name = "dashboard"
urlpatterns = [
    path("", view=dashboard_view, name="dashboard"),

]
