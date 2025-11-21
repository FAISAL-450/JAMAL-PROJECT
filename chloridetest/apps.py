from django.apps import AppConfig

class ChloridetestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chloridetest'

    def ready(self):
        # Import signals to register them
        import chloridetest.signals

