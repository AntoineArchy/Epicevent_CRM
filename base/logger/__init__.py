import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from utils import get_sentry_link_from_config

# dsn = (
#     "https://02eff9afe5d44fe1ee9125f156b9353d@o4506082518564864.ingest.sentry.io/4506082524004352",
# )

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.WARNING,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


sentry_sdk.init(
    dsn=get_sentry_link_from_config(),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[sentry_logging],
)
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration du journal local
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Gestionnaire de fichiers rotatifs basé sur la date
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
daily_log_handler = TimedRotatingFileHandler(
    log_filename,
    when="midnight",
    interval=1,
    encoding="utf-8",
    delay=False,
)
daily_log_handler.setFormatter(log_formatter)
logger.addHandler(daily_log_handler)

# Ajout d'un gestionnaire de console pour afficher les logs dans la console tant que Rich n'est pas en route
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(log_formatter)
# logger.addHandler(console_handler)
