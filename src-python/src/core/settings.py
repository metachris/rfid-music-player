import os
import platform

DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
IS_RASPBERRY = platform.linux_distribution()[0].lower() == 'debian'

# Possible modes
MODE_PLAYBACK = object()
MODE_CONFIG = object()

# Set current mode
MODE = MODE_PLAYBACK

# DB File
FN_DATABASE = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "settings.json"))
PATH_MUSIC = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "music"))
PATH_WEB_FRONTEND = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "web-frontend"))

# Logging
LOGFILE = None
FN_PLAY_LOGS = os.path.realpath(os.path.join(DIR_SCRIPT, "..", "..", "playback.log"))

# Possible audio file extensions
EXTENSIONS_AUDIO = [
    "act", "aiff", "aif", "aac", "alac", "au", "flac", "m4a", "m4p", "mp3",
    "ogg", "raw", "wav"
]
