#!/usr/bin/env python

"""
Demo code for the mbedrpc module.
Can be used with sample.c on the mbed.
"""
from mbedrpc import *
serdev = "/dev/ttyACM0"
mbed = SerialRPC(serdev, 9600) 

leds = []
for i in range(0,4):
    leds.append(DigitalOut(mbed,pins[i]))

while True:
        for i in range(3,0,-1):
            print "Enabling LED: %d" % i
            if i == 3:
                leds[i-1].write(0)
            else:
                leds[i+1].write(0)
            leds[i].write(1)
            wait(0.2)        
        for i in range(0,3):
            print "Enabling LED: %d" % i
            if i == 0:
                leds[i+1].write(0)
            else:
                leds[i-1].write(0)
            leds[i].write(1)
            wait(0.2)

