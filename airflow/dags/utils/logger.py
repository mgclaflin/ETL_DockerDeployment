import os
import logging
from config import LOG_PATH

# Ensure the logs directory exists
log_dir = os.path.dirname(LOG_PATH)
os.makedirs(log_dir, exist_ok=True)  # Create directory if it doesn't exist

# clear existing handlers to prevent duplicates
logger = logging.getLogger(__name__)
logger.handlers.clear()

# Configure Logging w/ the correct log file path
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger.info("Logger initialized successfully.")
