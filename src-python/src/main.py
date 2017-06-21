#!/usr/bin/env python3
"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
from logzero import setup_logger

import settings
from api import API
from player import Player
from rfidreader import RFIDReader

logger = setup_logger(logfile=settings.LOGFILE)



def main():
    api = API()
    api.run(threaded=True, debug=False)

    player = Player()

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

if __name__ == "__main__":
    main()
