# A - App Configuration
from django.apps import AppConfig

class CustomerdetailedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customerdetailed'

    # B - Signal Registration
    def ready(self):
        import customerdetailed.signals

