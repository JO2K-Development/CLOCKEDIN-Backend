from django.apps import AppConfig


class ClockedInConfig(AppConfig):
    name = "CLOCKEDIN_Backend"

    def ready(self):
        import CLOCKEDIN_Backend.signals
