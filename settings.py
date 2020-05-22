import os

TOKEN = os.environ.get("TELEGRAM_API_TOKEN", '1092917717:AAGPTG8s-y38so6HNS1ubnA6ubUnHTpqWBU')

ENABLED_USERS = os.environ.get("ENABLED_USERS", '822528623')
ENABLED_USERS = set(int(e.strip()) for e in ENABLED_USERS.split(','))