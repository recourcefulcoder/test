import datetime
import os
from pathlib import Path

from dotenv import load_dotenv


def load_environ():
    base_url = Path(__file__).resolve().parent.parent
    print(base_url / ".env")
    if os.path.isfile(base_url / ".env"):
        load_dotenv(base_url / ".env")


load_environ()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
CLOSE_PERIOD = datetime.timedelta(hours=1)
