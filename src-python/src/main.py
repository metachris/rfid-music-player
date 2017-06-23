#!/usr/bin/env python
"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
from logzero import setup_logger

from core import settings
from core.api import API
from core.player import Player
from core.inputs.rfid_mfrc522 import RFIDReader

logger = setup_logger(logfile=settings.LOGFILE)



def main():
    # The api, which runs in a background thread
    api = API()
    api.run(threaded=True, debug=False)

    # The player asynchronously waits for events and plays in the background
    player = Player()

    # The input manager also runs in the background, and can handle a number
    # of inputs such as RFID, GPIO, etc.
    rfid = RFIDReader()

    try:
        rfid.run()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.exception(exc)
        raise
    finally:
        player.shutdown()
        rfid.shutdown()

if __name__ == "__main__":
    main()
