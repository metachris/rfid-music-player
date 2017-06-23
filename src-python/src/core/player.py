import os
import time
import signal
import subprocess
import datetime
from threading import Thread, Event

from logzero import setup_logger

from core import database
from core import settings
from core import utils
from core.eventhub import ee

logger = setup_logger(logfile=settings.LOGFILE)


class Player(object):
    def __init__(self):
        self.player_process = None
        self.fn_sound = None
        self.is_playing = False

        @ee.on("rfid_detected")
        def _rfid_detected(rfid_id):
            self.rfid_detected(rfid_id)

    def shutdown(self):
        self.kill_player()

    def rfid_detected(self, rfid_id):
        logger.info("rfid_detected: %s", rfid_id)

        # - Find song in database
        tag = database.get_tag(rfid_id)
        logger.info("- db returned tag: %s", tag)
        if not tag:
            logger.info("- no song found for this tag.")
            return

        self.fn_sound = os.path.join(settings.PATH_MUSIC, tag["song"])
        self.start_playback_threaded()

    def start_playback(self):
        # Write playback log entry
        with open(settings.FN_PLAY_LOGS, "a") as f:
            now = datetime.datetime.now()
            f.write("%s: start: %s\n" % (now.isoformat(), self.fn_sound))

        # If already playing, kill player
        if self.is_playing:
            self.kill_player()

        player_cmd = utils.make_cmd_playback(self.fn_sound)
        logger.info("Starting playback with command: %s", " ".join(player_cmd))
        self.player_process = subprocess.Popen(player_cmd, preexec_fn=os.setsid)
        self.is_playing = True
        logger.info('player PID is ' + str(self.player_process.pid))
        self.player_process.wait()  # Now wait for player to finish
        self.player_process = None
        self.is_playing = False
        logger.info("end of playback: >> %.3f", time.time() % 100)

    def start_playback_threaded(self):
        logger.info("starting threaded playback mode")
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
            logger.info("killing player with PID %s", str(self.player_process.pid))
            try:
                os.killpg(os.getpgid(self.player_process.pid), signal.SIGTERM)
            except Exception as e:
                logger.warn("could not kill player: %s", str(e))
