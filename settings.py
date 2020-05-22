import os

TOKEN = os.environ.get("TELEGRAM_API_TOKEN", '')

ENABLED_USERS = os.environ.get("ENABLED_USERS", '')
ENABLED_USERS = set(int(e.strip()) for e in ENABLED_USERS.split(','))
