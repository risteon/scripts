#!/usr/bin/env python3
__author__ = "Christoph Rist"
__copyright__ = "Copyright 2015, Christoph Rist"
__license__ = "MIT"
__email__ = "dev@bitloot.de"


from random import randrange
import struct
import binascii
import subprocess


def generateRandomRGBColorString():

    rgb = (randrange(0,256), randrange(0,256), randrange(0,256))
    return binascii.hexlify(struct.pack('BBB', *rgb)).decode('utf-8')


def main():
    command = "i3lock -c " + generateRandomRGBColorString()
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    main()

