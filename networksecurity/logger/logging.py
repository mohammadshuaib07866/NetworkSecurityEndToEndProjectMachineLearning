import sys
import os
import logging
from datetime import datetime

# Generate a unique log file name based on the current datetime
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_H_%M_%S')}.log"

# Define the path to the log directory
log_path = os.path.join(os.getcwd(), "logs")

# Create the logs directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

# Create the full path for the log file
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
