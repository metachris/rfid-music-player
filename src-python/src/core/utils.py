import os
import hashlib
from core import settings

def get_music_files():
    """ Return all audio files available """
    files = [fn for fn in os.listdir(settings.PATH_MUSIC) \
            if not fn.startswith(".") \
            and not os.path.isdir(fn) \
            and os.path.splitext(fn)[1][1:] in settings.EXTENSIONS_AUDIO]

    ret = sorted(files, key=lambda fn: fn.lower())
    return ret

def get_songs():
    """ Return music files with thumbnail """
    songs = []
    for fn in get_music_files():
        fn_without_ext = os.path.splitext(fn)[0]
        fn_thumbnail = fn_without_ext + ".jpg"
        path_thumbnail = os.path.join(settings.PATH_MUSIC, fn_without_ext + ".jpg")
        # print(fn_without_ext, path_thumbnail)
        thumbnail = fn_thumbnail if os.path.isfile(path_thumbnail) else None
        song = {
            "filename": fn,
            "thumbnail": thumbnail,
            "hash": hashlib.md5(fn).hexdigest()
        }
        songs.append(song)
    return songs


def make_cmd_playback(fn_audio):
    """ Build the playback command depending on the platform """
    if settings.IS_RASPBERRY:
        return ["omxplayer", fn_audio, "-o", "both"]
    else:
        return ["afplay", fn_audio]


if __name__ == "__main__":
    # print(get_music_files())
    print(get_songs())
