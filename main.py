from networksecurity.logger.logging import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys
logging.info("Hello World.")

try:
    1 / 0
except Exception as e:
    raise NetworkSecurityException(e, sys.exc_info())
