The Python code for the RFID music player. Runs on the Raspberry Pi or a development machine (eg. OSX).


## Architecture

This diagram shows the basic architecture:

![Architecture](https://raw.githubusercontent.com/metachris/rfid-music-player/master/docs/python-architecture-overview.jpg)


## Python Code Overview

#### Components

File | Functionality
--- | ---
`player.py` | Playing the songs when the RFID events arrive.
`rfidreader.py` | Interacts with the RFID reader.
`api.py` | REST + Websockets API for the web interface.
`eventbus.py`| simple, central event bus which all components can import to subscribe to events and to emit events.

#### Other files

File | Functionality
--- | ---
`main.py` | simple entry point which starts all components
`database.py` | a simple and crude JSON file database
`settings.py` | project configuration and settings
`utils.py` | a few utilities

#### External modules

* [logzero](https://github.com/metachris/logzero) for logging, which is a very simple single-file logging module. It provides nice and colored output to the console and can log to files too.
* [Flask](http://flask.pocoo.org/) for the API
* [pymitter](https://github.com/riga/pymitter) for the event bus
* [youtube-dl](https://github.com/rg3/youtube-dl) for downloading songs from YouTube


## Getting started

This is how you can get started:

    # Create a virtual environment with Python 3
    $ virtualenv -p python3 .venv3

    # Activate the virtual env
    $ . .venv3/bin/activate

    # Install the dependencies
    $ pip install -r requirements.txt

Now the system is set up and you can start either only the API or the whole system:

    # Change into the actual source directory
    $ cd src

    # Start the API (enter anything on the keyboard to mock detected RFID chips)
    $ python api.py

    # Start the whole system
    $ python main.py


## Issues & Improvements

If you encounter any issues or have ideas, please [open an issue](https://github.com/metachris/rfid-music-player/issues/new) or submit a pull request.
