from django.apps import AppConfig


class DemoConfig(AppConfig):
    name = "demo"
    verbose_name = "Demo application."
    default_auto_field = "django.db.models.AutoField"
