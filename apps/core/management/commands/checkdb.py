from django.apps import apps
from django.core.management.base import CommandError, BaseCommand

from config.settings.apps import LOCAL_APPS


class Command(BaseCommand):
    help = "A command to setup api for an application in APPS_DIR or given directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--appname",
            type=str,
            help="The current Django project folder name",
            default=None,
        )

    def format_warning(self, message: str, warning_type: str = None):
        if warning_type == "str":
            return self.style.WARNING(
                f"Warning: Model {message} has not __str__ method."
            )

    def handle(self, *args, **options):
        app_name = options.get("appname")

        if app_name:
            try:
                app = apps.get_app_config(app_name)
            except LookupError as exc:
                raise CommandError(
                    f"LookupError: No installed app with label '{app_name}'"
                ) from exc
            models = app.get_models()
            warnings = [
                self.format_warning(model, warning_type="str")
                for model in models
                if "__str__" not in model.__dict__
            ]

            if warnings:
                self.stdout.write("\n".join(warnings))
            else:
                self.stdout.write(self.style.SUCCESS("No problems found."))

        else:
            warnings = []
            for app_name in LOCAL_APPS:
                try:
                    app_name = app_name.rsplit(".", maxsplit=1)[-1]
                    app = apps.get_app_config(app_name)
                except LookupError as exc:
                    raise CommandError(
                        f"LookupError: No installed app with label '{app_name}'"
                    ) from exc
                models = app.get_models()
                warnings += [
                    self.format_warning(model, warning_type="str")
                    for model in models
                    if "__str__" not in model.__dict__
                ]

            if warnings:
                self.stdout.write("\n".join(warnings))
            else:
                self.stdout.write(self.style.SUCCESS("No problems found."))
