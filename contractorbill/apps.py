from django.apps import AppConfig

class ContractorbillConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contractorbill'

    def ready(self):
        import contractorbill.signals
