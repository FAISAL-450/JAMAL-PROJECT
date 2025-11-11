from django.apps import AppConfig

class CustomerdetailedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customerdetailed'

    def ready(self):
        # Import signals to register them
        import customerdetailed.signals

