from config.settings.handler import *

FIREBASE_CREDENTIALS_FILE_NAME = env.str(
    "FIREBASE_CREDENTIALS_FILE_NAME", default="firebase_key.json"
)
