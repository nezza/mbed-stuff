"""
mbedrpc.py - mbed RPC interface for Python

Copyright (c) 2010 ARM Ltd
Modified by Thomas (nezza-_-) Roth - code@stacksmashing.net 2010


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Example:
    from mbedrpc import *
    mbed = SerialRPC("/dev/ttyACM0", 9600)
    led1 = DigitalOut(LED1);
    while True:
        led1.write(1)
        wait(1)
        led1.write(0)
        wait(1)

"""

import serial, urllib2, time

class pin():
        def __init__(self, id):
                self.name = id

# A list of pins so that you can access the pins by Number:
# led1 = DigitalOut(pins[0])
pins = []

# Define LED1 - LED4
for i in range(0,4):
    globals()["LED"+str(i+1)] = pin("LED"+str(i+1))
    pins.append(globals()["LED"+str(i+1)])

# Define p5 - p30
for i in range(4,30):
    globals()["p"+str(i+1)] = pin("p"+str(i+1))
    pins.append(globals()["p"+str(i+1)])

#mbed super class
class mbed:
	def __init__(self):
            print("This will work as a demo but no transport mechanism has been selected")
        
	def rpc(self, name, method, args):
            print("Superclass method not overridden")

#Transport mechanisms, derived from mbed

class SerialRPC(mbed):

	def __init__(self,port, baud):
	    self.ser = serial.Serial(port)
       	    self.ser.setBaudrate(baud)


        def rpc(self, name, method, args):
        	    self.ser.write("/" + name + "/" + method + " " + " ".join(args) + "\n")
        	    return self.ser.readline().strip()

class HTTPRPC(mbed):

    def __init__(self, ip):
        self.host = "http://" + ip

    def rpc(self, name, method, args):
        response = urllib2.urlopen(self.host + "/rpc/" + name + "/" + method + "," + ",".join(args))
        return response.read().strip()


#mbed Interfaces

class StandardPinInterface:
    def __init__(self, this_mbed, mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc(self.__class__.__name__, "new", [mpin.name])
        else:
            raise Exception('Please specifiy a pin or a LED.')

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

class DigitalOut(StandardPinInterface):

    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
      
class AnalogIn(StandardPinInterface):

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

    def read_u16(self):
        r = self.mbed.rpc(self.name, "read_u16", [])
        return int(r)

class AnalogOut(StandardPinInterface):

    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def write_u16(self, value):
        r = self.mbed.rpc(self.name, "write_u16", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

class DigitalIn(StandardPinInterface):

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return int(r)

class PwmOut(StandardPinInterface):
    
    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

    def period(self, value):
        r = self.mbed.rpc(self.name, "period", [str(value)])
        
    def period_ms(self, value):
        r = self.mbed.rpc(self.name, "period_ms", [str(value)])

    def period_us(self, value):
        r = self.mbed.rpc(self.name, "period_us", [str(value)])
        
    def puslewidth(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth", [str(value)])
        
    def puslewidth_ms(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth_ms", [str(value)])

    def puslewidth_us(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth_us", [str(value)])

class Serial():
        
    def __init__(self, this_mbed , tx, rx = ""):
        self.mbed = this_mbed
        if isinstance(tx, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("Serial", "new", [tx.name, rx.name])
             
    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def putc(self, value):
        r = self.mbed.rpc(self.name, "putc", [str(value)])

    def puts(self, value):
        r = self.mbed.rpc(self.name, "puts", [ "\"" + str(value) + "\""])

    def getc(self):
        r = self.mbed.rpc(self.name, "getc", [])
        return int(r)

class RPCFunction():

    def __init__(self, this_mbed , name):
        self.mbed = this_mbed
        if isinstance(name, str):
            self.name = name

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return int(r)

    def run(self, input):
        r = self.mbed.rpc(self.name, "run", [input])
        return r

class RPCVariable():

    def __init__(self, this_mbed , name):
        self.mbed = this_mbed
        if isinstance(name, str):
            self.name = name

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def write(self, value):
        self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return r

def wait(s):
    time.sleep(s)
