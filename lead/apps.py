from django.apps import AppConfig

class LeadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lead'

    def ready(self):
        # Import signals to connect them when the app is ready
        import lead.signals
