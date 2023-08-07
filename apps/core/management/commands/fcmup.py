import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, "requirements/base.txt"), "r+"
        ) as fcm_requirement:
            requirements_content = fcm_requirement.read()
            if "firebase-admin==6.1.0" not in requirements_content:
                fcm_requirement.write("firebase-admin==6.1.0")

        with open(os.path.join(settings.BASE_DIR, "apps/core/fcm.py"), "w") as fcm:
            with open(
                os.path.join(
                    settings.BASE_DIR, "apps/core/management/commands/fcm.txt"
                ),
                "r",
            ) as fcm_txt:
                fcm.write(fcm_txt.read())
        self.stdout.write(
            self.style.SUCCESS(
                "FCM is up Check the core directory and follow the instruction in README"
            )
        )
