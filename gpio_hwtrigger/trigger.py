__author__ = 'patrick@codegrafix.de'
# !/usr/bin/python
import sys
from time import sleep
import time
import wiringpi

on = 1
off = 0

class raspiCamHWTrigger():

    # HW pin (11,12,13,15)
    # http://wiringpi.com/wp-content/uploads/2013/03/gpio1.png
    # left center right
    pins=[0,1,2,3]


    hz = float(sys.argv[1])
    trigger_delta=float(1/hz/len(pins))
    pulse_length = float(trigger_delta*3/4)  # seconds
    print("Hz: %d - TriggerDelta: %f -  Pulselength: %f" % (hz,trigger_delta,pulse_length))

    def __init__(self):
        wiringpi.wiringPiSetup()
        # Set pins as output
        for pin in self.pins:
            #print("Set pin %d as output", pin)
            wiringpi.pinMode(pin, 1)

    def trigger(self):
        for pin in self.pins:
            wiringpi.digitalWrite(pin, on)
            #print("pin: %d ON" % pin)
            sleep(self.pulse_length)
            #print("pin: %d OFF after %f" % (pin, self.pulse_length))
            wiringpi.digitalWrite(pin, off)
            sleep(self.trigger_delta-self.pulse_length)
            #print("Sleeping for %f" % (self.trigger_delta-self.pulse_length))

if __name__ == '__main__':

    trigger = raspiCamHWTrigger()

    while 1:
        start = time.time()
        trigger.trigger()
        elapsed = time.time() - start
        print("hz count: %f" % ( 1/elapsed))



