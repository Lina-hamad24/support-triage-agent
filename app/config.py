import logging


# Application configuration
APP_NAME = "Support Triage Agent"


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("support-triage-agent")