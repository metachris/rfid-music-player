"""
The RFIDReader class only detects new RFID chips and
when detected starts all registered callbacks.
"""
import time
import signal

from logzero import LogFormatter, setup_logger

from rfid_music_player.core import settings
from rfid_music_player.core.eventhub import ee, EVENT_RFID_TAG_DETECTED, EVENT_RFID_TAG_REMOVED
from rfid_music_player.components.basecomponent import BaseComponent

if settings.IS_RASPBERRY:
    import RPi.GPIO as GPIO
    import MFRC522

log_formatter = LogFormatter(fmt='%(color)s[%(levelname)1.1s %(asctime)s %(name)s:%(lineno)d]%(end_color)s %(message)s')
logger = setup_logger("rfid-mfrc522", logfile=settings.LOGFILE, formatter=log_formatter, level=settings.LOGLEVEL)


# Timeout for sending the last detected tag a second time
SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC = 10
SEND_EVENT_TAG_REMOVED = True


class RFIDReader(BaseComponent):
    MIFAREReader = None
    tag_last_uid = None
    tag_last_timestamp = 0

    def __init__(self):
        BaseComponent.__init__(self)

        self.tag_last_uid = None
        self.tag_last_timestamp = 0

    def run_component(self):
        # Running on the dev machine
        if not settings.IS_RASPBERRY:
            return self.run_fake()

        # Running on the Pi
        self.MIFAREReader = MFRC522.MFRC522()  # TODO: This line has problems if not in read_rfid()!!
        while not self.event_quit.is_set():
            self.read_rfid()
            time.sleep(0.5)

    def read_rfid(self):
        # logger.debug("read_rfid")
        time_now = time.time()

        # Normal RFID handling for the raspberry
        # Create an object of the class MFRC522
        (status, tag_type) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        # If a card is found
        # if status == self.MIFAREReader.MI_OK:
        #     logger.info("Card detected")

        # Get the UID of the card
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:
            # Print UID
            card_uid = "%s-%s-%s-%s" % (str(uid[0]), str(uid[1]), str(uid[2]), str(uid[3]))
            logger.debug("Card detected with UID: %s", card_uid)

            if card_uid == self.tag_last_uid:
                # After detecting a chip, wait at least this amount of time until
                # sending another "detected" event
                if time_now - self.tag_last_timestamp < SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC:
                    # extend the timeout, else it will always resend after X seconds
                    self.tag_last_timestamp = time_now
                    logger.debug("- same card uid within SEND_EVENT_TAG_DETECTED_AGAIN_TIMEOUT_SEC, not sending again")
                    return

            self.tag_last_uid = card_uid
            self.tag_last_timestamp = time_now
            logger.debug("sending event rfid_tag_removed:%s" % self.tag_last_uid)
            ee.emit(EVENT_RFID_TAG_DETECTED, card_uid)

        else:
            # logger.debug("nothing found. last_uid: %s, send_event_tag_removed: %s", self.tag_last_uid, SEND_EVENT_TAG_REMOVED)
            if self.tag_last_uid:
                if SEND_EVENT_TAG_REMOVED:
                    logger.debug("sending event rfid_tag_removed:%s" % self.tag_last_uid)
                    ee.emit(EVENT_RFID_TAG_REMOVED, self.tag_last_uid)
                self.tag_last_uid = None


    def run_fake(self):
        """ Waits for RFID input and plays the correct song """
        while not self.event_quit.is_set():
            logger.info("Faking RFID 1234 found.")
            ee.emit(EVENT_RFID_TAG_DETECTED, "1234xxx")
            self.event_quit.wait(60)

    def shutdown(self):
        self.event_quit.set()

        if settings.IS_RASPBERRY:
            GPIO.cleanup()


if __name__ == "__main__":
    RFIDReader().run_dev()
