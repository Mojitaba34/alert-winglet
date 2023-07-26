from .handler import BASE_DIR

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = ["apps.core", "apps.test_api", "apps.alert_winglet"]

# CHECK IF INSTALLED APPS INCLUDE THE PACKAGE FIRST
THIRD_PARTY_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

APPS_DIR = BASE_DIR / "apps"
