"""
This module is used for filesystem read-only / read-write related things.
"""
import os

HOME = os.path.expanduser("~")
print(HOME)

CMD_RW = "sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot ; sudo mount -o remount,rw /mnt/sd-vfat"
CMD_RO = "sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot ; sudo mount -o remount,ro /mnt/sd-vfat"

def is_writeable():
    return os.access(HOME, os.W_OK)

def set_writable(writable=True):
    os.system(CMD_RW if writable else CMD_RO)

def set_readonly(readonly=True):
    os.system(CMD_RO if readonly else CMD_RW)


if __name__ == "__main__":
    print("is writable:", is_writeable())
