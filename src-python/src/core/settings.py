import os
import platform

# Path of the current script, used as base for relative path and file references
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))

# This is quick and cheap, but will recognize normal Debian Linux as Raspberry Pi
IS_RASPBERRY = platform.linux_distribution()[0].lower() == 'debian'

# Web frontend path (internal, fixed, used for the API)
PATH_WEB_FRONTEND = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "web-frontend"))
if not IS_RASPBERRY:
    PATH_WEB_FRONTEND = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "src-web-frontend", "dist"))

# Database file
FN_DATABASE = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "settings.json"))

# Music root (can be overwritten)
PATH_MUSIC_DEFAULT = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "music"))
PATH_MUSIC = os.getenv("RFID_PLAYER_MUSIC_ROOT", PATH_MUSIC_DEFAULT)

# Log file (can be overwritten)
LOGFILE = os.getenv("RFID_PLAYER_LOGFILE")

# Playback logs (can be overwritten)
FN_PLAY_LOGS_DEFAULT = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "playback.log"))
FN_PLAY_LOGS = os.getenv("RFID_PLAYER_PLAYLOGFILE", FN_PLAY_LOGS_DEFAULT)

# Possible audio file extensions
EXTENSIONS_AUDIO = [
    "act", "aiff", "aif", "aac", "alac", "au", "flac", "m4a", "m4p", "mp3",
    "ogg", "raw", "wav"
]
