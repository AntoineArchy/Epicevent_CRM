import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.WARNING,
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

sentry_sdk.init(
    dsn="https://02eff9afe5d44fe1ee9125f156b9353d@o4506082518564864.ingest.sentry.io/4506082524004352",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[sentry_logging],
)
