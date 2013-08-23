import os
import sys 
from serial.tools import list_ports
from serial.serialutil import SerialException
import serial
from hardware.xbee.Settings import ReadException
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read settings from a ZigBee radio.')
    parser.add_argument('serialport', 
                       help='port to which radio is connected')
    
    args = parser.parse_args()

    