"""
This is a blueprint for components.
Subclass it and you get a lot of goodies.
"""
import signal
from threading import Thread, Event

from logzero import setup_logger
from rfid_music_player.core import settings

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


class BaseComponent(Thread):
    """ Example component """
    event_quit = None

    def __init__(self):
        Thread.__init__(self)
        self.event_quit = Event()

    def run(self):
        try:
            self.run_component()
        except Exception as e:
            logger.exception(e)
            self.shutdown()

    def run_component(self):
        while not self.event_quit.is_set():
            logger.debug("Do nothing for 10 sec...")
            self.event_quit.wait(10)
            # raise Exception("123")

    def shutdown(self):
        """ Shut down the thread. May be called multiple times. """
        self.event_quit.set()

    def run_dev(self):
        """
        Helper to test the component independently by starting it from the
        command line (eg. with `BaseComponent().run_dev()`). It starts the
        thread and waits for a signal (eg. CTRL+C) and then calls shutdown.
        """
        self.start()

        try:
            while self.is_alive():
                self.join(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
            print("bye")

        self.join()


# You can test this component from the command line
if __name__ == "__main__":
    BaseComponent().run_dev()
