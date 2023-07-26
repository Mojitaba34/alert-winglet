import os

from django.core.management.templates import TemplateCommand
from django.conf import settings


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the APPS_DIR defined in settings.py or the given directory"
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop("name")
        target = options.pop("directory")

        os.mkdir(settings.BASE_DIR / settings.APPS_DIR / app_name)
        if target is None:
            target = settings.APPS_DIR / app_name

        super().handle("app", app_name, target, **options)
        self.stdout.write(
            self.style.SUCCESS(f"App {app_name} created in directory: {target}")
        )
