"""
This module is used for filesystem read-only / read-write related things.
"""
import os
import uuid

from logzero import setup_logger
from rfid_music_player.core import settings

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)

HOME = os.path.expanduser("~")

CMD_RW = "sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot ; sudo mount -o remount,rw /mnt/sd-vfat"
CMD_RO = "sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot ; sudo mount -o remount,ro /mnt/sd-vfat"

# Each component which wants to write can get a lock. Only after all locks
# have been released, fs will be switched back to read-only.
locks = []

def is_writeable():
    return os.access(HOME, os.W_OK)

def _set_writable():
    if is_writeable():
        return
    os.system(CMD_RW)

def _set_readonly():
    if not is_writeable():
        return
    os.system(CMD_RO)

def make_writable():
    """
    Make filesystem writeable. Must be released with release_writable(..)
    Returns a uid that must be supplied to release_writable(uid).
    """
    uid = str(uuid.uuid4())
    locks.append(uid)
    _set_writable()
    return uid

def release_writable(uid):
    logger.debug("release_writable. locks: %s", locks)
    locks.remove(uid)
    if not locks:
        logger.info("release_writable. no more locks, switching back to read-only.")
        _set_readonly()

if __name__ == "__main__":
    print("is writable:", is_writeable())
