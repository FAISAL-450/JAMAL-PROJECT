from django.apps import AppConfig

class CustomerbillConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customerbill'

    def ready(self):
        import customerbill.signals  # Ensures signals are registered when the app is ready

