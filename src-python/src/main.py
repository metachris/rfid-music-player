#!/usr/bin/env python
"""

"""
import signal
from threading import Event

from logzero import setup_logger

from rfid_music_player.core import settings
from rfid_music_player.components.api import API
from rfid_music_player.components.player import Player
from rfid_music_player.components.updater import Updater
from rfid_music_player.components.basecomponent import BaseComponent
from rfid_music_player.inputs import start_all_input_threads, stop_all_input_threads, is_all_input_threads_alive

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


FAKE_UPDATE_AVAILABLE = True  # Set to None for real update check, True/False for mock

class MainPlayer(object):
    """
    Master player runtime which instantiates all components and waits for exit signals.
    """
    def __init__(self):
        self.event_exit = Event()

        # Instantiate components
        self.api = API()
        self.player = Player()
        self.updater = Updater(FAKE_UPDATE_AVAILABLE)
        self.input_threads = []

    def start(self):
        """
        Start the whole system, and wait forever
        (until SIGINT or until a component/thread has died)
        """
        # Register handler for SIGINT to shutdown the system
        signal.signal(signal.SIGINT, lambda sig, frame: self.shutdown())

        # Start components in background threads
        self.api.start()
        self.player.start()
        self.updater.start()
        self.input_threads = start_all_input_threads()

        # Now just wait.
        while not self.event_exit.is_set():
            self.event_exit.wait(1)

            # Shutdown if any of the components have dies
            if not self.event_exit.is_set() and not self.is_all_components_alive():
                logger.error("Not all components are alive. Shutting down.")
                self.shutdown()

    def shutdown(self):
        """ Shutdown the whole system """
        logger.info("shutdown...")
        self.event_exit.set()

        self.updater.shutdown()
        self.api.shutdown()
        self.player.shutdown()
        stop_all_input_threads()

    def is_all_components_alive(self):
        """
        Returns True if all components/background threads are alive, else False
        """
        return all([
            self.api.is_alive(),
            self.player.is_alive(),
            self.updater.is_alive(),
            is_all_input_threads_alive()
        ])


if __name__ == "__main__":
    MainPlayer().start()
