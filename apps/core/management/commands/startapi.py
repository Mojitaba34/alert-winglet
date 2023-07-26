from django.core.management.base import CommandError, BaseCommand
from django.conf import settings

from apps.core.management.templates import ApiTemplate


class Command(BaseCommand):
    help = "A command to setup api for an application in APPS_DIR or given directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "appname",
            type=str,
            help="The current Django project folder name",
        )
        parser.add_argument(
            "--appdir",
            type=str,
            help="Directory that app lives in -if it is not in the default APPS_DIR directory",
        )

    def handle(self, *args, **options):
        app_name = options.get("appname")
        app_dir = options.get("appdir")

        if not app_name:
            raise CommandError(
                "You must either provide appname or both appname and appdir"
            )

        if not app_dir:
            parent_directory = settings.APPS_DIR / app_name
        else:
            parent_directory = app_dir

        ApiTemplate(parent_directory=parent_directory).make_template()
        self.stdout.write(f"Api created successfully for app '{app_name}'")
