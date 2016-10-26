__author__ = 'patrick@codegrafix.de'
# !/usr/bin/python
import sys
from time import sleep

import wiringpi

on = 1
off = 0

class raspiCamHWTrigger():

    hz = float(sys.argv[1])
    pulselength = float(1/hz/2)  # seconds
    print(pulselength)

    # HW pin (11,12,13,15)
    pins=[0,1,2,3]

    def __init__(self):
        wiringpi.wiringPiSetup()
        # Set pins as output
        for pin in self.pins:
            print("Set pin to %d", pin)
            wiringpi.pinMode(pin, 1)

    def trigger(self, number_of_high_pulses, number_of_low_pulses):

        wiringpi.digitalWrite(self.pins[0], on)
        sleep(self.pulselength * number_of_high_pulses)
        wiringpi.digitalWrite(self.pins[0], off)

        wiringpi.digitalWrite(self.pins[1], on)
        sleep(self.pulselength * number_of_low_pulses)
        wiringpi.digitalWrite(self.pins[1], off)

        wiringpi.digitalWrite(self.pins[2], on)
        sleep(self.pulselength * number_of_high_pulses)
        wiringpi.digitalWrite(self.pins[2], off)

        wiringpi.digitalWrite(self.pins[3], on)
        sleep(self.pulselength * number_of_low_pulses)
        wiringpi.digitalWrite(self.pins[3], off)

if __name__ == '__main__':

    trigger = raspiCamHWTrigger()
    print("Trigger time for all cameras: %d Hz"  %(trigger.hz) )

    while 1:
        trigger.trigger( 1, 1)
        #sleep(self.pulselength)
        #trigger.trigger(1, 1, 1)
        #sleep(self.pulselength)
