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

