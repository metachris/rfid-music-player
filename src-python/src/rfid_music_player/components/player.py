import os
import time
import signal
import subprocess
import datetime
from threading import Thread, Event

from logzero import setup_logger

from rfid_music_player.core import database
from rfid_music_player.core import settings
from rfid_music_player.core import utils
from rfid_music_player.core.eventhub import ee, EVENT_RFID_TAG_DETECTED, EVENT_RFID_TAG_REMOVED
from rfid_music_player.components.basecomponent import BaseComponent

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


class Player(BaseComponent):
    """
    The player is completely asynchronous, it just starts omxplayer in the background.
    """
    def __init__(self):
        BaseComponent.__init__(self)

        self.player_process = None
        self.fn_sound = None
        self.is_playing = False

    def run_component(self):
        @ee.on(EVENT_RFID_TAG_DETECTED)
        def _rfid_detected(rfid_id):
            self.rfid_detected(rfid_id)

        @ee.on(EVENT_RFID_TAG_REMOVED)
        def _rfid_removed(rfid_id):
            if self.is_playing:
                self.kill_player()

        # Now just wait forever (until quit event)
        self.event_quit.wait()

    def shutdown(self):
        self.kill_player()
        self.event_quit.set()

    def rfid_detected(self, rfid_id):
        logger.debug("rfid_detected: %s", rfid_id)

        # - Find song in database
        tag = database.get_tag(rfid_id)
        logger.debug("- db returned tag: %s", tag)
        if not tag:
            logger.info("- no song found for this tag.")
            return

        self.fn_sound = os.path.join(settings.PATH_MUSIC, tag["song"])
        self.start_playback_threaded()

    def start_playback(self):
        # Write playback log entry
        # with open(settings.FN_PLAY_LOGS, "a") as f:
        #     now = datetime.datetime.now()
        #     f.write("%s: start: %s\n" % (now.isoformat(), self.fn_sound))

        # If already playing, kill player
        if self.is_playing:
            self.kill_player()

        player_cmd = utils.make_cmd_playback(self.fn_sound)
        logger.debug("Starting playback with command: %s", " ".join(player_cmd))
        self.player_process = subprocess.Popen(player_cmd, preexec_fn=os.setsid)
        self.is_playing = True
        # logger.debug('player PID is ' + str(self.player_process.pid))
        self.player_process.wait()  # Now wait for player to finish
        self.player_process = None
        self.is_playing = False

    def start_playback_threaded(self):
        # logger.info("starting threaded playback mode")
        thread = Thread(target=self.start_playback)
        thread.daemon = True
        thread.start()
        return thread

    def kill_player(self):
        """
        Send kill command to player.
        """
        if self.player_process and not self.player_process.poll():
            # player is running... kill now by sending SIGTERM
            # to all children of the process groups
            logger.debug("killing player with PID %s", str(self.player_process.pid))
            try:
                os.killpg(os.getpgid(self.player_process.pid), signal.SIGTERM)
            except Exception as e:
                logger.warn("could not kill player: %s", str(e))
