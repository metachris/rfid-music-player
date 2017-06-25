#!/usr/bin/env python
"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
import signal

from logzero import setup_logger

from rfid_music_player.core import settings
from rfid_music_player.components.api import API
from rfid_music_player.components.player import Player
from rfid_music_player.inputs import start_all_input_threads, stop_all_input_threads

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


def main():
    # Start the api
    api = API()
    api.start()

    # Start the player
    player = Player()
    player.start()

    # Start all input threads (RFID, GPIO, etc)
    input_threads = start_all_input_threads()

    # All systems up and running. Now wait forever
    logger.info("All threads started. Now waiting for events.")
    try:
        signal.pause()
    except KeyboardInterrupt:
        print("")
    finally:
        # Finally, shutdown everything
        api.shutdown()
        player.shutdown()
        stop_all_input_threads()

    logger.info("bye")


if __name__ == "__main__":
    main()
