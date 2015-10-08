#! /usr/bin/python

"""
receive_samples.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example continuously reads the serial port and processes IO data
received from a remote XBee.
"""

from xbee import ZigBee
from digimesh import DigiMesh
import serial

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
xbee = ZigBee(ser)

# Continuously read and print packets
while True:
    try:
        print("about to read.")
        #response = ser.read()
        response = xbee.wait_read_frame()
        print("source address64 is: ")
        print("".join('{:02x} '.format(x) for x in response['source_addr_long']))
        print("source address16 is: ")
        print("".join('{:02x} '.format(x) for x in response['source_addr']))
        print("rf data is: ")
        print("".join('{:02x} '.format(x) for x in response['rf_data']))

    except KeyboardInterrupt:
        break
        
ser.close()
