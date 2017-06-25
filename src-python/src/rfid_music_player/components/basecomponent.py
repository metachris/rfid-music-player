from threading import Thread, Event

class BaseComponent(Thread):
    """ Example component """
    event_quit = None

    def __init__(self):
        Thread.__init__(self)
        self.event_quit = Event()

    def run(self):
        self.event_quit.wait()

    def shutdown(self):
        self.event_quit.set()
