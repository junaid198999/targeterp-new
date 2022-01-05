from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = "TARGET.dashboard"
    verbose_name = "Dashboard"

    def ready(self):
        pass
