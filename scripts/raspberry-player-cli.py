#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RFID Music Player CLI
"""
# Python 2 and 3 compatibility imports (see http://bit.ly/pyfuture2to3)
import os
import argparse

__version__ = "v1.0.0"

SYSTEMCTL_ID = "rfid-music-player"

def main(args):
    if args.action == "status":
        os.system("sudo systemctl status %s" % SYSTEMCTL_ID)

    elif args.action == "logs":
        os.system("sudo journalctl -u %s -f" % SYSTEMCTL_ID)

    elif args.action == "start":
        os.system("sudo systemctl start %s" % SYSTEMCTL_ID)

    elif args.action == "stop":
        os.system("sudo systemctl stop %s" % SYSTEMCTL_ID)

    elif args.action == "restart":
        os.system("sudo systemctl restart %s" % SYSTEMCTL_ID)

    else:
        print("Action '%s' not recognized" % args.action)
        exit(1)


if __name__ == "__main__":
    """
    This is executed when run from the command line
    """
    parser = argparse.ArgumentParser(
            description='RFID Music Player CLI',
    )

    parser.add_argument("action", help="[status, logs, start, stop, restart")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s (version {version})'.format(version=__version__))
    args = parser.parse_args()
    main(args)
