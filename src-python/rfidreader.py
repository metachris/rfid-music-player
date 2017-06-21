"""
The RFIDReader class only detects new RFID chips and
when detected starts all registered callbacks.
"""
import time
from logzero import setup_logger

import database
import settings
from eventbus import ee

logger = setup_logger(logfile=settings.LOGFILE)


class RFIDReader(object):
    def run(self):
        """ Waits for RFID input and plays the correct song """
        logger.info("Waiting for RFID chip...")
        while True:
            # TODO: wait for RFID change
            ee.emit("rfid_detected", "1234")
            time.sleep(120)
