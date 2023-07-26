import os
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Renames a Django project"

    def add_arguments(self, parser):
        parser.add_argument(
            "current_name", type=str, help="The current Django project folder name"
        )
        parser.add_argument("new_name", type=str, help="The new Django project name")

    def handle(self, *args, **kwargs):
        current_project_name = kwargs.get("current_name")
        new_project_name = kwargs.get("new_name")

        if not current_project_name or not new_project_name:
            raise CommandError(
                "You must provide both current_name and new_name to change project name"
            )

        files_to_rename = [
            f"{current_project_name}/settings/base.py",
            f"{current_project_name}/settings/__init__.py",
            f"{current_project_name}/wsgi.py",
            f"{current_project_name}/asgi.py",
            ".envs/local/.django",
            "manage.py",
        ]

        for file_to_rename in files_to_rename:
            with open(file_to_rename, "r+", encoding="utf-8") as file:
                file_data = file.read()
                file_data = file_data.replace(current_project_name, new_project_name)
                file.seek(0)
                file.truncate()
                file.write(file_data)

        os.rename(current_project_name, new_project_name)

        self.stdout.write(
            self.style.SUCCESS(f"Project has been renamed to {new_project_name}")
        )
