import mimetypes
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

DEBUG = env.bool("DEBUG", None)

if DEBUG is None:
    environ.Env.read_env(BASE_DIR / ".envs" / "django.env.example")
    DEBUG = env.bool("DEBUG", False)

mimetypes.add_type("application/javascript", ".js", True)
