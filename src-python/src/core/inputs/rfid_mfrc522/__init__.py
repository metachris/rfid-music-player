"""
The RFIDReader class only detects new RFID chips and
when detected starts all registered callbacks.
"""
import time
from logzero import LogFormatter, setup_logger

from core import settings
from core.eventhub import ee

if settings.IS_RASPBERRY:
    import RPi.GPIO as GPIO
    import MFRC522

log_formatter = LogFormatter(fmt='%(color)s[%(levelname)1.1s %(asctime)s %(name)s:%(lineno)d]%(end_color)s %(message)s')
logger = setup_logger("rfid-mfrc522", logfile=settings.LOGFILE, formatter=log_formatter)


# Timeout for sending the last detected tag a second time
SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC = 10
SEND_EVENT_TAG_REMOVED = True


class RFIDReader(object):
    is_running = False
    tag_last_uid = None
    tag_last_timestamp = 0

    def __init__(self):
        self.is_running = False
        self.tag_last_uid = None
        self.tag_last_timestamp = 0

    def run(self):
        self.is_running = True

        if not settings.IS_RASPBERRY:
            return self.run_fake()

        while self.is_running:
            self.read_rfid()
            time.sleep(0.5)

    def read_rfid(self):
        # logger.debug("read_rfid")
        time_now = time.time()

        # Normal RFID handling for the raspberry
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        (status, tag_type) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        # if status == MIFAREReader.MI_OK:
        #     logger.info("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            card_uid = "%s-%s-%s-%s" % (str(uid[0]), str(uid[1]), str(uid[2]), str(uid[3]))
            logger.debug("Card detected with UID: %s", card_uid)

            if card_uid == self.tag_last_uid:
                # After detecting a chip, wait at least this amount of time until
                # sending another "detected" event
                if time_now - self.tag_last_timestamp < SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC:
                    logger.debug("- same card uid within SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC, not sending again")
                    return

            self.tag_last_uid = card_uid
            self.tag_last_timestamp = time_now
            ee.emit("rfid_detected", card_uid)

        else:
            # logger.debug("nothing found. last_uid: %s, send_event_tag_removed: %s", self.tag_last_uid, SEND_EVENT_TAG_REMOVED)
            if self.tag_last_uid:
                if SEND_EVENT_TAG_REMOVED:
                    logger.debug("sending event rfid_tag_removed:%s" % self.tag_last_uid)
                    ee.emit("rfid_tag_removed", self.tag_last_uid)
                self.tag_last_uid = None


    def run_fake(self):
        """ Waits for RFID input and plays the correct song """
        logger.info("Waiting for RFID chip...")
        while self.is_running:
            # TODO: wait for RFID change
            ee.emit("rfid_detected", "1234")
            time.sleep(30)

    def shutdown(self):
        if not settings.IS_RASPBERRY:
            return

        GPIO.cleanup()


if __name__ == "__main__":
    rfid_reader = RFIDReader()
    rfid_reader.run()
