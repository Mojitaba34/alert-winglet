from apps.core.management.templates import BaseTemplate
from django.core.management.templates import TemplateCommand
from string import Template

base_template = BaseTemplate()


class Command(TemplateCommand):
    """Celery Command"""

    help = "This command will setup the celery on your project."
    missing_args_message = "You must provide a task and an application name."

    def handle(self, **kwargs):
        task_name = kwargs.get("name")
        app_name = kwargs.get("directory")

        celery_file = "config/celery_app.py"
        task_file = f"apps/{app_name}/tasks.py"
        celery_data = Template(
            "from __future__ import absolute_import, unicode_literals\n"
            "from celery import Celery \n"
            "import os \n"
            "from django.apps import apps \n"
            "from celery.schedules import crontab \n"
            '\nos.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") \n'
            'app = Celery("config") \n'
            'app.config_from_object("django.conf:settings", namespace="CELERY") \n'
            "app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()]) \n"
            "\n@app.task(bind=True) \n"
            "def debug_task(self): \n"
            '   print(f"Request: {self.request!r}") \n'
            "\n# here is a sample beat schedule \n"
            "app.conf.beat_schedule = { \n"
            ' "test_celery_task": { \n'
            f' "task": "apps.{app_name}.tasks.{task_name}", \n'
            '"schedule": crontab(), \n'
            "    }, \n"
            "} \n"
        )

        task_data = Template(
            "from celery import shared_task\n"
            "import logging\n"
            "logger = logging.getLogger(__name__)\n"
            "\n@shared_task\n"
            f"def {task_name}():\n"
            "   logger.info('Task is Running!')"
        )
        BaseTemplate().write_file(
            celery_file,
            celery_data.substitute(app_name=f"{app_name}", task_name=f"{task_name}"),
        )
        BaseTemplate().write_file(
            task_file, task_data.substitute(task_name=f"{task_name}")
        )

        self.stdout.write(self.style.SUCCESS("Celery added"))
