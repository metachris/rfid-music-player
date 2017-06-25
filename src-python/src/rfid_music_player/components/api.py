"""
API for the web frontend for the ghoust game Python service.

See also https://www.python-boilerplate.com/flask
"""
import os
import time
import threading

from flask import Flask, jsonify, send_file, request, send_from_directory
from flask_cors import CORS

# Websocket imports
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

# Other imports
import youtube_dl
from logzero import setup_logger

# Internal imports
from rfid_music_player.core import database
from rfid_music_player.core import settings
from rfid_music_player.core import filesystem
from rfid_music_player.core import utils
from rfid_music_player.core.eventhub import ee
from basecomponent import BaseComponent

logger = setup_logger(logfile=settings.LOGFILE, level=settings.LOGLEVEL)


class API(BaseComponent):
    app = None
    server = None
    sockets = None

    # active websocket connections to clients
    websockets = []

    # state by youtube-dl hook
    state_download = None

    def __init__(self):
        BaseComponent.__init__(self)

        # Shutting down self.server takes about 1 minute, which is way too long. Therefore this
        # thread is run in daemon mode so it exits immediately when the main process exits.
        self.daemon = True

        try:
            self.state_download = None
            self.websockets = []
            self.app, self.sockets = self.create_app()
        except Exception as e:
            logger.exception(e)
            raise

    def create_app(self):
        """ Creates the Flask app """
        app = Flask(__name__, static_url_path='')
        app.config.update(dict(DEBUG=False))

        # Setup cors headers to allow all domains
        CORS(app)

        # Setup Flask-internal error logging
        for handler in list(logger.handlers):
            app.logger.addHandler(handler)

        # Setup error logging inside routes with automatic http responses.
        # The error will already be logged through the above added handlers,
        # so no need to log again.
        @app.errorhandler(500)
        def _internal_error(exception):
            return jsonify({
                "error": str(exception)
            }), 500

        # Setup WebSockets
        sockets = Sockets(app)

        def process_websocket_message(websocket, message):
            """ Processing of incoming websocket messages """
            logger.info("ws> %s" % message)
            websocket.send(message)  # Just echo

        @sockets.route('/ws')
        def _websocket_conn(websocket):
            self.websockets.append(websocket)
            while not websocket.closed:
                message = websocket.receive()
                if message and not websocket.closed:
                    process_websocket_message(websocket, message)
            self.websockets.remove(websocket)

        # Definition of the routes.
        @app.route("/")
        def _home():
            return send_from_directory(settings.PATH_WEB_FRONTEND, "index.html")

        @app.route('/thumbnail/<path:path>')
        def _thumbnail(path):
            logger.debug("thumbnail: %s", path)
            return send_from_directory(settings.PATH_MUSIC, path)

        @app.route('/static/<path:path>')
        def _static(path):
            logger.debug("static: %s", path)
            return send_from_directory(os.path.join(settings.PATH_WEB_FRONTEND, "static"), path)

        @app.route("/songs")
        def _api_get_songs():
            return jsonify({
                "songs": utils.get_songs()
            })

        @app.route("/tags", methods=['GET', 'POST'])
        def _api_get_tags():
            if request.method == 'POST':
                new_tag = request.json
                logger.info("new tag: %s", new_tag)
                database.add_tag(new_tag)

            return jsonify({
                "tags": database.get("tags")
            })

        @app.route("/tags/<tagId>", methods=['GET', 'POST', 'DELETE'])
        def _api_tag(tagId):
            if not database.get_tag(tagId):
                return jsonify({}), 404

            if request.method == 'DELETE':
                logger.info("API delete tag %s", tagId)
                database.delete_tag(tagId)
                return jsonify({})

            elif request.method == 'POST':
                logger.info("API update tag %s", tagId)

            return jsonify({
                "tag": database.get_tag(tagId)
            })

        @app.route("/youtube-dl/<youtubeId>")
        def _api_youtube_dl(youtubeId):
            # eg. rJWZhitXWzI
            self.youtube_download(youtubeId)
            return "download started"

        return app, sockets

    def youtube_download(self, youtube_id):
        """
        Download a video from youtube and convert to audio.
        Broadcast progress via websockets.
        """
        lock_uid = filesystem.make_writable()
        self.state_download = "started"
        ee.emit("download_state", self.state_download)

        def my_hook(d):
            """ Progress hook for youtube-dl """
            logger.info('my_hook %s', d)
            if d['status'] != self.state_download:
                self.state_download = d['status']
                ee.emit("download_state", self.state_download)

            if d['status'] == 'downloading':
                _percent_str = d["_percent_str"].strip()
                _percent_int = int(float(_percent_str[:-1]))
                ee.emit("download_progress", _percent_int)

        # https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L134
        ydl_opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'writeinfojson': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
                # 'preferredquality': '192',
            }],
            'logger': logger,
            'progress_hooks': [my_hook]
        }

        os.chdir(settings.PATH_MUSIC)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_id])

        filesystem.release_writable(lock_uid)

    def websocket_send(self, message):
        for websocket in self.websockets:
            websocket.send(message)

    def run(self):
        """ Runs the app """
        debug=False

        # Step 1: Setup eventhub handlers
        @ee.on("rfid_detected")
        def _rfid_detected(rfid_id):
            logger.info("rfid_detected: %s", rfid_id)
            self.websocket_send("rfid_detected:%s" % rfid_id)

        @ee.on("download_progress")
        def _download_progress(progress):
            logger.info("download_progress: %s", progress)
            self.websocket_send("download_progress:%s" % progress)

        @ee.on("download_state")
        def _download_state(state):
            logger.info("download_state: %s", state)
            self.websocket_send("download_state:%s" % state)

        # Step 2: Run the app
        try:
            port = int(os.environ.get("RFID_API_PORT", 5000))
            self.app.config.update(dict(DEBUG=debug))
            logger.info("Webserver listening on http://localhost:%s", port)
            self.server = pywsgi.WSGIServer(('', port), self.app, handler_class=WebSocketHandler)
            self.server.serve_forever()
        except Exception as e:
            logger.exception(e)
            raise
        finally:
            logger.info("api end")

    def shutdown(self):
        # This server.stop() takes exactly 1 minute (wtf). To make this faster, this
        # thread is run in daemon mode so it exits immediately when the main process exits.
        self.server.stop()


def test_fake_download():
    """ Fake download progress """
    logger.info("test fake download")
    for i in xrange(0, 100, 5):
        ee.emit("download_progress", i)
        time.sleep(0.5)


def test_threaded():
    """ Test api with keyboard input sent out as rfid_detected """
    api = API()
    api.start()

    try:
        # Wait for input to fake rfid_detected messages
        while True:
            msg = raw_input("> ")
            if msg.startswith("dl"):
                test_fake_download()
            else:
                ee.emit("rfid_detected", msg)
    except KeyboardInterrupt:
        pass
    finally:
        api.shutdown()
        print("\nbye")


if __name__ == "__main__":
    test_threaded()
