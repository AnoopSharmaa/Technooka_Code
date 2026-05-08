from django.apps import AppConfig


class LmsConfig(AppConfig):
    name = 'LMS'

    def ready(self):

        import LMS.signals
