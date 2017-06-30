""" Project-wide settings """
import os
import logging
import platform
import types

from logzero import setup_logger

_logger = setup_logger()


# Path of the current script, used as base for relative path and file references
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))

# This is quick and cheap, but will recognize normal Debian Linux as Raspberry Pi
IS_RASPBERRY = platform.linux_distribution()[0].lower() == 'debian'

PATH_PROJECT_ROOT = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "..", ".."))

# Web frontend path (internal, fixed, used for the API)
PATH_WEB_FRONTEND = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "..", "..", "src-web-frontend", "dist"))
if not IS_RASPBERRY:
    PATH_WEB_FRONTEND = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "..", "..", "src-web-frontend"))

# Database file
FN_DATABASE = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "..", "..", "settings.json"))

# Music root (can be overwritten)
PATH_MUSIC_DEFAULT = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "..", "..", "music"))
PATH_MUSIC = os.getenv("RFID_PLAYER_MUSIC_ROOT", PATH_MUSIC_DEFAULT)

# Log file (can be overwritten)
LOGFILE = os.getenv("RFID_PLAYER_LOGFILE")

 # Loglevel. See https://docs.python.org/2/library/logging.html#logging-levels for available ones.
LOGLEVEL = int(os.getenv("RFID_PLAYER_LOGLEVEL", logging.DEBUG))

# Playback logs (can be overwritten)
FN_PLAY_LOGS_DEFAULT = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "playback.log"))
FN_PLAY_LOGS = os.getenv("RFID_PLAYER_PLAYLOGFILE", FN_PLAY_LOGS_DEFAULT)

# Possible audio file extensions
EXTENSIONS_AUDIO = [
    "act", "aiff", "aif", "aac", "alac", "au", "flac", "m4a", "m4p", "mp3",
    "ogg", "raw", "wav"
]

# Print all settings
for var_name, var in sorted(vars().iteritems()):
    if type(var) not in [types.ModuleType, types.FunctionType] and not var_name.startswith("_"):
        _logger.info("settings.%s: %s [%s]" % (var_name, var, type(var).__name__))
