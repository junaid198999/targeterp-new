from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "TARGET.common"
    verbose_name = "Common"

    def ready(self):
        pass
