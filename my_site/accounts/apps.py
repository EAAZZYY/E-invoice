from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    """ Import Signals in signals.py """
    def ready(self):
        import accounts.signals