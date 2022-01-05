from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = "TARGET.crm"
    verbose_name = "Crm"

    def ready(self):
        pass

