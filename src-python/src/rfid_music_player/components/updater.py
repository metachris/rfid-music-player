import subprocess
import semver

from logzero import setup_logger

from rfid_music_player.core import settings
from rfid_music_player.components.basecomponent import BaseComponent
from rfid_music_player.core.eventhub import (
    ee,
    EVENT_UPDATE_AVAILABLE,
    EVENT_UPDATE_EXECUTE,
    EVENT_UPDATE_STATUS
)

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


# SECONDS_BETWEEN_CHECKS = 60 * 60  # 1h
SECONDS_BETWEEN_CHECKS = 30


def execute_update():
    logger.info("Executing update...")
    ee.emit(EVENT_UPDATE_STATUS, "initiated")

    # Git get latest tag
    cmd_update_git_latest_tag = "cd %s && git tag -l | tail -n 1" % (settings.PATH_PROJECT_ROOT)
    logger.debug(cmd_update_git_latest_tag)
    tag_latest = subprocess.check_output(cmd_update_git_latest_tag, shell=True).strip()

    # Git reset --hard
    cmd = "cd %s && git reset --hard" % (settings.PATH_PROJECT_ROOT)
    logger.debug(cmd)
    # subprocess.check_output(cmd, shell=True)

    # Git checkout tag
    cmd = 'cd %s && git checkout "tags/%s"' % (settings.PATH_PROJECT_ROOT, tag_latest)
    logger.debug(cmd)
    # subprocess.check_output(cmd, shell=True)

    ee.emit(EVENT_UPDATE_STATUS, "restarting")
    # Restart service


class Updater(BaseComponent):
    """
    Service which checks for updates periodically
    """
    def __init__(self, fake_update_available=None):
        BaseComponent.__init__(self)
        if fake_update_available is None:
            self.fake_tag_current = None
            self.fake_tag_latest = None
        else:
            if fake_update_available:
                self.fake_tag_current = "0.1.0"
                self.fake_tag_latest = "0.2.0"
            else:
                self.fake_tag_current = "0.1.0"
                self.fake_tag_latest = "0.1.0"

    def run_component(self):
        # Register event handlers
        @ee.on(EVENT_UPDATE_EXECUTE)
        def _update_execute():
            execute_update()

        # Check for updates, forever
        while not self.event_quit.is_set():
            self.check_for_updates()
            self.event_quit.wait(SECONDS_BETWEEN_CHECKS)

    def check_for_updates(self):
        logger.info("Checking for updates...")

        if self.fake_tag_latest:
            tag_latest = self.fake_tag_latest.strip().strip("v")
        else:
            cmd_update_git_info = "cd %s && git fetch github --tags" % (settings.PATH_PROJECT_ROOT)
            subprocess.check_output(cmd_update_git_info, shell=True)

            cmd_update_git_latest_tag = "cd %s && git tag -l | tail -n 1" % (settings.PATH_PROJECT_ROOT)
            tag_latest = subprocess.check_output(cmd_update_git_latest_tag, shell=True).strip().strip("v")
            # logger.debug("Latest Tag: %s", tag_latest)

        if self.fake_tag_current:
            tag_current = self.fake_tag_current.strip().strip("v")
        else:
            cmd_git_current_tag = "cd %s && git describe --tags --abbrev=0" % (settings.PATH_PROJECT_ROOT)
            tag_current = subprocess.check_output(cmd_git_current_tag, shell=True).strip().strip("v")
            # logger.debug("Current Tag: %s", tag_current)

        update_available = semver.compare(tag_current, tag_latest) == -1
        logger.info("Versions: current=%s, latest=%s, update_available=%s", tag_current, tag_latest, update_available)

        if update_available:
            ee.emit(EVENT_UPDATE_AVAILABLE, (tag_current, tag_latest))


if __name__ == "__main__":
    @ee.on(EVENT_UPDATE_AVAILABLE)
    def _update_available(msg):
        tag_current, tag_latest = msg
        logger.debug("> ee update available: %s -> %s", tag_current, tag_latest)
        # ee.emit(EVENT_UPDATE_EXECUTE)
        # exit(0)

    Updater(True).run_dev()
