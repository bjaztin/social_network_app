from django.apps import AppConfig

class HelloyouappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helloYouApp'

    def ready(self):
        import helloYouApp.signals
