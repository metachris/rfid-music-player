# RFID Music Player

A simple music player for kids age ~2+.

* Songs are started by holding RFID tags to the sensor
* Can play any mp3 or aac files, and download songs from YouTube
* Nice web interface with Vue.js to download songs and to map songs to RFID tags
* Runs on a Raspberry Pi

You need an RFID reader such as the [RC522](https://www.amazon.com/SunFounder-Mifare-Antenna-Proximity-Arduino/dp/B00E0ODLWQ/ref=sr_1_3?ie=UTF8&qid=1498075429&sr=8-3&keywords=rfid+rc522) and a Raspberry Pi.

Author: Chris Hager <chris@linuxuser.at> ([metachris.com](https://www.metachris.com))

License: GPLv3


## Project Status: Soon Alpha (not yet fully working)

The project is advancing quickly and a working version is expected by end of June 2017.


## Project Structure

* `src-python/`: Code for the Raspberry Pi
* `src-web-frontend/`: Vue.js code for the web interface


## Raspberry Pi Code

This diagram shows the basic architecture of the Raspberry Pi code:

![Architecture](https://raw.githubusercontent.com/metachris/rfid-music-player/master/docs/python-architecture-overview.jpg)


## Feature Ideas

Upcoming features may include:

* Music Library
  * Songs
  * Audiobooks
  * Streams & Webradio
* Download from other sources than YouTube
* Got other ideas? [Open an issue!](https://github.com/metachris/rfid-music-player/issues/new)


## Contribute

Contributions are welcome! Please submit pull requests or just open issues.
